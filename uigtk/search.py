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

from uigtk import filters
from uigtk import playerinfo
import constants
import dialogs
import game
import menu
import scout
import transfer
import user
import widgets


class Search(Gtk.Grid):
    __name__ = "players"

    def __init__(self):
        self.tree_columns = [[], [], []]

        Gtk.Grid.__init__(self)
        self.set_row_spacing(5)

        grid = Gtk.Grid()
        grid.set_column_spacing(5)
        self.attach(grid, 0, 0, 1, 1)

        liststoreSearch = Gtk.ListStore(str)
        entrycompletion = Gtk.EntryCompletion()
        entrycompletion.set_model(liststoreSearch)
        entrycompletion.set_text_column(0)

        self.entrySearch = Gtk.SearchEntry()
        self.entrySearch.set_placeholder_text("Search")
        self.entrySearch.set_completion(entrycompletion)
        self.entrySearch.set_tooltip_text("Enter name of player to search.")
        self.entrySearch.connect("activate", self.search_activated)
        self.entrySearch.connect("icon-press", self.reset_activated)
        self.entrySearch.connect_after("backspace", self.backspace_activated)
        self.entrySearch.add_accelerator("grab-focus",
                                         game.accelgroup,
                                         102,
                                         Gdk.ModifierType.CONTROL_MASK,
                                         Gtk.AccelFlags.VISIBLE)
        grid.attach(self.entrySearch, 0, 0, 1, 1)

        buttonbox = Gtk.ButtonBox()
        buttonbox.set_hexpand(True)
        buttonbox.set_spacing(5)
        buttonbox.set_layout(Gtk.ButtonBoxStyle.END)
        buttonbox.set_orientation(Gtk.Orientation.HORIZONTAL)
        grid.attach(buttonbox, 2, 0, 1, 1)

        label = Gtk.Label("_View")
        label.set_hexpand(True)
        label.set_alignment(1, 0.5)
        label.set_use_underline(True)
        buttonbox.add(label)
        comboboxView = Gtk.ComboBoxText()
        comboboxView.append("0", "Personal")
        comboboxView.append("1", "Skills")
        comboboxView.append("2", "Form")
        comboboxView.set_active(1)
        comboboxView.connect("changed", self.view_changed)
        label.set_mnemonic_widget(comboboxView)
        buttonbox.add(comboboxView)

        buttonFilter = widgets.Button("_Filter")
        buttonFilter.connect("clicked", self.filter_dialog)
        buttonbox.add(buttonFilter)
        self.buttonReset = widgets.Button("_Reset")
        self.buttonReset.set_sensitive(False)
        self.buttonReset.connect("clicked", self.reset_activated)
        buttonbox.add(self.buttonReset)

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_vexpand(True)
        scrolledwindow.set_hexpand(True)
        self.attach(scrolledwindow, 0, 1, 1, 1)

        self.liststorePlayers = Gtk.ListStore(int, str, int, int, str,
                                              str, str, int, int, int,
                                              int, int, int, int, int,
                                              int, int, str, int, str,
                                              int, str, bool, bool, str,
                                              int, int, str, int, str,)

        self.treemodelfilter = self.liststorePlayers.filter_new()
        self.treemodelfilter.set_visible_func(self.filter_visible, game.players)

        self.treemodelsort = Gtk.TreeModelSort(self.treemodelfilter)
        self.treemodelsort.set_default_sort_func(self.default_sort)
        self.treemodelsort.set_sort_column_id(16, Gtk.SortType.DESCENDING)

        self.treeviewPlayers = Gtk.TreeView()
        self.treeviewPlayers.set_model(self.treemodelsort)
        self.treeviewPlayers.set_headers_clickable(True)
        self.treeviewPlayers.set_enable_search(False)
        self.treeviewPlayers.set_search_column(-1)
        self.treeviewPlayers.connect("row-activated", self.row_activated)
        self.treeviewPlayers.connect("button-release-event", self.context_menu)
        self.treeselection = self.treeviewPlayers.get_selection()
        scrolledwindow.add(self.treeviewPlayers)

        treeviewcolumn = widgets.TreeViewColumn(title="Name", column=1)
        treeviewcolumn.set_sort_column_id(1)
        self.treeviewPlayers.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Age", column=2)
        self.treeviewPlayers.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Club", column=4)
        self.treeviewPlayers.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Nationality", column=5)
        self.treeviewPlayers.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Position", column=6)
        self.treeviewPlayers.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Value", column=17)
        treeviewcolumn.set_sort_column_id(16)
        self.tree_columns[0].append(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Wage", column=19)
        treeviewcolumn.set_sort_column_id(18)
        self.tree_columns[0].append(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Contract", column=21)
        self.tree_columns[0].append(treeviewcolumn)

        for column in self.tree_columns[0]:
            column.set_expand(True)
            column.set_visible(False)
            self.treeviewPlayers.append_column(column)

        for count, item in enumerate(constants.short_skill, start=7):
            label = Gtk.Label("%s" % (item))
            label.set_tooltip_text(constants.skill[count - 7])
            label.show()
            treeviewcolumn = widgets.TreeViewColumn(column=count)
            treeviewcolumn.set_widget(label)
            treeviewcolumn.set_expand(True)
            self.tree_columns[1].append(treeviewcolumn)
            self.treeviewPlayers.append_column(treeviewcolumn)

        treeviewcolumn = widgets.TreeViewColumn(title="Games", column=24)
        self.tree_columns[2].append(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Goals", column=25)
        self.tree_columns[2].append(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Assists", column=26)
        self.tree_columns[2].append(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Cards", column=27)
        self.tree_columns[2].append(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="MOTM", column=28)
        self.tree_columns[2].append(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Rating", column=29)
        self.tree_columns[2].append(treeviewcolumn)

        for column in self.tree_columns[2]:
            column.set_expand(True)
            column.set_visible(False)
            self.treeviewPlayers.append_column(column)

        self.contextmenu = menu.PlayersContextMenu()
        self.contextmenu.menuitemTransfer.connect("activate", self.make_transfer_offer, 0)
        self.contextmenu.menuitemLoan.connect("activate", self.make_transfer_offer, 1)
        self.contextmenu.menuitemAddShortlist.connect("activate", self.add_to_shortlist)
        self.contextmenu.menuitemRemoveShortlist.connect("activate", self.remove_from_shortlist)
        self.contextmenu.menuitemComparison1.connect("activate", self.add_to_comparison, 0)
        self.contextmenu.menuitemComparison2.connect("activate", self.add_to_comparison, 1)
        self.scout_handler_id = self.contextmenu.menuitemRecommends.connect("activate", self.scout_recommends)

        self.searchfilter = filters.SearchFilter()

    def scout_recommends(self, menuitem):
        '''
        View players determined by scout to be recommended for the club.
        '''
        club = user.get_user_club()

        if club.scouts.get_number_of_scouts() > 0:
            if menuitem.get_active():
                players = scout.recommends()

                self.populate_data(players)
            else:
                self.populate_data(game.players)
        else:
            menuitem.handler_block(self.scout_handler_id)
            menuitem.set_active(False)
            menuitem.handler_unblock(self.scout_handler_id)

            dialogs.error(10)

    def add_to_comparison(self, menuitem, index):
        '''
        Add selected player to comparison dialog.
        '''
        model, treeiter = self.treeselection.get_selected()

        dialogs.comparison.comparison[index] = model[treeiter][0]

    def row_activated(self, treeview, treepath, treeviewcolumn):
        '''
        Display extended player information dialog.
        '''
        model = treeview.get_model()
        playerid = model[treepath][0]

        dialog = playerinfo.PlayerInfo(playerid)
        dialog.run()
        dialog.destroy()

    def search_activated(self, entry):
        '''
        Trigger filter of model based on search criteria.
        '''
        criteria = entry.get_text()

        if criteria is not "":
            self.treemodelfilter.refilter()
            self.buttonReset.set_sensitive(True)

            entrycompletion = entry.get_completion()
            model = entrycompletion.get_model()

            entries = [text[0] for text in model]

            if criteria not in entries:
                model.append([criteria])

    def backspace_activated(self, entry):
        '''
        Refilter search criteria when entry is emptied.
        '''
        if entry.get_text_length() == 0:
            self.populate_data(game.players)
            self.treemodelfilter.refilter()

    def reset_activated(self, widget=None, position=None, event=None):
        '''
        Clear applied settings and reset back to default view.
        '''
        self.contextmenu.menuitemRecommends.set_active(False)
        self.buttonReset.set_sensitive(False)
        self.entrySearch.set_text("")

        self.searchfilter.reset_defaults()

        self.populate_data(game.players)
        self.treemodelfilter.refilter()

    def make_transfer_offer(self, menuitem, transfer_type):
        '''
        Initiate transfer offer for purchase, loan or free transfer.
        '''
        model, treeiter = self.treeselection.get_selected()

        playerid = model[treeiter][0]
        player = game.players[playerid]

        if not player.club:
            transfer_type = 2

        transfer.make_enquiry(playerid, transfer_type)

    def add_to_shortlist(self, menuitem):
        '''
        Add selected player to shortlist.
        '''
        model, treeiter = self.treeselection.get_selected()

        club = user.get_user_club()
        club.shortlist.add_player(model[treeiter][0])

    def remove_from_shortlist(self, menuitem):
        '''
        Remove selected player from shortlist.
        '''
        model, treeiter = self.treeselection.get_selected()

        club = user.get_user_club()
        club.shortlist.remove_player(model[treeiter][0])

    def context_menu(self, treeview, event):
        if event.button == 3:
            model, treeiter = self.treeselection.get_selected()

            if treeiter:
                playerid = model[treeiter][0]
                player = game.players[playerid]
                club = user.get_user_club()

                if playerid not in club.squad:
                    self.contextmenu.display()

                    if club.shortlist.get_player_in_shortlist(playerid):
                        self.contextmenu.menuitemAddShortlist.set_sensitive(False)
                        self.contextmenu.menuitemRemoveShortlist.set_sensitive(True)
                    else:
                        self.contextmenu.menuitemAddShortlist.set_sensitive(True)
                        self.contextmenu.menuitemRemoveShortlist.set_sensitive(False)

                    if player.club:
                        self.contextmenu.menuitemLoan.set_sensitive(True)
                    else:
                        self.contextmenu.menuitemLoan.set_sensitive(False)
                else:
                    self.contextmenu.display(mode=1)

                self.contextmenu.popup(None, None, None, None, event.button, event.time)

    def filter_dialog(self, button):
        '''
        Show filter dialog and refilter treeview with specified options.
        '''
        self.searchfilter.display()

        sensitive = self.searchfilter.options != self.searchfilter.defaults
        self.buttonReset.set_sensitive(sensitive)

        self.treemodelfilter.refilter()

    def filter_visible(self, model, treeiter, data):
        show = True

        # Filter by player name
        criteria = self.entrySearch.get_text()

        for search in (model[treeiter][1],):
            search = "".join((c for c in unicodedata.normalize("NFD", search) if unicodedata.category(c) != "Mn"))

            if not re.findall(criteria, search, re.IGNORECASE):
                show = False

        criteria = self.searchfilter.options

        # Filter own players
        if not criteria["own_players"]:
            if model[treeiter][3] == game.teamid:
                show = False

        # Filter position
        if criteria["position"] == 1:
            if model[treeiter][6] != "GK":
                show = False
        elif criteria["position"] == 2:
            if model[treeiter][6] not in ("DL", "DR", "DC", "D"):
                show = False
        elif criteria["position"] == 3:
            if model[treeiter][6] not in ("ML", "MR", "MC", "M"):
                show = False
        elif criteria["position"] == 4:
            if model[treeiter][6] not in ("AS", "AF"):
                show = False

        # Filter player values
        if show:
            show = criteria["value"][0] <= model[treeiter][16] <= criteria["value"][1]

        # Filter player ages
        if show:
            show = criteria["age"][0] <= model[treeiter][2] <= criteria["age"][1]

        # Filter transfer list, loan list and contract statuses
        if criteria["status"] == 1:
            if not model[treeiter][22]:
                show = False
        elif criteria["status"] == 2:
            if not model[treeiter][23]:
                show = False
        elif criteria["status"] == 3:
            if model[treeiter][20] != 0:
                show = False
        elif criteria["status"] == 4:
            if model[treeiter][20] > 52:
                show = False

        # Filter skills
        if show:
            show = criteria["keeping"][0] <= model[treeiter][7] <= criteria["keeping"][1]

        if show:
            show = criteria["tackling"][0] <= model[treeiter][8] <= criteria["tackling"][1]

        if show:
            show = criteria["passing"][0] <= model[treeiter][9] <= criteria["passing"][1]

        if show:
            show = criteria["shooting"][0] <= model[treeiter][10] <= criteria["shooting"][1]

        if show:
            show = criteria["heading"][0] <= model[treeiter][11] <= criteria["heading"][1]

        if show:
            show = criteria["pace"][0] <= model[treeiter][12] <= criteria["pace"][1]

        if show:
            show = criteria["stamina"][0] <= model[treeiter][13] <= criteria["stamina"][1]

        if show:
            show = criteria["ball_control"][0] <= model[treeiter][14] <= criteria["ball_control"][1]

        if show:
            show = criteria["set_pieces"][0] <= model[treeiter][15] <= criteria["set_pieces"][1]

        return show

    def default_sort(self, treesortable, treeiter1, treeiter2, destroy):
        state = treesortable[treeiter1][16] < treesortable[treeiter2][16]

        return state

    def view_changed(self, combobox):
        index = int(combobox.get_active_id())

        for count, column_list in enumerate(self.tree_columns):
            for column in column_list:
                column.set_visible(count == index)

    def populate_data(self, data):
        self.liststorePlayers.clear()

        for playerid, player in data.items():
            name = player.get_name()
            age = player.get_age()
            clubid = player.club
            club = player.get_club()
            nation = player.get_nationality()
            display_value = player.get_value()
            display_wage = player.get_wage()
            display_contract = player.get_contract()
            transfer_list = player.transfer[0]
            loan_list = player.transfer[1]
            appearances = player.get_appearances()
            cards = player.get_cards()
            rating = player.get_rating()

            self.liststorePlayers.append([playerid,
                                          name,
                                          age,
                                          clubid,
                                          club,
                                          nation,
                                          player.position,
                                          player.keeping,
                                          player.tackling,
                                          player.passing,
                                          player.shooting,
                                          player.heading,
                                          player.pace,
                                          player.stamina,
                                          player.ball_control,
                                          player.set_pieces,
                                          player.value,
                                          display_value,
                                          player.wage,
                                          display_wage,
                                          player.contract,
                                          display_contract,
                                          transfer_list,
                                          loan_list,
                                          appearances,
                                          player.goals,
                                          player.assists,
                                          cards,
                                          player.man_of_the_match,
                                          rating])

    def run(self):
        self.populate_data(game.players)

        self.show_all()
