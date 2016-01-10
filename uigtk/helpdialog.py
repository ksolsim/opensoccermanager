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
import os

import data
import uigtk.widgets


class HelpDialog(Gtk.Dialog):
    def __init__(self):
        Gtk.Dialog.__init__(self)
        self.set_transient_for(data.window)
        self.set_modal(True)
        self.set_default_size(480, 320)
        self.set_title("Help Content")
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
