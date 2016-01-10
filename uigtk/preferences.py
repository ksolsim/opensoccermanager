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
import music
import structures.currency
import uigtk.widgets


class Dialog(Gtk.Dialog):
    def __init__(self, *args):
        Gtk.Dialog.__init__(self)
        self.set_transient_for(data.window)
        self.set_modal(True)
        self.set_resizable(False)
        self.set_title("Preferences")
        self.add_button("_Close", Gtk.ResponseType.CLOSE)
        self.connect("response", self.on_response)
        self.vbox.set_border_width(5)
        self.vbox.set_spacing(5)

        frame = uigtk.widgets.CommonFrame("Music")
        self.vbox.add(frame)

        checkbuttonMusic = Gtk.CheckButton("_Play (Annoying) USM Music In Background")
        checkbuttonMusic.set_use_underline(True)
        checkbuttonMusic.set_active(data.preferences.play_music)
        checkbuttonMusic.connect("toggled", self.on_music_playback_toggled)
        frame.insert(checkbuttonMusic)

        frame = uigtk.widgets.CommonFrame("Display")
        self.vbox.add(frame)

        label = uigtk.widgets.Label("In-Game _Opening Screen", leftalign=True)
        frame.grid.attach(label, 0, 1, 1, 1)
        comboboxScreen = Gtk.ComboBoxText()
        comboboxScreen.append("squad", "Squad")
        comboboxScreen.append("fixtures", "Fixtures")
        comboboxScreen.append("news", "News")
        comboboxScreen.append("playersearch", "Player Search")
        comboboxScreen.set_active_id(data.preferences.start_screen)
        comboboxScreen.set_tooltip_text("Choose which screen should first appear when starting new and loading saved games.")
        comboboxScreen.connect("changed", self.on_start_screen_changed)
        label.set_mnemonic_widget(comboboxScreen)
        frame.grid.attach(comboboxScreen, 1, 1, 2, 1)

        label = uigtk.widgets.Label("Display _Currency", leftalign=True)
        frame.grid.attach(label, 0, 2, 1, 1)
        comboboxCurrency = Gtk.ComboBoxText()

        for key, value in data.currency.get_currency_names():
            comboboxCurrency.append(str(key), value)

        comboboxCurrency.set_active_id(str(data.preferences.currency))
        comboboxCurrency.set_tooltip_text("The monetary currency which will be used in-game.")
        comboboxCurrency.connect("changed", self.on_currency_changed)
        label.set_mnemonic_widget(comboboxCurrency)
        frame.grid.attach(comboboxCurrency, 1, 2, 2, 1)

        checkbuttonConfirmQuit = uigtk.widgets.CheckButton("_Confirm Quit When Exiting")
        checkbuttonConfirmQuit.set_active(data.preferences.confirm_quit)
        checkbuttonConfirmQuit.set_tooltip_text("Confirm from user whether they want to quit the game.")
        checkbuttonConfirmQuit.connect("toggled", self.on_confirm_quit_toggled)
        frame.grid.attach(checkbuttonConfirmQuit, 0, 3, 3, 1)

        # Data locations
        frame = uigtk.widgets.CommonFrame("Data")
        frame.grid.set_row_homogeneous(True)
        self.vbox.add(frame)

        label = uigtk.widgets.Label("Default _Database Location", leftalign=True)
        frame.grid.attach(label, 0, 0, 1, 1)
        filechooserDatabaseLocation = Gtk.FileChooserButton()
        filechooserDatabaseLocation.set_tooltip_text("Location of default database file to load.")
        filechooserDatabaseLocation.set_action(Gtk.FileChooserAction.OPEN)
        filechooserDatabaseLocation.set_filename(data.preferences.database_path)
        filechooserDatabaseLocation.connect("file-set", self.on_database_location_changed)
        label.set_mnemonic_widget(filechooserDatabaseLocation)
        frame.grid.attach(filechooserDatabaseLocation, 1, 0, 1, 1)

        label = uigtk.widgets.Label("_Game Data Location", leftalign=True)
        frame.grid.attach(label, 0, 1, 1, 1)
        filechooserSaveLocation = Gtk.FileChooserButton()
        filechooserSaveLocation.set_tooltip_text("Default location where game data is stored.")
        filechooserSaveLocation.set_action(Gtk.FileChooserAction.SELECT_FOLDER)
        filechooserSaveLocation.set_filename(data.preferences.data_path)
        filechooserSaveLocation.connect("file-set", self.on_data_location_changed)
        label.set_mnemonic_widget(filechooserSaveLocation)
        frame.grid.attach(filechooserSaveLocation, 1, 1, 1, 1)

        # Manager names
        frame = uigtk.widgets.CommonFrame("User")
        self.vbox.add(frame)

        label = uigtk.widgets.Label("Clear Previous Manager Names", leftalign=True)
        frame.grid.attach(label, 0, 0, 1, 1)
        buttonbox = Gtk.ButtonBox()
        frame.grid.attach(buttonbox, 1, 0, 1, 1)
        buttonClear = uigtk.widgets.Button("_Clear Names")
        buttonClear.connect("clicked", self.on_clear_names)
        buttonbox.add(buttonClear)

        self.show_all()

    def on_music_playback_toggled(self, checkbutton):
        '''
        Toggle playback on in-game music.
        '''
        if not data.preferences.play_music:
            data.music.play()
        else:
            data.music.stop()

        data.preferences.write_to_config()

    def on_confirm_quit_toggled(self, checkbutton):
        '''
        Toggle quit confirmation dialog.
        '''
        data.preferences.confirm_quit = checkbutton.get_active()
        data.preferences.write_to_config()

    def on_currency_changed(self, combobox):
        '''
        Update selected display currency.
        '''
        data.preferences.currency = int(combobox.get_active_id())
        data.preferences.write_to_config()

    def on_start_screen_changed(self, combobox):
        '''
        Update starting screen for new or loaded games.
        '''
        data.preferences.start_screen = combobox.get_active_id()
        data.preferences.write_to_config()

    def on_database_location_changed(self, filechooser):
        '''
        Set default location of database.
        '''
        directory = filechooser.get_uri()
        data.preferences.database_path = directory[7:]

        data.preferences.write_to_config()

    def on_data_location_changed(self, filechooser):
        '''
        Set location of data files and save game folder.
        '''
        directory = filechooser.get_uri()
        data.preferences.data_path = directory[7:]
        data.preferences.save_path = os.path.join(data.preferences.data_path, "saves")

        os.makedirs(data.preferences.save_path)

        data.preferences.write_to_config()

    def on_clear_names(self, *args):
        '''
        Clear existing names file.
        '''
        filepath = os.path.join(data.preferences.data_path, "users.txt")
        open(filepath, "w").close()

        data.names.clear_names()

    def on_response(self, *args):
        self.destroy()

        data.window.screen.refresh_visible_screen()
