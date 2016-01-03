#!/usr/bin/env python3

from gi.repository import Gtk
from gi.repository import GdkPixbuf
import os

import data


class Dialog(Gtk.AboutDialog):
    def __init__(self, *args):
        logo = data.window.logo.scale_simple(64, 64, GdkPixbuf.InterpType.BILINEAR)

        Gtk.AboutDialog.__init__(self)
        self.set_transient_for(data.window)
        self.set_program_name("OpenSoccerManager")
        self.set_website("https://opensoccermanager.org/")
        self.set_website_label("Website")
        self.set_license_type(Gtk.License.GPL_3_0)
        self.set_logo(logo)
        self.set_comments("Free software soccer management game written in Python and GTK+.")
        self.connect("response", self.on_response)

        self.show()

    def on_response(self, *args):
        self.destroy()
