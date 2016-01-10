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
        self.injuries.run()
        self.suspensions.run()
        self.show_all()


class Injuries(uigtk.widgets.CommonFrame):
    def __init__(self):
        uigtk.widgets.CommonFrame.__init__(self, title="Injuries")

        overlay = Gtk.Overlay()
        self.grid.attach(overlay, 0, 0, 1, 1)

        self.labelNoInjuries = Gtk.Label("No players are currently injured.")
        overlay.add_overlay(self.labelNoInjuries)

        scrolledwindow = uigtk.widgets.ScrolledWindow()
        scrolledwindow.set_sensitive(False)
        overlay.add(scrolledwindow)

        self.liststore = Gtk.ListStore(int, str, str, str, int)

        treeview = uigtk.widgets.TreeView()
        treeview.set_vexpand(True)
        treeview.set_hexpand(True)
        treeview.set_model(self.liststore)
        scrolledwindow.add(treeview)

        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Name", column=1)
        treeviewcolumn.set_expand(True)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Injury", column=2)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Period", column=3)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Fitness", column=4)
        treeview.append_column(treeviewcolumn)

    def run(self):
        self.liststore.clear()

        club = data.clubs.get_club_by_id(data.user.team)

        for playerid in club.squad.get_squad():
            pass


class Suspensions(uigtk.widgets.CommonFrame):
    def __init__(self):
        uigtk.widgets.CommonFrame.__init__(self, title="Suspensions")

        overlay = Gtk.Overlay()
        self.grid.attach(overlay, 0, 0, 1, 1)

        self.labelNoSuspensions = Gtk.Label("No players are currently suspended.")
        overlay.add_overlay(self.labelNoSuspensions)

        scrolledwindow = uigtk.widgets.ScrolledWindow()
        scrolledwindow.set_sensitive(False)
        overlay.add(scrolledwindow)

        self.liststore = Gtk.ListStore(int, str, str, str)

        treeview = uigtk.widgets.TreeView()
        treeview.set_vexpand(True)
        treeview.set_hexpand(True)
        treeview.set_model(self.liststore)
        scrolledwindow.add(treeview)

        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Name", column=1)
        treeviewcolumn.set_expand(True)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Suspension", column=2)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Period", column=3)
        treeview.append_column(treeviewcolumn)

    def run(self):
        self.liststore.clear()
