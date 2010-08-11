#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Filename: kfzcheck_qt.py
Version: 0.2
last change: 2010-08-11
Function: KFZcheck is a small program written in python and uses the Qt toolkit. 
It searches for car (in german kfz) license plates shortcuts and the citys according to the 
searchword - german example: S for Stuttgart. 

Copyright (C) 2010 Patrick Beck <pbeck at yourse dot de>  

I have to thanks Bartholomäus Wloka for the created austrian and poland country package

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

#from PySide.QtCore import * # for using on the device
#from PySide.QtGui import * # for using on the device
from PyQt4 import * # for using on the pc
from PyQt4.QtCore import * # for using on the pc 
from PyQt4.QtGui import * # for using on the pc

import signal
signal.signal(signal.SIGINT, signal.SIG_DFL) # to destroy the app with ctrl-c

import sys
import locale
import csv
import re
import os
import gettext
import ConfigParser
from gui import Ui_KFZcheck

class KFZcheck(QMainWindow):
    workingDir = os.getcwd() # get the current directory
    appName = sys.argv[0].split('/')[-1] # get the application name
    pathToFile = sys.argv[0].rstrip(appName) # extract the path from the current dir to the app - and exclude the application name
    kfzcheck_dir = '%s/%s' % (workingDir, pathToFile) # create the absolute path to the application dir

    listfield_list = [] # data for searching
    
    Config = ConfigParser.ConfigParser()
    kfzcheck_ini = os.path.expanduser('~/.kfzcheck.ini') # configuration file for the country selection
    if os.path.isfile(kfzcheck_ini) == False: # when the ini file not exists create it in ~./.kfzcheck.ini
        ini_file = open(kfzcheck_ini, 'w') # open the file and create it when not exists
        Config.add_section('Country')
        Config.set('Country', 'firstload', 'de') # first standard load is the german file
        Config.write(ini_file)
        ini_file.close()

    Config.read(kfzcheck_ini)
    firstload = Config.get('Country', 'firstload') # load the country that specified in the configuration file

    def __init__(self, parent=None):
        translator = QTranslator(app) # translation       
        translator.load('%slocale/%s.qm' % (self.kfzcheck_dir, locale.getlocale()[0])) # all files in locale/ as language code de_DE.qm as example
        app.installTranslator(translator) # use the file if the language exists
        
        QWidget.__init__(self, parent)
        self.ui = Ui_KFZcheck() # load the qt-designer generated gui file
        self.ui.setupUi(self)

        self.countrybox = QDialog() # create a dialog for the country selector
        self.countrybox.setFixedHeight(350) # it's not the best way ...
        self.countryvertical = QVBoxLayout(self.countrybox) # create a vertical layout - full width of the screen
        self.countryfield = QListWidget(self.countrybox) # for the country selector
        self.countryvertical.addWidget(self.countryfield) # full witdh for the listwidget

        self.qa = QActionGroup(self)
        self.qa.addAction(self.ui.actionTop)
        self.qa.addAction(self.ui.actionMiddle)
        self.qa.addAction(self.ui.actionBottom)

        QObject.connect(self.ui.searchfield, SIGNAL('textChanged(QString)'), self.searching) # call the searching function on every text change - on the fly search
        QObject.connect(self.ui.actionTop, SIGNAL('triggered()'), self.filterTop)
        QObject.connect(self.ui.actionMiddle, SIGNAL('triggered()'), self.filterMiddle)
        QObject.connect(self.ui.actionBottom, SIGNAL('triggered()'), self.filterBottom)
        QObject.connect(self.ui.actionAbout, SIGNAL('triggered()'), self.about)
        QObject.connect(self.ui.actionCountry, SIGNAL('triggered()'), self.countrySelector)
        QObject.connect(self.countryfield, SIGNAL('itemActivated(QListWidgetItem *)'), self.loadCountry)

        self.load(self.firstload)

    def load(self, kfzlist):
        csvfile = '%skfzlist/%s.csv' % (self.kfzcheck_dir, kfzlist)
        try:
            file = csv.reader(open(csvfile), delimiter=',') # parse the csv file
        
            for i in file:
                i[0] = unicode(i[0], 'utf-8') # listfield_list is unicode, too. When i append the item.
                i[1] = unicode(i[1], 'utf-8')

                if len(i) == 3: # check if the csv file has 3 values
                    i[2] = unicode(i[2], 'utf-8')
                    self.listfield_list.append(i)
                    self.addItemstoList('%s, %s\n%s' % (i[0], i[1], i[2]))
                else:
                    self.listfield_list.append(i)
                    self.addItemstoList('%s, %s' % (i[0], i[1])) # when only 2 values in the csv files
        
        except:
            self.addItemstoList(self.tr("csv file not found or has not enough rights."))
            self.ui.searchfield.hide() # no searchoption - the message will be stay on the screen
        
        self.filterTop() # jump to the beginning after loading a new csv file 
    
    def loadCountry(self):
        self.ui.searchfield.setText(QString(''))
        self.listfield_list = [] # clear the searching list from the old entries
        self.ui.listfield.clear() # clear the ui from the old entries
        selected_country = self.countryfield.currentItem().text()

        self.Config.set('Country', 'firstload', selected_country) # set the config file to the selected country
        ini_file = open(self.kfzcheck_ini, 'w') # open the file
        self.Config.write(ini_file) # write and save it
        ini_file.close # close the ini file
       
        self.countrybox.hide() # hide the QDialog
        self.countryfield.hide() # hide the country selector after pressing the next file to load
        self.countryfield.clear() # delete the content of the selector - or it will be twice in the field
        self.load(selected_country) # load the csv file
            
    def searching(self):
        self.ui.listfield.clear()
        text = unicode(self.ui.searchfield.text()) # a QString is not as nice as unicode :)
        for i in self.listfield_list:
            if i[0].startswith(text): # when uppercase writing show all license plates that starts with searchtext
                if len(i) == 3:
                    self.addItemstoList('%s, %s\n%s' % (i[0], i[1], i[2]))
                else:
                    self.addItemstoList('%s, %s' % (i[0], i[1]))
            else:
                if text.islower(): # lowercase writing
                    if text.lower() == i[0].lower(): # if the license plate matches exactly
                        self.ui.listfield.clear() # show only the right
                        if len(i) == 3:
                            self.addItemstoList('%s, %s\n%s' % (i[0], i[1], i[2]))
                        else:
                            self.addItemstoList('%s, %s' % (i[0], i[1]))
                        break # and break the loop after it

                    else: 
                        if i[1].lower().startswith(text.lower()): # lowercase, search after the city
                            if len(i) == 3:
                                self.addItemstoList('%s, %s\n%s' % (i[0], i[1], i[2]))
                            else:
                                self.addItemstoList('%s, %s' % (i[0], i[1]))
        
        if self.ui.listfield.count() == 0: # check if no items in list
            self.addItemstoList(self.tr("No matches found")) # add a descriptions text 
                
    def addItemstoList(self, textToadd):
        newItem = QListWidgetItem()
        newItem.setText(textToadd)
        textToAddList = unicode(textToadd).splitlines()

        if len(textToAddList) == 2: # when two lines - the state is always on a newline - check if a image exists - it's not a problem when no image exists
            textIcon = textToAddList[1] # get the name of the image
            self.Config.read(self.kfzcheck_ini)
            secondload = self.Config.get('Country', 'firstload') # get the selected country in the moment
            icon = QIcon('%s/wappen/%s/%s.png' % (self.kfzcheck_dir, secondload, textIcon)) # set it as QIcon
            newItem.setIcon(icon) # and add it to the newItem
        
        self.ui.listfield.addItem(newItem) # add the item to the QlistWidget
        
    def filterTop(self):
        self.ui.listfield.setCurrentRow(0) # jump to the top
        self.ui.listfield.setCurrentRow(1) # It's not possible to jump into a selected area twice, 
                                           # this happens when you scroll manually down with a scrollbar - so we have to change it
        self.ui.listfield.clearSelection() # no selection should be visible

    def filterMiddle(self):
        rows = self.ui.listfield.count()
        self.ui.listfield.setCurrentRow(rows/2) # jump to the middle
        self.ui.listfield.setCurrentRow(rows/2-1)
        self.ui.listfield.clearSelection() # no selection should be visible
        
    def filterBottom(self):
        rows = self.ui.listfield.count()
        self.ui.listfield.setCurrentRow(rows-1) # jump to the end (-1 because it count from 0)
        self.ui.listfield.setCurrentRow(rows-2) # 
        self.ui.listfield.clearSelection() # no selection should be visible

    def about(self):
        text = self.tr("""KFZcheck searches for kfz license plates shortcuts and citys / regions.
 
Uppercase searches for all license plates starting with your search. Lowercase matches exactly for the license plates and searches after the city / region, if no license plate exists.

It's possible to use other data sources (numbers, city codes, etc.) Visit the project website at http://kfzcheck.yourse.de.

Feedback is welcome at pbeck@yourse.de""")
        QMessageBox.about(None, self.tr("About"), text)

    def countrySelector(self):
        country_list = []
        path = '%s/kfzlist/' % (self.kfzcheck_dir)
        for i in os.walk(path): # search all csv files and create a country code list
            for i in i[2]:
                country_list.append(i.replace('.csv', ''))
        country_list.sort() # alphabetical sort
        for i in country_list:
            newCountry = QListWidgetItem()
            newCountry.setText(i)
            self.countryfield.addItem(newCountry)

        self.countryfield.show() # the qlistwidget
        self.countrybox.show() # the qdialog

if __name__ == "__main__":
    app = QApplication(sys.argv)
    kfzcheck = KFZcheck()
    kfzcheck.show()
    sys.exit(app.exec_())


