#!/usr/bin/env python3

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
