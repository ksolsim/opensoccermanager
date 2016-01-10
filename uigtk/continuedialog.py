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
from gi.repository import GObject

import data


class ContinueDialog(Gtk.Dialog):
    '''
    Dialog displayed when moving between dates in the game.
    '''
    def __init__(self):
        Gtk.Dialog.__init__(self)
        self.set_transient_for(data.window)
        self.set_modal(True)
        self.set_title("Continue Game")
        self.set_default_size(200, -1)
        self.set_resizable(False)
        self.vbox.set_border_width(5)

        self.progressbar = Gtk.ProgressBar()
        self.progressbar.set_text("")
        self.vbox.add(self.progressbar)

        self.count = 0

    def on_timeout_event(self, *args):
        if self.count < 10:
            self.count += 1
            self.progressbar.set_fraction(self.count * 0.1)

            state = True
        else:
            self.destroy()
            data.window.mainscreen.information.update_date()

            state = False

        return state

    def show(self):
        self.show_all()

        GObject.timeout_add(10, self.on_timeout_event)
