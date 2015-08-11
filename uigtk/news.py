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

import constants
import game
import widgets


class News(Gtk.Grid):
    __name__ = "news"

    def __init__(self):
        Gtk.Grid.__init__(self)
        self.set_row_spacing(5)

        self.liststoreNews = Gtk.ListStore(int, str, str, str, int, str, bool, int)

        self.treemodelfilter = self.liststoreNews.filter_new()
        self.treemodelfilter.set_visible_func(self.filter_visible, game.clubs)

        treemodelsort = Gtk.TreeModelSort(self.treemodelfilter)
        treemodelsort.set_sort_column_id(0, Gtk.SortType.DESCENDING)

        grid = Gtk.Grid()
        grid.set_column_spacing(5)
        self.attach(grid, 0, 0, 1, 1)

        self.entrySearch = Gtk.SearchEntry()
        self.entrySearch.set_placeholder_text("Search")
        self.entrySearch.connect("activate", self.search_activated)
        self.entrySearch.connect("icon-press", self.search_cleared)
        self.entrySearch.connect("changed", self.search_changed)
        self.entrySearch.add_accelerator("grab-focus",
                                         game.accelgroup,
                                         102,
                                         Gdk.ModifierType.CONTROL_MASK,
                                         Gtk.AccelFlags.VISIBLE)
        grid.attach(self.entrySearch, 0, 0, 1, 1)

        label = Gtk.Label("_Filter")
        label.set_hexpand(True)
        label.set_alignment(1, 0.5)
        label.set_use_underline(True)
        grid.attach(label, 1, 0, 1, 1)
        self.comboboxFilter = Gtk.ComboBoxText()
        self.comboboxFilter.append("0", "All")

        for categoryid, category in constants.category.items():
            self.comboboxFilter.append(str(categoryid), category)

        self.comboboxFilter.set_active(0)
        self.comboboxFilter.connect("changed", self.filter_changed)
        label.set_mnemonic_widget(self.comboboxFilter)
        grid.attach(self.comboboxFilter, 2, 0, 1, 1)

        paned = Gtk.Paned()
        paned.set_position(150)
        paned.set_orientation(Gtk.Orientation.VERTICAL)
        self.attach(paned, 0, 1, 1, 1)

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_vexpand(True)
        scrolledwindow.set_hexpand(True)
        paned.add1(scrolledwindow)

        self.treeviewNews = Gtk.TreeView()
        self.treeviewNews.set_model(treemodelsort)
        self.treeviewNews.set_activate_on_single_click(True)
        self.treeviewNews.set_enable_search(False)
        self.treeviewNews.set_search_column(-1)
        self.treeviewNews.connect("row-activated", self.item_selected)
        scrolledwindow.add(self.treeviewNews)

        self.treeselection = self.treeviewNews.get_selection()

        treeviewcolumn = widgets.TreeViewColumn(title="Date", column=1)
        self.treeviewNews.append_column(treeviewcolumn)

        treeviewcolumn = Gtk.TreeViewColumn("Title")
        treeviewcolumn.set_expand(True)
        self.treeviewNews.append_column(treeviewcolumn)
        cellrendererTitle = Gtk.CellRendererText()
        treeviewcolumn.pack_start(cellrendererTitle, True)
        treeviewcolumn.add_attribute(cellrendererTitle, "text", 2)
        treeviewcolumn.add_attribute(cellrendererTitle, "weight-set", 6)
        treeviewcolumn.add_attribute(cellrendererTitle, "weight", 7)

        treeviewcolumn = widgets.TreeViewColumn(title="Category", column=5)
        self.treeviewNews.append_column(treeviewcolumn)

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.ALWAYS)
        paned.add2(scrolledwindow)

        self.textviewNews = Gtk.TextView()
        self.textviewNews.set_editable(False)
        self.textviewNews.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        self.textviewNews.set_left_margin(5)
        self.textviewNews.set_right_margin(5)
        self.textviewNews.set_vexpand(True)
        self.textviewNews.set_hexpand(True)
        scrolledwindow.add(self.textviewNews)

    def select_oldest_item(self):
        '''
        Highlight the oldest unread item in the list.
        '''
        items = [item for item in self.liststoreNews]
        items.reverse()

        for item in items:
            if item[6]:
                treemodelsort = self.treeviewNews.get_model()
                path1 = treemodelsort.convert_child_path_to_path(item.path)
                treemodelfilter = treemodelsort.get_model()
                path2 = treemodelfilter.convert_child_path_to_path(path1)
                self.treeselection.select_path(path2)

    def search_changed(self, entry):
        '''
        Refilter when user deletes all characters.
        '''
        if entry.get_text_length() == 0:
            self.treemodelfilter.refilter()

    def search_activated(self, entry):
        '''
        Refilter when user activates Entry.
        '''
        if entry.get_text_length() > 0:
            self.treemodelfilter.refilter()

    def search_cleared(self, entry, position, event):
        '''
        Refilter when user clicks to clear the Entry.
        '''
        if position == Gtk.EntryIconPosition.SECONDARY:
            self.treemodelfilter.refilter()

    def item_selected(self, treeview, treepath, treeviewcolumn):
        model = treeview.get_model()

        newsid = model[treepath][0]
        article = game.news.articles[newsid]

        textbuffer = self.textviewNews.get_buffer()
        textbuffer.set_text(article.message)

        article.unread = False

        # Convert TreeModelSort path to access underlying ListStore model
        child_treepath = model.convert_path_to_child_path(treepath)
        child_model = model.get_model()
        child_model[child_treepath][7] = 400

        if game.news.get_unread_count() == 0:
            widgets.news.hide()

    def filter_changed(self, combobox):
        self.treemodelfilter.refilter()

    def filter_visible(self, model, treeiter, data):
        show = True

        criteria = self.entrySearch.get_text()

        for search in (model[treeiter][2], model[treeiter][3],):
            show = re.findall(criteria, search, re.IGNORECASE)

        if show:
            filterid = int(self.comboboxFilter.get_active_id())

            if filterid != 0:
                show = filterid == model[treeiter][4]

        return show

    def populate_data(self, data):
        self.liststoreNews.clear()

        for newsid, article in data.items():
            category = constants.category[article.category]

            if article.unread:
                weight = 700
            else:
                weight = 400

            self.liststoreNews.append([newsid,
                                       article.date,
                                       article.title,
                                       article.message,
                                       article.category,
                                       category,
                                       article.unread,
                                       weight])

    def run(self):
        self.populate_data(game.news.articles)

        self.show_all()
