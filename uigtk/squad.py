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
import random
import re
import unicodedata

from uigtk import filters
from uigtk import playerinfo
from uigtk import playerselect
import club
import constants
import dialogs
import display
import evaluation
import events
import game
import menu
import player
import widgets


class Squad(Gtk.Grid):
    __name__ = "squad"

    def __init__(self):
        targets = [("MY_TREE_MODEL_ROW", Gtk.TargetFlags.SAME_APP, 0),
                   ("text/plain", 0, 1),
                   ("TEXT", 0, 2),
                   ("STRING", 0, 3),
                  ]

        self.playerselect = playerselect.PlayerSelect()
        self.squadfilter = filters.SquadFilter()

        self.tree_columns = ([], [], [])

        Gtk.Grid.__init__(self)
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
        self.treemodelfilter.set_visible_func(self.filter_visible, player.players)

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
        scrolledwindow.set_policy(Gtk.PolicyType.NEVER,
                                  Gtk.PolicyType.AUTOMATIC)
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

        treeviewcolumn = widgets.TreeViewColumn(title="Name", column=1)
        treeviewcolumn.set_expand(True)
        treeviewSquad.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Position", column=2)
        treeviewcolumn.set_expand(True)
        treeviewSquad.append_column(treeviewcolumn)

        # Personal
        treeviewcolumn = widgets.TreeViewColumn(title="Nationality", column=13)
        self.tree_columns[0].append(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Value", column=14)
        self.tree_columns[0].append(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Wages", column=15)
        self.tree_columns[0].append(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Contract", column=16)
        self.tree_columns[0].append(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Morale", column=17)
        self.tree_columns[0].append(treeviewcolumn)

        for column in self.tree_columns[0]:
            column.set_expand(True)
            column.set_visible(False)
            treeviewSquad.append_column(column)

        # Skills
        for count, item in enumerate(constants.short_skill, start=3):
            label = Gtk.Label("%s" % (item))
            label.set_tooltip_text(constants.skill[count - 3])
            label.show()
            treeviewcolumn = widgets.TreeViewColumn(column=count)
            treeviewcolumn.set_widget(label)
            self.tree_columns[1].append(treeviewcolumn)

        treeviewcolumn = widgets.TreeViewColumn(title="Fitness", column=12)
        self.tree_columns[1].append(treeviewcolumn)

        for column in self.tree_columns[1]:
            column.set_expand(True)
            treeviewSquad.append_column(column)

        # Form
        treeviewcolumn = widgets.TreeViewColumn(title="Games", column=18)
        self.tree_columns[2].append(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Goals", column=19)
        self.tree_columns[2].append(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Assists", column=20)
        self.tree_columns[2].append(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Cards", column=21)
        self.tree_columns[2].append(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="MOTM", column=22)
        self.tree_columns[2].append(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Rating", column=23)
        self.tree_columns[2].append(treeviewcolumn)

        for column in self.tree_columns[2]:
            column.set_expand(True)
            column.set_visible(False)
            column.set_fixed_width(50)
            treeviewSquad.append_column(column)

        self.notebook = Gtk.Notebook()
        self.notebook.set_size_request(200, -1)
        self.notebook.set_hexpand(False)
        self.notebook.set_vexpand(True)
        self.attach(self.notebook, 1, 0, 1, 2)

        # Team notebook page
        label = Gtk.Label("_Team")
        label.set_use_underline(True)

        self.gridTeam = Gtk.Grid()
        self.gridTeam.set_border_width(5)
        self.gridTeam.set_row_spacing(5)
        self.gridTeam.set_column_spacing(5)
        self.notebook.append_page(self.gridTeam, label)

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

        self.buttonTeam = []

        for count in range(0, 16):
            button = Gtk.Button("")
            button.set_hexpand(True)
            button.drag_dest_set(Gtk.DestDefaults.ALL, [], Gdk.DragAction.COPY)
            button.drag_dest_add_text_targets()
            button.connect("drag-data-received", self.on_drag_data_received)
            button.connect("clicked", self.squad_dialog, count)
            self.buttonTeam.append(button)

            if count < 11:
                self.gridTeam.attach(button, 1, count, 1, 1)
            else:
                self.gridSubs.attach(button, 1, count - 11, 1, 1)

        # Context menu
        self.contextmenu = menu.SquadContextMenu()
        self.contextmenu.menuitemRemovePosition.connect("activate", self.remove_from_position)
        self.contextmenu.menuitemAddTransfer.connect("activate", self.transfer_status, 0)
        self.contextmenu.menuitemRemoveTransfer.connect("activate", self.transfer_status, 0)
        self.contextmenu.menuitemAddLoan.connect("activate", self.transfer_status, 1)
        self.contextmenu.menuitemRemoveLoan.connect("activate", self.transfer_status, 1)
        self.contextmenu.menuitemRelease.connect("activate", self.release_player)
        self.contextmenu.menuitemRenewContract.connect("activate", self.renew_contract)
        self.contextmenu.menuitemNotForSale.connect("toggled", self.not_for_sale)
        self.contextmenu.menuitemExtendLoan.connect("activate", self.extend_loan)
        self.contextmenu.menuitemCancelLoan.connect("activate", self.cancel_loan)
        self.contextmenu.menuitemPlayerInfo.connect("activate", self.row_activated)

    def squad_dialog(self, button, count):
        selected = self.playerselect.display()

        if selected == 0:
            pass
        elif selected == -1:
            button.set_label("")
            club.clubitem.clubs[game.teamid].team[count] = 0
        else:
            self.update_squad(selected, count)

    def display_squad(self):
        '''
        Display the set items within the squad button list, or clear if
        player is no longer set. Also used to clear the button text when
        starting a game from new.
        '''
        for count, playerid in enumerate(club.clubs[game.teamid].team.values()):
            if playerid != 0:
                player = player.playeritem.players[playerid]
                name = player.get_name()
                self.buttonTeam[count].set_label(name)
            else:
                self.buttonTeam[count].set_label("")

    def on_drag_data_get(self, treeview, context, selection, info, time):
        treeselection = treeview.get_selection()
        model, treeiter = treeselection.get_selected()
        data = "%s" % (model[treeiter][0])
        data = bytes(data, "utf-8")
        selection.set(selection.get_target(), 8, data)

    def on_drag_data_received(self, button, context, x, y, selection, info, time):
        playerid = selection.get_data().decode("utf-8")
        playerid = int(playerid)

        count = 0

        for widget in self.buttonTeam:
            if button is widget:
                key = count

            count += 1

        self.update_squad(playerid, key)

        if context.get_actions() == Gdk.DragAction.COPY:
            context.finish(True, False, time)

        return

    def update_squad(self, playerid, count):
        '''
        Remove player if they already exist in the squad list, and then
        set the player into the new position.
        '''
        for key, item in club.clubs[game.teamid].team.items():
            if item != 0 and str(item) == str(playerid):
                club.clubs[game.teamid].team[key] = 0
                self.buttonTeam[key].set_label("")

        playerObject = player.players[playerid]
        name = playerObject.get_name()
        button = self.buttonTeam[count]
        button.set_label("%s" % (name))
        club.clubs[game.teamid].team[count] = playerid

    def row_activated(self, widget, path=None, treeviewcolumn=None):
        '''
        Display the extra player information dialog box when double
        clicking a row in the squad.
        '''
        model, treeiter = self.treeselection.get_selected()
        playerid = model[treeiter][0]

        dialog = playerinfo.PlayerInfo(playerid)
        dialog.run()
        dialog.destroy()

    def context_menu(self, widget, event):
        model, treeiter = self.treeselection.get_selected()

        if treeiter and event.button == 3:
            playerid = model[treeiter][0]
            playerObject = player.players[playerid]

            self.contextmenu.menuitemNotForSale.set_active(playerObject.not_for_sale)

            self.contextmenu.show_all()

            if playerid in game.loans:
                self.contextmenu.menuitemAddTransfer.set_visible(False)
                self.contextmenu.menuitemRemoveTransfer.set_visible(False)
                self.contextmenu.menuitemAddLoan.set_visible(False)
                self.contextmenu.menuitemRemoveLoan.set_visible(False)
                self.contextmenu.menuitemRelease.set_visible(False)
                self.contextmenu.menuitemRenewContract.set_visible(False)
                self.contextmenu.menuitemNotForSale.set_visible(False)
                self.contextmenu.menuitemExtendLoan.set_visible(True)
                self.contextmenu.menuitemCancelLoan.set_visible(True)
            else:
                if playerObject.transfer[0]:
                    self.contextmenu.menuitemAddTransfer.set_sensitive(False)
                    self.contextmenu.menuitemRemoveTransfer.set_sensitive(True)
                    self.contextmenu.menuitemNotForSale.set_sensitive(False)
                else:
                    self.contextmenu.menuitemAddTransfer.set_sensitive(True)
                    self.contextmenu.menuitemRemoveTransfer.set_sensitive(False)
                    self.contextmenu.menuitemNotForSale.set_sensitive(True)

                if playerObject.transfer[1]:
                    self.contextmenu.menuitemAddLoan.set_sensitive(False)
                    self.contextmenu.menuitemRemoveLoan.set_sensitive(True)
                else:
                    self.contextmenu.menuitemAddLoan.set_sensitive(True)
                    self.contextmenu.menuitemRemoveLoan.set_sensitive(False)

                self.contextmenu.menuitemRelease.set_visible(True)
                self.contextmenu.menuitemNotForSale.set_visible(True)
                self.contextmenu.menuitemExtendLoan.set_visible(False)
                self.contextmenu.menuitemCancelLoan.set_visible(False)

            self.contextmenu.popup(None, None, None, None, event.button, event.time)

    def view_changed(self, combobox):
        index = int(combobox.get_active_id())

        for count, column_list in enumerate(self.tree_columns):
            for column in column_list:
                column.set_visible(count == index)

    def filter_squad(self, button):
        self.squadfilter.display()

        sensitive = self.squadfilter.options != self.squadfilter.defaults
        self.buttonReset.set_sensitive(sensitive)

        self.treemodelfilter.refilter()

    def filter_reset(self, button):
        self.squadfilter.reset_defaults()

        self.buttonReset.set_sensitive(False)
        self.treemodelfilter.refilter()

    def filter_visible(self, model, treeiter, data):
        display = True

        # Filter by selected position
        if self.squadfilter.options["position"] == 1:
            if model[treeiter][2] not in ("GK"):
                display = False
        elif self.squadfilter.options["position"] == 2:
            if model[treeiter][2] not in ("DL", "DR", "DC", "D"):
                display = False
        elif self.squadfilter.options["position"] == 3:
            if model[treeiter][2] not in ("ML", "MR", "MC", "M"):
                display = False
        elif self.squadfilter.options["position"] == 4:
            if model[treeiter][2] not in ("AF", "AS"):
                display = False

        # Filter injured and suspended players
        if self.squadfilter.options["availableonly"]:
            if model[treeiter][24] != 0:
                display = False

            if model[treeiter][25] != 0:
                display = False

        return display

    def add_to_position(self, menuitem, event, index):
        '''
        Add selected player to specified position.
        '''
        model, treeiter = self.treeselection.get_selected()
        playerid = model[treeiter][0]
        playerObject = player.players[playerid]

        name = playerObject.get_name()

        self.buttonTeam[index].set_label(name)
        club.clubs[game.teamid].team[index] = playerid

    def remove_from_position(self, menuitem):
        '''
        Find player in squad list and remove from set position.
        '''
        model, treeiter = self.treeselection.get_selected()
        playerid = model[treeiter][0]

        for key, item in club.clubs[game.teamid].team.items():
            if item == playerid:
                club.clubs[game.teamid].team[key] = 0
                self.buttonTeam[key].set_label("")

    def renew_contract(self, menuitem):
        '''
        Initiate contract negotiations for selected player.
        '''
        model, treeiter = self.treeselection.get_selected()
        playerid = model[treeiter][0]

        if game.players[playerid].renew_contract:
            if dialogs.renew_player_contract(playerid):
                self.populate_data()
        else:
            dialogs.error(8)

    def release_player(self, menuitem):
        '''
        Initiate release of selected player from the club.
        '''
        model, treeiter = self.treeselection.get_selected()

        playerid = model[treeiter][0]
        player = game.players[playerid]

        name = player.get_name(mode=1)
        cost = player.contract * player.wage

        if dialogs.release_player(name, cost):
            club = club.clubitem.clubs[game.teamid]

            if club.accounts.request(amount=cost):
                club.accounts.withdraw(amount=cost, category="playerwage")

                player.club = None
                club.squad.remove(playerid)

                self.populate_data()

    def extend_loan(self, menuitem):
        '''
        Request loan extension from parent club of selected player.
        '''
        model, treeiter = self.treeselection.get_selected()

        playerid = model[treeiter][0]

        game.loans[playerid].extend_loan()

    def cancel_loan(self, menuitem):
        '''
        Cancel loan deal for selected player and return to parent club.
        '''
        model, treeiter = self.treeselection.get_selected()

        playerid = model[treeiter][0]
        player = game.players[playerid]
        name = player.get_name(mode=1)

        loan = game.loans[playerid]

        if loan.cancel_loan():
            loan.end_loan()

            for key, item in club.clubitem.clubs[game.teamid].team.items():
                if item == playerid:
                    club.clubitem.clubs[game.teamid].team[key] = 0
                    self.buttonTeam[key].set_label("")

            self.populate_data()

    def transfer_status(self, menuitem, index):
        model, treeiter = self.treeselection.get_selected()

        playerid = model[treeiter][0]
        player = game.players[playerid]

        if index == 0:
            player.transfer[0] = not player.transfer[0]

            # Decrease morale
            if player.transfer[0]:
                value = random.randint(15, 25)
                player.set_morale(value)
                player.not_for_sale = False
        elif index == 1:
            player.transfer[1] = not player.transfer[1]

    def not_for_sale(self, menuitem):
        '''
        Set the selected player as not for sale.
        '''
        model, treeiter = self.treeselection.get_selected()
        playerid = model[treeiter][0]

        game.players[playerid].not_for_sale = menuitem.get_active()

    def populate_data(self):
        self.liststoreSquad.clear()

        for playerid in club.clubs[game.teamid].squad:
            playerObject = player.get_player(playerid)

            self.liststoreSquad.append([playerid,
                                        playerObject.get_name(),
                                        playerObject.position,
                                        playerObject.keeping,
                                        playerObject.tackling,
                                        playerObject.passing,
                                        playerObject.shooting,
                                        playerObject.heading,
                                        playerObject.pace,
                                        playerObject.stamina,
                                        playerObject.ball_control,
                                        playerObject.set_pieces,
                                        playerObject.fitness,
                                        playerObject.get_nationality(),
                                        playerObject.get_value(),
                                        playerObject.get_wage(),
                                        playerObject.get_contract(),
                                        playerObject.get_morale(),
                                        playerObject.get_appearances(),
                                        playerObject.goals,
                                        playerObject.assists,
                                        playerObject.get_cards(),
                                        playerObject.man_of_the_match,
                                        playerObject.get_rating(),
                                        playerObject.injury_type,
                                        playerObject.suspension_type,
                                        ])

    def run(self):
        formationid = club.clubs[game.teamid].tactics.formation

        for count in range(0, 16):
            button = self.buttonTeam[count]

            playerid = club.clubs[game.teamid].team[count]

            if count < 11:
                position = constants.formations[formationid][1][count]
                self.labelTeam[count].set_label("_%s" % (position))
                self.labelTeam[count].set_mnemonic_widget(button)
            else:
                self.labelSubs[count - 11].set_label("Sub _%s" % (count - 10))
                self.labelSubs[count - 11].set_mnemonic_widget(button)

        # Context menu for "Add To Position"
        self.menuPosition = Gtk.Menu()
        self.contextmenu.menuitemAddPosition.set_submenu(self.menuPosition)

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
        self.display_squad()

        self.show_all()
