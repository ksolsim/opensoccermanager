#!/usr/bin/env python3

from gi.repository import Gtk

import data


class QuitDialog(Gtk.MessageDialog):
    '''
    Dialog displayed when quitting the game but no active game is running.
    '''
    def __init__(self):
        Gtk.MessageDialog.__init__(self)
        self.set_transient_for(data.window)
        self.set_title("Quit Game")
        self.set_property("message-type", Gtk.MessageType.QUESTION)
        self.set_markup("Do you want to quit the game?")
        self.add_button("_Do Not Quit", Gtk.ResponseType.CANCEL)
        self.add_button("_Quit", Gtk.ResponseType.OK)
        self.set_default_response(Gtk.ResponseType.CANCEL)

    def show(self):
        self.run()


class UnsavedDialog(Gtk.MessageDialog):
    '''
    Dialog shown when quitting the game and an unsaved game may be lost.
    '''
    def __init__(self):
        Gtk.MessageDialog.__init__(self)
        self.set_transient_for(data.window)
        self.set_title("Quit Game")
        self.set_property("message-type", Gtk.MessageType.QUESTION)
        self.set_markup("<span size='12000'><b>The game currently has unsaved data.</b></span>")
        self.format_secondary_text("Do you wish to save the game?")
        self.add_button("_Do Not Save", Gtk.ResponseType.REJECT)
        self.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("_Save Game", Gtk.ResponseType.ACCEPT)
        self.set_default_response(Gtk.ResponseType.ACCEPT)

    def show(self):
        self.run()
