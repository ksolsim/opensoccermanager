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


class Unavailable(uigtk.widgets.Grid):
    '''
    Listing of unavailable players in squad.
    '''
    __name__ = "unavailable"

    def __init__(self):
        uigtk.widgets.Grid.__init__(self)
        self.set_column_homogeneous(True)

        self.injuries = Injuries()
        self.attach(self.injuries, 0, 0, 1, 1)

        self.suspensions = Suspensions()
        self.attach(self.suspensions, 1, 0, 1, 1)

    def run(self):
        self.show_all()
        self.injuries.run()
        self.suspensions.run()


class Interface(uigtk.widgets.CommonFrame):
    '''
    Base layout for unavailable players interface.
    '''
    def __init__(self, title):
        uigtk.widgets.CommonFrame.__init__(self, title=title)

        self.overlay = Gtk.Overlay()
        self.grid.attach(self.overlay, 0, 0, 1, 1)

        self.scrolledwindow = uigtk.widgets.ScrolledWindow()
        self.scrolledwindow.set_sensitive(False)
        self.overlay.add(self.scrolledwindow)

        self.treeview = uigtk.widgets.TreeView()
        self.treeview.set_vexpand(True)
        self.treeview.set_hexpand(True)
        self.treeview.connect("row-activated", self.on_row_activated)
        self.scrolledwindow.add(self.treeview)

        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Name", column=1)
        treeviewcolumn.set_expand(True)
        self.treeview.append_column(treeviewcolumn)

    def on_row_activated(self, treeview, treepath, treeviewcolumn):
        '''
        Handle row activation for listed player.
        '''
        playerid = self.liststore[treepath][0]

        player = data.players.get_player_by_id(playerid)

        data.window.screen.change_visible_screen("playerinformation")
        data.window.screen.active.set_visible_player(player)


class Injuries(Interface):
    '''
    Listing of injured players.
    '''
    def __init__(self):
        Interface.__init__(self, title="Injuries")

        self.labelNoInjuries = Gtk.Label("No players are currently injured.")
        self.overlay.add_overlay(self.labelNoInjuries)

        self.liststore = Gtk.ListStore(int, str, str, str, str)
        self.treeview.set_model(self.liststore)

        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Injury", column=2)
        self.treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Period", column=3)
        self.treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Fitness", column=4)
        self.treeview.append_column(treeviewcolumn)

    def populate_data(self):
        self.liststore.clear()

        for player in data.user.club.squad.get_injured_players():
            self.liststore.append([player.playerid,
                                   player.get_name(),
                                   player.injury.get_injury_name(),
                                   player.injury.get_injury_period(),
                                   "%i%%" % (player.injury.fitness)])

    def run(self):
        self.populate_data()

        self.show_all()

        state = len(data.user.club.squad.get_injured_players()) > 0
        self.scrolledwindow.set_sensitive(state)
        self.labelNoInjuries.set_visible(not state)


class Suspensions(Interface):
    '''
    Listing of suspended players.
    '''
    def __init__(self):
        Interface.__init__(self, title="Suspensions")

        self.labelNoSuspensions = Gtk.Label("No players are currently suspended.")
        self.overlay.add_overlay(self.labelNoSuspensions)

        self.liststore = Gtk.ListStore(int, str, str, str)
        self.treeview.set_model(self.liststore)

        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Suspension",
                                                      column=2)
        self.treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Period", column=3)
        self.treeview.append_column(treeviewcolumn)

    def populate_data(self):
        self.liststore.clear()

        for player in data.user.club.squad.get_suspended_players():
            self.liststore.append([player.playerid,
                                   player.get_name(),
                                   player.suspension.get_suspension_name(),
                                   player.suspension.get_suspension_period()])

    def run(self):
        self.populate_data()

        self.show_all()

        state = len(data.user.club.squad.get_suspended_players()) > 0
        self.scrolledwindow.set_sensitive(state)
        self.labelNoSuspensions.set_visible(not state)
