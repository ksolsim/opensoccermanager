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

import constants
import dialogs
import display
import filters
import game
import menu
import scout
import transfer
import widgets


class Players(Gtk.Grid):
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
        self.entrySearch.set_tooltip_text("Enter player name to search for")
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
            treeviewcolumn = widgets.TreeViewColumn(title="", column=count)
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
        if len(game.clubs[game.teamid].scouts_hired) > 0:
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

        dialog = dialogs.PlayerInfo(playerid)
        dialog.show_all()
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

        game.clubs[game.teamid].shortlist.add(model[treeiter][0])

    def remove_from_shortlist(self, menuitem):
        '''
        Remove selected player from shortlist.
        '''
        model, treeiter = self.treeselection.get_selected()

        game.clubs[game.teamid].shortlist.remove(model[treeiter][0])

    def context_menu(self, treeview, event):
        if event.button == 3:
            model, treeiter = self.treeselection.get_selected()

            if treeiter:
                playerid = model[treeiter][0]
                player = game.players[playerid]

                if playerid not in game.clubs[game.teamid].squad:
                    self.contextmenu.display()

                    if playerid in game.clubs[game.teamid].shortlist:
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
        self.treeviewPlayers.freeze_child_notify()
        self.treeviewPlayers.set_model(None)

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

        self.treeviewPlayers.set_model(self.treemodelsort)
        self.treeviewPlayers.thaw_child_notify()

    def run(self):
        self.populate_data(game.players)

        self.show_all()


class Negotiations(Gtk.Grid):
    __name__ = "negotiations"

    def __init__(self):
        Gtk.Grid.__init__(self)
        self.set_row_spacing(5)

        self.liststoreInbound = Gtk.ListStore(int, str, str, str, str, str)
        self.liststoreOutbound = Gtk.ListStore(int, str, str, str, str, str)

        # Inbound transfers
        label = widgets.AlignedLabel("<b>Inbound</b>")
        label.set_use_markup(True)
        self.attach(label, 0, 0, 1, 1)

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_vexpand(True)
        scrolledwindow.set_hexpand(True)
        self.attach(scrolledwindow, 0, 1, 1, 1)

        treeviewInbound = Gtk.TreeView()
        treeviewInbound.set_model(self.liststoreInbound)
        treeviewInbound.set_enable_search(False)
        treeviewInbound.set_search_column(-1)
        treeviewInbound.connect("row-activated", self.inbound_activated)
        treeviewInbound.connect("button-release-event", self.context_menu)
        self.treeselectionInbound = treeviewInbound.get_selection()
        scrolledwindow.add(treeviewInbound)

        treeviewcolumn = widgets.TreeViewColumn(title="Name", column=1)
        treeviewInbound.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Offer Date", column=2)
        treeviewInbound.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Offer Type", column=3)
        treeviewInbound.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Club", column=4)
        treeviewInbound.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Status", column=5)
        treeviewInbound.append_column(treeviewcolumn)

        # Outbound transfers
        label = widgets.AlignedLabel("<b>Outbound</b>")
        label.set_use_markup(True)
        self.attach(label, 0, 2, 1, 1)

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_vexpand(True)
        scrolledwindow.set_hexpand(True)
        self.attach(scrolledwindow, 0, 3, 1, 1)

        treeviewOutbound = Gtk.TreeView()
        treeviewOutbound.set_model(self.liststoreOutbound)
        treeviewOutbound.set_enable_search(False)
        treeviewOutbound.set_search_column(-1)
        treeviewOutbound.connect("row-activated", self.outbound_activated)
        treeviewOutbound.connect("button-release-event", self.context_menu)
        self.treeselectionOutbound = treeviewOutbound.get_selection()
        scrolledwindow.add(treeviewOutbound)

        treeviewcolumn = widgets.TreeViewColumn(title="Name", column=1)
        treeviewOutbound.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Offer Date", column=2)
        treeviewOutbound.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Offer Type", column=3)
        treeviewOutbound.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Club", column=4)
        treeviewOutbound.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Status", column=5)
        treeviewOutbound.append_column(treeviewcolumn)

        self.contextmenu = Gtk.Menu()
        menuitem = widgets.MenuItem("_Cancel Transfer")
        menuitem.connect("activate", self.cancel_transfer)
        self.contextmenu.append(menuitem)

    def cancel_transfer(self, menuitem):
        model, treeiter = self.treeselection.get_selected()

        negotiationid = model[treeiter][0]
        negotiation = game.negotiations[negotiationid]

        if negotiation.club == game.teamid:
            if dialogs.withdraw_transfer(negotiationid):
                del game.negotiations[negotiationid]
        else:
            if dialogs.cancel_transfer(negotiationid):
                del game.negotiations[negotiationid]

        self.populate_data()

    def inbound_activated(self, treeview, path, column):
        model = treeview.get_model()

        negotiationid = model[path][0]
        negotiation = game.negotiations[negotiationid]

        negotiation.response()

        self.populate_data()

    def outbound_activated(self, treeview, path, column):
        model = treeview.get_model()

        negotiationid = model[path][0]
        negotiation = game.negotiations[negotiationid]

        negotiation.response()

        self.populate_data()

    def context_menu(self, treeview, event):
        if event.button == 3:
            treeselection = treeview.get_selection()
            model, treeiter = treeselection.get_selected()

            if treeiter:
                self.treeselection = treeselection
                self.contextmenu.show_all()
                self.contextmenu.popup(None, None, None, None, event.button, event.time)

    def populate_data(self):
        self.liststoreInbound.clear()
        self.liststoreOutbound.clear()

        for negotiationid, negotiation in game.negotiations.items():
            playerid = negotiation.playerid
            player = game.players[playerid]

            name = player.get_name(mode=1)
            transfer = ("Purchase", "Loan", "Free Transfer")[negotiation.transfer_type]

            if negotiation.club == game.teamid:
                club = player.get_club()
                status = constants.transfer_inbound_status[negotiation.status]

                self.liststoreInbound.append([negotiationid,
                                              name,
                                              negotiation.date,
                                              transfer,
                                              club,
                                              status])
            elif player.club == game.teamid:
                club = display.club(negotiation.club)
                status = constants.transfer_outbound_status[negotiation.status]

                self.liststoreOutbound.append([negotiationid,
                                               name,
                                               negotiation.date,
                                               transfer,
                                               club,
                                               status])

    def run(self):
        self.populate_data()

        self.show_all()


class Shortlist(Gtk.Grid):
    __name__ = "shortlist"

    def __init__(self):
        Gtk.Grid.__init__(self)
        self.set_row_spacing(5)

        self.liststorePlayers = Gtk.ListStore(int, str, int, str, str, str, str, str)

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_policy(Gtk.PolicyType.NEVER,
                                  Gtk.PolicyType.AUTOMATIC)
        scrolledwindow.set_vexpand(True)
        scrolledwindow.set_hexpand(True)
        self.attach(scrolledwindow, 0, 0, 1, 1)

        treeview = Gtk.TreeView()
        treeview.set_model(self.liststorePlayers)
        treeview.set_activate_on_single_click(True)
        treeview.set_enable_search(False)
        treeview.set_search_column(-1)
        self.treeselection = treeview.get_selection()
        self.treeselection.connect("changed", self.selection_changed)
        scrolledwindow.add(treeview)

        treeviewcolumn = widgets.TreeViewColumn(title="Name", column=1)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Age", column=2)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Club", column=3)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Nationality", column=4)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Position", column=5)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Value", column=6)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Wage", column=7)
        treeview.append_column(treeviewcolumn)

        buttonbox = Gtk.ButtonBox()
        buttonbox.set_layout(Gtk.ButtonBoxStyle.END)
        buttonbox.set_spacing(5)
        self.attach(buttonbox, 0, 1, 1, 1)

        self.buttonScout = widgets.Button("_Scout Report")
        self.buttonScout.set_sensitive(False)
        self.buttonScout.connect("clicked", self.scout_report)
        buttonbox.add(self.buttonScout)
        self.buttonBuy = widgets.Button("_Buy")
        self.buttonBuy.set_sensitive(False)
        self.buttonBuy.connect("clicked", self.make_transfer_offer, 0)
        buttonbox.add(self.buttonBuy)
        self.buttonLoan = widgets.Button("_Loan")
        self.buttonLoan.set_sensitive(False)
        self.buttonLoan.connect("clicked", self.make_transfer_offer, 1)
        buttonbox.add(self.buttonLoan)
        self.buttonRemove = widgets.Button("_Remove")
        self.buttonRemove.set_sensitive(False)
        self.buttonRemove.connect("clicked", self.remove_from_shortlist)
        buttonbox.add(self.buttonRemove)

    def selection_changed(self, treeselection):
        model, treeiter = self.treeselection.get_selected()

        if treeiter:
            playerid = model[treeiter][0]
            player = game.players[playerid]

            if len(game.clubs[game.teamid].scouts_hired) > 0:
                self.buttonScout.set_sensitive(True)

            if playerid in game.loans:
                self.buttonBuy.set_sensitive(False)
                self.buttonLoan.set_sensitive(False)
            else:
                self.buttonBuy.set_sensitive(True)
                self.buttonLoan.set_sensitive(True)

                if not player.club:
                    self.buttonLoan.set_sensitive(False)

            self.buttonRemove.set_sensitive(True)
        else:
            self.buttonScout.set_sensitive(False)
            self.buttonBuy.set_sensitive(False)
            self.buttonLoan.set_sensitive(False)
            self.buttonRemove.set_sensitive(False)

    def remove_from_shortlist(self, button):
        model, treeiter = self.treeselection.get_selected()
        playerid = model[treeiter][0]

        if dialogs.remove_from_shortlist(playerid):
            game.clubs[game.teamid].shortlist.remove(playerid)

            self.populate_data()

    def scout_report(self, button):
        model, treeiter = self.treeselection.get_selected()

        playerid = model[treeiter][0]

        status = scout.individual(playerid)
        name = game.players[playerid].get_name(mode=1)

        dialogs.scout_report(name, status)

    def make_transfer_offer(self, menuitem, transfer_type):
        model, treeiter = self.treeselection.get_selected()

        playerid = model[treeiter][0]

        # Set to free transfer if player has no club
        if game.players[playerid].club == 0:
            transfer_type = 2

        transfer.make_enquiry(playerid, transfer_type)

    def populate_data(self):
        self.liststorePlayers.clear()

        for playerid in game.clubs[game.teamid].shortlist:
            player = game.players[playerid]
            name = player.get_name()
            age = player.get_age()
            club = player.get_club()
            nation = player.get_nationality()
            value = player.get_value()
            wage = player.get_wage()

            self.liststorePlayers.append([playerid,
                                          name,
                                          age,
                                          club,
                                          nation,
                                          player.position,
                                          value,
                                          wage])

    def run(self):
        self.populate_data()

        self.show_all()


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

        for playerid in game.clubs[game.teamid].squad:
            player = game.players[playerid]

            if player.injury_type != 0:
                name = player.get_name(mode=1)
                fitness = player.fitness
                injury = constants.injuries[player.injury_type][0]
                period = player.get_injury()

                self.liststoreInjuries.append([name, fitness, injury, period])

        state = len(self.liststoreInjuries) > 0
        self.treeviewInjuries.set_sensitive(state)
        self.labelNoInjuries.set_visible(not state)

    def populate_all_injured_data(self):
        self.liststoreInjuries.clear()

        for player in game.players.values():
            if player.injury_type != 0:
                name = player.get_name(mode=1)
                fitness = player.fitness
                injury = constants.injuries[player.injury_type][0]
                period = player.get_injury()

                self.liststoreInjuries.append([name, fitness, injury, period])

        state = len(self.liststoreInjuries) > 0
        self.treeviewInjuries.set_sensitive(state)
        self.labelNoInjuries.set_visible(not state)

    def populate_team_suspended_data(self):
        self.liststoreSuspensions.clear()

        for playerid in game.clubs[game.teamid].squad:
            player = game.players[playerid]

            if player.suspension_type != 0:
                name = player.get_name(mode=1)
                suspension = constants.suspensions[player.suspension_type][0]
                period = player.get_suspension()

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
        club = game.clubs[game.teamid].name

        self.radiobuttonTeamInjured.set_label("Show Only %s Players" % (club))
        self.radiobuttonTeamSuspended.set_label("Show Only %s Players" % (club))

        self.show_all()

        if self.radiobuttonTeamInjured.get_active():
            self.populate_team_injured_data()
        else:
            self.populate_all_injured_data()

        if self.radiobuttonTeamSuspended.get_active():
            self.populate_team_suspended_data()
        else:
            self.populate_all_suspended_data()
