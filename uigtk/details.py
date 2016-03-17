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

import data
import structures.start
import uigtk.mainscreen
import uigtk.widgets


class Details(uigtk.widgets.Grid):
    '''
    Details collection screen including name, year, league, club, and financial
    selection.
    '''
    class User(uigtk.widgets.Grid):
        '''
        User details collection interface.
        '''
        class Finances(uigtk.widgets.Grid):
            def __init__(self):
                uigtk.widgets.Grid.__init__(self)

                label = uigtk.widgets.Label("Finances", leftalign=True)
                Details.sizegroupLabel.add_widget(label)
                self.attach(label, 0, 0, 1, 1)

                buttonbox = uigtk.widgets.ButtonBox()
                buttonbox.set_layout(Gtk.ButtonBoxStyle.START)
                self.attach(buttonbox, 1, 0, 1, 1)

                self.radiobuttonReputational = uigtk.widgets.RadioButton("_Reputational")
                self.radiobuttonReputational.finances = 0
                self.radiobuttonReputational.set_tooltip_text("Initial bank balance based on club reputation.")
                self.radiobuttonReputational.connect("toggled", self.on_finances_toggled)
                buttonbox.add(self.radiobuttonReputational)
                self.radiobuttonCategorised = uigtk.widgets.RadioButton("C_ategorised")
                self.radiobuttonCategorised.join_group(self.radiobuttonReputational)
                self.radiobuttonCategorised.finances = 1
                self.radiobuttonCategorised.set_tooltip_text("Initial bank balance based on set value.")
                self.radiobuttonCategorised.connect("toggled", self.on_finances_toggled)
                buttonbox.add(self.radiobuttonCategorised)

                self.comboboxCategorisedAmount = Gtk.ComboBoxText()
                self.comboboxCategorisedAmount.set_sensitive(False)
                self.comboboxCategorisedAmount.set_tooltip_text("Starting balance for categorised finances.")
                self.attach(self.comboboxCategorisedAmount, 1, 1, 2, 1)

                self.finances = structures.finances.Categories()

            def on_finances_toggled(self, radiobutton):
                '''
                Enable category-based finances dropdown menu.
                '''
                if radiobutton.finances == 1:
                    state = radiobutton.get_active()
                    self.comboboxCategorisedAmount.set_sensitive(state)

            def populate_finances(self):
                self.comboboxCategorisedAmount.remove_all()

                for key, value in self.finances.get_categories():
                    amount = data.currency.get_amount(value[0])
                    amount = data.currency.get_comma_value(amount)
                    category = "%s (%s)" % (value[1], "%s%s" % (data.currency.get_currency_symbol(), amount))
                    self.comboboxCategorisedAmount.append(str(key), category)

                self.comboboxCategorisedAmount.set_active(0)

        def __init__(self):
            uigtk.widgets.Grid.__init__(self)

            frame = uigtk.widgets.CommonFrame("User")
            self.attach(frame, 0, 0, 1, 1)

            label = uigtk.widgets.Label("_Name", leftalign=True)
            Details.sizegroupLabel.add_widget(label)
            frame.grid.attach(label, 0, 0, 1, 1)
            self.comboboxName = Gtk.ComboBoxText.new_with_entry()
            self.comboboxName.set_hexpand(True)
            self.comboboxName.set_tooltip_text("Managerial name of user to be used in-game.")
            self.entryName = self.comboboxName.get_child()
            self.entryName.set_input_purpose(Gtk.InputPurpose.NAME)
            label.set_mnemonic_widget(self.comboboxName);
            frame.grid.attach(self.comboboxName, 1, 0, 1, 1)

            frame = uigtk.widgets.CommonFrame("Game")
            self.attach(frame, 0, 1, 1, 1)

            label = uigtk.widgets.Label("_Start Season", leftalign=True)
            Details.sizegroupLabel.add_widget(label)
            frame.grid.attach(label, 0, 0, 1, 1)
            self.comboboxSeason = Gtk.ComboBoxText()
            self.comboboxSeason.set_hexpand(False)
            self.comboboxSeason.set_tooltip_text("Specify starting season of the game.")
            self.comboboxSeason.connect("changed", self.on_season_changed)
            label.set_mnemonic_widget(self.comboboxSeason)
            frame.grid.attach(self.comboboxSeason, 1, 0, 1, 1)

            label = uigtk.widgets.Label("_League", leftalign=True)
            Details.sizegroupLabel.add_widget(label)
            frame.grid.attach(label, 0, 1, 1, 1)
            self.comboboxLeague = Gtk.ComboBoxText()
            self.comboboxLeague.set_hexpand(True)
            self.comboboxLeague.set_tooltip_text("League in which the club to manage is located.")
            self.comboboxLeague.connect("changed", self.on_league_changed)
            label.set_mnemonic_widget(self.comboboxLeague)
            frame.grid.attach(self.comboboxLeague, 1, 1, 1, 1)

            label = uigtk.widgets.Label("_Club", leftalign=True)
            Details.sizegroupLabel.add_widget(label)
            frame.grid.attach(label, 0, 2, 1, 1)
            self.comboboxClub = Gtk.ComboBoxText()
            self.comboboxClub.set_hexpand(True)
            self.comboboxClub.set_tooltip_text("Club which the user will take charge of.")
            label.set_mnemonic_widget(self.comboboxClub)
            frame.grid.attach(self.comboboxClub, 1, 2, 1, 1)

            # Finances
            self.finances = self.Finances()
            frame.grid.attach(self.finances, 0, 3, 2, 1)

        def populate_names(self):
            '''
            Load list of previously used player names.
            '''
            self.entryName.set_text("")
            self.comboboxName.remove_all()

            for name in data.names.get_names():
                self.comboboxName.append_text(name)

        def populate_seasons(self):
            '''
            Load season selection into dropdown.
            '''
            self.comboboxSeason.remove_all()

            for season in data.seasons.get_seasons():
                text = "%i/%i" % (season, season + 1)
                self.comboboxSeason.append(str(season), text)

            self.comboboxSeason.set_active(0)

        def on_season_changed(self, combobox):
            '''
            Adjust data for selected season.
            '''
            self.populate_leagues()

        def populate_leagues(self):
            '''
            Load league selection for given season.
            '''
            season = self.comboboxSeason.get_active_id()

            data.database.cursor.execute("SELECT * FROM league \
                                         JOIN leagueattr \
                                         ON league.id = leagueattr.league \
                                         WHERE leagueattr.year = ? \
                                         ORDER BY league.name ASC",
                                         (season,))
            leagues = data.database.cursor.fetchall()

            self.comboboxLeague.remove_all()

            for league in leagues:
                self.comboboxLeague.append(str(league[0]), league[1])

            self.comboboxLeague.set_active(0)

        def on_league_changed(self, combobox):
            '''
            Adjust data for selected league.
            '''
            self.populate_clubs()

        def populate_clubs(self):
            '''
            Load club selection for given league.
            '''
            season = self.comboboxSeason.get_active_id()
            leagueid = self.comboboxLeague.get_active_id()

            data.database.cursor.execute("SELECT * FROM club \
                                          JOIN clubattr \
                                          ON club.id = clubattr.club \
                                          WHERE clubattr.league = ? \
                                          AND clubattr.year = ? \
                                          ORDER BY club.name ASC",
                                          (leagueid, season))
            clubs = data.database.cursor.fetchall()

            self.comboboxClub.remove_all()

            for club in clubs:
                self.comboboxClub.append(str(club[0]), club[1])

            self.comboboxClub.set_active(0)

    class Buttons(uigtk.widgets.ButtonBox):
        '''
        Button interface for continue or back.
        '''
        def __init__(self):
            uigtk.widgets.ButtonBox.__init__(self)
            self.set_layout(Gtk.ButtonBoxStyle.END)

            self.buttonBack = uigtk.widgets.Button("_Back")
            self.buttonBack.set_tooltip_text("Return back to the main menu.")
            self.add(self.buttonBack)

            self.buttonStart = uigtk.widgets.Button("_Start Game")
            self.buttonStart.set_sensitive(False)
            self.buttonStart.set_tooltip_text("Start playing game with entered details.")
            self.add(self.buttonStart)

        def set_start_sensitive(self, sensitive):
            self.buttonStart.set_sensitive(sensitive)

    sizegroupLabel = Gtk.SizeGroup()

    def __init__(self):
        uigtk.widgets.Grid.__init__(self)
        self.set_border_width(5)

        self.sizegroupLabel.set_mode(Gtk.SizeGroupMode.HORIZONTAL)

        label = Gtk.Label()
        label.set_hexpand(True)
        self.attach(label, 0, 0, 1, 1)
        label = Gtk.Label()
        label.set_hexpand(True)
        self.attach(label, 2, 0, 1, 1)

        grid = uigtk.widgets.Grid()
        grid.set_hexpand(False)
        self.attach(grid, 1, 0, 1, 1)

        frame = uigtk.widgets.CommonFrame("Database")
        grid.attach(frame, 0, 0, 1, 1)

        label = uigtk.widgets.Label("_Location", leftalign=True)
        self.sizegroupLabel.add_widget(label)
        frame.grid.attach(label, 0, 1, 1, 1)
        self.filechooserDatabase = Gtk.FileChooserButton()
        self.filechooserDatabase.set_hexpand(True)
        self.filechooserDatabase.set_title("Select Database")
        self.filechooserDatabase.set_action(Gtk.FileChooserAction.OPEN)
        self.filechooserDatabase.set_tooltip_text("Database of data to be loaded and used by the game.")
        self.filechooserDatabase.connect("file-set", self.on_database_file_set)
        label.set_mnemonic_widget(self.filechooserDatabase)
        frame.grid.attach(self.filechooserDatabase, 1, 1, 1, 1)

        filefilter = Gtk.FileFilter()
        filefilter.set_name("Database Files")
        filefilter.add_pattern("*.db")
        self.filechooserDatabase.add_filter(filefilter)
        label.set_mnemonic_widget(self.filechooserDatabase)

        self.user = self.User()
        self.user.set_sensitive(False)
        self.user.entryName.connect("changed", self.on_name_changed)
        grid.attach(self.user, 0, 1, 1, 1)

        self.buttons = self.Buttons()
        self.buttons.buttonBack.connect("clicked", self.on_back_clicked)
        self.buttons.buttonStart.connect("clicked", self.on_start_clicked)
        grid.attach(self.buttons, 0, 2, 1, 1)

    def on_database_file_set(self, filechooserbutton):
        '''
        Enable details entry if database is selected.
        '''
        if self.filechooserDatabase.get_filename():
            self.user.set_sensitive(True)
        else:
            self.user.set_sensitive(False)

    def on_name_changed(self, entry):
        '''
        Allow game to be started if name is entered.
        '''
        state = entry.get_text_length() > 0
        self.buttons.set_start_sensitive(state)

    def on_back_clicked(self, *args):
        '''
        Return back to main menu screen.
        '''
        data.window.remove(self)
        data.window.add(data.window.welcome)

    def on_start_clicked(self, *args):
        '''
        Load main game screen with screen from preferences.
        '''
        season = self.user.comboboxSeason.get_active_id()
        clubid = int(self.user.comboboxClub.get_active_id())

        start = structures.start.Start(clubid, season)

        name = self.user.entryName.get_text()
        start.set_manager_name(name)

        self.set_initial_finances()

        data.window.remove(self)
        data.window.add(data.window.mainscreen)
        data.window.mainscreen.grid.attach(data.window.screen, 0, 0, 1, 1)

        data.window.mainscreen.information.update_date()

        data.window.screen.run()
        data.window.screen.change_visible_screen("squad")

        data.database.close()

        start.setup_initial_values()

    def set_initial_finances(self):
        '''
        Call initial balance generation based on option.
        '''
        if self.user.finances.radiobuttonReputational.get_active():
            option = -1
        else:
            option = int(self.user.finances.comboboxCategorisedAmount.get_active_id())

        data.clubs.set_initial_balance(option)

    def run(self):
        if data.database.connect("databases/opensoccermanager.db"):
            self.filechooserDatabase.set_filename("databases/opensoccermanager.db")

            self.user.set_sensitive(True)
            self.user.populate_names()

            data.seasons = structures.seasons.Seasons()
            self.user.populate_seasons()

            if len(data.names.get_names()) > 0:
                self.user.entryName.set_text(data.names.get_first_name())

            self.user.finances.populate_finances()

        self.user.finances.radiobuttonReputational.set_active(True)

        self.show_all()
