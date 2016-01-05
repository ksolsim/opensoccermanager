#!/usr/bin/env python3

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
