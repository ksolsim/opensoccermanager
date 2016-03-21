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

import data
import structures.news
import uigtk.widgets


class News(uigtk.widgets.Grid):
    __name__ = "news"

    def __init__(self):
        uigtk.widgets.Grid.__init__(self)

        grid = uigtk.widgets.Grid()
        self.attach(grid, 0, 0, 1, 1)

        self.entrySearch = Gtk.SearchEntry()
        self.entrySearch.set_placeholder_text("Search News...")
        self.entrySearch.add_accelerator("grab-focus",
                                         data.window.accelgroup,
                                         Gtk.accelerator_parse("F")[0],
                                         Gdk.ModifierType.CONTROL_MASK,
                                         Gtk.AccelFlags.VISIBLE)
        self.entrySearch.connect("activate", self.on_search_activated)
        self.entrySearch.connect("icon-press", self.on_search_pressed)
        self.entrySearch.connect("changed", self.on_search_changed)
        grid.attach(self.entrySearch, 0, 0, 1, 1)

        label = uigtk.widgets.Label("_Filter", rightalign=True)
        label.set_hexpand(True)
        grid.attach(label, 1, 0, 1, 1)
        self.comboboxFilter = Gtk.ComboBoxText()
        self.comboboxFilter.append("0", "All")

        self.categories = structures.news.Categories()

        categories = sorted(self.categories.categories, key=self.categories.categories.get)

        for categoryid in categories:
            category = self.categories.get_category_by_id(categoryid)
            self.comboboxFilter.append(str(categoryid), category)

        self.comboboxFilter.set_active(0)
        self.comboboxFilter.set_tooltip_text("Filter visible news items by category.")
        self.comboboxFilter.connect("changed", self.on_filter_changed)
        label.set_mnemonic_widget(self.comboboxFilter)
        grid.attach(self.comboboxFilter, 2, 0, 1, 1)

        paned = Gtk.Paned()
        paned.set_orientation(Gtk.Orientation.VERTICAL)
        paned.set_hexpand(True)
        paned.set_vexpand(True)
        paned.set_position(150)
        self.attach(paned, 0, 1, 1, 1)

        scrolledwindow = uigtk.widgets.ScrolledWindow()
        paned.add1(scrolledwindow)

        self.liststoreNews = Gtk.ListStore(int, str, str, str, int, str, bool, int)
        self.treemodelfilter = self.liststoreNews.filter_new()
        self.treemodelfilter.set_visible_func(self.filter_visible, data.user.club.news)
        treemodelsort = Gtk.TreeModelSort(self.treemodelfilter)
        treemodelsort.set_sort_column_id(0, Gtk.SortType.DESCENDING)

        self.treeview = uigtk.widgets.TreeView()
        self.treeview.set_model(treemodelsort)
        self.treeview.treeselection.connect("changed", self.on_article_selected)
        scrolledwindow.add(self.treeview)

        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Date", column=1)
        self.treeview.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Title")
        treeviewcolumn.set_expand(True)
        self.treeview.append_column(treeviewcolumn)
        cellrendererTitle = Gtk.CellRendererText()
        treeviewcolumn.pack_start(cellrendererTitle, True)
        treeviewcolumn.add_attribute(cellrendererTitle, "text", 2)
        treeviewcolumn.add_attribute(cellrendererTitle, "weight-set", 6)
        treeviewcolumn.add_attribute(cellrendererTitle, "weight", 7)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Category", column=5)
        self.treeview.append_column(treeviewcolumn)

        scrolledwindow = Gtk.ScrolledWindow()
        paned.add2(scrolledwindow)

        self.textview = uigtk.widgets.TextView()
        self.textview.set_sensitive(False)
        self.textview.set_editable(False)
        self.textview.set_cursor_visible(False)
        self.textview.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        self.textview.set_left_margin(5)
        self.textview.set_right_margin(5)
        scrolledwindow.add(self.textview)

    def on_search_activated(self, entry):
        '''
        Handle entered search query.
        '''
        self.treemodelfilter.refilter()

    def on_search_pressed(self, entry, position, event):
        '''
        Clear search entry when secondary icon is pressed.
        '''
        if position == Gtk.EntryIconPosition.SECONDARY:
            self.entrySearch.set_text("")
            self.treemodelfilter.refilter()

    def on_search_changed(self, entry):
        '''
        Clear filter if text length is zero.
        '''
        if entry.get_text_length() == 0:
            self.treemodelfilter.refilter()

    def on_article_selected(self, treeselection):
        '''
        Get selected message content and display in text view.
        '''
        model, treeiter = treeselection.get_selected()

        if treeiter:
            newsid = model[treeiter][0]
            article = data.user.club.news.articles[newsid]
            article.unread = False

            self.textview.textbuffer.set_text(article.message)
            self.textview.set_sensitive(True)

            child_treeiter = model.convert_iter_to_child_iter(treeiter)
            child_model = model.get_model()
            child_model[child_treeiter][7] = 400
        else:
            self.textview.textbuffer.set_text("")
            self.textview.set_sensitive(False)

        data.window.mainscreen.information.update_news_visible()

    def on_filter_changed(self, *args):
        '''
        Update view with messages matching selected filter.
        '''
        self.treemodelfilter.refilter()

    def select_oldest_item(self):
        '''
        Highlight the oldest unread item in the list.
        '''
        news = (item for item in self.liststoreNews)

        for item in news:
            if item[6]:
                treemodelsort = self.treeview.get_model()
                path1 = treemodelsort.convert_child_path_to_path(item.path)
                treemodelfilter = treemodelsort.get_model()
                path2 = treemodelfilter.convert_child_path_to_path(path1)

                self.treeview.treeselection.select_path(path2)

                return

    def filter_visible(self, model, treeiter, data):
        display = True

        criteria = self.entrySearch.get_text()

        for search in (model[treeiter][2], model[treeiter][3],):
            display = re.findall(criteria, search, re.IGNORECASE)

        if display:
            selected = int(self.comboboxFilter.get_active_id())

            if selected != 0:
                if selected != model[treeiter][4]:
                    display = False

        return display

    def populate_news(self):
        self.liststoreNews.clear()

        for articleid, article in data.user.club.news.articles.items():
            if article.unread:
                weight = 700
            else:
                weight = 400

            self.liststoreNews.append([articleid,
                                       article.date,
                                       article.title,
                                       article.message,
                                       article.category,
                                       self.categories.get_category_by_id(article.category),
                                       article.unread,
                                       weight])

    def run(self):
        self.populate_news()
        self.show_all()

        self.select_oldest_item()
