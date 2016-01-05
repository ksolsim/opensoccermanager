#!/usr/bin/env python3

from gi.repository import Gtk
from gi.repository import GdkPixbuf
import os

import data
import uigtk.helpdialog
import uigtk.quitdialog
import uigtk.screen
import uigtk.welcome


class Window(Gtk.Window):
    def __init__(self):
        data.preferences.read_from_config()

        iconpath = os.path.join("resources", "logo.svg")
        self.logo = GdkPixbuf.Pixbuf.new_from_file(iconpath)

        Gtk.Window.__init__(self)
        self.set_title("OpenSoccerManager")
        self.set_default_icon(self.logo)
        self.connect("delete-event", self.on_quit_game)
        self.connect("window-state-event", self.on_window_state_event)

        if data.preferences.window_maximized:
            self.maximize()
        else:
            xposition, yposition = data.preferences.window_position
            self.move(xposition, yposition)

        self.set_default_size(*data.preferences.window_size)

        self.accelgroup = Gtk.AccelGroup()
        self.add_accel_group(self.accelgroup)

    def on_window_state_event(self, *args):
        '''
        Handle move to original position on unmaximize event.
        '''
        if self.is_maximized():
            xposition, yposition = data.preferences.window_position
            self.move(xposition, yposition)

    def on_quit_game(self, *args):
        '''
        Quit game, displaying confirmation prompt if set to show.
        '''
        data.preferences.write_to_config()

        if data.preferences.confirm_quit:
            dialog = uigtk.quitdialog.QuitDialog()

            if dialog.run() == Gtk.ResponseType.OK:
                Gtk.main_quit()
            else:
                dialog.destroy()
        else:
            Gtk.main_quit()

        return True

    def run(self):
        self.mainscreen = uigtk.mainscreen.MainScreen()
        self.screen = uigtk.screen.Screen()
        self.help_dialog = uigtk.helpdialog.HelpDialog()

        self.welcome = uigtk.welcome.Welcome()
        self.add(self.welcome)

        self.show_all()

        Gtk.main()
