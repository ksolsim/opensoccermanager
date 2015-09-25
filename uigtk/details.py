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

import club
import constants
import data
import date
import display
import game
import preferences
import user
import widgets


class Details(Gtk.Grid):
    '''
    Grab details for the game including manager name, club and finances.
    '''
    def __init__(self):
        Gtk.Grid.__init__(self)
        self.set_row_spacing(5)
        self.set_column_spacing(5)
        self.set_border_width(5)

        self.liststoreName = Gtk.ListStore(str)
        self.liststoreYears = Gtk.ListStore(int)
        self.liststoreLeagues = Gtk.ListStore(int, str)
        self.liststoreClubs = Gtk.ListStore(int, str)

        treemodelsort = Gtk.TreeModelSort(self.liststoreClubs)
        treemodelsort.set_sort_column_id(1, Gtk.SortType.ASCENDING)

        label = widgets.AlignedLabel("_Name")
        self.attach(label, 0, 0, 1, 1)
        self.comboboxName = Gtk.ComboBoxText.new_with_entry()
        self.comboboxName.set_model(self.liststoreName)
        self.comboboxName.set_tooltip_text("Your manager name which will be used in the game.")
        self.entryName = self.comboboxName.get_child()
        self.entryName.connect("changed", self.continue_status)
        label.set_mnemonic_widget(self.comboboxName)
        self.attach(self.comboboxName, 1, 0, 1, 1)

        label = widgets.AlignedLabel("_Database")
        self.attach(label, 0, 1, 1, 1)
        self.filechooserDatabase = Gtk.FileChooserButton()
        self.filechooserDatabase.set_title("Select Database")
        self.filechooserDatabase.set_action(Gtk.FileChooserAction.OPEN)
        self.filechooserDatabase.connect("file-set", self.file_chooser_set)
        filefilter = Gtk.FileFilter()
        filefilter.set_name("Database Files")
        filefilter.add_pattern("*.db")
        self.filechooserDatabase.add_filter(filefilter)
        label.set_mnemonic_widget(self.filechooserDatabase)
        self.attach(self.filechooserDatabase, 1, 1, 1, 1)

        cellrenderertext = Gtk.CellRendererText()

        label = widgets.AlignedLabel("_Year")
        self.attach(label, 0, 2, 1, 1)
        self.comboboxYear = Gtk.ComboBox()
        self.comboboxYear.set_model(self.liststoreYears)
        self.comboboxYear.pack_start(cellrenderertext, True)
        self.comboboxYear.add_attribute(cellrenderertext, "text", 0)
        self.comboboxYear.connect("changed", self.year_changed)
        self.comboboxYear.set_tooltip_text("Season in which the game will start.")
        label.set_mnemonic_widget(self.comboboxYear)
        self.attach(self.comboboxYear, 1, 2, 1, 1)

        label = widgets.AlignedLabel("_League")
        self.attach(label, 0, 3, 1, 1)
        self.comboboxLeague = Gtk.ComboBox()
        self.comboboxLeague.set_model(self.liststoreLeagues)
        self.comboboxLeague.pack_start(cellrenderertext, True)
        self.comboboxLeague.add_attribute(cellrenderertext, "text", 1)
        self.comboboxLeague.connect("changed", self.league_changed)
        self.comboboxLeague.set_tooltip_text("League in which the team you wish to manage is found.")
        label.set_mnemonic_widget(self.comboboxLeague)
        self.attach(self.comboboxLeague, 1, 3, 1, 1)

        label = widgets.AlignedLabel("_Club")
        self.attach(label, 0, 4, 1, 1)
        self.comboboxClub = Gtk.ComboBox()
        self.comboboxClub.set_model(treemodelsort)
        self.comboboxClub.pack_start(cellrenderertext, True)
        self.comboboxClub.add_attribute(cellrenderertext, "text", 1)
        self.comboboxClub.connect("changed", self.continue_status)
        self.comboboxClub.set_tooltip_text("Club which you wish to manage.")
        label.set_mnemonic_widget(self.comboboxClub)
        self.attach(self.comboboxClub, 1, 4, 1, 1)

        label = widgets.AlignedLabel("_Finances")
        self.attach(label, 0, 5, 1, 1)
        self.radiobuttonFinancesRep = Gtk.RadioButton("Reputation-Based Finances")
        self.radiobuttonFinancesRep.set_tooltip_text("Starting bank balance based on popularity of club.")
        self.radiobuttonFinancesRep.connect("toggled", self.finances_changed)
        label.set_mnemonic_widget(self.radiobuttonFinancesRep)
        self.attach(self.radiobuttonFinancesRep, 1, 5, 1, 1)
        self.radiobuttonFinancesUSM = Gtk.RadioButton("USM-Based Finances")
        self.radiobuttonFinancesUSM.join_group(self.radiobuttonFinancesRep)
        self.radiobuttonFinancesUSM.set_tooltip_text("Starting bank balance for all teams at set amount.")
        self.radiobuttonFinancesUSM.connect("toggled", self.finances_changed)
        self.attach(self.radiobuttonFinancesUSM, 2, 5, 1, 1)
        self.comboboxFinances = Gtk.ComboBoxText()
        self.comboboxFinances.set_sensitive(False)
        self.attach(self.comboboxFinances, 1, 6, 2, 1)

        buttonbox = Gtk.ButtonBox()
        buttonbox.set_spacing(5)
        buttonbox.set_layout(Gtk.ButtonBoxStyle.END)
        self.attach(buttonbox, 0, 7, 3, 1)
        buttonBack = widgets.Button("_Back")
        buttonBack.connect("clicked", self.back_button_clicked)
        buttonBack.set_tooltip_text("Go back to main menu.")
        buttonbox.add(buttonBack)
        self.buttonContinue = widgets.Button("_Continue")
        self.buttonContinue.set_sensitive(False)
        self.buttonContinue.connect("clicked", self.continue_button_clicked)
        self.buttonContinue.set_tooltip_text("Start the game with entered details.")
        buttonbox.add(self.buttonContinue)

        self.user = user.Names()

    def run(self):
        # Load financials
        self.comboboxFinances.remove_all()

        for key, item in constants.money.items():
            amount = display.currency(item[0])
            self.comboboxFinances.append(str(key), "%s (%s)" % (item[1], amount))

        # Load manager names
        self.liststoreName.clear()

        for name in self.user.read_names():
            self.liststoreName.append([name])

        self.entryName.set_text("")
        self.radiobuttonFinancesRep.set_active(True)
        self.comboboxFinances.set_active(0)

        if game.database.connect():
            # Set database to open
            filepath = os.path.join("databases", "%s" % (game.database_filename))
            self.filechooserDatabase.select_filename(filepath)

            self.load_year_list()

        self.show_all()
        self.entryName.grab_focus()

    def year_changed(self, combobox=None):
        self.load_league_list()

    def league_changed(self, combobox=None):
        self.load_club_list()

    def load_year_list(self):
        year_data = game.database.cursor.execute("SELECT * FROM year ORDER BY year ASC")

        self.liststoreYears.clear()

        for year in year_data.fetchall():
            self.liststoreYears.append([year[0]])

        self.comboboxYear.set_active(0)

    def load_league_list(self):
        model = self.comboboxYear.get_model()
        treeiter = self.comboboxYear.get_active()

        if treeiter != -1:
            year = model[treeiter][0]

            league_data = game.database.cursor.execute("SELECT league.id, league.name FROM league JOIN leagueattr ON leagueattr.league = league.id WHERE year = ?", (year,))

            self.liststoreLeagues.clear()

            for league in league_data.fetchall():
                self.liststoreLeagues.append(league)

            sensitive = len(self.liststoreLeagues) > 0
            self.comboboxLeague.set_sensitive(sensitive)
            self.comboboxLeague.set_active(0)

    def load_club_list(self):
        active = self.comboboxYear.get_active()
        year = self.liststoreYears[active][0]

        active = self.comboboxLeague.get_active()

        if active != -1:
            league = self.liststoreLeagues[active][0]

            club_data = game.database.cursor.execute("SELECT club.id, club.name FROM club JOIN clubattr ON clubattr.club = club.id WHERE year = ? AND league = ?", (year, league))

            self.liststoreClubs.clear()

            for club in club_data.fetchall():
                self.liststoreClubs.append(club)

            sensitive = len(self.liststoreClubs) > 0
            self.comboboxClub.set_sensitive(sensitive)
            self.comboboxClub.set_active(0)
        else:
            sensitive = len(self.liststoreClubs) > 0
            self.comboboxClub.set_sensitive(sensitive)
            self.liststoreClubs.clear()

    def file_chooser_set(self, filechooserbutton):
        game.database_filename = filechooserbutton.get_filename()
        game.database.connect(game.database_filename)

        preferences.preferences["DATABASE"]["Database"] = game.database_filename
        preferences.preferences.writefile()

        self.load_year_list()

    def finances_changed(self, radiobutton):
        active = self.radiobuttonFinancesUSM.get_active()
        self.comboboxFinances.set_sensitive(active)

    def continue_status(self, widget=None):
        sensitive = self.entryName.get_text_length() > 0

        if sensitive:
            sensitive = self.comboboxClub.get_active() != -1

        self.buttonContinue.set_sensitive(sensitive)

    def back_button_clicked(self, button):
        game.window.remove(game.window.screenDetails)
        game.window.add(game.window.screenMain)

    def continue_button_clicked(self, button):
        game.date = date.Date()

        active = self.comboboxYear.get_active()
        game.date.year = int(self.liststoreYears[active][0])

        # Get club ID number from combobox
        treeiter = self.comboboxClub.get_active_iter()
        model = self.comboboxClub.get_model()
        game.teamid = model[treeiter][0]

        data.datainit()

        # Save manager name entered by player
        manager = self.entryName.get_text()
        club.clubs[game.teamid].manager = manager

        self.user.add_name(manager)

        # Grab finance setup
        if self.radiobuttonFinancesUSM.get_active():
            finance = int(self.comboboxFinances.get_active_id())
        else:
            finance = -1

        data.dataloader(finance)

        game.database.connection.close()

        game.window.remove(game.window.screenDetails)
        game.window.add(game.window.screenGame)
        game.window.screen_loader(preferences.preferences.start_screen)
        game.window.screenGame.run()
