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
import uigtk.widgets


class PrintDialog(Gtk.Dialog):
    def __init__(self):
        Gtk.Dialog.__init__(self)
        self.set_transient_for(data.window)
        self.set_modal(True)
        self.set_title("Print")
        self.add_button("_Close", Gtk.ResponseType.CLOSE)
        self.add_button("_Print", Gtk.ResponseType.OK)
        self.set_default_response(Gtk.ResponseType.OK)
        self.vbox.set_spacing(5)

        self.radiobuttonSquad = uigtk.widgets.RadioButton("_Squad")
        self.vbox.add(self.radiobuttonSquad)
        self.radiobuttonShortlist = uigtk.widgets.RadioButton("S_hortlist")
        self.radiobuttonShortlist.join_group(self.radiobuttonSquad)
        self.vbox.add(self.radiobuttonShortlist)
        self.radiobuttonFixtures = uigtk.widgets.RadioButton("_Fixtures")
        self.radiobuttonFixtures.join_group(self.radiobuttonSquad)
        self.vbox.add(self.radiobuttonFixtures)
        self.radiobuttonAccounts = uigtk.widgets.RadioButton("_Accounts")
        self.radiobuttonAccounts.join_group(self.radiobuttonSquad)
        self.vbox.add(self.radiobuttonAccounts)

    def show(self):
        self.show_all()
        self.run()
        self.destroy()
