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


class Standings(Gtk.Grid):
    __name__ = "standings"

    def __init__(self):
        Gtk.Grid.__init__(self)
        self.set_row_spacing(5)

        grid = uigtk.widgets.Grid()
        self.attach(grid, 0, 0, 1, 1)

        self.liststoreLeagues = Gtk.ListStore(str, str)
        treemodelsort = Gtk.TreeModelSort(self.liststoreLeagues)
        treemodelsort.set_sort_column_id(1, Gtk.SortType.ASCENDING)

        label = uigtk.widgets.Label("League")
        grid.attach(label, 0, 0, 1, 1)

        self.comboboxLeague = uigtk.widgets.ComboBox(column=1)
        self.comboboxLeague.set_model(treemodelsort)
        self.comboboxLeague.set_id_column(0)
        self.comboboxLeague.connect("changed", self.on_league_changed)
        grid.attach(self.comboboxLeague, 1, 0, 1, 1)

        scrolledwindow = uigtk.widgets.ScrolledWindow()
        self.attach(scrolledwindow, 0, 1, 1, 1)

        self.liststoreStandings = Gtk.ListStore(int, str, int, int, int, int,
                                                int, int, int, int, str)

        treeview = uigtk.widgets.TreeView()
        treeview.set_hexpand(True)
        treeview.set_vexpand(True)
        treeview.set_model(self.liststoreStandings)
        treeview.connect("row-activated", self.on_row_activated)
        scrolledwindow.add(treeview)

        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Club", column=1)
        treeviewcolumn.set_expand(True)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Played", column=2)
        treeviewcolumn.set_fixed_width(50)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Wins", column=3)
        treeviewcolumn.set_fixed_width(50)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Draws", column=4)
        treeviewcolumn.set_fixed_width(50)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Losses", column=5)
        treeviewcolumn.set_fixed_width(50)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="GF",
                                                      tooltip="Goals For",
                                                      column=6)
        treeviewcolumn.set_fixed_width(50)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="GA",
                                                      tooltip="Goals Against",
                                                      column=7)
        treeviewcolumn.set_fixed_width(50)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="GD",
                                                      tooltip="Goal Difference",
                                                      column=8)
        treeviewcolumn.set_fixed_width(50)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Points", column=9)
        treeviewcolumn.set_fixed_width(50)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Form", column=10)
        treeviewcolumn.set_fixed_width(100)
        treeview.append_column(treeviewcolumn)

    def on_row_activated(self, treeview, treepath, treeviewcolumn):
        '''
        Load club information for selected team.
        '''
        model = treeview.get_model()
        clubid = model[treepath][0]

        data.window.screen.change_visible_screen("clubinformation")
        data.window.screen.active.set_visible_club(clubid)

    def on_league_changed(self, *args):
        '''
        Update data list when league selection changes.
        '''
        self.populate_data()

    def populate_leagues(self):
        self.liststoreLeagues.clear()

        for leagueid, league in data.leagues.get_leagues():
            self.liststoreLeagues.append([str(leagueid), league.name])

        self.comboboxLeague.set_active(0)

    def populate_data(self):
        club = data.clubs.get_club_by_id(data.user.team)

        self.liststoreStandings.clear()

        if self.comboboxLeague.get_active_id():
            leagueid = int(self.comboboxLeague.get_active_id())
            league = data.leagues.get_league_by_id(leagueid)

            for standing in league.standings.get_data():
                club = data.clubs.get_club_by_id(standing[0])

                self.liststoreStandings.append([standing[0],
                                                club.name,
                                                standing[1],
                                                standing[2],
                                                standing[3],
                                                standing[4],
                                                standing[5],
                                                standing[6],
                                                standing[7],
                                                standing[8],
                                                club.form.get_form_string_for_length(6)])

    def run(self):
        self.populate_leagues()
        self.show_all()
