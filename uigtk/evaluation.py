#!/usr/bin/env python3

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
