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
