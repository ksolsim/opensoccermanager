#!/usr/bin/env python3

from gi.repository import Gtk

import data
import uigtk.information
import uigtk.menu
import uigtk.screen
import uigtk.widgets


class MainScreen(Gtk.Grid):
    '''
    Main shell of the in-game window containing menus and information bar.
    '''
    def __init__(self):
        Gtk.Grid.__init__(self)

        menu = uigtk.menu.Menu()
        self.attach(menu, 0, 0, 1, 1)

        self.grid = uigtk.widgets.Grid()
        self.grid.set_vexpand(True)
        self.grid.set_border_width(5)
        self.attach(self.grid, 0, 1, 1, 1)

        self.information = uigtk.information.Information()
        self.grid.attach(self.information, 0, 1, 1, 1)

        self.show_all()
