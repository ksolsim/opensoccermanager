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
import uigtk.widgets


class Fixtures(uigtk.widgets.Grid):
    __name__ = "fixtures"

    def __init__(self):
        uigtk.widgets.Grid.__init__(self)

        grid = uigtk.widgets.Grid()
        self.attach(grid, 0, 0, 1, 1)

        self.liststoreLeagues = Gtk.ListStore(str, str)
        treemodelsort = Gtk.TreeModelSort(self.liststoreLeagues)
        treemodelsort.set_sort_column_id(1, Gtk.SortType.ASCENDING)

        label = uigtk.widgets.Label("_League")
        grid.attach(label, 0, 0, 1, 1)
        self.comboboxLeagues = uigtk.widgets.ComboBox(column=1)
        self.comboboxLeagues.set_model(treemodelsort)
        self.comboboxLeagues.set_id_column(0)
        self.comboboxLeagues.set_tooltip_text("Select league to show visible fixtures.")
        self.comboboxLeagues.connect("changed", self.on_league_changed)
        label.set_mnemonic_widget(self.comboboxLeagues)
        grid.attach(self.comboboxLeagues, 1, 0, 1, 1)

        label = uigtk.widgets.Label("Display", leftalign=True)
        grid.attach(label, 2, 0, 1, 1)

        self.radiobuttonAllFixtures = uigtk.widgets.RadioButton("_All Fixtures")
        self.radiobuttonAllFixtures.view = 0
        self.radiobuttonAllFixtures.set_tooltip_text("Display fixtures for all clubs.")
        self.radiobuttonAllFixtures.connect("toggled", self.on_view_toggled)
        grid.attach(self.radiobuttonAllFixtures, 3, 0, 1, 1)
        self.radiobuttonClubFixtures = uigtk.widgets.RadioButton()
        self.radiobuttonClubFixtures.join_group(self.radiobuttonAllFixtures)
        self.radiobuttonClubFixtures.view = 1
        self.radiobuttonClubFixtures.set_tooltip_text("Display only fixtures for your club.")
        self.radiobuttonClubFixtures.connect("toggled", self.on_view_toggled)
        grid.attach(self.radiobuttonClubFixtures, 4, 0, 1, 1)

        label = Gtk.Label()
        label.set_hexpand(True)
        grid.attach(label, 5, 0, 1, 1)

        buttonFriendly = uigtk.widgets.Button("Arrange _Friendly")
        buttonFriendly.set_tooltip_text("Arrange a pre-season friendly with another club.")
        buttonFriendly.connect("clicked", self.on_friendly_clicked)
        grid.attach(buttonFriendly, 6, 0, 1, 1)

        scrolledwindow = uigtk.widgets.ScrolledWindow()
        self.attach(scrolledwindow, 0, 1, 1, 1)

        self.treestore = Gtk.TreeStore(int, str, str, str, str, int)

        self.treeview = uigtk.widgets.TreeView()
        self.treeview.set_vexpand(True)
        self.treeview.set_hexpand(True)
        self.treeview.set_model(self.treestore)
        self.treeview.connect("row-activated", self.on_fixture_clicked)
        scrolledwindow.add(self.treeview)

        cellrenderertext = Gtk.CellRendererText()

        treeviewcolumn = Gtk.TreeViewColumn("Home")
        treeviewcolumn.set_expand(True)
        treeviewcolumn.pack_start(cellrenderertext, True)
        treeviewcolumn.add_attribute(cellrenderertext, "text", 1)
        treeviewcolumn.add_attribute(cellrenderertext, "weight", 5)
        self.treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Result", column=2)
        treeviewcolumn.set_fixed_width(60)
        self.treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Away", column=3)
        treeviewcolumn.set_expand(True)
        self.treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Stadium", column=4)
        treeviewcolumn.set_expand(True)
        self.treeview.append_column(treeviewcolumn)

    def on_view_toggled(self, radiobutton):
        '''
        Change visible view and repopulate shown data.
        '''
        if radiobutton.view == 0:
            self.comboboxLeagues.set_sensitive(True)
            self.treeview.set_show_expanders(True)
            self.populate_all_data()
        else:
            self.comboboxLeagues.set_sensitive(False)
            self.treeview.set_show_expanders(False)
            self.populate_club_data()

    def on_fixture_clicked(self, treeview, treepath, treeviewcolumn):
        '''
        Load result view screen for selected fixture.
        '''
        model = treeview.get_model()
        treeiter = model.get_iter(treepath)

        if not model.iter_has_child(treeiter):
            fixtureid = model[treeiter][0]
            leagueid = int(self.comboboxLeagues.get_active_id())

            data.window.screen.change_visible_screen("result")
            data.window.screen.active.set_visible_result(leagueid, fixtureid)

    def on_friendly_clicked(self, *args):
        '''
        Launch dialog to arrange a pre-season friendly.
        '''
        dialog = FriendlyDialog()

    def on_league_changed(self, *args):
        '''
        Change selection of visible league.
        '''
        self.populate_all_data()

    def populate_leagues(self):
        self.liststoreLeagues.clear()

        for leagueid, league in data.leagues.get_leagues():
            self.liststoreLeagues.append([str(leagueid), league.name])

        self.comboboxLeagues.set_active(0)

    def populate_all_data(self):
        if self.comboboxLeagues.get_active_id():
            self.treestore.clear()

            leagueid = int(self.comboboxLeagues.get_active_id())
            league = data.leagues.get_league_by_id(leagueid)

            rounds = league.fixtures.get_number_of_rounds()

            for week in range(0, rounds):
                day, month = league.fixtures.events[week]

                title = "Round %i - %i/%i" % (week + 1, day, month)
                parent = self.treestore.append(None, [None, title, "", "", "", 700])

                fixtures = league.fixtures.get_fixtures_for_week(week)

                for fixtureid, fixture in fixtures.items():
                    home = data.clubs.get_club_by_id(fixture.home.clubid)
                    away = data.clubs.get_club_by_id(fixture.away.clubid)

                    if fixture.result:
                        result = "%i - %i" % (fixture.result)
                    else:
                        result = ""

                    self.treestore.append(parent, [fixtureid,
                                                   home.name,
                                                   result,
                                                   away.name,
                                                   home.stadium.name,
                                                   400])

            self.treeview.expand_all()

    def populate_club_data(self):
        self.treestore.clear()

        rounds = data.user.club.league.fixtures.get_number_of_rounds()

        for week in range(0, rounds):
            fixtures = data.user.club.league.fixtures.get_fixtures_for_week(week)

            for fixtureid, fixture in fixtures.items():
                if data.user.clubid in (fixture.home.clubid, fixture.away.clubid):
                    home = data.clubs.get_club_by_id(fixture.home.clubid)
                    away = data.clubs.get_club_by_id(fixture.away.clubid)

                    if fixture.result:
                        result = "%i - %i" % (fixture.result)
                    else:
                        result = ""

                    self.treestore.append(None, [fixtureid,
                                                 home.name,
                                                 result,
                                                 away.name,
                                                 home.stadium.name,
                                                 400])

    def run(self):
        self.populate_leagues()
        self.populate_all_data()

        self.radiobuttonAllFixtures.set_active(True)
        self.radiobuttonClubFixtures.set_label("%s _Fixtures" % (data.user.club.name))

        self.show_all()


class FriendlyDialog(Gtk.Dialog):
    '''
    Dialog displayed when arranging a friendly match.
    '''
    def __init__(self):
        Gtk.Dialog.__init__(self)
        self.set_transient_for(data.window)
        self.set_resizable(False)
        self.set_modal(True)
        self.set_title("Arrange Friendly")
        self.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("_Arrange", Gtk.ResponseType.OK)
        self.set_default_response(Gtk.ResponseType.CANCEL)
        self.connect("response", self.on_response)
        self.vbox.set_border_width(5)

        grid = uigtk.widgets.Grid()
        self.vbox.add(grid)

        self.liststoreLeagues = Gtk.ListStore(str, str)
        self.treemodelsort = Gtk.TreeModelSort(self.liststoreLeagues)
        self.treemodelsort.set_sort_column_id(1, Gtk.SortType.ASCENDING)

        label = uigtk.widgets.Label("_League", leftalign=True)
        grid.attach(label, 0, 0, 1, 1)
        self.comboboxLeague = uigtk.widgets.ComboBox(column=1)
        self.comboboxLeague.set_model(self.treemodelsort)
        self.comboboxLeague.set_id_column(0)
        self.comboboxLeague.set_tooltip_text("Choose league of opposition team for friendly.")
        self.comboboxLeague.connect("changed", self.on_league_changed)
        label.set_mnemonic_widget(self.comboboxLeague)
        grid.attach(self.comboboxLeague, 1, 0, 1, 1)

        self.liststoreClubs = Gtk.ListStore(str, str)
        self.treemodelsort = Gtk.TreeModelSort(self.liststoreClubs)
        self.treemodelsort.set_sort_column_id(1, Gtk.SortType.ASCENDING)

        label = uigtk.widgets.Label("_Opposition", leftalign=True)
        grid.attach(label, 0, 1, 1, 1)
        self.comboboxOpposition = uigtk.widgets.ComboBox(column=1)
        self.comboboxOpposition.set_model(self.treemodelsort)
        self.comboboxOpposition.set_id_column(0)
        self.comboboxOpposition.set_tooltip_text("Choose opposition to compete in friendly match.")
        label.set_mnemonic_widget(self.comboboxOpposition)
        grid.attach(self.comboboxOpposition, 1, 1, 1, 1)

        self.populate_leagues()

        self.show_all()

        self.comboboxLeague.set_active(0)

    def on_league_changed(self, combobox):
        '''
        Repopulate clubs list when league selection is changed.
        '''
        if combobox.get_active_id():
            self.populate_clubs()

    def populate_leagues(self):
        self.liststoreLeagues.clear()

        for leagueid, league in data.leagues.get_leagues():
            self.liststoreLeagues.append([str(leagueid), league.name])

    def populate_clubs(self):
        self.liststoreClubs.clear()

        for leagueid, league in data.leagues.get_leagues():
            for clubid in league.get_clubs():
                if leagueid == int(self.comboboxLeague.get_active_id()):
                    if clubid != data.user.clubid:
                        club = data.clubs.get_club_by_id(clubid)
                        self.liststoreClubs.append([str(clubid), club.name])

        self.comboboxOpposition.set_active(0)

    def on_response(self, dialog, response):
        self.destroy()
