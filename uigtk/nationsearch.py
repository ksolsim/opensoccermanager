#!/usr/bin/env python3

from gi.repository import Gtk
import re
import unicodedata

import data
import uigtk.widgets


class NationSearch(uigtk.widgets.Grid):
    __name__ = "nationsearch"

    def __init__(self):
        uigtk.widgets.Grid.__init__(self)

        # Search
        grid = uigtk.widgets.Grid()
        grid.set_vexpand(True)
        self.attach(grid, 0, 0, 1, 2)

        scrolledwindow = uigtk.widgets.ScrolledWindow()
        grid.attach(scrolledwindow, 0, 0, 1, 1)

        self.liststoreNations = Gtk.ListStore(int, str)
        self.treemodelfilter = self.liststoreNations.filter_new()
        self.treemodelfilter.set_visible_func(self.filter_visible, data.nations.get_nations())
        self.treemodelsort = Gtk.TreeModelSort(self.treemodelfilter)
        self.treemodelsort.set_sort_column_id(1, Gtk.SortType.ASCENDING)

        self.treeviewSearch = uigtk.widgets.TreeView()
        self.treeviewSearch.set_vexpand(True)
        self.treeviewSearch.set_headers_visible(False)
        self.treeviewSearch.set_model(self.treemodelsort)
        self.treeviewSearch.treeselection.set_mode(Gtk.SelectionMode.BROWSE)
        self.treeviewSearch.treeselection.connect("changed", self.on_selection_changed)
        scrolledwindow.add(self.treeviewSearch)

        self.treeviewcolumn = uigtk.widgets.TreeViewColumn(column=1)
        self.treeviewSearch.append_column(self.treeviewcolumn)

        self.entrySearch = Gtk.SearchEntry()
        key, modifier = Gtk.accelerator_parse("<Control>F")
        self.entrySearch.add_accelerator("grab-focus",
                                         data.window.accelgroup,
                                         key,
                                         modifier,
                                         Gtk.AccelFlags.VISIBLE)
        self.entrySearch.connect("activate", self.on_search_activated)
        self.entrySearch.connect("icon-press", self.on_search_pressed)
        grid.attach(self.entrySearch, 0, 1, 1, 1)

        # Squad
        grid = uigtk.widgets.Grid()
        grid.set_vexpand(True)
        grid.set_hexpand(True)
        self.attach(grid, 1, 0, 1, 1)

        self.labelName = uigtk.widgets.Label()
        grid.attach(self.labelName, 0, 0, 2, 1)

        position = Position("Goalkeepers")
        grid.attach(position, 0, 1, 1, 1)

        position = Position("Defenders")
        grid.attach(position, 0, 2, 1, 1)

        position = Position("Midfielders")
        grid.attach(position, 1, 1, 1, 1)

        position = Position("Attackers")
        grid.attach(position, 1, 2, 1, 1)

    def set_visible_nation(self, nationid):
        '''
        Select passed nation and highlight row in search.
        '''
        for item in self.liststoreNations:
            if nationid == item[0]:
                treepath = item.path
                break

        treepath = self.treemodelsort.convert_child_path_to_path(treepath)
        treepath = self.treemodelfilter.convert_child_path_to_path(treepath)
        self.treeviewSearch.treeselection.select_path(treepath)
        self.treeviewSearch.scroll_to_cell(treepath, self.treeviewcolumn, True, False, False)

    def on_selection_changed(self, treeselection):
        '''
        Update the display with the visible nation for given id.
        '''
        model, treeiter = treeselection.get_selected()

        if treeiter:
            nationid = model[treeiter][0]
            nation = data.nations.get_nation_by_id(nationid)

            name = nation.name.replace('&', '&amp;')
            self.labelName.set_markup("<span size='24000'><b>%s</b></span>" % (name))

    def on_search_activated(self, entry):
        '''
        Refilter when search entry is activated by return button.
        '''
        if entry.get_text_length() > 0:
            self.treemodelfilter.refilter()

    def on_search_pressed(self, entry, position, event):
        '''
        Clear search entry and refilter results.
        '''
        if position == Gtk.EntryIconPosition.SECONDARY:
            entry.set_text("")
            self.treemodelfilter.refilter()

    def filter_visible(self, model, treeiter, data):
        visible = True

        criteria = self.entrySearch.get_text()

        for search in (model[treeiter][1],):
            search = "".join((c for c in unicodedata.normalize("NFD", search) if unicodedata.category(c) != "Mn"))

            if not re.findall(criteria, search, re.IGNORECASE):
                visible = False

        return visible

    def populate_nations(self):
        self.liststoreNations.clear()

        for nationid, nation in data.nations.get_nations():
            self.liststoreNations.append([nationid, nation.name])

    def run(self):
        self.populate_nations()
        self.show_all()

        self.entrySearch.set_text("")

        self.treemodelfilter.refilter()
        treeiter = self.treemodelsort.get_iter_first()
        self.treeviewSearch.treeselection.select_iter(treeiter)


class Position(uigtk.widgets.CommonFrame):
    def __init__(self, position):
        uigtk.widgets.CommonFrame.__init__(self, title=position)

        scrolledwindow = uigtk.widgets.ScrolledWindow()
        self.grid.attach(scrolledwindow, 0, 0, 1, 1)

        treeview = uigtk.widgets.TreeView()
        treeview.set_vexpand(True)
        treeview.set_hexpand(True)
        scrolledwindow.add(treeview)

        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Name")
        treeviewcolumn.set_expand(True)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Position")
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Club")
        treeview.append_column(treeviewcolumn)
