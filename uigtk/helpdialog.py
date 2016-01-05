#!/usr/bin/env python3

from gi.repository import Gtk
import os

import data
import uigtk.widgets


class HelpDialog(Gtk.Dialog):
    def __init__(self):
        Gtk.Dialog.__init__(self)
        self.set_transient_for(data.window)
        self.set_title("Help Content")
        self.set_default_size(480, 320)
        self.add_button("_Close", Gtk.ResponseType.CLOSE)
        self.connect("response", self.on_response)

        scrolledwindow = uigtk.widgets.ScrolledWindow()
        scrolledwindow.set_vexpand(True)
        scrolledwindow.set_hexpand(True)
        self.vbox.add(scrolledwindow)

        textview = Gtk.TextView()
        textview.set_editable(False)
        textview.set_wrap_mode(Gtk.WrapMode.WORD)
        textview.set_left_margin(5)
        textview.set_right_margin(5)
        scrolledwindow.add(textview)
        self.textbuffer = textview.get_buffer()

    def show(self):
        filename = os.path.join("help", "%s.txt" % (data.window.screen.active.name))

        try:
            with open(filename, "r") as fp:
                content = fp.read()
                content = content.rstrip("\n")

            self.textbuffer.set_text(content, -1)
            self.show_all()
        except FileNotFoundError:
            HelpNotFound()

    def on_response(self, *args):
        self.hide()


class HelpNotFound(Gtk.MessageDialog):
    def __init__(self):
        Gtk.MessageDialog.__init__(self)
        self.set_transient_for(data.window)
        self.set_title("Help Not Found")
        self.set_markup("No help file was found for this screen.")
        self.set_property("message-type", Gtk.MessageType.ERROR)
        self.add_button("_Close", Gtk.ResponseType.CLOSE)
        self.connect("response", self.on_response)

        self.show()

    def on_response(self, *args):
        self.destroy()
