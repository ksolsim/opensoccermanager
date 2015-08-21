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
import re
import unicodedata

import uigtk.window
import club
import game
import player
import widgets


class PlayerSelect(Gtk.Dialog):
    def __init__(self):
        Gtk.Dialog.__init__(self)
        self.set_transient_for(uigtk.window.window)
        self.set_default_size(-1, 250)
        self.set_title("Player Selection")
        self.add_button("C_lear", Gtk.ResponseType.REJECT)
        self.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("_Select", Gtk.ResponseType.OK)
        self.set_default_response(Gtk.ResponseType.OK)

        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        self.vbox.add(grid)

        scrolledwindow = Gtk.ScrolledWindow()
        grid.attach(scrolledwindow, 0, 0, 1, 1)

        self.liststore = Gtk.ListStore(str, str)

        self.treemodelfilter = self.liststore.filter_new()
        self.treemodelfilter.set_visible_func(self.filter_visible, player.players)

        treemodelsort = Gtk.TreeModelSort(self.treemodelfilter)
        treemodelsort.set_sort_column_id(1, Gtk.SortType.ASCENDING)

        treeview = Gtk.TreeView()
        treeview.set_hexpand(True)
        treeview.set_vexpand(True)
        treeview.set_headers_visible(False)
        treeview.set_model(treemodelsort)
        treeview.set_enable_search(False)
        treeview.set_search_column(-1)
        treeview.connect("row-activated", self.row_activated)
        treeviewcolumn = widgets.TreeViewColumn(column=1)
        treeview.append_column(treeviewcolumn)
        self.treeselection = treeview.get_selection()
        self.treeselection.connect("changed", self.selection_changed)
        scrolledwindow.add(treeview)

        self.searchentry = Gtk.SearchEntry()
        self.searchentry.connect("activate", self.search_activated)
        self.searchentry.connect("changed", self.search_changed)
        self.searchentry.connect("icon-press", self.search_cleared)
        grid.attach(self.searchentry, 0, 1, 1, 1)

    def filter_visible(self, model, treeiter, data):
        display = True

        criteria = self.searchentry.get_text()

        for search in (model[treeiter][1],):
            search = "".join((c for c in unicodedata.normalize("NFD", search) if unicodedata.category(c) != "Mn"))

            if not re.findall(criteria, search, re.IGNORECASE):
                display = False

        return display

    def row_activated(self, treeview, treepath, column):
        self.response(Gtk.ResponseType.OK)

    def search_activated(self, searchentry):
        criteria = searchentry.get_text()

        if len(criteria) > 0:
            self.treemodelfilter.refilter()

    def search_changed(self, searchentry):
        if searchentry.get_text_length() == 0:
            self.treemodelfilter.refilter()

    def search_cleared(self, searchentry, icon, entry):
        if icon == Gtk.EntryIconPosition.SECONDARY:
            self.treemodelfilter.refilter()

    def selection_changed(self, treeselection):
        model, treeiter = treeselection.get_selected()

        if treeiter:
            self.set_response_sensitive(Gtk.ResponseType.OK, True)
        else:
            self.set_response_sensitive(Gtk.ResponseType.OK, False)

    def populate_data(self, data=None):
        self.liststore.clear()

        for playerid in data:
            playerObject = player.players[playerid]
            name = playerObject.get_name()

            self.liststore.append([str(playerid), name])

    def display(self):
        self.populate_data(club.clubs[game.teamid].squad)

        self.show_all()
        response = self.run()

        selected = 0

        if response == Gtk.ResponseType.OK:
            model, treeiter = self.treeselection.get_selected()
            selected = model[treeiter][0]
            selected = int(selected)
        elif response == Gtk.ResponseType.REJECT:
            selected = -1

        self.hide()

        return selected
