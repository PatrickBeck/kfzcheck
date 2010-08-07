#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Filename: kfzcheck_qt.py
Version: 0.0.1
last change: 2010-08-1
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
import csv
import re
import os
import gettext
from gui import Ui_KFZcheck

APP = 'kfzcheck' # get i18n support - english and german
DIR = '/home/pbeck/kfzcheck_devel/src/opt/kfzcheck/locale'

gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)
_ = gettext.gettext

class KFZcheck(QMainWindow):

    kfzcheck_dir = '/home/pbeck/kfzcheck_devel/src/opt/kfzcheck/'
    kfzcheck_ini = os.path.expanduser('~/.kfzcheck.ini') # configuration file for the country selection
    listfield_list = []
    country = 'de' # has to be replaced with a gui

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.ui = Ui_KFZcheck() # load the qt-designer generated gui file
        self.ui.setupUi(self)
        QObject.connect(self.ui.searchfield, SIGNAL('textChanged(QString)'), self.searching) # call the searching function on every text change - on the fly search
        
        self.qa = QActionGroup(None)
        self.qa.addAction(self.ui.actionTop)
        self.qa.addAction(self.ui.actionMiddle)
        self.qa.addAction(self.ui.actionBottom)
        QObject.connect(self.ui.actionTop, SIGNAL('triggered()'), self.filterTop)
        QObject.connect(self.ui.actionMiddle, SIGNAL('triggered()'), self.filterMiddle)
        QObject.connect(self.ui.actionBottom, SIGNAL('triggered()'), self.filterBottom)


    def load(self, kfzlist):
        csvfile = '%s/kfzlist/%s.csv' % (self.kfzcheck_dir, kfzlist) 
        try:
            file = csv.reader(open(csvfile), delimiter=',') # parse the csv file
        except:
            self.addItemstoList('No csv file found')
        
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
                
    def searching(self):
        self.ui.listfield.clear()
        text = str(self.ui.searchfield.text())
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
            self.addItemstoList('No matches found') # add a descriptions text 
                
    def addItemstoList(self, textToadd):
        newItem = QListWidgetItem()
        newItem.setText(textToadd)
        textToAddList = textToadd.splitlines()

        if len(textToAddList) == 2: # when two lines - the state is always on a newline - check if a image exists - it's not a problem when no image exists
            textIcon = textToAddList[1] # get the name of the image
            icon = QIcon('%s/wappen/%s/%s.png' % (self.kfzcheck_dir, self.country, textIcon)) # set it as Qicon
            newItem.setIcon(icon) # and add it to the newItem
        
        self.ui.listfield.addItem(newItem) # add the item to the QlistWidget
        
    def filterTop(self):
#        self.ui.listfield.scrollToItem()
        
    def filterMiddle(self):
#        self.selector.set_active(0, self.count_rows/2)
        
    def filterBottom(self):
#        self.selector.set_active(0, self.count_rows-1)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    kfzcheck = KFZcheck()
    kfzcheck.load('de') # has to be replaced with a gui to select
    kfzcheck.show()
    sys.exit(app.exec_())


