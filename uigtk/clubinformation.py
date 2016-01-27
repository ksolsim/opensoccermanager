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

        self.liststore = Gtk.ListStore(int, str, str, str, str, int, int, int,
                                       int, int, int, int, int, int)

        treemodelsort = Gtk.TreeModelSort(self.liststore)
        treemodelsort.set_sort_column_id(1, Gtk.SortType.ASCENDING)

        treeview = uigtk.widgets.TreeView()
        treeview.set_vexpand(True)
        treeview.set_hexpand(True)
        treeview.set_model(treemodelsort)
        treeview.connect("row-activated", self.on_row_activated)
        treeview.connect("button-release-event", self.on_button_release_event)
        scrolledwindow.add(treeview)

        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Name", column=1)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Position", column=2)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Value", column=3)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Wage", column=4)
        treeview.append_column(treeviewcolumn)

        skills = structures.skills.Skills()

        for count, skill in enumerate(skills.get_skills(), start=5):
            label = Gtk.Label("%s" % (skill[0]))
            label.set_tooltip_text(skill[1])
            label.show()
            treeviewcolumn = uigtk.widgets.TreeViewColumn(column=count)
            treeviewcolumn.set_widget(label)
            treeviewcolumn.set_expand(True)
            treeview.append_column(treeviewcolumn)

        frame = uigtk.widgets.CommonFrame("Form")
        self.attach(frame, 1, 2, 1, 1)

        scrolledwindow = uigtk.widgets.ScrolledWindow()
        frame.grid.attach(scrolledwindow, 0, 0, 1, 1)

        treeviewForm = uigtk.widgets.TreeView()
        treeviewForm.set_hexpand(True)
        scrolledwindow.add(treeviewForm)

        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Season")
        treeviewForm.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Position")
        treeviewForm.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Wins")
        treeviewForm.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Draws")
        treeviewForm.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Losses")
        treeviewForm.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="GF")
        treeviewForm.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="GA")
        treeviewForm.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="GD")
        treeviewForm.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Points")
        treeviewForm.append_column(treeviewcolumn)

        self.number = structures.number.Number()

        self.contextmenu1 = uigtk.playersearch.ContextMenu1()
        self.contextmenu2 = uigtk.playersearch.ContextMenu2()

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

        data.window.screen.change_visible_screen("playerinformation")
        data.window.screen.active.set_visible_player(playerid)

    def on_button_release_event(self, treeview, event):
        if event.button == 3:
            model, treeiter = treeview.treeselection.get_selected()
            playerid = model[treeiter][0]
            player = data.players.get_player_by_id(playerid)
            club = data.clubs.get_club_by_id(data.user.team)

            if playerid in club.squad.get_squad():
                contextmenu = self.contextmenu1
            else:
                contextmenu = self.contextmenu2

            contextmenu.playerid = playerid
            contextmenu.show()
            contextmenu.popup(None, None, None, None, event.button, event.time)

    def set_visible_club(self, clubid):
        '''
        Update the display with the visible club for given id.
        '''
        club = data.clubs.get_club_by_id(clubid)
        stadium = data.stadiums.get_stadium_by_id(club.stadium)
        league = data.leagues.get_league_by_id(club.league)

        position = league.standings.get_position_for_club(clubid)

        self.labelName.set_label("<span size='24000'><b>%s</b></span>" % (club.name))
        self.labelNickname.set_label(club.nickname)
        self.labelManager.set_label(club.manager)
        self.labelChairman.set_label(club.chairman)
        self.labelStadiumName.set_label(stadium.name)
        self.labelStadiumCapacity.set_label("%i" % (stadium.get_capacity()))
        self.labelLeagueName.set_label(league.name)
        self.labelLeaguePosition.set_label(self.number.get_ordinal_number(position))
        self.labelPlayerCount.set_label("%i" % (club.squad.get_squad_count()))
        self.labelAverageAge.set_label("%.1f" % (club.squad.get_average_age()))
        self.labelSquadValue.set_label(data.currency.get_rounded_amount(club.get_total_value()))
        self.labelWeeklyWage.set_label(data.currency.get_rounded_amount(club.get_total_wage()))

        self.liststore.clear()

        for playerid, player in club.squad.get_squad():
            self.liststore.append([playerid,
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

    def run(self):
        self.show_all()


class ContextMenu(uigtk.playersearch.ContextMenu2):
    def __init__(self):
        uigtk.playersearch.ContextMenu2.__init__(self)
