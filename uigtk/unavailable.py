#!/usr/bin/env python3

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
