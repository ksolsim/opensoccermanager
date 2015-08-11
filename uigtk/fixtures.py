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

import club
import game
import league
import user
import widgets


class Fixtures(Gtk.Grid):
    __name__ = "fixtures"

    page = 0

    def __init__(self):
        Gtk.Grid.__init__(self)
        self.set_row_spacing(5)
        self.set_column_spacing(5)

        self.liststoreClubFixtures = Gtk.ListStore(str)         # Club fixtures
        self.liststoreFixtures = Gtk.ListStore(str, str, str)  # All fixtures

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_policy(Gtk.PolicyType.NEVER,
                                  Gtk.PolicyType.AUTOMATIC)
        self.attach(scrolledwindow, 0, 1, 1, 1)

        # Fixtures for players club
        label = widgets.AlignedLabel("Your Fixtures")
        self.attach(label, 0, 0, 1, 1)

        self.treeviewClubFixtures = Gtk.TreeView()
        self.treeviewClubFixtures.set_headers_visible(False)
        self.treeviewClubFixtures.set_model(self.liststoreClubFixtures)
        self.treeviewClubFixtures.set_vexpand(True)
        self.treeviewClubFixtures.set_enable_search(False)
        self.treeviewClubFixtures.set_search_column(-1)
        scrolledwindow.add(self.treeviewClubFixtures)

        treeviewcolumn = widgets.TreeViewColumn(column=0)
        self.treeviewClubFixtures.append_column(treeviewcolumn)

        # Fixtures for all clubs
        self.labelFixturesView = widgets.AlignedLabel("Round 1")
        self.attach(self.labelFixturesView, 1, 0, 1, 1)

        buttonbox = Gtk.ButtonBox()
        buttonbox.set_spacing(5)
        buttonbox.set_layout(Gtk.ButtonBoxStyle.END)
        self.buttonPrevious = widgets.Button("_Previous")
        self.buttonPrevious.set_sensitive(False)
        self.buttonPrevious.connect("clicked", self.change_fixtures, -1)
        buttonbox.add(self.buttonPrevious)
        self.buttonNext = widgets.Button("_Next")
        self.buttonNext.connect("clicked", self.change_fixtures, 1)
        buttonbox.add(self.buttonNext)
        self.attach(buttonbox, 2, 0, 1, 1)

        self.comboboxLeagues = Gtk.ComboBoxText()
        self.comboboxLeagues.set_hexpand(False)
        self.comboboxLeagues.connect("changed", self.combobox_changed)
        self.attach(self.comboboxLeagues, 3, 0, 1, 1)

        treeviewFixtures = Gtk.TreeView()
        treeviewFixtures.set_model(self.liststoreFixtures)
        treeviewFixtures.set_enable_search(False)
        treeviewFixtures.set_search_column(-1)
        treeviewFixtures.set_vexpand(True)
        treeviewFixtures.set_hexpand(True)
        treeselection = treeviewFixtures.get_selection()
        treeselection.set_mode(Gtk.SelectionMode.NONE)
        self.attach(treeviewFixtures, 1, 1, 3, 1)

        treeviewcolumn = widgets.TreeViewColumn(title="Home", column=0)
        treeviewcolumn.set_expand(True)
        treeviewFixtures.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Away", column=1)
        treeviewcolumn.set_expand(True)
        treeviewFixtures.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Venue", column=2)
        treeviewcolumn.set_expand(True)
        treeviewFixtures.append_column(treeviewcolumn)

    def change_fixtures(self, button, direction):
        leagueid = int(self.comboboxLeagues.get_active_id())

        fixtures = league.leagueitem.leagues[leagueid].fixtures

        self.page += direction

        sensitive = self.page > 0
        self.buttonPrevious.set_sensitive(sensitive)

        sensitive = self.page < fixtures.get_number_of_rounds() - 1
        self.buttonNext.set_sensitive(sensitive)

        self.populate_data()

    def combobox_changed(self, combobox):
        self.populate_data()

    def populate_data(self):
        self.liststoreClubFixtures.clear()

        clubobj = user.get_user_club()

        fixtures = league.leagueitem.leagues[clubobj.league].fixtures

        for week in fixtures.fixtures:
            for match in week:
                if game.teamid in match:
                    match = "%s - %s" % (club.clubitem.clubs[match[0]].name,
                                         club.clubitem.clubs[match[1]].name)
                    self.liststoreClubFixtures.append([match])

        self.liststoreFixtures.clear()

        self.labelFixturesView.set_label("Round %i" % (self.page + 1))

        if self.comboboxLeagues.get_active_id():
            leagueid = int(self.comboboxLeagues.get_active_id())

            fixtures = league.leagueitem.leagues[leagueid].fixtures

            for teamid1, teamid2 in fixtures.fixtures[self.page]:
                team1 = club.clubitem.clubs[teamid1].name
                team2 = club.clubitem.clubs[teamid2].name

                #stadium = club.clubitem.clubs[teamid1].get_stadium_name()
                stadium = ""

                self.liststoreFixtures.append([team1, team2, stadium])

    def run(self):
        self.page = game.date.fixturesindex

        sensitive = self.page > 0
        self.buttonPrevious.set_sensitive(sensitive)

        self.comboboxLeagues.remove_all()

        for leagueid, value in league.leagueitem.leagues.items():
            self.comboboxLeagues.append(str(leagueid), value.name)

        self.comboboxLeagues.set_active(0)

        self.populate_data()

        self.show_all()
