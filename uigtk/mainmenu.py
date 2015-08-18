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
import subprocess

from uigtk import interface
import dialogs
import game
import version
import widgets


class MainMenu(Gtk.Grid):
    def __init__(self):
        Gtk.Grid.__init__(self)
        self.set_row_spacing(40)
        self.set_border_width(5)

        buttonbox = Gtk.ButtonBox()
        buttonbox.set_hexpand(True)
        buttonbox.set_vexpand(True)
        buttonbox.set_orientation(Gtk.Orientation.VERTICAL)
        buttonbox.set_layout(Gtk.ButtonBoxStyle.EXPAND)
        buttonbox.set_border_width(25)
        self.attach(buttonbox, 1, 1, 1, 1)

        buttonNewGame = widgets.Button("_New Game")
        buttonNewGame.set_tooltip_text("Start a new game.")
        buttonNewGame.connect("clicked", self.new_game_clicked)
        buttonbox.add(buttonNewGame)
        buttonLoadGame = widgets.Button("_Load Game")
        buttonLoadGame.set_tooltip_text("Load a previously saved game.")
        buttonLoadGame.connect("clicked", self.load_game_clicked)
        buttonbox.add(buttonLoadGame)
        buttonDeleteGame = widgets.Button("_Delete Game")
        buttonDeleteGame.set_tooltip_text("Delete a previously saved game.")
        buttonDeleteGame.connect("clicked", self.delete_game_clicked)
        buttonbox.add(buttonDeleteGame)
        buttonPreferences = widgets.Button("_Preferences")
        buttonPreferences.set_tooltip_text("Adjust game settings.")
        buttonPreferences.connect("clicked", self.preferences_dialog_clicked)
        buttonbox.add(buttonPreferences)
        buttonEditor = widgets.Button("_Data Editor")
        buttonEditor.set_tooltip_text("Create new or edit existing game database.")
        buttonEditor.connect("clicked", self.editor_clicked)
        buttonbox.add(buttonEditor)
        buttonQuit = widgets.Button("_Quit")
        buttonQuit.set_tooltip_text("Quit the game.")
        buttonQuit.connect("clicked", game.window.exit_game)
        buttonbox.add(buttonQuit)

        self.buttonInfo = widgets.Button()
        self.buttonInfo.set_relief(Gtk.ReliefStyle.NONE)
        self.buttonInfo.set_label("Version %s (Build %s)" % (version.VERSION,
                                                             version.DATE))
        self.buttonInfo.connect("clicked", self.information_button_clicked)
        self.attach(self.buttonInfo, 0, 2, 1, 1)

        label = Gtk.Label()
        label.set_markup("<a href='%s'>%s Website</a>" % (version.WEBSITE,
                                                          version.NAME))
        label.set_alignment(1, 0.5)
        self.attach(label, 2, 2, 1, 1)

    def new_game_clicked(self, button):
        game.window.remove(game.window.screenMain)
        game.window.add(game.window.screenDetails)
        game.window.screenDetails.run()

    def load_game_clicked(self, button):
        dialog = interface.OpenDialog()

        if dialog.display():
            game.window.remove(game.window.screenMain)
            game.window.add(game.window.screenGame)
            game.window.screen_loader(game.active_screen_id)
            game.window.screenGame.run()

    def delete_game_clicked(self, button):
        dialog = interface.DeleteDialog()
        dialog.display()

    def editor_clicked(self, button):
        try:
            filepath = os.path.join("editor", "editor")
            subprocess.Popen(filepath, shell=False)
        except FileNotFoundError:
            dialogs.editor_not_found_error()

    def preferences_dialog_clicked(self, button):
        dialog = interface.PreferencesDialog()
        dialog.display()

    def information_button_clicked(self, button):
        dialog = interface.AboutDialog()
        dialog.display()
