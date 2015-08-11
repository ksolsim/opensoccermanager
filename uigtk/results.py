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

import league
import widgets


class Results(Gtk.Grid):
    __name__ = "results"

    def __init__(self):
        self.page = 0

        Gtk.Grid.__init__(self)
        self.set_row_spacing(5)
        self.set_column_spacing(5)

        scrolledwindow = Gtk.ScrolledWindow()
        self.attach(scrolledwindow, 0, 1, 2, 1)

        self.overlay = Gtk.Overlay()
        scrolledwindow.add(self.overlay)
        self.labelNoResults = Gtk.Label("No fixtures have yet been played.")
        self.overlay.add_overlay(self.labelNoResults)

        buttonbox = Gtk.ButtonBox()
        buttonbox.set_spacing(5)
        buttonbox.set_layout(Gtk.ButtonBoxStyle.END)
        self.attach(buttonbox, 0, 0, 1, 1)

        self.buttonPrevious = widgets.Button("_Previous")
        self.buttonPrevious.set_sensitive(False)
        self.buttonPrevious.connect("clicked", self.change_page, 0)
        buttonbox.add(self.buttonPrevious)
        self.buttonNext = widgets.Button("_Next")
        self.buttonNext.set_sensitive(False)
        self.buttonNext.connect("clicked", self.change_page, 1)
        buttonbox.add(self.buttonNext)

        self.comboboxLeagues = Gtk.ComboBoxText()
        self.comboboxLeagues.connect("changed", self.combobox_changed)
        self.attach(self.comboboxLeagues, 1, 0, 1, 1)

        self.liststoreResults = Gtk.ListStore(str, int, int, str)

        self.treeviewResults = Gtk.TreeView()
        self.treeviewResults.set_model(self.liststoreResults)
        self.treeviewResults.set_hexpand(True)
        self.treeviewResults.set_vexpand(True)
        treeselection = self.treeviewResults.get_selection()
        treeselection.set_mode(Gtk.SelectionMode.NONE)
        self.overlay.add(self.treeviewResults)

        treeviewcolumn = widgets.TreeViewColumn(title="Home", column=0)
        treeviewcolumn.set_expand(True)
        self.treeviewResults.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(column=1)
        self.treeviewResults.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(column=2)
        self.treeviewResults.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Away", column=3)
        treeviewcolumn.set_expand(True)
        self.treeviewResults.append_column(treeviewcolumn)

    def combobox_changed(self, combobox):
        if self.comboboxLeagues.get_active_id():
            self.leagueid = int(self.comboboxLeagues.get_active_id())

            self.populate_data()

    def populate_data(self):
        self.liststoreResults.clear()

        self.treeviewResults.set_sensitive(False)

        if len(league.leagueitem.leagues[self.leagueid].results) > 0:
            for result in league.leagueitem.leagues[self.leagueid].results[self.page]:
                team1 = game.clubs[result[0]].name
                team2 = game.clubs[result[3]].name

                self.liststoreResults.append([team1, result[1], result[2], team2])

            self.labelNoResults.hide()
            self.treeviewResults.set_sensitive(True)

        if len(league.leagueitem.leagues[self.leagueid].results) > 1:
            self.buttonNext.set_sensitive(True)
            self.buttonPrevious.set_sensitive(True)

            if self.page == 0:
                self.buttonPrevious.set_sensitive(False)
            elif self.page == len(game.leagues[self.leagueid].results) - 1:
                self.buttonNext.set_sensitive(False)
        else:
            self.buttonNext.set_sensitive(False)
            self.buttonPrevious.set_sensitive(False)

    def populate_leagues(self):
        self.comboboxLeagues.remove_all()

        for leagueid, value in league.leagueitem.leagues.items():
            self.comboboxLeagues.append(str(leagueid), value.name)

        self.comboboxLeagues.set_active(0)

        self.leagueid = 1

    def change_page(self, button, mode):
        if mode == 0:
            if self.page > 0:
                self.page -= 1
        elif mode == 1:
            leagueid = int(self.comboboxLeagues.get_active_id())

            if self.page < len(game.leagues[leagueid].results) - 1:
                self.page += 1

        self.populate_data()

    def run(self):
        self.populate_leagues()

        self.show_all()
