#!/usr/bin/env python3

#  This file is part of OpenSoccerManager.
#
#  OpenSoccerManager is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by the
#  Free Software Foundation, either version 3 of the License, or (at your
#  option) any later version.
#
#  OpenSoccerManager is distributed in the hope that it will be useful, but
#  WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
#  or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
#  more details.
#
#  You should have received a copy of the GNU General Public License along with
#  OpenSoccerManager.  If not, see <http://www.gnu.org/licenses/>.


from gi.repository import Gtk

import data


class LoadDialog(Gtk.FileChooserDialog):
    '''
    File selection dialog for loading games.
    '''
    def __init__(self, *args):
        Gtk.FileChooserDialog.__init__(self)
        self.set_transient_for(data.window)
        self.set_modal(True)
        self.set_title("Load Game")
        self.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("_Open", Gtk.ResponseType.OK)
        self.set_action(Gtk.FileChooserAction.OPEN)
        self.set_current_folder(data.preferences.save_path)
        self.connect("response", self.on_response)

        filefilter = Gtk.FileFilter()
        filefilter.set_name("Saved Game")
        filefilter.add_pattern("*.osm")
        self.add_filter(filefilter)

        self.show()

    def on_response(self, dialog, response):
        self.destroy()


class SaveDialog(Gtk.FileChooserDialog):
    '''
    File selection dialog for saving games.
    '''
    def __init__(self, *args):
        Gtk.FileChooserDialog.__init__(self)
        self.set_transient_for(data.window)
        self.set_modal(True)
        self.set_title("Save Game")
        self.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("_Save", Gtk.ResponseType.OK)
        self.set_action(Gtk.FileChooserAction.SAVE)
        self.set_current_folder(data.preferences.save_path)
        self.connect("response", self.on_response)

        filefilter = Gtk.FileFilter()
        filefilter.set_name("Saved Game")
        filefilter.add_pattern("*.osm")
        self.add_filter(filefilter)

        self.show()

    def on_response(self, dialog, response):
        self.destroy()
