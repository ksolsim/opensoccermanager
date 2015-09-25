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
import player
import user
import widgets


class InjSus(Gtk.Grid):
    __name__ = "injsus"

    def __init__(self):
        Gtk.Grid.__init__(self)
        self.set_column_spacing(5)
        self.set_column_homogeneous(True)

        # Injuries
        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        self.attach(grid, 0, 0, 1, 1)

        label = widgets.AlignedLabel("<b>Injuries</b>")
        label.set_use_markup(True)
        grid.attach(label, 0, 0, 1, 1)

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_vexpand(True)
        scrolledwindow.set_hexpand(True)
        grid.attach(scrolledwindow, 0, 1, 1, 1)

        overlay = Gtk.Overlay()
        self.labelNoInjuries = Gtk.Label("No players are currently injured.")
        overlay.add_overlay(self.labelNoInjuries)
        scrolledwindow.add(overlay)

        self.liststoreInjuries = Gtk.ListStore(str, int, str, str)
        treemodelsort = Gtk.TreeModelSort(self.liststoreInjuries)
        treemodelsort.set_sort_column_id(0, Gtk.SortType.ASCENDING)

        self.treeviewInjuries = Gtk.TreeView()
        self.treeviewInjuries.set_model(treemodelsort)
        self.treeviewInjuries.set_sensitive(False)
        self.treeviewInjuries.set_enable_search(False)
        self.treeviewInjuries.set_search_column(-1)
        treeselection = self.treeviewInjuries.get_selection()
        treeselection.set_mode(Gtk.SelectionMode.NONE)
        overlay.add(self.treeviewInjuries)

        treeviewcolumn = widgets.TreeViewColumn(title="Name", column=0)
        self.treeviewInjuries.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Fitness", column=1)
        self.treeviewInjuries.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Injury", column=2)
        self.treeviewInjuries.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Duration", column=3)
        self.treeviewInjuries.append_column(treeviewcolumn)

        gridButton = Gtk.Grid()
        grid.set_column_spacing(5)
        grid.attach(gridButton, 0, 2, 1, 1)

        label = Gtk.Label("Display")
        gridButton.attach(label, 0, 0, 1, 1)
        self.radiobuttonTeamInjured = Gtk.RadioButton()
        self.radiobuttonTeamInjured.display = 0
        self.radiobuttonTeamInjured.connect("toggled", self.injured_player_display)
        gridButton.attach(self.radiobuttonTeamInjured, 1, 0, 1, 1)
        radiobuttonAll = Gtk.RadioButton("Show All Players")
        radiobuttonAll.join_group(self.radiobuttonTeamInjured)
        radiobuttonAll.display = 1
        radiobuttonAll.connect("toggled", self.injured_player_display)
        gridButton.attach(radiobuttonAll, 2, 0, 1, 1)

        # Suspensions
        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        self.attach(grid, 1, 0, 1, 1)

        label = widgets.AlignedLabel("<b>Suspensions</b>")
        label.set_use_markup(True)
        grid.attach(label, 0, 0, 1, 1)

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_vexpand(True)
        scrolledwindow.set_hexpand(True)
        grid.attach(scrolledwindow, 0, 1, 1, 1)

        overlay = Gtk.Overlay()
        self.labelNoSuspensions = Gtk.Label("No players are currently suspended.")
        overlay.add_overlay(self.labelNoSuspensions)
        scrolledwindow.add(overlay)

        self.liststoreSuspensions = Gtk.ListStore(str, str, str)
        treemodelsort = Gtk.TreeModelSort(self.liststoreSuspensions)
        treemodelsort.set_sort_column_id(0, Gtk.SortType.ASCENDING)

        self.treeviewSuspensions = Gtk.TreeView()
        self.treeviewSuspensions.set_model(treemodelsort)
        self.treeviewSuspensions.set_sensitive(False)
        self.treeviewSuspensions.set_enable_search(False)
        self.treeviewSuspensions.set_search_column(-1)
        treeselection = self.treeviewSuspensions.get_selection()
        treeselection.set_mode(Gtk.SelectionMode.NONE)
        overlay.add(self.treeviewSuspensions)

        treeviewcolumn = widgets.TreeViewColumn(title="Name", column=0)
        self.treeviewSuspensions.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Suspension", column=1)
        self.treeviewSuspensions.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Duration", column=2)
        self.treeviewSuspensions.append_column(treeviewcolumn)

        gridButton = Gtk.Grid()
        grid.set_column_spacing(5)
        grid.attach(gridButton, 0, 2, 1, 1)

        label = Gtk.Label("Display")
        gridButton.attach(label, 0, 0, 1, 1)
        self.radiobuttonTeamSuspended = Gtk.RadioButton()
        self.radiobuttonTeamSuspended.display = 0
        self.radiobuttonTeamSuspended.connect("toggled", self.suspended_player_display)
        gridButton.attach(self.radiobuttonTeamSuspended, 1, 0, 1, 1)
        radiobuttonAll = Gtk.RadioButton("Show All Players")
        radiobuttonAll.join_group(self.radiobuttonTeamSuspended)
        radiobuttonAll.display = 1
        radiobuttonAll.connect("toggled", self.suspended_player_display)
        gridButton.attach(radiobuttonAll, 2, 0, 1, 1)

    def injured_player_display(self, radiobutton):
        self.liststoreInjuries.clear()

        if radiobutton.get_active():
            if radiobutton.display == 0:
                self.populate_team_injured_data()
            else:
                self.populate_all_injured_data()

        state = len(self.liststoreInjuries) > 0
        self.treeviewInjuries.set_sensitive(state)
        self.labelNoInjuries.set_visible(not state)

    def suspended_player_display(self, radiobutton):
        self.liststoreSuspensions.clear()

        if radiobutton.get_active():
            if radiobutton.display == 0:
                self.populate_team_suspended_data()
            else:
                self.populate_all_suspended_data()

        state = len(self.liststoreSuspensions) > 0
        self.treeviewSuspensions.set_sensitive(state)
        self.labelNoSuspensions.set_visible(not state)

    def populate_team_injured_data(self):
        self.liststoreInjuries.clear()

        club = user.get_user_club()

        for playerid in club.squad:
            playerObject = player.get_player(playerid)

            if playerObject.injury_type != 0:
                name = playerObject.get_name(mode=1)
                fitness = playerObject.fitness
                injury_name = injury.injuryitem.injuries[playerObject.injury_type][0]
                injury_period = playerObject.get_injury()

                self.liststoreInjuries.append([name,
                                               fitness,
                                               injury_name,
                                               injury_period])

        state = len(self.liststoreInjuries) > 0
        self.treeviewInjuries.set_sensitive(state)
        self.labelNoInjuries.set_visible(not state)

    def populate_all_injured_data(self):
        self.liststoreInjuries.clear()

        for player in game.players.values():
            if player.injury_type != 0:
                name = player.get_name(mode=1)
                fitness = player.fitness
                injury_name = injury.injuryitem.injuries[player.injury_type][0]
                injury_period = player.get_injury()

                self.liststoreInjuries.append([name,
                                               fitness,
                                               injury_name,
                                               injury_period])

        state = len(self.liststoreInjuries) > 0
        self.treeviewInjuries.set_sensitive(state)
        self.labelNoInjuries.set_visible(not state)

    def populate_team_suspended_data(self):
        self.liststoreSuspensions.clear()

        club = user.get_user_club()

        for playerid in club.squad:
            playerObject = player.get_player(playerid)

            if playerObject.suspension_type != 0:
                name = playerObject.get_name(mode=1)
                suspension = constants.suspensions[playerObject.suspension_type][0]
                period = playerObject.get_suspension()

                self.liststoreSuspensions.append([name, suspension, period])

        state = len(self.liststoreSuspensions) > 0
        self.treeviewSuspensions.set_sensitive(state)
        self.labelNoSuspensions.set_visible(not state)

    def populate_all_suspended_data(self):
        self.liststoreSuspensions.clear()

        for player in game.players.values():
            if player.suspension_type != 0:
                name = player.get_name(mode=1)
                suspension = constants.suspensions[player.suspension_type][0]
                period = player.get_suspension()

                self.liststoreSuspensions.append([name, suspension, period])

        state = len(self.liststoreSuspensions) > 0
        self.treeviewSuspensions.set_sensitive(state)
        self.labelNoSuspensions.set_visible(not state)

    def run(self):
        club = user.get_user_club()

        self.radiobuttonTeamInjured.set_label("Show Only %s Players" % (club.name))
        self.radiobuttonTeamSuspended.set_label("Show Only %s Players" % (club.name))

        self.show_all()

        if self.radiobuttonTeamInjured.get_active():
            self.populate_team_injured_data()
        else:
            self.populate_all_injured_data()

        if self.radiobuttonTeamSuspended.get_active():
            self.populate_team_suspended_data()
        else:
            self.populate_all_suspended_data()
