#!/usr/bin/env python3

from gi.repository import Gtk
import gi
import platform

import data
import uigtk.widgets


class VersionDialog(Gtk.Dialog):
    def __init__(self, *args):
        Gtk.Dialog.__init__(self)
        self.set_transient_for(data.window)
        self.set_modal(True)
        self.set_resizable(False)
        self.set_title("Versions")
        self.add_button("_Close", Gtk.ResponseType.CLOSE)
        self.connect("response", self.on_response)
        self.vbox.set_border_width(5)

        grid = uigtk.widgets.Grid()
        self.vbox.add(grid)

        label = uigtk.widgets.Label("Python Version", leftalign=True)
        grid.attach(label, 0, 0, 1, 1)
        label = uigtk.widgets.Label("%s" % (platform.python_version()),
                                    leftalign=True)
        grid.attach(label, 1, 0, 1, 1)

        label = uigtk.widgets.Label("GTK+ Version", leftalign=True)
        grid.attach(label, 0, 1, 1, 1)
        label = uigtk.widgets.Label("%i.%i.%i" % (Gtk.MAJOR_VERSION,
                                                  Gtk.MINOR_VERSION,
                                                  Gtk.MICRO_VERSION),
                                    leftalign=True)
        grid.attach(label, 1, 1, 1, 1)

        label = uigtk.widgets.Label("GObject Version", leftalign=True)
        grid.attach(label, 0, 2, 1, 1)
        label = uigtk.widgets.Label("%i.%i.%i" % (gi.version_info),
                                    leftalign=True)
        grid.attach(label, 1, 2, 1, 1)

        self.show_all()

    def on_response(self, dialog, response):
        self.destroy()
