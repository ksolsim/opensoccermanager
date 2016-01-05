#!/usr/bin/env python3

from gi.repository import Gtk

import data


class Stadium(Gtk.Grid):
    def __init__(self):
        Gtk.Grid.__init__(self)

    def run(self):
        self.show_all()


class ConfirmStadium(Gtk.MessageDialog):
    '''
    Confirm specified improvements to stadium construction.
    '''
    def __init__(self, cost=0):
        Gtk.MessageDialog.__init__(self)
        self.set_transient_for(data.window)
        self.set_modal(True)
        self.set_title("Upgrade Stadium")
        self.set_property("message-type", Gtk.MessageType.QUESTION)
        self.set_markup("Begin the construction of upgrades to the stadium at cost of %s?" % (cost))
        self.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("_Upgrade", Gtk.ResponseType.OK)
        self.set_default_response(Gtk.ResponseType.CANCEL)
        self.connect("response", self.on_response)

        self.show()

    def on_response(self, dialog, response):
        self.destroy()
