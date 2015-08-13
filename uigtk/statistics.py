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
import statistics

import game
import widgets


class Statistics(Gtk.Grid):
    __name__ = "statistics"

    class TreeView(Gtk.TreeView):
        def __init__(self):
            Gtk.TreeView.__init__(self)
            self.set_hexpand(True)
            self.set_fixed_height_mode(True)
            self.set_enable_search(False)
            self.set_search_column(-1)

            treeviewcolumn = widgets.TreeViewColumn(title="Season", column=0)
            treeviewcolumn.set_fixed_width(75)
            treeviewcolumn.set_sizing(Gtk.TreeViewColumnSizing.FIXED)
            self.append_column(treeviewcolumn)
            treeviewcolumn = widgets.TreeViewColumn(title="Played", column=1)
            treeviewcolumn.set_fixed_width(50)
            treeviewcolumn.set_sizing(Gtk.TreeViewColumnSizing.FIXED)
            self.append_column(treeviewcolumn)
            treeviewcolumn = widgets.TreeViewColumn(title="Won", column=2)
            treeviewcolumn.set_fixed_width(50)
            treeviewcolumn.set_sizing(Gtk.TreeViewColumnSizing.FIXED)
            self.append_column(treeviewcolumn)
            treeviewcolumn = widgets.TreeViewColumn(title="Drawn", column=3)
            treeviewcolumn.set_fixed_width(50)
            treeviewcolumn.set_sizing(Gtk.TreeViewColumnSizing.FIXED)
            self.append_column(treeviewcolumn)
            treeviewcolumn = widgets.TreeViewColumn(title="Lost", column=4)
            treeviewcolumn.set_fixed_width(50)
            treeviewcolumn.set_sizing(Gtk.TreeViewColumnSizing.FIXED)
            self.append_column(treeviewcolumn)
            treeviewcolumn = widgets.TreeViewColumn(title="Goals For", column=5)
            treeviewcolumn.set_fixed_width(100)
            treeviewcolumn.set_sizing(Gtk.TreeViewColumnSizing.FIXED)
            self.append_column(treeviewcolumn)
            treeviewcolumn = widgets.TreeViewColumn(title="Goals Against", column=6)
            treeviewcolumn.set_fixed_width(100)
            treeviewcolumn.set_sizing(Gtk.TreeViewColumnSizing.FIXED)
            self.append_column(treeviewcolumn)
            treeviewcolumn = widgets.TreeViewColumn(title="Goal Difference", column=7)
            treeviewcolumn.set_fixed_width(100)
            treeviewcolumn.set_sizing(Gtk.TreeViewColumnSizing.FIXED)
            self.append_column(treeviewcolumn)
            treeviewcolumn = widgets.TreeViewColumn(title="Points", column=8)
            treeviewcolumn.set_fixed_width(50)
            treeviewcolumn.set_sizing(Gtk.TreeViewColumnSizing.FIXED)
            self.append_column(treeviewcolumn)
            treeviewcolumn = widgets.TreeViewColumn(title="Position", column=9)
            treeviewcolumn.set_sizing(Gtk.TreeViewColumnSizing.FIXED)
            self.append_column(treeviewcolumn)

    def __init__(self):
        Gtk.Grid.__init__(self)
        self.set_row_spacing(5)
        self.set_column_spacing(5)

        commonframe = widgets.CommonFrame("Games")
        self.attach(commonframe, 0, 0, 1, 1)

        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)
        commonframe.insert(grid)

        label = widgets.AlignedLabel("Largest Win")
        grid.attach(label, 0, 0, 1, 1)
        self.labelWin = widgets.AlignedLabel()
        grid.attach(self.labelWin, 1, 0, 1, 1)
        label = widgets.AlignedLabel("Largest Loss")
        grid.attach(label, 0, 1, 1, 1)
        self.labelLoss = widgets.AlignedLabel()
        grid.attach(self.labelLoss, 1, 1, 1, 1)

        commonframe = widgets.CommonFrame("Goals")
        self.attach(commonframe, 0, 1, 1, 1)

        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)
        commonframe.insert(grid)

        label = widgets.AlignedLabel("Leading Goalscorer")
        grid.attach(label, 0, 0, 1, 1)
        self.labelGoalscorer = widgets.AlignedLabel()
        grid.attach(self.labelGoalscorer, 1, 0, 1, 1)
        label = widgets.AlignedLabel("Leading Assister")
        grid.attach(label, 0, 1, 1, 1)
        self.labelAssister = widgets.AlignedLabel()
        grid.attach(self.labelAssister, 1, 1, 1, 1)

        commonframe = widgets.CommonFrame("Cards")
        self.attach(commonframe, 1, 0, 1, 1)

        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)
        commonframe.insert(grid)

        label = widgets.AlignedLabel("Yellow Cards")
        grid.attach(label, 0, 0, 1, 1)
        self.labelYellowCards = widgets.AlignedLabel()
        grid.attach(self.labelYellowCards, 1, 0, 1, 1)
        label = widgets.AlignedLabel("Red Cards")
        grid.attach(label, 0, 1, 1, 1)
        self.labelRedCards = widgets.AlignedLabel()
        grid.attach(self.labelRedCards, 1, 1, 1, 1)

        commonframe = widgets.CommonFrame("Stadium")
        self.attach(commonframe, 1, 1, 1, 1)

        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)
        commonframe.insert(grid)

        label = widgets.AlignedLabel("Highest Attendance")
        grid.attach(label, 0, 0, 1, 1)
        self.labelHighAttendance = widgets.AlignedLabel()
        grid.attach(self.labelHighAttendance, 1, 0, 1, 1)
        label = widgets.AlignedLabel("Lowest Attendance")
        grid.attach(label, 0, 1, 1, 1)
        self.labelLowAttendance = widgets.AlignedLabel()
        grid.attach(self.labelLowAttendance, 1, 1, 1, 1)
        label = widgets.AlignedLabel("Average Attendance")
        grid.attach(label, 0, 2, 1, 1)
        self.labelAverageAttendance = widgets.AlignedLabel()
        grid.attach(self.labelAverageAttendance, 1, 2, 1, 1)

        commonframe = widgets.CommonFrame("Salary")
        self.attach(commonframe, 2, 0, 1, 1)

        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)
        commonframe.insert(grid)

        label = widgets.AlignedLabel("Highest Salary")
        grid.attach(label, 0, 0, 1, 1)
        self.labelHighSalary = widgets.AlignedLabel()
        grid.attach(self.labelHighSalary, 1, 0, 1, 1)
        label = widgets.AlignedLabel("Lowest Salary")
        grid.attach(label, 0, 1, 1, 1)
        self.labelLowSalary = widgets.AlignedLabel()
        grid.attach(self.labelLowSalary, 1, 1, 1, 1)
        label = widgets.AlignedLabel("Average Salary")
        grid.attach(label, 0, 2, 1, 1)
        self.labelAvgSalary = widgets.AlignedLabel()
        grid.attach(self.labelAvgSalary, 1, 2, 1, 1)

        commonframe = widgets.CommonFrame("Value")
        self.attach(commonframe, 2, 1, 1, 1)

        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)
        commonframe.insert(grid)

        label = widgets.AlignedLabel("Highest Value")
        grid.attach(label, 0, 0, 1, 1)
        self.labelHighValue = widgets.AlignedLabel()
        grid.attach(self.labelHighValue, 1, 0, 1, 1)
        label = widgets.AlignedLabel("Lowest Value")
        grid.attach(label, 0, 1, 1, 1)
        self.labelLowValue = widgets.AlignedLabel()
        grid.attach(self.labelLowValue, 1, 1, 1, 1)
        label = widgets.AlignedLabel("Average Value")
        grid.attach(label, 0, 2, 1, 1)
        self.labelAvgValue = widgets.AlignedLabel()
        grid.attach(self.labelAvgValue, 1, 2, 1, 1)

        self.liststoreRecordCurrent = Gtk.ListStore(str, int, int, int, int, int, int, int, int, str)
        self.liststoreRecordPrevious = Gtk.ListStore(str, int, int, int, int, int, int, int, int, str)

        commonframe = widgets.CommonFrame("Current League Record")
        self.attach(commonframe, 0, 2, 3, 1)

        treeview = self.TreeView()
        treeview.set_model(self.liststoreRecordCurrent)
        treeselection = treeview.get_selection()
        treeselection.set_mode(Gtk.SelectionMode.NONE)
        commonframe.insert(treeview)

        commonframe = widgets.CommonFrame("Previous League Record")
        self.attach(commonframe, 0, 3, 3, 1)

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)
        commonframe.insert(scrolledwindow)

        treeview = self.TreeView()
        treeview.set_model(self.liststoreRecordPrevious)
        treeselection = treeview.get_selection()
        treeselection.set_mode(Gtk.SelectionMode.NONE)
        scrolledwindow.add(treeview)

    def run(self):
        self.show_all()

        # Display current season record
        self.liststoreRecordCurrent.clear()

        club = game.clubs[game.teamid]
        league = game.leagues[club.league]

        position = league.standings.find_position(game.teamid)
        position = display.format_position(position)
        season = game.date.get_season()

        details = league.standings.clubs[game.teamid]

        record = (season,
                  details.played,
                  details.wins,
                  details.draws,
                  details.losses,
                  details.goals_for,
                  details.goals_against,
                  details.goal_difference,
                  details.points,
                  position
                 )

        self.liststoreRecordCurrent.insert(0, record)

        # Display previous seasons records
        self.liststoreRecordPrevious.clear()

        for item in game.statistics.record:
            self.liststoreRecordPrevious.append(item)

        # Highest win / loss
        if game.statistics.win != (None, ()):
            clubid = game.statistics.win[0]
            opposition = game.clubs[clubid].name
            self.labelWin.set_label("%i - %i (against %s)" % (game.statistics.win[1][0],
                                                              game.statistics.win[1][1],
                                                              opposition)
                                   )
        else:
            self.labelWin.set_label("-")

        if game.statistics.loss != (None, ()):
            clubid = game.statistics.loss[0]
            opposition = game.clubs[clubid].name
            self.labelLoss.set_label("%i - %i (against %s)" % (game.statistics.loss[1][0],
                                                               game.statistics.loss[1][1],
                                                               opposition)
                                    )
        else:
            self.labelLoss.set_label("-")

        # Top goalscorer
        top = [0, 0]

        for playerid in game.clubs[game.teamid].squad:
            player = game.players[playerid]

            if player.goals > top[1]:
                top[0] = playerid
                top[1] = player.goals

        if top[0] != 0:
            player = game.players[top[0]]
            name = player.get_name(mode=1)
            self.labelGoalscorer.set_label("%s (%i goals)" % (name, top[1]))
        else:
            self.labelGoalscorer.set_label("-")

        # Top assister
        top = [0, 0]

        for playerid in game.clubs[game.teamid].squad:
            player = game.players[playerid]

            if player.assists > top[1]:
                top[0] = playerid
                top[1] = player.assists

        if top[0] != 0:
            player = game.players[top[0]]
            name = player.get_name(mode=1)
            self.labelAssister.set_label("%s (%i assists)" % (name, top[1]))
        else:
            self.labelAssister.set_label("-")

        # Highest wage / player value
        wage = [game.players[key].wage for key in game.clubs[game.teamid].squad]
        value = [game.players[key].value for key in game.clubs[game.teamid].squad]

        maximum = display.currency(max(wage))
        self.labelHighSalary.set_label("%s" % (maximum))
        minimum = display.currency(min(wage))
        self.labelLowSalary.set_label("%s" % (minimum))
        average = display.currency(statistics.mean(wage))
        self.labelAvgSalary.set_label("%s" % (average))

        maximum = display.currency(max(value))
        self.labelHighValue.set_label("%s" % (maximum))
        minimum = display.currency(min(value))
        self.labelLowValue.set_label("%s" % (minimum))
        average = display.currency(statistics.mean(value))
        self.labelAvgValue.set_label("%s" % (average))

        # Cards
        self.labelYellowCards.set_label("%i" % (game.statistics.yellows))
        self.labelRedCards.set_label("%i" % (game.statistics.reds))

        # Attendance
        attendance = game.clubs[game.teamid].attendances

        if len(attendance) > 0:
            self.labelHighAttendance.set_label("%i" % (max(attendance)))
            self.labelLowAttendance.set_label("%i" % (min(attendance)))
            self.labelAverageAttendance.set_label("%i" % (statistics.mean(attendance)))
        else:
            self.labelHighAttendance.set_label("-")
            self.labelLowAttendance.set_label("-")
            self.labelAverageAttendance.set_label("-")
