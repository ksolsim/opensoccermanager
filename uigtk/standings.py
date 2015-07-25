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

import game
import league
import widgets


class Standings(Gtk.Grid):
    __name__ = "standings"

    def __init__(self):
        Gtk.Grid.__init__(self)
        self.set_row_spacing(5)

        self.comboboxLeagues = Gtk.ComboBoxText()
        self.comboboxLeagues.connect("changed", self.league_changed)
        self.attach(self.comboboxLeagues, 0, 0, 1, 1)

        scrolledwindow = Gtk.ScrolledWindow()
        self.attach(scrolledwindow, 0, 1, 1, 1)

        self.liststoreStandings = Gtk.ListStore(int, str, int, int, int, int,
                                                int, int, int, int, str)

        treeviewStandings = Gtk.TreeView()
        treeviewStandings.set_model(self.liststoreStandings)
        treeviewStandings.set_enable_search(False)
        treeviewStandings.set_search_column(-1)
        treeviewStandings.set_vexpand(True)
        treeviewStandings.set_hexpand(True)
        treeviewStandings.set_activate_on_single_click(True)
        treeviewStandings.connect("row-activated", self.row_activated)
        treeselection = treeviewStandings.get_selection()
        treeselection.set_mode(Gtk.SelectionMode.NONE)
        scrolledwindow.add(treeviewStandings)

        treeviewcolumn = widgets.TreeViewColumn(title="Team", column=1)
        treeviewcolumn.set_expand(True)
        treeviewStandings.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Played", column=2)
        treeviewcolumn.set_fixed_width(48)
        treeviewStandings.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Won", column=3)
        treeviewcolumn.set_fixed_width(48)
        treeviewStandings.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Drawn", column=4)
        treeviewcolumn.set_fixed_width(48)
        treeviewStandings.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Lost", column=5)
        treeviewcolumn.set_fixed_width(48)
        treeviewStandings.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title=None, column=6)
        label = Gtk.Label("GF")
        label.set_tooltip_text("Goals For")
        label.show()
        treeviewcolumn.set_widget(label)
        treeviewcolumn.set_fixed_width(48)
        treeviewStandings.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title=None, column=7)
        label = Gtk.Label("GA")
        label.set_tooltip_text("Goals Against")
        label.show()
        treeviewcolumn.set_widget(label)
        treeviewcolumn.set_fixed_width(48)
        treeviewStandings.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title=None, column=8)
        label = Gtk.Label("GD")
        label.set_tooltip_text("Goal Difference")
        label.show()
        treeviewcolumn.set_widget(label)
        treeviewcolumn.set_fixed_width(48)
        treeviewStandings.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Points", column=9)
        treeviewcolumn.set_fixed_width(48)
        treeviewStandings.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Form", column=10)
        treeviewcolumn.set_fixed_width(96)
        treeviewStandings.append_column(treeviewcolumn)

    def row_activated(self, treeview, treepath, treeviewcolumn):
        clubid = self.liststoreStandings[treepath][0]

        if clubid != game.teamid:
            clubid = str(clubid)

            dialog = dialogs.Opposition()
            dialog.display(show=clubid)

    def league_changed(self, combobox):
        self.populate_data()

    def populate_data(self):
        self.liststoreStandings.clear()

        if self.comboboxLeagues.get_active_id():
            club = int(self.comboboxLeagues.get_active_id())

            standings = league.leagueitem.leagues[club].standings

            for item in standings.get_data():
                self.liststoreStandings.append(item)

    def populate_leagues(self):
        self.comboboxLeagues.remove_all()

        for leagueid, item in league.leagueitem.leagues.items():
            self.comboboxLeagues.append(str(leagueid), item.name)

        self.comboboxLeagues.set_active(0)

    def run(self):
        self.populate_leagues()

        self.show_all()
