#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Filename: kfzcheck.py
Version: 1.6
last change: 2010-03-15
Function: KFZcheck is a small program written in python and uses the gtk toolkit. 
It searches for car (in german kfz) license plates shortcuts and the citys according to the 
searchword - german example: S for Stuttgart. 

Copyright (C) 2010 Patrick Beck <pbeck at yourse dot de>  

I have to thanks Bartholomäus Wloka for the created austrian and poland country package and his 
help to find a bug with the picture creation and the improvement of the search engine :)

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

import pygtk
import gtk
import hildon
import gobject
import sys
import csv
import re
import os
import ConfigParser
import portrait # auto rotate - thanks to thp
import gettext

APP = 'kfzcheck' # get i18n support - english and german
DIR = '/opt/kfzcheck/locale'

gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)
_ = gettext.gettext

from optparse import OptionParser


class Kfzcheck(object):
    parser = OptionParser()
    parser.add_option("-s", "--search", dest="searchparameter")
    (optionen, args) = parser.parse_args()
    searchparameter = optionen.searchparameter
    
    count_rows = 0
    bl_image = {} # list with the created pixbuf images
    kfzcheck_dir = '/opt/kfzcheck'
    kfzcheck_ini = os.path.expanduser('~/.kfzcheck.ini') # configuration file for the country selection

    Config = ConfigParser.ConfigParser()

    if os.path.isfile(kfzcheck_ini) == False: # when the ini file not exists create it in ~./.kfzcheck.ini
        ini_file = open(kfzcheck_ini, 'w') # open the file and create it when not exists
        Config.add_section('Country')
        Config.set('Country', 'firstload', 'de') # first standard load is the german file
        Config.write(ini_file)
        ini_file.close()
        
    Config.read(kfzcheck_ini)
    firstload = Config.get('Country', 'firstload') # load the country that specified in the configuration file

    def load(self, kfzlist):
        csvfile = '%s/kfzlist/%s.csv' % (self.kfzcheck_dir, kfzlist) 
        if 1 == 1:
#        try: # check if the file is readable
            file = csv.reader(open(csvfile), delimiter=',') # parse the csv file
            if len(self.bl_image) == 0: # if 0 the country is changed - then create the new pixbufs
                imagelist = []
                path = '%s/wappen/%s' % (self.kfzcheck_dir, kfzlist)
                for filepath in os.walk(path): # search all emblems in the wappen dir
                    for emblem in filepath[2]:
                        imagelist.append(emblem)
                for bl in imagelist: # generate the pixbufs to display faster a result
                    text = '%s/wappen/%s/%s' % (self.kfzcheck_dir, kfzlist, bl)
                    image = gtk.gdk.pixbuf_new_from_file_at_size(text, 60, 60)#.scale_simple(60, 60, gtk.gdk.INTERP_HYPER)            
                    self.bl_image[bl.replace('.png', '')] = image # if file extension is set, replace it with nothing and add only the state name
            return file
        if 0 == 1:
#        except IOError:
            store_items = gtk.ListStore(gobject.TYPE_STRING)
            new_item = store_items.append()
            nofile = _('csv file not found or has not enough rights.')
            store_items.set(new_item, 0, nofile)
            self.count_rows += 1
            
            renderer = gtk.CellRendererText()
            renderer.set_property('xalign', 0.5) # set it to center
            renderer.set_property('size-points', 14) # set the size manually
            column = self.selector.append_column(store_items, renderer) #i have to call a renderer, not None
           
#            column.pack_start(renderer, 0)
            column.set_attributes(renderer, text=0)
#            column.set_property("text-column", 0) 
    
    def searchdata(self, row0, row1, store_items, row2=None): # add the Bundesland (state in germany) and a emblem
        new_item = store_items.append()
        if row2 == None:
            output2 = '%s, %s' % (row0, row1)
            store_items.set(new_item, 0, None, 1, output2)
            self.count_rows += 1
        else:
            output3 = '%s, %s \n%s' % (row0, row1, row2)
            self.count_rows += 1

            try: # when no images exists - thanks to Bartholomäus Wloka
                store_items.set(new_item, 0, self.bl_image[row2], 1, output3)
            except KeyError:
                store_items.set(new_item, 0, None, 1, output3)
                
        return store_items
                
    def search(self, widget=None, entry=None, country=None):
        self.deletecolumn() # delete the whole column before you add new items
        self.count_rows = 0 # for top, middle, bottom scrolling    
        try:
            searchword = unicode(entry.get_text(), 'utf-8')
        except AttributeError:
            searchword = unicode(entry, 'utf-8') # if the search function is called directly without the changed signal from gtk
        searchtext = searchword.replace(' ', '')  # ignore any spaces (replace it with nothing)
        store_items = gtk.ListStore(gtk.gdk.Pixbuf, gobject.TYPE_STRING)
        file = self.load(country) # load the csv file
        if file is not None: # see the load function
            for row in file:
                row[0] = unicode(row[0], 'utf-8') # unicode for äöü
                row[1] = unicode(row[1], 'utf-8')
                
                if re.match(searchtext, row[0]) != None: # if uppercase searchtext show all license plates thats starts with searchtext
                    try:
                        self.searchdata(row[0], row[1], store_items, row[2])
                    except IndexError:
                        self.searchdata(row[0], row[1], store_items)
                else:
                    if searchtext.islower():
                        if searchtext.upper() in row: # search for the license plate and show only the right (not casesensitive)
                            store_items.clear() 
                            try:
                                self.searchdata(row[0], row[1], store_items, row[2])
                            except IndexError:
                                self.searchdata(row[0], row[1], store_items)
                        
                            break # when the shortcut matches exactly => break the loop
                        else:
                            if re.match(searchtext, row[1], re.IGNORECASE) != None: # search for the city (not casesensitive)
                                try:
                                    self.searchdata(row[0], row[1], store_items, row[2])
                                except IndexError:
                                    self.searchdata(row[0], row[1], store_items)
                     
            try: # display a message when no results are found
                store_items[0] # it raises a error when no items stored
            except IndexError:    
                new_item = store_items.append()
                nomatch = _('No matches found')
                store_items.set(new_item, 0, None, 1, nomatch)
                self.count_rows += 1
            
            renderer = gtk.CellRendererPixbuf() 
            renderer.set_property('xalign', 0.1) # set it to center
            column = self.selector.append_column(store_items, renderer) #i have to call a renderer, not None
           
            column.pack_start(renderer, 0)
            column.set_attributes(renderer, pixbuf=0)
        
            renderer = gtk.CellRendererText()
            renderer.set_property('xalign', 0) # set it to center
            renderer.set_property('size-points', 14) # set the size manually
            column.pack_start(renderer, 1)
            column.set_attributes(renderer, text=1)

#            column.set_property("text-column", 0) 
            return self.selector
   
    def create_country_selector(self):
        self.country_selector = hildon.TouchSelector()
        country_list = []
        path = '%s/kfzlist/' % (self.kfzcheck_dir)
        for i in os.walk(path): # search all csv files and create a country code list
            for i in i[2]:
                country_list.append(i.replace('.csv', ''))
        country_list.sort() # alphabetical sort
        try:
            active = country_list.index(self.firstload) # get the index of the current loaded country - to select the right item 
        except ValueError: # when no csv files available set active to None
            active = None

        store_countrys = gtk.ListStore(gobject.TYPE_STRING)
        for country in country_list:
            new_iter = store_countrys.append()
            store_countrys.set_value(new_iter, 0, country)

        renderer = gtk.CellRendererText()
        
        self.country_column = self.country_selector.append_column(store_countrys, renderer)
#        self.country_column.pack_start(renderer, 0)
        self.country_column.set_attributes(renderer, text=0)
        self.country_selector.set_column_selection_mode(hildon.TOUCH_SELECTOR_SELECTION_MODE_SINGLE)
#        self.country_column.set_property('text-column', 0) 

        return active

    def about(self, widget):
        about = gtk.AboutDialog()
        about.set_program_name('KFZcheck')
        about.set_version('1.6')
        about.set_comments(_("KFZcheck searches for kfz license plates shortcuts and citys / regions. Uppercase searches for all license plates starting with your search. Lowercase matches exactly for the license plates and searches after the city / region if no license plate exists.")) 
        about.set_website('http://wiki.yourse.de/doku.php?id=python:kfzcheck')
        about.set_logo(gtk.gdk.pixbuf_new_from_file('/usr/share/pixmaps/kfzcheck.png'))
        about.run()
        about.destroy()
    
    def country(self, widget):
        self.bl_image.clear() # clear the dict, it's a work around so it will only load the images they will be used
        self.entry.connect('changed', self.search, self.entry, self.button_country.get_value()) # when changed load the correct csv file
        self.search(entry = '', country = self.button_country.get_value()) # show the whole list
        self.Config.set('Country', 'firstload', self.button_country.get_value()) # set the config file to the last selected country
        ini_file = open(self.kfzcheck_ini, 'w') # open the file
        self.Config.write(ini_file) # write and save it
        ini_file.close # close the ini file
        self.entry.set_text('') # set the entry field to nothing when the country field changed

    def filter(self, button, label):
        if label == 'Top':
            self.selector.set_active(0, 0)
            self.selector.center_on_selected()
        if label == 'Middle':
            self.selector.set_active(0, self.count_rows/2)
            self.selector.center_on_selected()
        if label == 'Bottom':
            self.selector.set_active(0, self.count_rows-1)
            self.selector.center_on_selected()

    def deletecolumn(self): # create a empty list and set it to the current
        self.selector.remove_column(0)

    def delete_event(self, widget, event, data=None):
        return False
        
    def destroy(self, widget, data=None):
        gtk.main_quit()
 
    def __init__(self):
        self.program = hildon.Program.get_instance()
        self.window = hildon.Window()
        self.program.add_window(self.window)
        
        self.window.set_title(_('KFZcheck'))
        self.window.connect('delete_event', self.delete_event)
        self.window.connect('destroy', self.destroy)
       
        self.selector = hildon.TouchSelector()
        self.selector.set_column_selection_mode(hildon.TOUCH_SELECTOR_SELECTION_MODE_SINGLE) # you can only select one item

        self.box = gtk.VBox(False,2)
        self.window.add(self.box)
        self.hbox = gtk.HBox(False,2)
        self.box.pack_end(self.hbox, False, False, 0)

        self.box.pack_start(self.selector, True, True, 0)       

        self.menu = hildon.AppMenu() 
      
        self.entry = hildon.Entry(gtk.HILDON_SIZE_AUTO)
        self.entry.set_max_length(0)
        self.entry.connect('activate', self.search, self.entry, self.firstload)
        self.entry.set_placeholder(_('license plate or cityname...'))
        
        self.top = hildon.GtkRadioButton(gtk.HILDON_SIZE_AUTO, None)
        self.top.set_label(_('Top'))
        self.top.connect("clicked", self.filter, 'Top')
        self.menu.add_filter(self.top)
        self.top.set_mode(False)

        self.middle = hildon.GtkRadioButton(gtk.HILDON_SIZE_AUTO, None)
        self.middle.set_label(_('Middle'))
        self.middle.connect("clicked", self.filter, 'Middle')
        self.menu.add_filter(self.middle)
        self.middle.set_mode(False)
        
        self.bottom = hildon.GtkRadioButton(gtk.HILDON_SIZE_AUTO, None)
        self.bottom.set_label(_('Bottom'))
        self.bottom.connect("clicked", self.filter, 'Bottom')
        self.menu.add_filter(self.bottom)
        self.bottom.set_mode(False)
        
        self.hbox.pack_start(self.entry, True, True, 2)

        country = self.create_country_selector() # create a list with all available countrys
        self.button_country = hildon.PickerButton(gtk.HILDON_SIZE_AUTO, hildon.BUTTON_ARRANGEMENT_VERTICAL)
        self.button_country.set_title(_('Country'))
        self.button_country.set_selector(self.country_selector)
        self.button_country.connect("value-changed", self.country) # when changed call the country function
        
        if country != None: # None will be set when no csv files available
            self.button_country.set_active(country) # set the right item active
        
        self.menu.append(self.button_country) # append the button to the system menu
        
        self.button_about = hildon.GtkButton(gtk.HILDON_SIZE_AUTO)
        self.button_about.set_label(_('About'))
        self.button_about.connect('clicked', self.about)
        self.menu.append(self.button_about)
        
        self.menu.show_all()
        self.window.set_app_menu(self.menu)
        self.window.show_all()
        
        if self.searchparameter != None: # when kfzcheck would be start with the -s parameter on the commandline
            self.entry.set_text(self.searchparameter)
            self.entry.set_position(-1)
            self.search(entry = self.searchparameter, country = self.firstload)
        else:
            self.search(entry = '', country = self.firstload)    

        main_window = self.window   # auto rotate function by thp
        app_name = 'kfzcheck'
        app_version = '1.6'
        initial_mode = portrait.FremantleRotation.AUTOMATIC
        rotation_object = portrait.FremantleRotation(app_name, main_window, app_version, initial_mode)

def main():
    gtk.main()
    return 0
    
if __name__ == '__main__':
    Kfzcheck()
    main()

