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
import uigtk.information
import uigtk.menu
import uigtk.widgets


class MainScreen(Gtk.Grid):
    '''
    Main shell of the in-game window containing menus and information bar.
    '''
    def __init__(self):
        Gtk.Grid.__init__(self)

        self.menu = uigtk.menu.Menu()
        self.attach(self.menu, 0, 0, 1, 1)

        self.grid = uigtk.widgets.Grid()
        self.grid.set_vexpand(True)
        self.grid.set_border_width(5)
        self.attach(self.grid, 0, 1, 1, 1)

        self.information = uigtk.information.Information()
        self.grid.attach(self.information, 0, 1, 1, 1)

        self.show_all()
