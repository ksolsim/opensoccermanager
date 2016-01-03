#!/usr/bin/env python3

from gi.repository import Gtk

import data

class TransferEnquiry(Gtk.MessageDialog):
    def __init__(self, playerid, transfer_type):
        Gtk.MessageDialog.__init__(self)
        self.set_transient_for(data.window)
        self.set_title("Transfer Enquiry")
        self.set_property("message-type", Gtk.MessageType.QUESTION)

        if transfer_type == 0:
            self.set_markup("Approach %s for the purchase of %s?" % (club.name, player.name))
        elif transfer_type == 1:
            self.set_markup("Approach %s for the loan of %s?" % (club.name, player.name))
        elif transfer_type == 2:
            self.set_markup("Approach %s for free transfer?" % (player.name))

        self.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("_Approach", Gtk.ResponseType.OK)
        self.set_default_response(Gtk.ResponseType.OK)
        self.connect("response", self.on_response)

        self.show()

    def on_response(self, dialog, response):
        self.destroy()
