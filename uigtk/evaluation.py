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

import uigtk.widgets


class Evaluation(uigtk.widgets.Grid):
    __name__ = "evaluation"

    def __init__(self):
        uigtk.widgets.Grid.__init__(self)
        self.set_hexpand(True)
        self.set_vexpand(True)

        frame = uigtk.widgets.CommonFrame("Players")
        self.attach(frame, 0, 0, 1, 1)
        frame = uigtk.widgets.CommonFrame("Fans")
        self.attach(frame, 1, 0, 1, 1)
        frame = uigtk.widgets.CommonFrame("Staff")
        self.attach(frame, 0, 1, 1, 1)
        frame = uigtk.widgets.CommonFrame("Media")
        self.attach(frame, 1, 1, 1, 1)
        frame = uigtk.widgets.CommonFrame("Overall")
        self.attach(frame, 0, 2, 2, 1)

    def run(self):
        self.show_all()
