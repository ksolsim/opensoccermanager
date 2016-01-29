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
import structures.filters
import structures.skills
import uigtk.widgets


targets = [("MY_TREE_MODEL_ROW", Gtk.TargetFlags.SAME_APP, 0),
           ("TEXT", 0, 1)]


class Squad(uigtk.widgets.Grid):
    __name__ = "squad"

    club = None

    squadfilter = None

    squadlist = None
    treeselection = None
    firstteam = None
    substitutions = None

    def __init__(self):
        uigtk.widgets.Grid.__init__(self)

        grid = uigtk.widgets.Grid()
        self.attach(grid, 0, 0, 1, 1)

        self.columnviews = uigtk.shared.ColumnViews()
        self.columnviews.comboboxView.connect("changed", self.on_view_changed)
        grid.attach(self.columnviews, 1, 0, 1, 1)

        label = Gtk.Label()
        label.set_hexpand(True)
        grid.attach(label, 2, 0, 1, 1)

        self.filterbuttons = uigtk.shared.FilterButtons()
        self.filterbuttons.buttonFilter.connect("clicked", self.on_filter_clicked)
        self.filterbuttons.buttonReset.connect("clicked", self.on_reset_clicked)
        grid.attach(self.filterbuttons, 3, 0, 1, 1)

        scrolledwindow = uigtk.widgets.ScrolledWindow()
        self.attach(scrolledwindow, 0, 1, 1, 1)

        Squad.squadlist = SquadList()

        self.treemodelfilter = Squad.squadlist.filter_new()
        self.treemodelfilter.set_visible_func(self.filter_visible, data.players.get_players())
        treemodelsort = Gtk.TreeModelSort(self.treemodelfilter)
        treemodelsort.set_sort_column_id(1, Gtk.SortType.ASCENDING)

        treeview = Gtk.TreeView()
        treeview.set_vexpand(True)
        treeview.set_hexpand(True)
        treeview.set_model(treemodelsort)
        treeview.set_search_column(1)
        treeview.enable_model_drag_source(Gdk.ModifierType.BUTTON1_MASK,
                                          targets,
                                          Gdk.DragAction.COPY)
        treeview.connect("row-activated", self.on_row_activated)
        treeview.connect("button-release-event", self.on_button_release_event)
        treeview.connect("key-press-event", self.on_key_press_event)
        treeview.connect("drag-data-get", self.on_drag_data_get)
        scrolledwindow.add(treeview)

        Squad.treeselection = treeview.get_selection()

        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Name", column=1)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Position", column=2)
        treeview.append_column(treeviewcolumn)

        self.tree_columns = ([], [], [])

        # Personal
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Nationality", column=13)
        self.tree_columns[0].append(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Value", column=14)
        self.tree_columns[0].append(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Wage", column=15)
        self.tree_columns[0].append(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Contract", column=16)
        self.tree_columns[0].append(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Morale", column=17)
        self.tree_columns[0].append(treeviewcolumn)

        # Skills
        skills = structures.skills.Skills()

        for count, skill in enumerate(skills.get_skills(), start=3):
            label = Gtk.Label("%s" % (skill[0]))
            label.set_tooltip_text(skill[1])
            label.show()
            treeviewcolumn = uigtk.widgets.TreeViewColumn(column=count)
            treeviewcolumn.set_expand(True)
            treeviewcolumn.set_widget(label)
            treeview.append_column(treeviewcolumn)
            self.tree_columns[1].append(treeviewcolumn)

        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Fitness", column=12)
        treeview.append_column(treeviewcolumn)
        self.tree_columns[1].append(treeviewcolumn)

        # Form
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Games", column=18)
        self.tree_columns[2].append(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Goals", column=19)
        self.tree_columns[2].append(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Assists", column=20)
        self.tree_columns[2].append(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Cards", column=21)
        self.tree_columns[2].append(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="MOTM", column=22)
        self.tree_columns[2].append(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Rating", column=23)
        self.tree_columns[2].append(treeviewcolumn)

        for columns in (self.tree_columns[0], self.tree_columns[2]):
            for column in columns:
                column.set_expand(True)
                column.set_visible(False)
                treeview.append_column(column)

        notebook = Gtk.Notebook()
        notebook.set_hexpand(False)
        notebook.set_size_request(225, -1)
        self.attach(notebook, 1, 0, 1, 2)

        Squad.firstteam = FirstTeam()
        label = uigtk.widgets.Label("_Team")
        notebook.append_page(Squad.firstteam, label)

        Squad.substitutions = Substitutions()
        label = uigtk.widgets.Label("_Subs")
        notebook.append_page(self.substitutions, label)

        self.contextmenu = ContextMenu()
        self.filter_dialog = Filter()

        Squad.squadfilter = structures.filters.Squad()

    def on_drag_data_get(self, treeview, context, selection, info, time):
        model, treeiter = Squad.treeselection.get_selected()

        data = bytes("%i" % (model[treeiter][0]), "utf-8")
        selection.set(selection.get_target(), 8, data)

    def on_key_press_event(self, widget, event):
        if Gdk.keyval_name(event.keyval) == "Menu":
            self.on_context_menu_event(event)

    def on_button_release_event(self, widget, event):
        self.on_context_menu_event(event)

    def on_context_menu_event(self, event):
        if event.button == 3:
            model, treeiter = Squad.treeselection.get_selected()
            playerid = model[treeiter][0]

            self.contextmenu.playerid = playerid
            self.contextmenu.show()
            self.contextmenu.popup(None,
                                   None,
                                   None,
                                   None,
                                   event.button,
                                   event.time)

    def on_row_activated(self, treeview, treepath, treeviewcolumn):
        '''
        Launch player information screen with player details.
        '''
        model = treeview.get_model()
        playerid = model[treepath][0]

        data.window.screen.change_visible_screen("playerinformation")
        data.window.screen.active.set_visible_player(playerid)

    def on_view_changed(self, combobox):
        '''
        Change which columns of information are visible.
        '''
        index = int(combobox.get_active_id())

        for count, column_list in enumerate(self.tree_columns):
            for column in column_list:
                column.set_visible(count == index)

    def on_filter_clicked(self, button):
        '''
        Display squad view filtering dialog.
        '''
        Squad.squadfilter.options = self.filter_dialog.show()

        active = Squad.squadfilter.get_filter_active()
        self.filterbuttons.buttonReset.set_sensitive(active)

        self.treemodelfilter.refilter()

    def on_reset_clicked(self, button):
        '''
        Clear filter settings and reset to default state.
        '''
        button.set_sensitive(False)
        Squad.squadfilter.reset_filter()

        self.treemodelfilter.refilter()

    def filter_visible(self, model, treeiter, data):
        display = True

        if Squad.squadfilter.options["position"] == 1:
            if model[treeiter][2] not in ("GK",):
                display = False
        elif Squad.squadfilter.options["position"] == 2:
            if model[treeiter][2] not in ("DL", "DR", "DC", "D"):
                display = False
        elif Squad.squadfilter.options["position"] == 3:
            if model[treeiter][2] not in ("ML", "MR", "MC", "M"):
                display = False
        elif Squad.squadfilter.options["position"] == 4:
            if model[treeiter][2] not in ("AF", "AS"):
                display = False

        return display

    def populate_data(self):
        Squad.squadlist.update()

    def populate_selection(self):
        '''
        Call to update team selection interface.
        '''
        self.firstteam.populate_team()
        self.substitutions.populate_subs()

    def run(self):
        Squad.club = data.clubs.get_club_by_id(data.user.team)

        self.populate_data()
        self.populate_selection()
        self.show_all()


class SquadList(Gtk.ListStore):
    '''
    ListStore holding list of players in squad.
    '''
    def __init__(self):
        Gtk.ListStore.__init__(self)
        self.set_column_types([int, str, str, int, int, int, int,
                               int, int, int, int, int, int, str,
                               str, str, str, str, str, int, int,
                               str, int, str, str, str])

    def update(self):
        self.clear()

        for playerid, player in Squad.club.squad.get_squad():
            self.append([playerid,
                         player.get_name(),
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
                         player.get_nationality_name(),
                         player.value.get_value_as_string(),
                         player.wage.get_wage_as_string(),
                         player.contract.get_contract(),
                         player.get_morale(),
                         player.get_appearances(),
                         player.goals,
                         player.assists,
                         player.get_cards(),
                         player.man_of_the_match,
                         player.rating.get_average_rating(),
                         player.injury.get_injury_type(),
                         player.suspension.get_suspension_type()])


class FirstTeam(uigtk.widgets.Grid):
    def __init__(self):
        uigtk.widgets.Grid.__init__(self)
        self.set_border_width(5)

        self.labels = []
        self.buttons = []

        for count in range(0, 11):
            label = uigtk.widgets.Label()
            self.attach(label, 0, count, 1, 1)
            self.labels.append(label)

            button = Gtk.Button("")
            button.set_hexpand(True)
            button.drag_source_set(Gdk.ModifierType.BUTTON1_MASK, None, Gdk.DragAction.COPY)
            button.drag_source_add_text_targets()
            button.drag_dest_set(Gtk.DestDefaults.ALL, [], Gdk.DragAction.COPY)
            button.drag_dest_add_text_targets()
            button.connect("drag-data-get", self.on_drag_data_get, count)
            button.connect("drag-data-received", self.on_drag_data_received, count)
            button.connect("clicked", self.on_player_select_clicked, count)
            label.set_mnemonic_widget(button)
            self.attach(button, 1, count, 1, 1)
            self.buttons.append(button)

    def on_drag_data_get(self, button, context, selection, info, time, positionid):
        '''
        Process dragged data and get player from specified position.
        '''
        playerid = Squad.club.squad.teamselection.team[positionid]

        if playerid:
            Squad.club.squad.teamselection.team[positionid] = None

            data = bytes("%i" % (playerid), "utf-8")
            selection.set(selection.get_target(), 8, data)

        return

    def on_drag_data_received(self, button, context, x, y, selection, info, time, positionid):
        '''
        Process dropped data and set player into squad at specified postion.
        '''
        playerid = int(selection.get_data().decode("utf-8"))

        Squad.club.squad.teamselection.add_to_team(playerid, positionid)
        Squad.populate_selection(Squad)

        if context.get_actions() == Gdk.DragAction.COPY:
            context.finish(True, False, time)

        return

    def on_player_select_clicked(self, button, positionid):
        '''
        Add player into squad at specified position.
        '''
        dialog = PlayerSelect()
        status = dialog.show(Squad.club.squad.teamselection.get_player_for_position(positionid))

        if status == -1:
            Squad.club.squad.teamselection.remove_from_team_by_position(positionid)
            Squad.populate_selection(Squad)
        elif status == 0:
            pass
        else:
            Squad.club.squad.teamselection.add_to_team(status, positionid)
            Squad.populate_selection(Squad)

    def populate_team(self):
        for count, position in enumerate(Squad.club.tactics.get_formation_positions()):
            label = self.labels[count]
            label.set_label("_%s" % (position))

        for count, playerid in enumerate(Squad.club.squad.teamselection.get_team_selection()):
            if playerid:
                player = data.players.get_player_by_id(playerid)
                self.buttons[count].set_label(player.get_name())
            else:
                self.buttons[count].set_label("")


class Substitutions(uigtk.widgets.Grid):
    def __init__(self):
        uigtk.widgets.Grid.__init__(self)
        self.set_border_width(5)

        self.buttons = []

        for count in range(0, 5):
            label = uigtk.widgets.Label("Sub _%i" % (count + 1))
            self.attach(label, 0, count, 1, 1)

            button = Gtk.Button("")
            button.set_hexpand(True)
            button.drag_source_set(Gdk.ModifierType.BUTTON1_MASK, None, Gdk.DragAction.COPY)
            button.drag_source_add_text_targets()
            button.drag_dest_set(Gtk.DestDefaults.ALL, [], Gdk.DragAction.COPY)
            button.drag_dest_add_text_targets()
            button.connect("drag-data-get", self.on_drag_data_get, count)
            button.connect("drag-data-received", self.on_drag_data_received, count)
            button.connect("clicked", self.on_player_select_clicked, count)
            label.set_mnemonic_widget(button)
            self.attach(button, 1, count, 1, 1)
            self.buttons.append(button)

    def on_drag_data_get(self, button, context, selection, info, time, positionid):
        '''
        Process dragged data and get player from specified position.
        '''
        playerid = Squad.club.squad.teamselection.subs[positionid]

        if playerid:
            Squad.club.squad.teamselection.subs[positionid] = None

            data = bytes("%i" % (playerid), "utf-8")
            selection.set(selection.get_target(), 8, data)

        return

    def on_drag_data_received(self, button, context, x, y, selection, info, time, positionid):
        '''
        Process dropped data and set player into squad at specified postion.
        '''
        playerid = int(selection.get_data().decode("utf-8"))

        Squad.club.squad.teamselection.add_to_subs(playerid, positionid)
        Squad.populate_selection(Squad)

        if context.get_actions() == Gdk.DragAction.COPY:
            context.finish(True, False, time)

        return

    def on_player_select_clicked(self, button, positionid):
        '''
        Add player into substitutes at specified position.
        '''
        dialog = PlayerSelect()
        status = dialog.show(Squad.club.squad.teamselection.get_sub_player_for_position(positionid))

        if status == -1:
            Squad.club.squad.teamselection.remove_from_subs_by_position(positionid)
            Squad.populate_selection(Squad)
        elif status == 0:
            pass
        else:
            Squad.club.squad.teamselection.add_to_subs(status, positionid)
            Squad.populate_selection(Squad)

    def populate_subs(self):
        for count, playerid in enumerate(Squad.club.squad.teamselection.get_subs_selection()):
            if playerid:
                player = data.players.get_player_by_id(playerid)
                self.buttons[count].set_label(player.get_name())
            else:
                self.buttons[count].set_label("")


class PlayerSelect(Gtk.Dialog):
    def __init__(self, *args):
        Gtk.Dialog.__init__(self)
        self.set_transient_for(data.window)
        self.set_modal(True)
        self.set_size_request(-1, 250)
        self.set_resizable(False)
        self.set_title("Player Selection")
        self.add_button("_Clear", Gtk.ResponseType.REJECT)
        self.add_button("C_lose", Gtk.ResponseType.CLOSE)
        self.add_button("_Select", Gtk.ResponseType.OK)
        self.set_default_response(Gtk.ResponseType.OK)
        self.set_response_sensitive(Gtk.ResponseType.OK, False)
        self.vbox.set_border_width(5)
        self.vbox.set_spacing(5)

        scrolledwindow = uigtk.widgets.ScrolledWindow()
        self.vbox.add(scrolledwindow)

        self.liststore = Gtk.ListStore(int, str)
        self.treemodelfilter = self.liststore.filter_new()
        self.treemodelfilter.set_visible_func(self.on_filter_visible,
                                              data.players.get_players())
        self.treemodelsort = Gtk.TreeModelSort(self.treemodelfilter)
        self.treemodelsort.set_sort_column_id(1, Gtk.SortType.ASCENDING)

        self.treeview = uigtk.widgets.TreeView()
        self.treeview.set_vexpand(True)
        self.treeview.set_hexpand(True)
        self.treeview.set_headers_visible(False)
        self.treeview.set_model(self.treemodelsort)
        self.treeview.connect("row-activated", self.on_row_activated)
        self.treeview.treeselection.connect("changed", self.on_treeselection_changed)
        scrolledwindow.add(self.treeview)

        treeviewcolumn = uigtk.widgets.TreeViewColumn(column=1)
        self.treeview.append_column(treeviewcolumn)

        self.entrySearch = Gtk.SearchEntry()
        self.entrySearch.set_placeholder_text("Search Players...")
        self.entrySearch.connect("activate", self.on_search_activated)
        self.entrySearch.connect("changed", self.on_search_changed)
        self.entrySearch.connect("icon-press", self.on_search_pressed)
        self.vbox.add(self.entrySearch)

        self.populate_data()

    def on_filter_visible(self, model, treeiter, data):
        visible = True

        criteria = self.entrySearch.get_text()

        for search in (model[treeiter][1],):
            search = "".join((c for c in unicodedata.normalize("NFD", search) if unicodedata.category(c) != "Mn"))

            if not re.findall(criteria, search, re.IGNORECASE):
                visible = False

        return visible

    def on_search_activated(self, entry):
        '''
        Filter items to match search criteria.
        '''
        if self.entrySearch.get_text_length() > 0:
            self.treemodelfilter.refilter()

    def on_search_pressed(self, entry, position, event):
        '''
        Clear text content of search entry.
        '''
        if position == Gtk.EntryIconPosition.SECONDARY:
            entry.set_text("")
            self.treemodelfilter.refilter()

    def on_search_changed(self, entry):
        '''
        Refilter visible players when search entry is emptied.
        '''
        if entry.get_text_length() == 0:
            self.treemodelfilter.refilter()

    def on_row_activated(self, *args):
        '''
        Confirm response on double-clicking of player.
        '''
        self.response(Gtk.ResponseType.OK)

    def on_treeselection_changed(self, treeselection):
        '''
        Update button state on treeview selection.
        '''
        model, treeiter =  treeselection.get_selected()

        if treeiter:
            self.set_response_sensitive(Gtk.ResponseType.OK, True)
        else:
            self.set_response_sensitive(Gtk.ResponseType.OK, False)

    def highlight_player(self, playerid):
        '''
        Find playerid in list and highlight row.
        '''
        for item in self.treemodelsort:
            if playerid == item[0]:
                self.treeview.treeselection.select_iter(item.iter)
                treepath = self.treemodelsort.get_path(item.iter)
                self.treeview.scroll_to_cell(treepath, None, False)

    def populate_data(self):
        self.liststore.clear()

        for playerid, player in Squad.club.squad.get_squad():
            self.liststore.append([playerid, player.get_name()])

    def show(self, playerid=None):
        if playerid:
            self.highlight_player(playerid)

        self.show_all()

        response = self.run()
        status = 0

        if response == Gtk.ResponseType.OK:
            model, treeiter = self.treeview.treeselection.get_selected()
            status = model[treeiter][0]
        elif response == Gtk.ResponseType.REJECT:
            status = -1

        self.destroy()

        return status


class Filter(Gtk.Dialog):
    def __init__(self, *args):
        Gtk.Dialog.__init__(self)
        self.set_transient_for(data.window)
        self.set_modal(True)
        self.set_resizable(False)
        self.set_title("Filter Squad")
        self.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("_Filter", Gtk.ResponseType.OK)
        self.set_default_response(Gtk.ResponseType.OK)
        self.vbox.set_border_width(5)
        self.vbox.set_spacing(5)

        grid = uigtk.widgets.Grid()
        self.vbox.add(grid)

        label = uigtk.widgets.Label("_Position", leftalign=True)
        grid.attach(label, 0, 0, 1, 1)
        self.comboboxPosition = Gtk.ComboBoxText()
        self.comboboxPosition.append("0", "All")
        self.comboboxPosition.append("1", "Goalkeeper")
        self.comboboxPosition.append("2", "Defender")
        self.comboboxPosition.append("3", "Midfielder")
        self.comboboxPosition.append("4", "Attacker")
        self.comboboxPosition.set_active(0)
        self.comboboxPosition.set_tooltip_text("Set position from which players should be visible.")
        label.set_mnemonic_widget(self.comboboxPosition)
        grid.attach(self.comboboxPosition, 1, 0, 1, 1)

        self.checkbuttonAvailable = uigtk.widgets.CheckButton("_Show Only Available Players")
        self.checkbuttonAvailable.set_tooltip_text("Hide injured or suspended players from display.")
        grid.attach(self.checkbuttonAvailable, 0, 1, 3, 1)

    def show(self):
        self.show_all()

        options = Squad.squadfilter.options

        self.comboboxPosition.set_active_id(str(options["position"]))
        self.checkbuttonAvailable.set_active(options["availableonly"])

        if self.run() == Gtk.ResponseType.OK:
            options["position"] = int(self.comboboxPosition.get_active_id())
            options["availableonly"] = self.checkbuttonAvailable.get_active()

        self.hide()

        return options


class ContextMenu(Gtk.Menu):
    playerid = None

    def __init__(self):
        Gtk.Menu.__init__(self)

        menuitem = uigtk.widgets.MenuItem("_Player Information")
        menuitem.connect("activate", self.on_player_information_clicked)
        self.append(menuitem)

        separator = Gtk.SeparatorMenuItem()
        self.append(separator)

        self.menuitemAddTeam = uigtk.widgets.MenuItem("_Add To Team")
        self.append(self.menuitemAddTeam)
        menuitem = uigtk.widgets.MenuItem("_Remove From Team")
        menuitem.connect("activate", self.on_remove_from_team_clicked)
        self.append(menuitem)

        separator = Gtk.SeparatorMenuItem()
        self.append(separator)

        self.menuitemAddPurchase = uigtk.widgets.MenuItem("_Add To Purchase List")
        self.menuitemAddPurchase.connect("activate", self.on_purchase_list_clicked)
        self.append(self.menuitemAddPurchase)
        self.menuitemRemovePurchase = uigtk.widgets.MenuItem("_Remove From Purchase List")
        self.menuitemRemovePurchase.connect("activate", self.on_purchase_list_clicked)
        self.append(self.menuitemRemovePurchase)
        self.menuitemAddLoan = uigtk.widgets.MenuItem("_Add To Loan List")
        self.menuitemAddLoan.connect("activate", self.on_loan_list_clicked)
        self.append(self.menuitemAddLoan)
        self.menuitemRemoveLoan = uigtk.widgets.MenuItem("_Remove From Loan List")
        self.menuitemRemoveLoan.connect("activate", self.on_loan_list_clicked)
        self.append(self.menuitemRemoveLoan)
        menuitem = uigtk.widgets.MenuItem("_Renew Contract")
        menuitem.connect("activate", self.on_renew_contract_clicked)
        self.append(menuitem)
        menuitem = uigtk.widgets.MenuItem("_Terminate Contract")
        menuitem.connect("activate", self.on_terminate_contract_clicked)
        self.append(menuitem)

        separator = Gtk.SeparatorMenuItem()
        self.append(separator)

        menuitem = uigtk.widgets.MenuItem("Add To _Comparison")
        menuitem.connect("activate", self.on_comparison_clicked)
        self.append(menuitem)

    def on_remove_from_team_clicked(self, *args):
        '''
        Remove player from team if found in team selection.
        '''
        Squad.club.squad.teamselection.remove_from_team(ContextMenu.playerid)

        Squad.populate_selection(Squad)

    def on_purchase_list_clicked(self, *args):
        '''
        Add player to the transfer list for sale.
        '''
        self.player.transfer[0] = not self.player.transfer[0]

    def on_loan_list_clicked(self, *args):
        '''
        Add player to the transfer list for loan.
        '''
        self.player.transfer[1] = not self.player.transfer[1]

    def on_renew_contract_clicked(self, *args):
        '''
        Query user to renew contract of selected player.
        '''
        dialog = RenewContract(self.playerid)

        if dialog.show() == 1:
            pass

    def on_terminate_contract_clicked(self, *args):
        '''
        Query user to terminate contract of selected player.
        '''
        dialog = TerminateContract(self.playerid)

        if dialog.show() == 1:
            player = data.players.get_player_by_id(self.playerid)
            player.contract.terminate_contract()

            Squad.squadlist.update()

    def on_comparison_clicked(self, *args):
        '''
        Add player to stack for comparison.
        '''
        data.comparison.add_to_comparison(self.playerid)

    def on_player_information_clicked(self, *args):
        '''
        Launch player information screen for selected player.
        '''
        data.window.screen.change_visible_screen("playerinformation")
        data.window.screen.active.set_visible_player(self.playerid)

    def show(self):
        ContextMenu.playerid = self.playerid
        self.player = data.players.get_player_by_id(self.playerid)

        self.menuitemAddPurchase.set_sensitive(not self.player.transfer[0])
        self.menuitemRemovePurchase.set_sensitive(self.player.transfer[0])
        self.menuitemAddLoan.set_sensitive(not self.player.transfer[1])
        self.menuitemRemoveLoan.set_sensitive(self.player.transfer[1])

        self.positionmenu = PositionMenu()
        self.menuitemAddTeam.set_submenu(self.positionmenu)
        self.positionmenu.show()

        self.show_all()


class PositionMenu(Gtk.Menu):
    '''
    Context submenu for adding players to positions via menu.
    '''
    def __init__(self):
        Gtk.Menu.__init__(self)

    def on_add_team_clicked(self, menuitem, event, positionid):
        '''
        Add player id to passed position id.
        '''
        Squad.club.squad.teamselection.add_to_team(ContextMenu.playerid, positionid)
        Squad.populate_selection(Squad)

    def on_add_subs_clicked(self, menuitem, event, subid):
        '''
        Add player id to passed position (substitution) id.
        '''
        Squad.club.squad.teamselection.add_to_subs(ContextMenu.playerid, subid)
        Squad.populate_selection(Squad)

    def show(self):
        for count, position in enumerate(Squad.club.tactics.get_formation_positions()):
            menuitem = uigtk.widgets.MenuItem("_%s" % (position))
            menuitem.connect("button-release-event", self.on_add_team_clicked, count)
            self.append(menuitem)

        for count in range(0, 5):
            menuitem = uigtk.widgets.MenuItem("Sub _%i" % (count + 1))
            menuitem.connect("button-release-event", self.on_add_subs_clicked, count)
            self.append(menuitem)


class RenewContract(Gtk.Dialog):
    '''
    Dialog to arrange details for renewing specified players contract.
    '''
    def __init__(self, playerid):
        player = data.players.get_player_by_id(playerid)

        Gtk.MessageDialog.__init__(self)
        self.set_transient_for(data.window)
        self.set_modal(True)
        self.set_resizable(False)
        self.set_title("Renew Contract")
        self.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("_Renew", Gtk.ResponseType.OK)
        self.set_default_response(Gtk.ResponseType.CANCEL)
        self.vbox.set_border_width(5)
        self.vbox.set_spacing(5)

        label = uigtk.widgets.Label("Contract renewal details for %s." % (player.get_name(mode=1)), leftalign=True)
        self.vbox.add(label)

        frame = uigtk.widgets.CommonFrame("Details")
        self.vbox.add(frame)

        label = uigtk.widgets.Label("_Weekly Wage", leftalign=True)
        frame.grid.attach(label, 0, 0, 1, 1)
        spinbuttonWage = uigtk.widgets.SpinButton(maximum=100000)
        label.set_mnemonic_widget(spinbuttonWage)
        #spinbuttonWage.set_value(wage)
        frame.grid.attach(spinbuttonWage, 1, 0, 1, 1)
        label = uigtk.widgets.Label("League _Champions Bonus", leftalign=True)
        frame.grid.attach(label, 0, 1, 1, 1)
        spinbuttonLeagueChampions = uigtk.widgets.SpinButton(maximum=200000)
        label.set_mnemonic_widget(spinbuttonLeagueChampions)
        #spinbuttonLeagueChampions.set_value(leaguewin)
        frame.grid.attach(spinbuttonLeagueChampions, 1, 1, 1, 1)
        label = uigtk.widgets.Label("League _Runner Up Bonus", leftalign=True)
        frame.grid.attach(label, 0, 2, 1, 1)
        spinbuttonLeagueRunnerUp = uigtk.widgets.SpinButton(maximum=200000)
        label.set_mnemonic_widget(spinbuttonLeagueRunnerUp)
        #spinbuttonLeagueRunnerUp.set_value(leaguerunnerup)
        frame.grid.attach(spinbuttonLeagueRunnerUp, 1, 2, 1, 1)
        label = uigtk.widgets.Label("_Win Bonus", leftalign=True)
        frame.grid.attach(label, 0, 3, 1, 1)
        spinbuttonWinBonus = uigtk.widgets.SpinButton(maximum=10000)
        label.set_mnemonic_widget(spinbuttonWinBonus)
        #spinbuttonWinBonus.set_value(winbonus)
        frame.grid.attach(spinbuttonWinBonus, 1, 3, 1, 1)
        label = uigtk.widgets.Label("_Goal Bonus", leftalign=True)
        frame.grid.attach(label, 0, 4, 1, 1)
        spinbuttonGoalBonus = uigtk.widgets.SpinButton(maximum=10000)
        label.set_mnemonic_widget(spinbuttonGoalBonus)
        #spinbuttonGoalBonus.set_value(goalbonus)
        frame.grid.attach(spinbuttonGoalBonus, 1, 4, 1, 1)
        label = uigtk.widgets.Label("_Contract Length", leftalign=True)
        frame.grid.attach(label, 0, 5, 1, 1)
        spinbuttonContract = Gtk.SpinButton.new_with_range(1, 5, 1)
        label.set_mnemonic_widget(spinbuttonContract)
        #spinbuttonContract.set_value(contract)
        frame.grid.attach(spinbuttonContract, 1, 5, 1, 1)

    def show(self, *args):
        self.show_all()

        state = 0

        if self.run() == Gtk.ResponseType.OK:
            print("Made offer to player...")
            state = 1

        self.destroy()

        return state


class TerminateContract(Gtk.MessageDialog):
    '''
    Confirmation dialog to arrange termination of a players contract.
    '''
    def __init__(self, playerid):
        player = data.players.get_player_by_id(playerid)

        payout = data.currency.get_currency(player.contract.get_termination_payout(), integer=True)

        Gtk.MessageDialog.__init__(self)
        self.set_transient_for(data.window)
        self.set_modal(True)
        self.set_title("Terminate Contract")
        self.set_property("message-type", Gtk.MessageType.QUESTION)
        self.set_markup("<span size='12000'><b>Do you wish to terminate the contract of %s?</b></span>" % (player.get_name(mode=1)))
        self.format_secondary_text("The player will be paid %s for the remainder of his contract." % (payout))
        self.add_button("_Do Not Terminate", Gtk.ResponseType.CANCEL)
        self.add_button("_Terminate Contract", Gtk.ResponseType.OK)
        self.set_default_response(Gtk.ResponseType.CANCEL)

    def show(self):
        state = 0

        if self.run() == Gtk.ResponseType.OK:
            state = 1

        self.destroy()

        return state
