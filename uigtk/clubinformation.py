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

import data
import structures.number
import structures.skills
import uigtk.playersearch
import uigtk.widgets


class ClubInformation(uigtk.widgets.Grid):
    __name__ = "clubinformation"

    def __init__(self):
        uigtk.widgets.Grid.__init__(self)

        self.labelName = Gtk.Label()
        self.labelName.set_hexpand(True)
        self.labelName.set_use_markup(True)
        self.attach(self.labelName, 0, 0, 2, 1)

        buttonbox = uigtk.widgets.ButtonBox()
        buttonbox.set_layout(Gtk.ButtonBoxStyle.END)
        self.attach(buttonbox, 1, 0, 1, 1)
        buttonBack = uigtk.widgets.Button("_Back")
        buttonBack.set_tooltip_text("Return to previously visible screen.")
        buttonBack.connect("clicked", self.on_back_clicked)
        buttonbox.add(buttonBack)

        sizegroup = Gtk.SizeGroup()
        sizegroup.set_mode(Gtk.SizeGroupMode.HORIZONTAL)

        grid = uigtk.widgets.Grid()
        self.attach(grid, 0, 1, 1, 2)

        frame = uigtk.widgets.CommonFrame("Details")
        grid.attach(frame, 0, 0, 1, 1)

        label = uigtk.widgets.Label("Nickname", leftalign=True)
        sizegroup.add_widget(label)
        frame.grid.attach(label, 0, 0, 1, 1)
        self.labelNickname = uigtk.widgets.Label(leftalign=True)
        frame.grid.attach(self.labelNickname, 1, 0, 1, 1)
        label = uigtk.widgets.Label("Manager", leftalign=True)
        sizegroup.add_widget(label)
        frame.grid.attach(label, 0, 1, 1, 1)
        self.labelManager = uigtk.widgets.Label(leftalign=True)
        frame.grid.attach(self.labelManager, 1, 1, 1, 1)
        label = uigtk.widgets.Label("Chairman", leftalign=True)
        sizegroup.add_widget(label)
        frame.grid.attach(label, 0, 2, 1, 1)
        self.labelChairman = uigtk.widgets.Label(leftalign=True)
        frame.grid.attach(self.labelChairman, 1, 2, 1, 1)

        frame = uigtk.widgets.CommonFrame("Stadium")
        grid.attach(frame, 0, 1, 1, 1)

        label = uigtk.widgets.Label("Name", leftalign=True)
        sizegroup.add_widget(label)
        frame.grid.attach(label, 0, 0, 1, 1)
        self.labelStadiumName = uigtk.widgets.Label(leftalign=True)
        frame.grid.attach(self.labelStadiumName, 1, 0, 1, 1)
        label = uigtk.widgets.Label("Capacity", leftalign=True)
        sizegroup.add_widget(label)
        frame.grid.attach(label, 0, 1, 1, 1)
        self.labelStadiumCapacity = uigtk.widgets.Label(leftalign=True)
        frame.grid.attach(self.labelStadiumCapacity, 1, 1, 1, 1)

        frame = uigtk.widgets.CommonFrame("League")
        grid.attach(frame, 0, 2, 1, 1)

        label = uigtk.widgets.Label("Name", leftalign=True)
        sizegroup.add_widget(label)
        frame.grid.attach(label, 0, 0, 1, 1)
        self.labelLeagueName = uigtk.widgets.Label(leftalign=True)
        frame.grid.attach(self.labelLeagueName, 1, 0, 1, 1)
        label = uigtk.widgets.Label("Position", leftalign=True)
        sizegroup.add_widget(label)
        frame.grid.attach(label, 0, 1, 1, 1)
        self.labelLeaguePosition = uigtk.widgets.Label(leftalign=True)
        frame.grid.attach(self.labelLeaguePosition, 1, 1, 1, 1)

        frame = uigtk.widgets.CommonFrame("Statistics")
        grid.attach(frame, 0, 3, 1, 1)

        label = uigtk.widgets.Label("Player Count", leftalign=True)
        sizegroup.add_widget(label)
        frame.grid.attach(label, 0, 0, 1, 1)
        self.labelPlayerCount = uigtk.widgets.Label(leftalign=True)
        frame.grid.attach(self.labelPlayerCount, 1, 0, 1, 1)
        label = uigtk.widgets.Label("Average Age", leftalign=True)
        sizegroup.add_widget(label)
        frame.grid.attach(label, 0, 1, 1, 1)
        self.labelAverageAge = uigtk.widgets.Label(leftalign=True)
        frame.grid.attach(self.labelAverageAge, 1, 1, 1, 1)
        label = uigtk.widgets.Label("Total Value", leftalign=True)
        sizegroup.add_widget(label)
        frame.grid.attach(label, 0, 2, 1, 1)
        self.labelSquadValue = uigtk.widgets.Label(leftalign=True)
        frame.grid.attach(self.labelSquadValue, 1, 2, 1, 1)
        label = uigtk.widgets.Label("Total Wage", leftalign=True)
        sizegroup.add_widget(label)
        frame.grid.attach(label, 0, 3, 1, 1)
        self.labelWeeklyWage = uigtk.widgets.Label(leftalign=True)
        frame.grid.attach(self.labelWeeklyWage, 1, 3, 1, 1)

        frame = uigtk.widgets.CommonFrame("Squad")
        self.attach(frame, 1, 1, 1, 1)

        scrolledwindow = uigtk.widgets.ScrolledWindow()
        frame.grid.attach(scrolledwindow, 0, 0, 1, 1)

        self.liststoreSquad = Gtk.ListStore(int, str, str, str, str, int, int,
                                            int, int, int, int, int, int, int)
        treemodelsort = Gtk.TreeModelSort(self.liststoreSquad)
        treemodelsort.set_sort_column_id(1, Gtk.SortType.ASCENDING)

        self.treeview = uigtk.widgets.TreeView()
        self.treeview.set_vexpand(True)
        self.treeview.set_hexpand(True)
        self.treeview.set_model(treemodelsort)
        self.treeview.connect("row-activated", self.on_row_activated)
        self.treeview.connect("button-release-event", self.on_button_release_event)
        self.treeview.connect("key-press-event", self.on_key_press_event)
        scrolledwindow.add(self.treeview)

        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Name", column=1)
        self.treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Position", column=2)
        self.treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Value", column=3)
        self.treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Wage", column=4)
        self.treeview.append_column(treeviewcolumn)

        skills = structures.skills.Skills()

        for count, skill in enumerate(skills.get_skills(), start=5):
            label = Gtk.Label("%s" % (skill[0]))
            label.set_tooltip_text(skill[1])
            label.show()
            treeviewcolumn = uigtk.widgets.TreeViewColumn(column=count)
            treeviewcolumn.set_widget(label)
            treeviewcolumn.set_expand(True)
            self.treeview.append_column(treeviewcolumn)

        frame = uigtk.widgets.CommonFrame("History")
        self.attach(frame, 1, 2, 1, 1)

        scrolledwindow = uigtk.widgets.ScrolledWindow()
        scrolledwindow.set_size_request(-1, 75)
        frame.grid.attach(scrolledwindow, 0, 0, 1, 1)

        self.liststoreHistory = Gtk.ListStore(str, str, int, int, int, int, int, int, int)

        treeviewHistory = uigtk.widgets.TreeView()
        treeviewHistory.set_hexpand(True)
        treeviewHistory.set_model(self.liststoreHistory)
        scrolledwindow.add(treeviewHistory)

        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Season", column=0)
        treeviewHistory.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Position", column=1)
        treeviewcolumn.set_fixed_width(75)
        treeviewHistory.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Wins", column=2)
        treeviewcolumn.set_fixed_width(50)
        treeviewHistory.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Draws", column=3)
        treeviewcolumn.set_fixed_width(50)
        treeviewHistory.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Losses", column=4)
        treeviewcolumn.set_fixed_width(50)
        treeviewHistory.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="GF",
                                                      tooltip="Goals For",
                                                      column=5)
        treeviewcolumn.set_fixed_width(50)
        treeviewHistory.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="GA",
                                                      tooltip="Goals Against",
                                                      column=6)
        treeviewcolumn.set_fixed_width(50)
        treeviewHistory.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="GD",
                                                      tooltip="Goal Difference",
                                                      column=7)
        treeviewcolumn.set_fixed_width(50)
        treeviewHistory.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Points", column=8)
        treeviewcolumn.set_fixed_width(50)
        treeviewHistory.append_column(treeviewcolumn)

        self.contextmenu1 = uigtk.contextmenu.ContextMenu1()
        self.contextmenu2 = uigtk.contextmenu.ContextMenu2()

    def on_back_clicked(self, *args):
        '''
        Return to previous screen when back button is clicked.
        '''
        data.window.screen.return_previous_screen()

    def on_row_activated(self, treeview, treepath, treeviewcolumn):
        '''
        Launch player information screen for selected player.
        '''
        model = treeview.get_model()
        playerid = model[treepath][0]

        player = data.players.get_player_by_id(playerid)

        data.window.screen.change_visible_screen("playerinformation", player=player)

    def on_button_release_event(self, treeview, event):
        '''
        Handle right-clicking on the treeview.
        '''
        if event.button == 3:
            self.on_context_menu_event(event)

    def on_key_press_event(self, treeview, event):
        '''
        Handle button clicks on the treeview.
        '''
        if Gdk.keyval_name(event.keyval) == "Menu":
            event.button = 3
            self.on_context_menu_event(event)

    def on_context_menu_event(self, event):
        '''
        Display context menu for selected player.
        '''
        model, treeiter = self.treeview.treeselection.get_selected()

        if treeiter:
            playerid = model[treeiter][0]

            player = data.players.get_player_by_id(playerid)

            if self.club == data.user.club:
                contextmenu = self.contextmenu1
            else:
                contextmenu = self.contextmenu2

            contextmenu.player = player
            contextmenu.show()
            contextmenu.popup(None, None, None, None, event.button, event.time)

    def set_visible_club(self, club):
        '''
        Update the display with the visible club for given id.
        '''
        self.club = club

        self.labelName.set_label("<span size='24000'><b>%s</b></span>" % (self.club.name))
        self.labelNickname.set_label(self.club.nickname)
        self.labelManager.set_label(self.club.manager)
        self.labelChairman.set_label(self.club.chairman)
        self.labelStadiumName.set_label(self.club.stadium.name)
        self.labelStadiumCapacity.set_label("%i" % (self.club.stadium.get_capacity()))
        self.labelLeagueName.set_label(self.club.league.name)
        self.labelLeaguePosition.set_label(self.club.league.standings.get_position_for_club(self.club.clubid))
        self.labelPlayerCount.set_label("%i" % (self.club.squad.get_squad_count()))
        self.labelAverageAge.set_label("%.1f" % (self.club.squad.get_average_age()))
        self.labelSquadValue.set_label(data.currency.get_rounded_amount(self.club.get_total_value()))
        self.labelWeeklyWage.set_label(data.currency.get_rounded_amount(self.club.get_total_wage()))

        self.liststoreSquad.clear()

        for playerid, player in self.club.squad.get_squad():
            self.liststoreSquad.append([playerid,
                                        player.get_name(),
                                        player.position,
                                        player.value.get_value_as_string(),
                                        player.wage.get_wage_as_string(),
                                        player.keeping,
                                        player.tackling,
                                        player.passing,
                                        player.shooting,
                                        player.heading,
                                        player.pace,
                                        player.stamina,
                                        player.ball_control,
                                        player.set_pieces])

        self.liststoreHistory.clear()

        self.liststoreHistory.insert(0, self.club.history.get_current_history())

    def run(self):
        if "club" in self.kwargs:
            ClubInformation.club = self.kwargs["club"]
            self.set_visible_club(ClubInformation.club)

            self.show_all()
