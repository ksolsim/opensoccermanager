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
from gi.repository import Gdk
import re
import unicodedata

import data
import uigtk.widgets


class ClubSearch(uigtk.widgets.Grid):
    __name__ = "clubsearch"

    treeselection = None

    def __init__(self):
        uigtk.widgets.Grid.__init__(self)

        grid = uigtk.widgets.Grid()
        self.attach(grid, 0, 0, 1, 1)

        self.entrySearch = Gtk.SearchEntry()
        self.entrySearch.set_placeholder_text("Search Clubs...")
        key, modifier = Gtk.accelerator_parse("<Control>F")
        self.entrySearch.add_accelerator("grab-focus",
                                         data.window.accelgroup,
                                         key,
                                         modifier,
                                         Gtk.AccelFlags.VISIBLE)
        self.entrySearch.connect("activate", self.on_search_activated)
        self.entrySearch.connect("icon-press", self.on_search_pressed)
        self.entrySearch.connect("changed", self.on_search_changed)
        grid.attach(self.entrySearch, 0, 0, 1, 1)

        label = Gtk.Label()
        label.set_hexpand(True)
        grid.attach(label, 1, 0, 1, 1)

        buttonbox = uigtk.widgets.ButtonBox()
        grid.attach(buttonbox, 2, 0, 1, 1)

        self.buttonReset = uigtk.widgets.Button("_Reset")
        self.buttonReset.connect("clicked", self.on_reset_clicked)
        buttonbox.add(self.buttonReset)

        scrolledwindow = uigtk.widgets.ScrolledWindow()
        self.attach(scrolledwindow, 0, 1, 1, 1)

        self.liststore = Gtk.ListStore(int, str, str, str, str, str, int, str,
                                       str)

        self.treemodelfilter = self.liststore.filter_new()
        self.treemodelfilter.set_visible_func(self.filter_visible, data.clubs)
        treemodelsort = Gtk.TreeModelSort(self.treemodelfilter)
        treemodelsort.set_sort_column_id(1, Gtk.SortType.ASCENDING)

        self.treeview = uigtk.widgets.TreeView()
        self.treeview.set_hexpand(True)
        self.treeview.set_vexpand(True)
        self.treeview.set_headers_clickable(True)
        self.treeview.set_model(treemodelsort)
        self.treeview.connect("row-activated", self.on_row_activated)
        self.treeview.connect("button-release-event", self.on_button_release_event)
        scrolledwindow.add(self.treeview)

        ClubSearch.treeselection = self.treeview.treeselection

        tree_columns = []

        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Name", column=1)
        treeviewcolumn.set_sort_column_id(1)
        tree_columns.append(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Manager", column=2)
        tree_columns.append(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Chairman", column=3)
        tree_columns.append(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Stadium", column=4)
        tree_columns.append(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="League", column=5)
        tree_columns.append(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Players", column=6)
        tree_columns.append(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Value", column=7)
        tree_columns.append(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Wage", column=8)
        tree_columns.append(treeviewcolumn)

        for column in tree_columns:
            column.set_expand(True)
            self.treeview.append_column(column)

        self.contextmenu = ContextMenu()

    def on_button_release_event(self, widget, event):
        if event.button == 3:
            self.on_context_menu_event(event)

    def on_context_menu_event(self, event):
        event.button = 3

        self.contextmenu.show()
        self.contextmenu.popup(None,
                               None,
                               None,
                               None,
                               event.button,
                               event.time)

    def on_reset_clicked(self, button):
        '''
        Clear search entry and reset view.
        '''
        self.entrySearch.set_text("")
        button.set_sensitive(False)

        self.reset_view()

    def on_row_activated(self, treeview, treepath, treeviewcolumn):
        '''
        Launch player information screen for selected player.
        '''
        model = treeview.get_model()
        clubid = model[treepath][0]

        data.window.screen.change_visible_screen("clubinformation")
        data.window.screen.active.set_visible_club(clubid)

    def on_search_activated(self, entry):
        '''
        Filter for entered name in players list.
        '''
        if entry.get_text_length() > 0:
            self.reset_view()

            self.buttonReset.set_sensitive(True)

    def on_search_pressed(self, entry, position, event):
        '''
        Clear search entry when secondary icon is pressed.
        '''
        if position == Gtk.EntryIconPosition.SECONDARY:
            self.entrySearch.set_text("")
            self.reset_view()

            self.buttonReset.set_sensitive(False)

    def on_search_changed(self, entry):
        '''
        Clear filter if text length is zero.
        '''
        if entry.get_text_length() == 0:
            self.reset_view()

    def reset_view(self):
        '''
        Refilter tree view and highlight top row.
        '''
        self.treemodelfilter.refilter()

        self.treeview.scroll_to_cell(0)
        self.treeselection.select_path(0)

    def filter_visible(self, model, treeiter, data):
        visible = True

        criteria = self.entrySearch.get_text()

        for search in (model[treeiter][1],):
            search = "".join((c for c in unicodedata.normalize("NFD", search) if unicodedata.category(c) != "Mn"))

            if not re.findall(criteria, search, re.IGNORECASE):
                visible = False

        return visible

    def populate_data(self):
        self.liststore.clear()

        for clubid, club in data.clubs.get_clubs():
            league = data.leagues.get_league_by_id(club.league)
            stadium = data.stadiums.get_stadium_by_id(club.stadium)

            value = data.currency.get_rounded_amount(club.get_total_value())
            wage = data.currency.get_rounded_amount(club.get_total_wage())

            self.liststore.append([clubid,
                                   club.name,
                                   club.manager,
                                   club.chairman,
                                   stadium.name,
                                   league.name,
                                   club.squad.get_squad_count(),
                                   value,
                                   wage])

    def run(self):
        self.populate_data()
        self.show_all()

        ClubSearch.treeselection.select_path(0)


class Filter(Gtk.Dialog):
    def __init__(self):
        Gtk.Dialog.__init__(self)
        self.set_transient_for(data.window)
        self.set_modal(True)
        self.set_resizable(False)
        self.set_title("Filter Clubs")


class ContextMenu(Gtk.Menu, ClubSearch):
    def __init__(self):
        Gtk.Menu.__init__(self)

        menuitem = uigtk.widgets.MenuItem("_Club Information")
        menuitem.connect("activate", self.on_club_information_clicked)
        self.append(menuitem)

    def on_club_information_clicked(self, *args):
        '''
        Launch player information screen for selected club.
        '''
        data.window.screen.change_visible_screen("clubinformation")
        data.window.screen.active.set_visible_club(self.clubid)

    def show(self):
        model, treeiter = ClubSearch.treeselection.get_selected()
        self.clubid = model[treeiter][0]

        self.show_all()
