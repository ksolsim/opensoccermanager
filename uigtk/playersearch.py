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
import structures.shortlist
import structures.skills
import uigtk.contextmenu
import uigtk.negotiations
import uigtk.shared
import uigtk.shortlist
import uigtk.widgets


class PlayerSearch(uigtk.widgets.Grid):
    __name__ = "playersearch"

    def __init__(self):
        uigtk.widgets.Grid.__init__(self)

        grid = uigtk.widgets.Grid()
        self.attach(grid, 0, 0, 1, 1)

        self.liststoreSearch = Gtk.ListStore(str)

        self.completionSearch = Gtk.EntryCompletion()
        self.completionSearch.set_model(self.liststoreSearch)
        self.completionSearch.set_text_column(0)

        self.entrySearch = Gtk.SearchEntry()
        self.entrySearch.set_placeholder_text("Search Players...")
        self.entrySearch.set_completion(self.completionSearch)
        key, modifier = Gtk.accelerator_parse("<Control>F")
        self.entrySearch.add_accelerator("grab-focus",
                                         data.window.accelgroup,
                                         key,
                                         modifier,
                                         Gtk.AccelFlags.VISIBLE)
        self.entrySearch.connect("activate", self.on_search_activated)
        self.entrySearch.connect("icon-press", self.on_search_pressed)
        self.entrySearch.connect("search-changed", self.on_search_changed)
        grid.attach(self.entrySearch, 0, 0, 1, 1)

        label = Gtk.Label()
        label.set_hexpand(True)
        grid.attach(label, 1, 0, 1, 1)

        self.columnviews = uigtk.shared.ColumnViews()
        self.columnviews.comboboxView.connect("changed", self.on_view_changed)
        grid.attach(self.columnviews, 2, 0, 1, 1)

        self.filterbuttons = uigtk.shared.FilterButtons()
        self.filterbuttons.buttonFilter.connect("clicked", self.on_filter_clicked)
        self.filterbuttons.buttonReset.connect("clicked", self.on_reset_clicked)
        grid.attach(self.filterbuttons, 4, 0, 1, 1)

        scrolledwindow = uigtk.widgets.ScrolledWindow()
        self.attach(scrolledwindow, 0, 1, 1, 1)

        PlayerSearch.playerlist = PlayerList()

        self.treemodelfilter = PlayerSearch.playerlist.filter_new()
        self.treemodelfilter.set_visible_func(self.filter_visible,
                                              data.players.get_players())
        self.treemodelsort = Gtk.TreeModelSort(self.treemodelfilter)
        self.treemodelsort.set_sort_column_id(16, Gtk.SortType.DESCENDING)

        self.treeview = uigtk.widgets.TreeView()
        self.treeview.set_hexpand(True)
        self.treeview.set_vexpand(True)
        self.treeview.set_headers_clickable(True)
        self.treeview.set_model(self.treemodelsort)
        self.treeview.connect("row-activated", self.on_row_activated)
        self.treeview.connect("button-release-event", self.on_button_release_event)
        self.treeview.connect("key-press-event", self.on_key_press_event)
        scrolledwindow.add(self.treeview)

        PlayerSearch.treeselection = self.treeview.get_selection()

        self.tree_columns = ([], [], [])

        # Personal
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Name", column=1)
        treeviewcolumn.set_sort_column_id(1)
        self.treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Age", column=2)
        self.treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Club", column=4)
        self.treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Nationality", column=5)
        self.treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Position", column=6)
        self.treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Value", column=17)
        treeviewcolumn.set_sort_column_id(16)
        self.tree_columns[0].append(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Wage", column=19)
        treeviewcolumn.set_sort_column_id(18)
        self.tree_columns[0].append(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Contract", column=21)
        self.tree_columns[0].append(treeviewcolumn)

        # Skills
        skills = structures.skills.Skills()

        for count, skill in enumerate(skills.get_skills(), start=7):
            label = Gtk.Label("%s" % (skill[0]))
            label.set_tooltip_text(skill[1])
            label.show()
            treeviewcolumn = uigtk.widgets.TreeViewColumn(column=count)
            treeviewcolumn.set_expand(True)
            treeviewcolumn.set_widget(label)
            self.treeview.append_column(treeviewcolumn)
            self.tree_columns[1].append(treeviewcolumn)

        # Form
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Games", column=24)
        self.tree_columns[2].append(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Goals", column=25)
        self.tree_columns[2].append(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Assists", column=26)
        self.tree_columns[2].append(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Cards", column=27)
        self.tree_columns[2].append(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="MOTM", column=28)
        self.tree_columns[2].append(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Rating", column=29)
        self.tree_columns[2].append(treeviewcolumn)

        for columns in (self.tree_columns[0], self.tree_columns[2]):
            for column in columns:
                column.set_expand(True)
                column.set_visible(False)
                self.treeview.append_column(column)

        self.contextmenu1 = uigtk.contextmenu.ContextMenu1()
        self.contextmenu2 = uigtk.contextmenu.ContextMenu2()
        self.filter_dialog = Filter()

        PlayerSearch.playerfilter = structures.filters.Player()

    def on_view_changed(self, combobox):
        '''
        Change visible columns in view.
        '''
        index = int(combobox.get_active_id())

        for count, columns in enumerate(self.tree_columns):
            for column in columns:
                column.set_visible(count == index)

    def on_key_press_event(self, widget, event):
        '''
        Key event when right-click menu is pressed on keyboard.
        '''
        if Gdk.keyval_name(event.keyval) == "Menu":
            event.button = 3
            self.on_context_menu_event(event)

    def on_button_release_event(self, treeview, event):
        '''
        Button event when right-click on mouse is made.
        '''
        if event.button == 3:
            self.on_context_menu_event(event)

    def on_context_menu_event(self, event):
        '''
        Display appropriate context menu for selected player.
        '''
        model, treeiter = self.treeselection.get_selected()

        if treeiter:
            playerid = model[treeiter][0]
            
            player = data.players.get_player_by_id(playerid)

            if data.user.club.squad.get_player_in_squad(player):
                contextmenu = self.contextmenu1
            else:
                contextmenu = self.contextmenu2

            contextmenu.player = player
            contextmenu.show()
            contextmenu.popup(None, None, None, None, event.button, event.time)

    def on_search_activated(self, entry):
        '''
        Filter for entered name in players list.
        '''
        if entry.get_text_length() > 0:
            self.reset_view()

            self.filterbuttons.buttonReset.set_sensitive(True)

            entries = [item[0] for item in self.liststoreSearch]

            search = entry.get_text()

            if search not in entries:
                self.liststoreSearch.append([search])

    def on_search_pressed(self, entry, position, event):
        '''
        Clear search entry when secondary icon is pressed.
        '''
        if position == Gtk.EntryIconPosition.SECONDARY:
            entry.set_text("")
            self.reset_view()

            self.filterbuttons.buttonReset.set_sensitive(False)

    def on_search_changed(self, entry):
        '''
        Clear filter if text length is zero.
        '''
        if entry.get_text_length() == 0:
            self.reset_view()

            self.filterbuttons.buttonReset.set_sensitive(False)

    def on_row_activated(self, treeview, treepath, treeviewcolumn):
        '''
        Launch player information screen for selected player.
        '''
        model = treeview.get_model()
        playerid = model[treepath][0]

        player = data.players.get_player_by_id(playerid)

        data.window.screen.change_visible_screen("playerinformation")
        data.window.screen.active.set_visible_player(player)

    def on_filter_clicked(self, button):
        '''
        Display filtering dialog.
        '''
        PlayerSearch.playerfilter.options = self.filter_dialog.show()

        active = PlayerSearch.playerfilter.get_filter_active()
        self.filterbuttons.buttonReset.set_sensitive(active)

        self.reset_view()

    def on_reset_clicked(self, button):
        '''
        Clear filter settings and reset view to default state.
        '''
        self.entrySearch.set_text("")
        button.set_sensitive(False)

        PlayerSearch.playerfilter.reset_filter()

        self.reset_view()

    def reset_view(self):
        '''
        Refilter tree view and highlight top row.
        '''
        self.treemodelfilter.refilter()

        if len(self.treemodelfilter) > 0:
            self.treeview.scroll_to_cell(0)
            self.treeselection.select_path(0)

    def filter_visible(self, model, treeiter, values):
        visible = True

        # Filter by search criteria
        criteria = self.entrySearch.get_text()

        for search in (model[treeiter][1],):
            search = "".join((c for c in unicodedata.normalize("NFD", search) if unicodedata.category(c) != "Mn"))

            if not re.findall(criteria, search, re.IGNORECASE):
                visible = False

        options = PlayerSearch.playerfilter.options

        # Filter user club
        if visible:
            if not options["own_players"]:
                if model[treeiter][3] == data.user.clubid:
                    visible = False

        # Filter position
        if visible:
            if options["position"] == 1:
                if model[treeiter][6] not in ("GK",):
                    visible = False
            elif options["position"] == 2:
                if model[treeiter][6] not in ("DL", "DR", "DC", "D"):
                    visible = False
            elif options["position"] == 3:
                if model[treeiter][6] not in ("ML", "MR", "MC", "M"):
                    visible = False
            elif options["position"] == 4:
                if model[treeiter][6] not in ("AF", "AS"):
                    visible = False

        # Filter age
        if visible:
            visible = options["age"][0] <= model[treeiter][2] <= options["age"][1]

        # Filter value
        if visible:
            visible = options["value"][0] <= model[treeiter][16] <= options["value"][1]

        # Filter status
        if visible:
            if options["status"] == 1:
                if not model[treeiter][22]:
                    visible = False
            if options["status"] == 2:
                if not model[treeiter][23]:
                    visible = False
            elif options["status"] == 3:
                if model[treeiter][20] != 0:
                    visible = False
            elif options["status"] == 4:
                if model[treeiter][20] > 52:
                    visible = False

        # Filter skills
        if visible:
            visible = options["keeping"][0] <= model[treeiter][7] <= options["keeping"][1]

        if visible:
            visible = options["tackling"][0] <= model[treeiter][8] <= options["tackling"][1]

        if visible:
            visible = options["passing"][0] <= model[treeiter][9] <= options["passing"][1]

        if visible:
            visible = options["shooting"][0] <= model[treeiter][10] <= options["shooting"][1]

        if visible:
            visible = options["heading"][0] <= model[treeiter][11] <= options["heading"][1]

        if visible:
            visible = options["pace"][0] <= model[treeiter][12] <= options["pace"][1]

        if visible:
            visible = options["stamina"][0] <= model[treeiter][13] <= options["stamina"][1]

        if visible:
            visible = options["ball_control"][0] <= model[treeiter][14] <= options["ball_control"][1]

        if visible:
            visible = options["set_pieces"][0] <= model[treeiter][15] <= options["set_pieces"][1]

        return visible

    def populate_data(self):
        PlayerSearch.playerlist.update()

    def run(self):
        self.populate_data()
        self.show_all()

        PlayerSearch.treeselection.select_path(0)


class PlayerList(Gtk.ListStore):
    def __init__(self):
        Gtk.ListStore.__init__(self)
        self.set_column_types([int, str, int, int, str, str, str, int, int, int,
                               int, int, int, int, int, int, int, str,int, str,
                               int, str, bool, bool, str, int, int, str, int,
                               str])

    def update(self):
        self.clear()

        for playerid, player in data.players.get_players():
            if player.club:
                clubid = player.club.clubid
                club = player.club.name
            else:
                clubid = None
                club = ""

            self.append([playerid,
                         player.get_name(),
                         player.get_age(),
                         clubid,
                         club,
                         player.nationality.name,
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
                         player.value.get_value(),
                         player.value.get_value_as_string(),
                         player.wage.get_wage(),
                         player.wage.get_wage_as_string(),
                         player.contract.contract,
                         player.contract.get_contract(),
                         data.purchase_list.get_player_listed(player),
                         data.loan_list.get_player_listed(player),
                         player.get_appearances(),
                         player.goals,
                         player.assists,
                         player.get_cards(),
                         player.man_of_the_match,
                         player.rating.get_average_rating()])


class Filter(Gtk.Dialog):
    class Attributes(Gtk.Grid):
        def __init__(self):
            Gtk.Grid.__init__(self)
            self.set_column_spacing(5)

            self.minimum = Gtk.SpinButton.new_with_range(0, 99, 1)
            self.minimum.connect("value-changed", self.on_minimum_changed)
            self.attach(self.minimum, 0, 0, 1, 1)

            self.maximum = Gtk.SpinButton.new_with_range(0, 99, 1)
            self.maximum.set_value(99)
            self.attach(self.maximum, 1, 0, 1, 1)

        def on_minimum_changed(self, spinbutton):
            '''
            Update minimum value permitted in maximum spin button.
            '''
            minimum = spinbutton.get_value_as_int()
            maximum = spinbutton.get_range()[1]
            self.maximum.set_range(minimum, maximum)

        def set_values(self, values):
            '''
            Set minimum and maximum values for skills.
            '''
            self.minimum.set_value(values[0])
            self.maximum.set_value(values[1])

        def get_values(self):
            '''
            Return list of minimum and maximum values.
            '''
            minimum = self.minimum.get_value_as_int()
            maximum = self.maximum.get_value_as_int()

            return [minimum, maximum]

    def __init__(self, *args):
        Gtk.Dialog.__init__(self)
        self.set_transient_for(data.window)
        self.set_modal(True)
        self.set_resizable(False)
        self.set_title("Filter Players")
        self.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("_Filter", Gtk.ResponseType.OK)
        self.set_default_response(Gtk.ResponseType.OK)
        self.vbox.set_border_width(5)
        self.vbox.set_spacing(5)

        self.checkbuttonShowOwnPlayers = uigtk.widgets.CheckButton()
        self.checkbuttonShowOwnPlayers.set_label("Display %s Players In Search Results" % (data.user.club.name))
        self.vbox.add(self.checkbuttonShowOwnPlayers)

        frame = uigtk.widgets.CommonFrame("Personal")
        self.vbox.pack_start(frame, True, True, 0)

        label = uigtk.widgets.Label("_Position", leftalign=True)
        frame.grid.attach(label, 0, 0, 1, 1)
        self.comboboxPosition = Gtk.ComboBoxText()
        self.comboboxPosition.append("0", "All")
        self.comboboxPosition.append("1", "Goalkeeper")
        self.comboboxPosition.append("2", "Defender")
        self.comboboxPosition.append("3", "Midfielder")
        self.comboboxPosition.append("4", "Attacker")
        label.set_mnemonic_widget(self.comboboxPosition)
        frame.grid.attach(self.comboboxPosition, 1, 0, 1, 1)

        label = uigtk.widgets.Label("_Age", leftalign=True)
        frame.grid.attach(label, 0, 1, 1, 1)
        self.spinbuttonAgeMinimum = Gtk.SpinButton.new_with_range(16, 50, 1)
        self.spinbuttonAgeMinimum.connect("value-changed", self.on_age_changed)
        label.set_mnemonic_widget(self.spinbuttonAgeMinimum)
        frame.grid.attach(self.spinbuttonAgeMinimum, 1, 1, 1, 1)
        self.spinbuttonAgeMaximum = Gtk.SpinButton.new_with_range(16, 50, 1)
        frame.grid.attach(self.spinbuttonAgeMaximum, 2, 1, 1, 1)

        label = uigtk.widgets.Label("_Value", leftalign=True)
        frame.grid.attach(label, 0, 2, 1, 1)
        self.spinbuttonValueMinimum = Gtk.SpinButton.new_with_range(0, 100000000, 100000)
        self.spinbuttonValueMinimum.connect("value-changed", self.on_value_changed)
        label.set_mnemonic_widget(self.spinbuttonValueMinimum)
        frame.grid.attach(self.spinbuttonValueMinimum, 1, 2, 1, 1)
        self.spinbuttonValueMaximum = Gtk.SpinButton.new_with_range(0, 100000000, 100000)
        frame.grid.attach(self.spinbuttonValueMaximum, 2, 2, 1, 1)

        label = uigtk.widgets.Label("_Status", leftalign=True)
        frame.grid.attach(label, 0, 3, 1, 1)
        self.comboboxStatus = Gtk.ComboBoxText()
        self.comboboxStatus.append("0", "All Players")
        self.comboboxStatus.append("1", "Available for Purchase")
        self.comboboxStatus.append("2", "Available for Loan")
        self.comboboxStatus.append("3", "Out of Contract")
        self.comboboxStatus.append("4", "One Year or Less Remaining on Contract")
        label.set_mnemonic_widget(self.comboboxStatus)
        frame.grid.attach(self.comboboxStatus, 1, 3, 3, 1)

        frame = uigtk.widgets.CommonFrame("Skills")
        self.vbox.pack_start(frame, True, True, 0)

        label = uigtk.widgets.Label("_Keeping", leftalign=True)
        frame.grid.attach(label, 0, 0, 1, 1)
        self.keeping = self.Attributes()
        label.set_mnemonic_widget(self.keeping.minimum)
        frame.grid.attach(self.keeping, 1, 0, 1, 1)
        label = uigtk.widgets.Label("_Tackling", leftalign=True)
        frame.grid.attach(label, 0, 1, 1, 1)
        self.tackling = self.Attributes()
        label.set_mnemonic_widget(self.tackling.minimum)
        frame.grid.attach(self.tackling, 1, 1, 1, 1)
        label = uigtk.widgets.Label("_Passing", leftalign=True)
        frame.grid.attach(label, 0, 2, 1, 1)
        self.passing = self.Attributes()
        label.set_mnemonic_widget(self.passing.minimum)
        frame.grid.attach(self.passing, 1, 2, 1, 1)
        label = uigtk.widgets.Label("_Shooting", leftalign=True)
        frame.grid.attach(label, 2, 0, 1, 1)
        self.shooting = self.Attributes()
        label.set_mnemonic_widget(self.shooting.minimum)
        frame.grid.attach(self.shooting, 3, 0, 1, 1)
        label = uigtk.widgets.Label("_Pace", leftalign=True)
        frame.grid.attach(label, 2, 1, 1, 1)
        self.pace = self.Attributes()
        label.set_mnemonic_widget(self.pace.minimum)
        frame.grid.attach(self.pace, 3, 1, 1, 1)
        label = uigtk.widgets.Label("_Heading", leftalign=True)
        frame.grid.attach(label, 2, 2, 1, 1)
        self.heading = self.Attributes()
        label.set_mnemonic_widget(self.heading.minimum)
        frame.grid.attach(self.heading, 3, 2, 1, 1)
        label = uigtk.widgets.Label("_Stamina", leftalign=True)
        frame.grid.attach(label, 4, 0, 1, 1)
        self.stamina = self.Attributes()
        label.set_mnemonic_widget(self.stamina.minimum)
        frame.grid.attach(self.stamina, 5, 0, 1, 1)
        label = uigtk.widgets.Label("_Ball Control", leftalign=True)
        frame.grid.attach(label, 4, 1, 1, 1)
        self.ball_control = self.Attributes()
        label.set_mnemonic_widget(self.ball_control.minimum)
        frame.grid.attach(self.ball_control, 5, 1, 1, 1)
        label = uigtk.widgets.Label("_Set Pieces", leftalign=True)
        frame.grid.attach(label, 4, 2, 1, 1)
        self.set_pieces = self.Attributes()
        label.set_mnemonic_widget(self.set_pieces.minimum)
        frame.grid.attach(self.set_pieces, 5, 2, 1, 1)

    def on_age_changed(self, spinbutton):
        '''
        Update age ranges on change of minimum age amount.
        '''
        minimum = spinbutton.get_value_as_int()
        maximum = spinbutton.get_range()[1]
        self.spinbuttonAgeMaximum.set_range(minimum, maximum)

    def on_value_changed(self, spinbutton):
        '''
        Update value ranges on change of minimum value amount.
        '''
        minimum = spinbutton.get_value_as_int()
        maximum = spinbutton.get_range()[1]
        self.spinbuttonValueMaximum.set_range(minimum, maximum)

    def show(self):
        self.show_all()

        options = PlayerSearch.playerfilter.options

        self.checkbuttonShowOwnPlayers.set_active(options["own_players"])
        self.comboboxPosition.set_active_id(str(options["position"]))
        self.spinbuttonAgeMinimum.set_value(options["age"][0])
        self.spinbuttonAgeMaximum.set_value(options["age"][1])
        self.spinbuttonValueMinimum.set_value(options["value"][0])
        self.spinbuttonValueMaximum.set_value(options["value"][1])
        self.comboboxStatus.set_active_id(str(options["status"]))
        self.keeping.set_values(options["keeping"])
        self.tackling.set_values(options["tackling"])
        self.passing.set_values(options["passing"])
        self.shooting.set_values(options["shooting"])
        self.heading.set_values(options["heading"])
        self.pace.set_values(options["pace"])
        self.stamina.set_values(options["stamina"])
        self.ball_control.set_values(options["ball_control"])
        self.set_pieces.set_values(options["set_pieces"])

        if self.run() == Gtk.ResponseType.OK:
            options["own_players"] = self.checkbuttonShowOwnPlayers.get_active()
            options["position"] = int(self.comboboxPosition.get_active_id())
            options["age"] = [self.spinbuttonAgeMinimum.get_value_as_int(),
                              self.spinbuttonAgeMaximum.get_value_as_int()]
            options["value"] = [self.spinbuttonValueMinimum.get_value_as_int(),
                                self.spinbuttonValueMaximum.get_value_as_int()]
            options["status"] = int(self.comboboxStatus.get_active_id())
            options["keeping"] = self.keeping.get_values()
            options["tackling"] = self.tackling.get_values()
            options["passing"] = self.passing.get_values()
            options["shooting"] = self.shooting.get_values()
            options["pace"] = self.pace.get_values()
            options["heading"] = self.heading.get_values()
            options["stamina"] = self.stamina.get_values()
            options["ball_control"] = self.ball_control.get_values()
            options["set_pieces"] = self.set_pieces.get_values()

        self.hide()

        return options
