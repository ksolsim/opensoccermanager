#!/usr/bin/env python3

from gi.repository import Gtk
from gi.repository import Gdk

import constants
import dialogs
import display
import events
import game
import money
import transfer
import widgets


class Squad(Gtk.Grid):
    def __init__(self):
        targets = [('MY_TREE_MODEL_ROW', Gtk.TargetFlags.SAME_APP, 0),
                   ('text/plain', 0, 1),
                   ('TEXT', 0, 2),
                   ('STRING', 0, 3),
                   ]

        self.tree_columns = ([], [], [])

        Gtk.Grid.__init__(self)
        self.set_border_width(5)
        self.set_row_spacing(5)
        self.set_column_spacing(5)

        self.liststoreSquad = Gtk.ListStore(int, str, str, int, int,
                                            int, int, int, int, int,
                                            int, int, int, str, str,
                                            str, str, str, str, int,
                                            int, str, int, str, int,
                                            int,)

        treemodelsort = Gtk.TreeModelSort(self.liststoreSquad)
        treemodelsort.set_sort_column_id(1, Gtk.SortType.ASCENDING)

        self.treemodelfilter = treemodelsort.filter_new()
        self.treemodelfilter.set_visible_func(self.filter_visible, game.clubs)

        grid = Gtk.Grid()
        grid.set_column_spacing(5)
        self.attach(grid, 0, 0, 1, 1)

        label = Gtk.Label("_View")
        label.set_use_underline(True)
        label.set_alignment(1, 0.5)
        grid.attach(label, 0, 0, 1, 1)
        comboboxView = Gtk.ComboBoxText()
        comboboxView.set_hexpand(False)
        comboboxView.append("0", "Personal")
        comboboxView.append("1", "Skills")
        comboboxView.append("2", "Form")
        comboboxView.set_active(1)
        comboboxView.connect("changed", self.view_changed)
        label.set_mnemonic_widget(comboboxView)
        grid.attach(comboboxView, 1, 0, 1, 1)

        label = Gtk.Label()
        label.set_hexpand(True)
        grid.attach(label, 2, 0, 1, 1)

        buttonbox = Gtk.ButtonBox()
        buttonbox.set_spacing(5)
        grid.attach(buttonbox, 3, 0, 1, 1)
        buttonFilter = widgets.Button("F_ilter")
        buttonFilter.connect("clicked", self.filter_squad)
        buttonbox.add(buttonFilter)
        self.buttonReset = widgets.Button("_Reset")
        self.buttonReset.set_sensitive(False)
        self.buttonReset.connect("clicked", self.filter_reset)
        buttonbox.add(self.buttonReset)

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.attach(scrolledwindow, 0, 1, 1, 1)

        treeviewSquad = Gtk.TreeView()
        treeviewSquad.set_model(self.treemodelfilter)
        treeviewSquad.set_vexpand(True)
        treeviewSquad.set_hexpand(True)
        treeviewSquad.set_search_column(1)
        treeviewSquad.enable_model_drag_source(Gdk.ModifierType.BUTTON1_MASK, targets, Gdk.DragAction.COPY)
        treeviewSquad.connect("row-activated", self.row_activated)
        treeviewSquad.connect("button-release-event", self.context_menu)
        treeviewSquad.connect("drag-data-get", self.on_drag_data_get)
        self.treeselection = treeviewSquad.get_selection()
        scrolledwindow.add(treeviewSquad)

        cellrenderertext = Gtk.CellRendererText()
        treeviewcolumn = Gtk.TreeViewColumn("Name", cellrenderertext, text=1)
        treeviewcolumn.set_expand(True)
        treeviewSquad.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Position", cellrenderertext, text=2)
        treeviewcolumn.set_expand(True)
        treeviewSquad.append_column(treeviewcolumn)

        # Personal
        treeviewcolumn = Gtk.TreeViewColumn("Nationality", cellrenderertext, text=13)
        self.tree_columns[0].append(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Value", cellrenderertext, text=14)
        self.tree_columns[0].append(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Wages", cellrenderertext, text=15)
        self.tree_columns[0].append(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Contract", cellrenderertext, text=16)
        self.tree_columns[0].append(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Morale", cellrenderertext, text=17)
        self.tree_columns[0].append(treeviewcolumn)

        [(column.set_expand(True),
          column.set_visible(False),
          treeviewSquad.append_column(column)) for column in self.tree_columns[0]]

        # Skills
        for count, item in enumerate(("KP", "TK", "PS", "SH", "HD", "PC", "ST", "BC", "SP"), start=3):
            label = Gtk.Label("%s" % (item))
            label.set_tooltip_text(constants.skill[count - 3])
            label.show()
            treeviewcolumn = Gtk.TreeViewColumn(None, cellrenderertext, text=count)
            treeviewcolumn.set_widget(label)
            self.tree_columns[1].append(treeviewcolumn)

        treeviewcolumn = Gtk.TreeViewColumn("Fitness", cellrenderertext, text=12)
        self.tree_columns[1].append(treeviewcolumn)

        [(column.set_expand(True),
          treeviewSquad.append_column(column)) for column in self.tree_columns[1]]

        # Form
        treeviewcolumn = Gtk.TreeViewColumn("Games", cellrenderertext, text=18)
        self.tree_columns[2].append(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Goals", cellrenderertext, text=19)
        self.tree_columns[2].append(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Assists", cellrenderertext, text=20)
        self.tree_columns[2].append(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Cards", cellrenderertext, text=21)
        self.tree_columns[2].append(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("MOTM", cellrenderertext, text=22)
        self.tree_columns[2].append(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Rating", cellrenderertext, text=23)
        self.tree_columns[2].append(treeviewcolumn)

        [(column.set_expand(True),
          column.set_visible(False),
          column.set_fixed_width(50),
          treeviewSquad.append_column(column)) for column in self.tree_columns[2]]

        self.notebook = Gtk.Notebook()
        self.notebook.set_hexpand(False)
        self.notebook.set_vexpand(True)
        self.checkbuttonLimit = Gtk.CheckButton("_Limit Listed Players")
        self.checkbuttonLimit.set_use_underline(True)
        self.checkbuttonLimit.set_border_width(1)
        self.checkbuttonLimit.set_tooltip_text("Show only players in each position which are best suited")
        self.checkbuttonLimit.connect("toggled", self.limit_player_list)
        self.checkbuttonLimit.show()
        self.notebook.set_action_widget(self.checkbuttonLimit, Gtk.PackType.END)
        self.attach(self.notebook, 1, 0, 1, 2)

        # Team notebook page
        label = Gtk.Label("_Team")
        label.set_use_underline(True)

        self.gridTeam = Gtk.Grid()
        self.gridTeam.set_border_width(5)
        self.gridTeam.set_row_spacing(5)
        self.gridTeam.set_column_spacing(5)
        self.notebook.append_page(self.gridTeam, label)

        self.comboSquadList = []
        self.comboDCList = [None] * 16

        self.labelTeam = []

        for count in range(0, 11):
            label = widgets.Label()
            self.gridTeam.attach(label, 0, count, 1, 1)
            self.labelTeam.append(label)

        # Subs notebook page
        label = Gtk.Label("_Subs")
        label.set_use_underline(True)

        self.gridSubs = Gtk.Grid()
        self.gridSubs.set_border_width(5)
        self.gridSubs.set_row_spacing(5)
        self.gridSubs.set_column_spacing(5)
        self.notebook.append_page(self.gridSubs, label)

        self.labelSubs = []

        for count in range(0, 5):
            label = widgets.Label()
            self.gridSubs.attach(label, 0, count, 1, 1)
            self.labelSubs.append(label)

        # Context menu
        self.menu = Gtk.Menu()
        self.menuitemAddPos = widgets.MenuItem("_Add To Position")
        self.menu.append(self.menuitemAddPos)
        menuitemRemovePos = widgets.MenuItem("_Remove From Position")
        menuitemRemovePos.connect("activate", self.remove_from_position)
        self.menu.append(menuitemRemovePos)
        separator = Gtk.SeparatorMenuItem()
        self.menu.append(separator)
        self.menuitemAddTransfer = widgets.MenuItem("Add To _Transfer List")
        self.menuitemAddTransfer.connect("activate", self.transfer_status, 0)
        self.menu.append(self.menuitemAddTransfer)
        self.menuitemRemoveTransfer = widgets.MenuItem("_Remove From Transfer List")
        self.menuitemRemoveTransfer.connect("activate", self.transfer_status, 0)
        self.menu.append(self.menuitemRemoveTransfer)
        self.menuitemAddLoan = widgets.MenuItem("Add To _Loan List")
        self.menuitemAddLoan.connect("activate", self.transfer_status, 1)
        self.menu.append(self.menuitemAddLoan)
        self.menuitemRemoveLoan = widgets.MenuItem("_Remove From Loan List")
        self.menuitemRemoveLoan.connect("activate", self.transfer_status, 1)
        self.menu.append(self.menuitemRemoveLoan)
        self.menuitemQuickSell = widgets.MenuItem("_Quick Sell")
        self.menuitemQuickSell.connect("activate", self.quick_sell)
        self.menu.append(self.menuitemQuickSell)
        self.menuitemRenewContract = widgets.MenuItem("Renew _Contract")
        self.menuitemRenewContract.connect("activate", self.renew_contract)
        self.menu.append(self.menuitemRenewContract)
        self.menuitemNotForSale = Gtk.CheckMenuItem("_Not For Sale")
        self.menuitemNotForSale.set_use_underline(True)
        self.menuitemNotForSale.connect("toggled", self.not_for_sale)
        self.menu.append(self.menuitemNotForSale)
        self.menuitemExtendLoan = widgets.MenuItem("_Extend Loan")
        self.menuitemExtendLoan.connect("activate", self.extend_loan)
        self.menu.append(self.menuitemExtendLoan)
        self.menuitemCancelLoan = widgets.MenuItem("_Cancel Loan")
        self.menuitemCancelLoan.connect("activate", self.cancel_loan)
        self.menu.append(self.menuitemCancelLoan)

        cellrenderertext = Gtk.CellRendererText()

        for count in range(0, 16):
            combobox = Gtk.ComboBox()
            combobox.set_hexpand(True)
            combobox.set_id_column(0)
            combobox.pack_start(cellrenderertext, True)
            combobox.add_attribute(cellrenderertext, "text", 1)
            combobox.drag_dest_set(Gtk.DestDefaults.ALL, [], Gdk.DragAction.COPY)
            combobox.drag_dest_add_text_targets()
            combobox.connect("drag-data-received", self.on_drag_data_received)
            connectid = combobox.connect("changed", self.update_squad, count)
            self.comboDCList[count] = connectid
            self.comboSquadList.append(combobox)

            if count < 11:
                self.gridTeam.attach(combobox, 1, count, 1, 1)
            else:
                self.gridSubs.attach(combobox, 1, count - 11, 1, 1)

    def run(self):
        formationid = game.clubs[game.teamid].tactics[0]

        for count in range(0, 16):
            if count < 11:
                position = constants.formations[formationid][1][count]
                self.labelTeam[count].set_label("_%s" % (position))
            else:
                self.labelSubs[count - 11].set_label("Sub _%s" % (count - 10))

            liststore = Gtk.ListStore(str, str)
            liststore.append([str(0), "Not Selected"])
            for playerid in game.clubs[game.teamid].squad:
                player = game.players[playerid]
                name = display.name(player)

                liststore.append([str(playerid), name])

            combobox = self.comboSquadList[count]
            combobox.set_model(liststore)
            combobox.set_id_column(0)
            combobox.disconnect(self.comboDCList[count])

            playerid = game.clubs[game.teamid].team[count]
            combobox.set_active_id(str(playerid))

            connectid = combobox.connect("changed", self.update_squad, count)
            self.comboDCList[count] = connectid

            if count < 11:
                self.labelTeam[count].set_mnemonic_widget(combobox)
            else:
                self.labelSubs[count - 11].set_mnemonic_widget(combobox)

        # Context menu for "Add To Position"
        self.menuPosition = Gtk.Menu()
        self.menuitemAddPos.set_submenu(self.menuPosition)

        for count, item in enumerate(constants.formations[formationid][1]):
            menuitem = Gtk.MenuItem("%s" % (item))
            menuitem.connect_after("button-release-event", self.add_to_position, count)
            self.menuPosition.append(menuitem)

        for item in range(1, 6):
            menuitem = Gtk.MenuItem("Sub %i" % (item))
            menuitem.connect_after("button-release-event", self.add_to_position, item + 10)
            self.menuPosition.append(menuitem)

        # Populate data across squad screen
        self.populate_data()
        self.limit_player_list()

        self.show_all()

    def on_drag_data_get(self, treeview, context, selection, info, time):
        treeselection = treeview.get_selection()
        model, treeiter = treeselection.get_selected()
        data = "%s" % (model[treeiter][0])
        data = bytes(data, "utf-8")
        selection.set(selection.get_target(), 8, data)

    def on_drag_data_received(self, combobox, context, x, y, selection, info, time):
        playerid = selection.get_data().decode("utf-8")

        if not combobox.set_active_id(playerid):
            self.checkbuttonLimit.set_active(False)
            combobox.set_active_id(playerid)

        if context.get_actions() == Gdk.DragAction.COPY:
            context.finish(True, False, time)

        return

    def update_squad(self, combobox, index):
        active = combobox.get_active()
        model = combobox.get_model()
        playerid = model[active][0]

        for key, item in game.clubs[game.teamid].team.items():
            if item != 0 and str(item) == str(playerid):
                game.clubs[game.teamid].team[key] = 0
                self.comboSquadList[key].set_active(0)

        game.clubs[game.teamid].team[index] = int(playerid)

    def limit_player_list(self, checkbutton=None):
        formationid = game.clubs[game.teamid].tactics[0]
        formation = constants.formations[formationid][0]
        formation = formation.split("-")
        formation.insert(0, 1)
        formation = tuple(map(int, formation))

        positions = (("GK"), ("DL", "DR", "DC", "D"), ("ML", "MR", "MC", "M"), ("AS", "AF"))

        tuple_index = 0
        position_count = 0

        for count in range(0, 11):
            combobox = self.comboSquadList[count]
            combobox.disconnect(self.comboDCList[count])

            model = combobox.get_model()
            model.clear()
            model.append([str(0), "Not Selected"])

            for playerid in game.clubs[game.teamid].squad:
                player = game.players[playerid]
                name = display.name(player)

                if self.checkbuttonLimit.get_active():
                    if player.position in positions[tuple_index]:
                        model.append([str(playerid), name])
                else:
                    model.append([str(playerid), name])

            # Set player onto combobox, however if the set is not valid
            # it will be cleared and player will be removed from team
            playerid = game.clubs[game.teamid].team[count]

            if not combobox.set_active_id(str(playerid)):
                combobox.set_active(0)
                game.clubs[game.teamid].team[count] = 0

            self.comboDCList[count] = combobox.connect("changed", self.update_squad, count)

            if position_count == formation[tuple_index] - 1:
                tuple_index += 1
                position_count = 0
            else:
                position_count += 1

    def row_activated(self, treeview, path, treeviewcolumn):
        '''
        Display the extra player information dialog box when double
        clicking a row in the squad.
        '''
        model = treeview.get_model()
        playerid = model[path][0]

        dialogs.player_info(playerid)

    def context_menu(self, widget, event):
        model, treeiter = self.treeselection.get_selected()

        if treeiter and event.button == 3:
            playerid = model[treeiter][0]
            player = game.players[playerid]

            self.menuitemNotForSale.set_active(player.not_for_sale)

            self.menu.show_all()

            if playerid in game.loans:
                self.menuitemAddTransfer.set_visible(False)
                self.menuitemRemoveTransfer.set_visible(False)
                self.menuitemAddLoan.set_visible(False)
                self.menuitemRemoveLoan.set_visible(False)
                self.menuitemQuickSell.set_visible(False)
                self.menuitemRenewContract.set_visible(False)
                self.menuitemNotForSale.set_visible(False)
                self.menuitemExtendLoan.set_visible(True)
                self.menuitemCancelLoan.set_visible(True)
            else:
                transfer = player.transfer[0]
                loan = player.transfer[1]

                if transfer is True:
                    self.menuitemAddTransfer.set_sensitive(False)
                    self.menuitemRemoveTransfer.set_sensitive(True)
                    self.menuitemNotForSale.set_active(False)
                    self.menuitemNotForSale.set_sensitive(False)
                else:
                    self.menuitemAddTransfer.set_sensitive(True)
                    self.menuitemRemoveTransfer.set_sensitive(False)

                if loan is True:
                    self.menuitemAddLoan.set_sensitive(False)
                    self.menuitemRemoveLoan.set_sensitive(True)
                else:
                    self.menuitemAddLoan.set_sensitive(True)
                    self.menuitemRemoveLoan.set_sensitive(False)

                self.menuitemNotForSale.set_visible(True)
                self.menuitemExtendLoan.set_visible(False)
                self.menuitemCancelLoan.set_visible(False)

            self.menu.popup(None, None, None, None, event.button, event.time)

    def view_changed(self, combobox):
        index = int(combobox.get_active_id())

        for count, column_list in enumerate(self.tree_columns):
            for column in column_list:
                column.set_visible(count == index)

    def filter_squad(self, button):
        dialogs.squad_filter()

        self.buttonReset.set_sensitive(not game.squad_filter == constants.squad_filter)
        self.treemodelfilter.refilter()

    def filter_reset(self, button):
        game.squad_filter = constants.squad_filter

        self.buttonReset.set_sensitive(False)
        self.treemodelfilter.refilter()

    def filter_visible(self, model, treeiter, data):
        display = True

        # Filter by selected position
        if game.squad_filter[0] == 1:
            if model[treeiter][2] not in ("GK"):
                display = False
        elif game.squad_filter[0] == 2:
            if model[treeiter][2] not in ("DL", "DR", "DC", "D"):
                display = False
        elif game.squad_filter[0] == 3:
            if model[treeiter][2] not in ("ML", "MR", "MC", "M"):
                display = False
        elif game.squad_filter[0] == 4:
            if model[treeiter][2] not in ("AF", "AS"):
                display = False

        # Filter injured and suspended players
        if game.squad_filter[1]:
            if model[treeiter][24] != 0:
                display = False

            if model[treeiter][25] != 0:
                display = False

        return display

    def add_to_position(self, menuitem, event, index):
        model, treeiter = self.treeselection.get_selected()
        playerid = model[treeiter][0]

        self.comboSquadList[index].set_active_id(str(playerid))

    def remove_from_position(self, menuitem):
        model, treeiter = self.treeselection.get_selected()
        playerid = model[treeiter][0]

        for key, item in game.clubs[game.teamid].team.items():
            if item == playerid:
                game.clubs[game.teamid].team[key] = 0
                self.comboSquadList[key].set_active(0)

    def renew_contract(self, menuitem):
        model, treeiter = self.treeselection.get_selected()
        playerid = model[treeiter][0]

        if events.renew_contract(playerid):
            state = dialogs.renew_player_contract(playerid)

            if state:
                self.populate_data()
        else:
            dialogs.error(8)

    def quick_sell(self, menuitem):
        model, treeiter = self.treeselection.get_selected()
        playerid = model[treeiter][0]
        player = game.players[playerid]

        name = display.name(player, mode=1)
        value = player.value * 0.5
        amount = display.value(value)
        new_club = transfer.quick_sell(player)

        club = game.clubs[new_club].name
        state = dialogs.quick_sell(name, club, amount)

        if state:
            class Negotiation:
                pass

            negotiation = Negotiation()
            negotiation.playerid = playerid
            negotiation.club = new_club
            negotiation.transfer_type = 0
            negotiation.amount = value
            game.negotiations[game.negotiationid] = negotiation

            valid = transfer.check(game.negotiationid)

            if valid == 0:
                transfer.move(game.negotiationid)
                game.negotiationid += 1

                for key, item in game.clubs[game.teamid].team.items():
                    if item == playerid:
                        game.clubs[game.teamid].team[key] = 0
                        self.comboSquadList[key].set_active(0)

                money.deposit(value, 6)

                self.populate_data()
            else:
                dialogs.error(state)

    def extend_loan(self, menuitem):
        model, treeiter = self.treeselection.get_selected()
        playerid = model[treeiter][0]
        player = game.players[playerid]

        transfer.extend_loan(playerid)

    def cancel_loan(self, menuitem):
        model, treeiter = self.treeselection.get_selected()
        playerid = model[treeiter][0]
        player = game.players[playerid]

        name = display.name(player, mode=1)
        state = dialogs.cancel_loan(name)

        if state:
            transfer.end_loan(playerid)

            for key, item in game.clubs[game.teamid].team.items():
                if item == playerid:
                    game.clubs[game.teamid].team[key] = 0
                    self.comboSquadList[key].set_active(0)

            self.populate_data()

    def transfer_status(self, menuitem, index):
        model, treeiter = self.treeselection.get_selected()
        playerid = model[treeiter][0]

        player = game.players[playerid]

        transfer = player.transfer[0]
        loan = player.transfer[1]

        if index == 0:
            player.transfer[0] = not transfer

            # Decrease morale
            if player.transfer[0]:
                value = random.randint(15, 25)
                evaluation.morale(playerid, value)
        elif index == 1:
            player.transfer[1] = not loan

    def not_for_sale(self, menuitem):
        model, treeiter = self.treeselection.get_selected()
        playerid = model[treeiter][0]

        game.players[playerid].not_for_sale = menuitem.get_active()

    def populate_data(self):
        self.liststoreSquad.clear()

        for playerid in game.clubs[game.teamid].squad:
            player = game.players[playerid]

            name = display.name(player)
            nationality = game.nations[player.nationality].name
            value = display.value(player.value)
            wage = display.wage(player.wage)
            contract = display.contract(player.contract)
            morale = display.player_morale(player.morale)
            appearances = "%i (%i)" % (player.appearances, player.substitute)
            cards = "%i/%i" % (player.yellow_cards, player.red_cards)
            rating = display.rating(player)

            self.liststoreSquad.append([playerid,
                                        name,
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
                                        player.fitness,
                                        nationality,
                                        value,
                                        wage,
                                        contract,
                                        morale,
                                        appearances,
                                        player.goals,
                                        player.assists,
                                        cards,
                                        player.man_of_the_match,
                                        rating,
                                        player.injury_type,
                                        player.suspension_type,
                                        ])
