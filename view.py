#!/usr/bin/env python3

from gi.repository import Gtk
from gi.repository import Gdk
import random
import unicodedata
import re
import statistics

import game
import dialogs
import widgets
import constants
import display
import money
import calculator
import transfer
import scout


class Players(Gtk.Grid):
    def __init__(self):
        self.tree_columns = [[], [], []]

        Gtk.Grid.__init__(self)
        self.set_vexpand(True)
        self.set_hexpand(True)
        self.set_border_width(5)
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
        self.entrySearch.add_accelerator("grab_focus",
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

        comboboxView = Gtk.ComboBoxText()
        comboboxView.append("0", "Personal")
        comboboxView.append("1", "Skills")
        comboboxView.append("2", "Form")
        comboboxView.set_active(1)
        comboboxView.connect("changed", self.view_changed)
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

        self.liststorePlayers = Gtk.ListStore(int, str, int, int, str, str, str,
                                              int, int, int, int, int, int, int,
                                              int, int, int, str, int, str, int,
                                              str, bool, bool, str, int, int,
                                              str, int, str,)

        self.treemodelfilter = self.liststorePlayers.filter_new()
        self.treemodelfilter.set_visible_func(self.filter_visible, game.players)

        self.treemodelsort = Gtk.TreeModelSort(self.treemodelfilter)
        self.treemodelsort.set_default_sort_func(lambda *args: -1)
        self.treemodelsort.set_sort_column_id(16, Gtk.SortType.DESCENDING)

        self.treeviewPlayers = Gtk.TreeView()
        self.treeviewPlayers.set_model(self.treemodelsort)
        self.treeviewPlayers.set_headers_clickable(True)
        self.treeviewPlayers.connect("row-activated", self.row_activated)
        self.treeviewPlayers.connect("button-release-event", self.context_menu)
        self.treeselection = self.treeviewPlayers.get_selection()
        scrolledwindow.add(self.treeviewPlayers)

        cellrenderertext = Gtk.CellRendererText()
        treeviewcolumn = Gtk.TreeViewColumn("Name", cellrenderertext, text=1)
        treeviewcolumn.set_sort_column_id(1)
        self.treeviewPlayers.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Age", cellrenderertext, text=2)
        self.treeviewPlayers.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Club", cellrenderertext, text=4)
        self.treeviewPlayers.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Nationality", cellrenderertext, text=5)
        self.treeviewPlayers.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Position", cellrenderertext, text=6)
        self.treeviewPlayers.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Value", cellrenderertext, text=17)
        treeviewcolumn.set_sort_column_id(16)
        self.tree_columns[0].append(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Wages", cellrenderertext, text=19)
        treeviewcolumn.set_sort_column_id(18)
        self.tree_columns[0].append(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Contract", cellrenderertext, text=21)
        self.tree_columns[0].append(treeviewcolumn)

        [(column.set_expand(True),
          column.set_visible(False),
          self.treeviewPlayers.append_column(column)) for column in self.tree_columns[0]]

        for count, item in enumerate(("KP", "TK", "PS", "SH", "HD", "PC", "ST", "BC", "SP"), start=7):
            label = Gtk.Label("%s" % (item))
            label.set_tooltip_text(constants.skill[count - 7])
            label.show()
            treeviewcolumn = Gtk.TreeViewColumn(None, cellrenderertext, text=count)
            treeviewcolumn.set_widget(label)
            self.tree_columns[1].append(treeviewcolumn)

        [(column.set_expand(True),
          self.treeviewPlayers.append_column(column)) for column in self.tree_columns[1]]

        treeviewcolumn = Gtk.TreeViewColumn("Games", cellrenderertext, text=24)
        self.tree_columns[2].append(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Goals", cellrenderertext, text=25)
        self.tree_columns[2].append(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Assists", cellrenderertext, text=26)
        self.tree_columns[2].append(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Cards", cellrenderertext, text=27)
        self.tree_columns[2].append(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("MOTM", cellrenderertext, text=28)
        self.tree_columns[2].append(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Rating", cellrenderertext, text=29)
        self.tree_columns[2].append(treeviewcolumn)

        [(column.set_expand(True),
          column.set_visible(False),
          self.treeviewPlayers.append_column(column)) for column in self.tree_columns[2]]

        self.contextmenu1 = Gtk.Menu()
        self.menuitemTransfer = widgets.MenuItem("Make _Transfer Offer")
        self.menuitemTransfer.connect("activate", self.make_transfer_offer, 0)
        self.contextmenu1.append(self.menuitemTransfer)
        self.menuitemLoan = widgets.MenuItem("Make _Loan Offer")
        self.menuitemLoan.connect("activate", self.make_transfer_offer, 1)
        self.contextmenu1.append(self.menuitemLoan)
        separator = Gtk.SeparatorMenuItem()
        self.contextmenu1.append(separator)
        self.menuitemAddShortlist = widgets.MenuItem("_Add To Shortlist")
        self.menuitemAddShortlist.connect("activate", self.add_to_shortlist)
        self.contextmenu1.append(self.menuitemAddShortlist)
        self.menuitemRemoveShortlist = widgets.MenuItem("_Remove From Shortlist")
        self.menuitemRemoveShortlist.connect("activate", self.remove_from_shortlist)
        self.contextmenu1.append(self.menuitemRemoveShortlist)
        separator = Gtk.SeparatorMenuItem()
        self.contextmenu1.append(separator)
        self.menuitemComparison1 = widgets.MenuItem("Add to Comparison _1")
        self.menuitemComparison1.connect("activate", self.add_to_comparison, 0)
        self.contextmenu1.append(self.menuitemComparison1)
        self.menuitemComparison2 = widgets.MenuItem("Add to Comparison _2")
        self.menuitemComparison2.connect("activate", self.add_to_comparison, 1)
        self.contextmenu1.append(self.menuitemComparison2)
        separator = Gtk.SeparatorMenuItem()
        self.contextmenu1.append(separator)
        self.menuitemRecommends = Gtk.CheckMenuItem("_Scout Recommends")
        self.menuitemRecommends.set_use_underline(True)
        self.menuitemRecommends.connect("activate", self.scout_recommends)
        self.contextmenu1.append(self.menuitemRecommends)

        self.contextmenu2 = Gtk.Menu()
        self.menuitemComparison1 = widgets.MenuItem("Add to Comparison _1")
        self.menuitemComparison1.connect("activate", self.add_to_comparison, 0)
        self.contextmenu2.append(self.menuitemComparison1)
        self.menuitemComparison2 = widgets.MenuItem("Add to Comparison _2")
        self.menuitemComparison2.connect("activate", self.add_to_comparison, 1)
        self.contextmenu2.append(self.menuitemComparison2)
        separator = Gtk.SeparatorMenuItem()
        self.contextmenu2.append(separator)
        self.menuitemRecommends = Gtk.CheckMenuItem("_Scout Recommends")
        self.menuitemRecommends.set_use_underline(True)
        self.menuitemRecommends.connect("activate", self.scout_recommends)
        self.contextmenu2.append(self.menuitemRecommends)

    def run(self):
        self.populate_data(game.players)

        self.show_all()

    def scout_recommends(self, menuitem):
        if len(game.clubs[game.teamid].scouts_hired) > 0:
            if menuitem.get_active():
                players = scout.recommends()

                self.populate_data(players)
            else:
                self.populate_data(game.players)
        else:
            dialogs.error(10)

    def add_to_comparison(self, menuitem, index):
        model, treeiter = self.treeselection.get_selected()
        playerid = model[treeiter][0]

        game.comparison[index] = playerid

    def row_activated(self, treeview, path, treeviewcolumn):
        model = treeview.get_model()
        playerid = model[path][0]

        dialogs.player_info(playerid)

    def search_activated(self, entry):
        criteria = entry.get_text()

        if criteria is not "":
            data = {}

            for playerid, player in game.players.items():
                both = "%s %s" % (player.first_name, player.second_name)

                for search in (player.second_name, player.common_name, player.first_name, both):
                    search = ''.join((c for c in unicodedata.normalize('NFD', search) if unicodedata.category(c) != 'Mn'))

                    if re.findall(criteria, search, re.IGNORECASE):
                        data[playerid] = player

                        break

            self.populate_data(data)
            self.buttonReset.set_sensitive(True)

            entrycompletion = entry.get_completion()
            model = entrycompletion.get_model()

            entries = [text[0] for text in model]

            if criteria not in entries:
                model.append([criteria])

    def backspace_activated(self, entry):
        if entry.get_text_length() == 0:
            self.reset_activated()

    def reset_activated(self, widget=None, position=None, event=None):
        self.menuitemRecommends.set_active(False)
        self.buttonReset.set_sensitive(False)
        self.entrySearch.set_text("")

        self.populate_data(game.players)
        game.player_filter = constants.player_filter
        self.treemodelfilter.refilter()

    def make_transfer_offer(self, menuitem, transfer_type):
        model, treeiter = self.treeselection.get_selected()

        playerid = model[treeiter][0]
        player = game.players[playerid]

        if player.club == 0:
            transfer_type = 2

        transfer.make_enquiry(playerid, transfer_type)

    def add_to_shortlist(self, menuitem):
        model, treeiter = self.treeselection.get_selected()

        game.clubs[game.teamid].shortlist.add(model[treeiter][0])

    def remove_from_shortlist(self, menuitem):
        model, treeiter = self.treeselection.get_selected()

        game.clubs[game.teamid].shortlist.remove(model[treeiter][0])

    def context_menu(self, treeview, event):
        if event.button == 3:
            model, treeiter = self.treeselection.get_selected()

            if treeiter:
                playerid = model[treeiter][0]
                player = game.players[playerid]

                if playerid not in game.clubs[game.teamid].squad:
                    self.contextmenu1.show_all()

                    if playerid in game.clubs[game.teamid].shortlist:
                        self.menuitemAddShortlist.set_sensitive(False)
                        self.menuitemRemoveShortlist.set_sensitive(True)
                    else:
                        self.menuitemAddShortlist.set_sensitive(True)
                        self.menuitemRemoveShortlist.set_sensitive(False)

                    self.menuitemTransfer.set_visible(True)
                    self.menuitemLoan.set_visible(True)
                    self.menuitemAddShortlist.set_visible(True)
                    self.menuitemRemoveShortlist.set_visible(True)

                    if player.club == 0:
                        self.menuitemLoan.set_sensitive(False)
                    else:
                        self.menuitemLoan.set_sensitive(True)

                    self.contextmenu1.popup(None, None, None, None, event.button, event.time)
                else:
                    self.contextmenu2.show_all()

                    self.menuitemTransfer.set_visible(False)
                    self.menuitemLoan.set_visible(False)
                    self.menuitemAddShortlist.set_visible(False)
                    self.menuitemRemoveShortlist.set_visible(False)

                    self.contextmenu2.popup(None, None, None, None, event.button, event.time)

    def filter_dialog(self, button):
        dialogs.player_filter()

        if game.player_filter == constants.player_filter:
            self.buttonReset.set_sensitive(False)
        else:
            self.buttonReset.set_sensitive(True)

        self.treemodelfilter.refilter()

    def filter_visible(self, model, treeiter, data):
        criteria = game.player_filter
        display = True

        # Filter own players
        if criteria[0] is False:
            if model[treeiter][3] == game.teamid:
                display = False

        # Filter position
        if criteria[1] == 1:
            if model[treeiter][6] not in ("GK"):
                display = False
        elif criteria[1] == 2:
            if model[treeiter][6] not in ("DL", "DR", "DC", "D"):
                display = False
        elif criteria[1] == 3:
            if model[treeiter][6] not in ("ML", "MR", "MC", "M"):
                display = False
        elif criteria[1] == 4:
            if model[treeiter][6] not in ("AS", "AF"):
                display = False

        # Filter player values
        if display:
            display = criteria[2][1] >= model[treeiter][16] >= criteria[2][0]

        # Filter player ages
        if display:
            display = criteria[3][1] >= model[treeiter][2] >= criteria[3][0]

        # Filter transfer list, loan list and contract statuses
        if criteria[4] == 1:
            if model[treeiter][22] is False:
                display = False
        elif criteria[4] == 2:
            if model[treeiter][23] is False:
                display = False
        elif criteria[4] == 3:
            if model[treeiter][20] != 0:
                display = False
        elif criteria[4] == 4:
            if model[treeiter][20] > 52:
                display = False

        # Filter skills
        if model[treeiter][7] < criteria[5][0] or model[treeiter][7] > criteria[5][1]:
            display = False
        if model[treeiter][8] < criteria[6][0] or model[treeiter][8] > criteria[6][1]:
            display = False
        if model[treeiter][9] < criteria[7][0] or model[treeiter][9] > criteria[7][1]:
            display = False
        if model[treeiter][10] < criteria[8][0] or model[treeiter][10] > criteria[8][1]:
            display = False
        if model[treeiter][11] < criteria[9][0] or model[treeiter][11] > criteria[9][1]:
            display = False
        if model[treeiter][12] < criteria[10][0] or model[treeiter][12] > criteria[10][1]:
            display = False
        if model[treeiter][13] < criteria[11][0] or model[treeiter][13] > criteria[11][1]:
            display = False
        if model[treeiter][14] < criteria[12][0] or model[treeiter][14] > criteria[12][1]:
            display = False
        if model[treeiter][15] < criteria[13][0] or model[treeiter][15] > criteria[13][1]:
            display = False

        return display

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
            name = display.name(player)
            age = player.age
            clubid = player.club
            club = display.club(clubid)
            nationid = player.nationality
            nation = display.nation(nationid)
            position = player.position
            value = player.value
            display_value = display.value(value)
            wage = player.wage
            display_wage = display.wage(wage)
            contract = player.contract
            display_contract = display.contract(contract)
            transfer_list = player.transfer[0]
            loan_list = player.transfer[1]
            appearances = "%i (%i)" % (player.appearances, player.substitute)
            cards = "%i/%i" % (player.yellow_cards, player.red_cards)
            rating = display.rating(player)

            self.liststorePlayers.append([playerid,
                                          name,
                                          age,
                                          clubid,
                                          club,
                                          nation,
                                          position,
                                          player.keeping,
                                          player.tackling,
                                          player.passing,
                                          player.shooting,
                                          player.heading,
                                          player.pace,
                                          player.stamina,
                                          player.ball_control,
                                          player.set_pieces,
                                          value,
                                          display_value,
                                          wage,
                                          display_wage,
                                          contract,
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


class Negotiations(Gtk.Grid):
    def __init__(self):
        Gtk.Grid.__init__(self)
        self.set_vexpand(True)
        self.set_hexpand(True)
        self.set_border_width(5)
        self.set_row_spacing(5)
        self.set_column_spacing(5)

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
        treeviewInbound.connect("row-activated", self.row_activated)
        treeviewInbound.connect("button-release-event", self.context_menu)
        self.treeselectionInbound = treeviewInbound.get_selection()
        scrolledwindow.add(treeviewInbound)

        cellrenderertext = Gtk.CellRendererText()
        treeviewcolumn = Gtk.TreeViewColumn("Name", cellrenderertext, text=1)
        treeviewInbound.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Offer Date", cellrenderertext, text=2)
        treeviewInbound.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Offer Type", cellrenderertext, text=3)
        treeviewInbound.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Club", cellrenderertext, text=4)
        treeviewInbound.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Status", cellrenderertext, text=5)
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
        treeviewOutbound.connect("row-activated", self.outbound_activated)
        treeviewOutbound.connect("button-release-event", self.context_menu)
        self.treeselectionOutbound = treeviewOutbound.get_selection()
        scrolledwindow.add(treeviewOutbound)

        treeviewcolumn = Gtk.TreeViewColumn("Name", cellrenderertext, text=1)
        treeviewOutbound.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Offer Date", cellrenderertext, text=2)
        treeviewOutbound.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Offer Type", cellrenderertext, text=3)
        treeviewOutbound.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Club", cellrenderertext, text=4)
        treeviewOutbound.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Status", cellrenderertext, text=5)
        treeviewOutbound.append_column(treeviewcolumn)

        self.contextmenu = Gtk.Menu()
        menuitem = widgets.MenuItem("_Cancel Transfer")
        menuitem.connect("activate", self.end_transfer)
        self.contextmenu.append(menuitem)

    def end_transfer(self, menuitem):
        model, treeiter = self.treeselection.get_selected()
        negotiationid = model[treeiter][0]

        state = dialogs.withdraw_transfer(negotiationid)

        if state:
            del game.negotiations[negotiationid]

            self.populate_data()

    def row_activated(self, treeview, path, column):
        model = treeview.get_model()
        negotiationid = model[path][0]

        negotiation = game.negotiations[negotiationid]

        if negotiation.transfer_type == 0:
            if negotiation.status == 1:
                transfer.rejection(negotiationid, transfer=0, index=0)
                del game.negotiations[negotiationid]
            elif negotiation.status == 2:
                transfer.transfer_enquiry_accepted(negotiationid)
            elif negotiation.status == 4:
                transfer.rejection(negotiationid, transfer=0, index=1)
                del game.negotiations[negotiationid]
            elif negotiation.status == 5:
                transfer.transfer_offer_accepted(negotiationid)
            elif negotiation.status == 7:
                transfer.rejection(negotiationid, transfer=0, index=2)
                del game.negotiations[negotiationid]
            elif negotiation.status == 8:
                transfer.transfer_contract_accepted(negotiationid)
        elif negotiation.transfer_type == 1:
            if negotiation.status == 1:
                transfer.rejection(negotiationid, transfer=1, index=0)
                del game.negotiations[negotiationid]
            elif negotiation.status == 2:
                transfer.loan_enquiry_accepted(negotiationid)
            elif negotiation.status == 4:
                transfer.rejection(negotiationid, transfer=1, index=1)
                del game.negotiations[negotiationid]
            elif negotiation.status == 5:
                transfer.loan_offer_accepted(negotiationid)
        elif negotiation.transfer_type == 2:
            if negotiation.status in (4, 7, 9):
                del game.negotiations[negotiationid]
            elif negotiation.status == 10:
                transfer.transfer_offer_accepted(negotiationid)
            elif negotiation.status == 8:
                transfer.transfer_contract_accepted(negotiationid)

        self.populate_data()

    def outbound_activated(self, treeview, path, column):
        model = treeview.get_model()
        negotiationid = model[path][0]
        negotiation = game.negotiations[negotiationid]

        if negotiation.transfer_type == 0:
            if negotiation.status == 0:
                transfer.transfer_enquiry_respond(negotiationid)
            elif negotiation.status == 2:
                transfer.transfer_offer_respond(negotiationid)
            elif negotiation.status == 4:
                transfer.transfer_confirm_respond(negotiationid)

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

            name = display.name(player, mode=1)
            date = negotiation.date
            transfer = ("Purchase", "Loan", "Free Transfer")[negotiation.transfer_type]

            if negotiation.club == game.teamid:
                club = display.club(player.club)
                status = constants.transfer_status[negotiation.status]

                self.liststoreInbound.append([negotiationid, name, date, transfer, club, status])
            elif player.club == game.teamid:
                club = display.club(negotiation.club)
                status = constants.transfer_outbound_status[negotiation.status]

                self.liststoreOutbound.append([negotiationid, name, date, transfer, club, status])

    def run(self):
        self.populate_data()

        self.show_all()


class Shortlist(Gtk.Grid):
    def __init__(self):
        Gtk.Grid.__init__(self)
        self.set_vexpand(True)
        self.set_hexpand(True)
        self.set_border_width(5)
        self.set_row_spacing(5)

        self.liststorePlayers = Gtk.ListStore(int, str, int, str, str, str, str, str)

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_vexpand(True)
        scrolledwindow.set_hexpand(True)
        self.attach(scrolledwindow, 0, 0, 1, 1)

        treeview = Gtk.TreeView()
        treeview.set_model(self.liststorePlayers)
        treeview.set_activate_on_single_click(True)
        self.treeselection = treeview.get_selection()
        self.treeselection.connect("changed", self.selection_changed)
        scrolledwindow.add(treeview)

        cellrenderertext = Gtk.CellRendererText()
        treeviewcolumn = Gtk.TreeViewColumn("Name", cellrenderertext, text=1)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Age", cellrenderertext, text=2)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Club", cellrenderertext, text=3)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Nationality", cellrenderertext, text=4)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Position", cellrenderertext, text=5)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Value", cellrenderertext, text=6)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Wage", cellrenderertext, text=7)
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

                if player.club == 0:
                    self.buttonLoan.set_sensitive(False)

            self.buttonRemove.set_sensitive(True)
        else:
            if len(game.clubs[game.teamid].scouts_hired) == 0:
                self.buttonScout.set_sensitive(False)

            self.buttonBuy.set_sensitive(False)
            self.buttonLoan.set_sensitive(False)
            self.buttonRemove.set_sensitive(False)

    def remove_from_shortlist(self, button):
        model, treeiter = self.treeselection.get_selected()
        playerid = model[treeiter][0]

        state = dialogs.remove_from_shortlist(playerid)

        if state:
            game.clubs[game.teamid].shortlist.remove(playerid)

        self.populate_data()

    def scout_report(self, button):
        model, treeiter = self.treeselection.get_selected()

        playerid = model[treeiter][0]
        player = game.players[playerid]

        status = scout.individual(playerid)
        name = display.name(player, mode=1)

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
            name = display.name(player)
            club = display.club(player.club)
            nation = game.nations[player.nationality].name
            value = display.value(player.value)
            wage = display.wage(player.wage)

            self.liststorePlayers.append([playerid,
                                          name,
                                          player.age,
                                          club,
                                          nation,
                                          player.position,
                                          value,
                                          wage])

    def run(self):
        self.populate_data()

        self.show_all()


class InjSus(Gtk.Grid):
    def __init__(self):
        Gtk.Grid.__init__(self)
        self.set_border_width(5)
        self.set_row_spacing(5)
        self.set_column_spacing(5)
        self.set_vexpand(True)
        self.set_hexpand(True)

        label = widgets.AlignedLabel("<b>Injuries</b>")
        label.set_use_markup(True)
        self.attach(label, 0, 0, 1, 1)

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_vexpand(True)
        scrolledwindow.set_hexpand(True)
        self.attach(scrolledwindow, 0, 1, 1, 1)

        overlay = Gtk.Overlay()
        self.labelNoInjury = Gtk.Label("No players are currently injured.")
        overlay.add_overlay(self.labelNoInjury)
        scrolledwindow.add(overlay)

        self.liststoreInjuries = Gtk.ListStore(str, int, str, str)
        self.treeviewInjuries = Gtk.TreeView()
        treeselection = self.treeviewInjuries.get_selection()
        treeselection.set_mode(Gtk.SelectionMode.NONE)
        self.treeviewInjuries.set_model(self.liststoreInjuries)
        self.treeviewInjuries.set_sensitive(False)
        overlay.add(self.treeviewInjuries)

        cellrenderertext = Gtk.CellRendererText()
        treeviewcolumn = Gtk.TreeViewColumn("Name", cellrenderertext, text=0)
        self.treeviewInjuries.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Fitness", cellrenderertext, text=1)
        self.treeviewInjuries.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Injury", cellrenderertext, text=2)
        self.treeviewInjuries.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Duration", cellrenderertext, text=3)
        self.treeviewInjuries.append_column(treeviewcolumn)

        label = widgets.AlignedLabel("<b>Suspensions</b>")
        label.set_use_markup(True)
        self.attach(label, 1, 0, 1, 1)

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_vexpand(True)
        scrolledwindow.set_hexpand(True)
        self.attach(scrolledwindow, 1, 1, 1, 1)

        overlay = Gtk.Overlay()
        self.labelNoSuspension = Gtk.Label("No players are currently suspended.")
        overlay.add_overlay(self.labelNoSuspension)
        scrolledwindow.add(overlay)

        self.liststoreSuspensions = Gtk.ListStore(str, str, str)
        self.treeviewSuspensions = Gtk.TreeView()
        treeselection = self.treeviewSuspensions.get_selection()
        treeselection.set_mode(Gtk.SelectionMode.NONE)
        self.treeviewSuspensions.set_model(self.liststoreSuspensions)
        self.treeviewSuspensions.set_sensitive(False)
        overlay.add(self.treeviewSuspensions)

        treeviewcolumn = Gtk.TreeViewColumn("Name", cellrenderertext, text=0)
        self.treeviewSuspensions.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Suspension", cellrenderertext, text=1)
        self.treeviewSuspensions.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Duration", cellrenderertext, text=2)
        self.treeviewSuspensions.append_column(treeviewcolumn)

    def run(self):
        self.liststoreInjuries.clear()
        self.liststoreSuspensions.clear()

        for playerid in game.clubs[game.teamid].squad:
            player = game.players[playerid]

            if player.injury_type != 0:
                name = display.name(player, mode=1)
                fitness = player.fitness
                injury = constants.injuries[player.injury_type][0]
                period = display.injury(player.injury_period)

                self.liststoreInjuries.append([name, fitness, injury, period])

            if player.suspension_type != 0:
                name = display.name(player, mode=1)
                suspension = constants.suspensions[player.suspension_type][0]
                period = display.suspension(player.suspension_period)

                self.liststoreSuspensions.append([name, suspension, period])

        self.show_all()

        if len(self.liststoreInjuries) > 0:
            self.treeviewInjuries.set_sensitive(True)
            self.labelNoInjury.hide()
        else:
            self.treeviewInjuries.set_sensitive(False)

        if len(self.liststoreSuspensions) > 0:
            self.treeviewSuspensions.set_sensitive(True)
            self.labelNoSuspension.hide()
        else:
            self.treeviewSuspensions.set_sensitive(False)
