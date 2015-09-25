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

import assists
import game
import goals
import widgets


class Charts(Gtk.Grid):
    __name__ = "charts"

    def __init__(self):
        self.views = {0: GoalScorers(),
                      1: Assists(),
                      2: Cards(),
                      3: Transfers(),
                      4: Referees(),
                     }

        self.charts = self.views[0]

        Gtk.Grid.__init__(self)
        self.set_row_spacing(5)

        buttonbox = Gtk.ButtonBox()
        buttonbox.set_spacing(5)
        buttonbox.set_layout(Gtk.ButtonBoxStyle.END)
        self.attach(buttonbox, 1, 0, 1, 1)

        label = Gtk.Label("View")
        label.set_alignment(1, 0.5)
        buttonbox.add(label)

        comboboxChart = Gtk.ComboBoxText()
        comboboxChart.append("0", "Goalscorers")
        comboboxChart.append("1", "Assists")
        comboboxChart.append("2", "Cards")
        comboboxChart.append("3", "Transfers")
        comboboxChart.append("4", "Referees")
        comboboxChart.set_active(0)
        comboboxChart.connect("changed", self.view_changed)
        buttonbox.add(comboboxChart)

        self.grid = Gtk.Grid()
        self.grid.set_vexpand(True)
        self.grid.set_hexpand(True)
        self.grid.set_row_spacing(5)
        self.grid.set_column_spacing(5)
        self.attach(self.grid, 0, 2, 2, 1)

        self.charts.set_vexpand(True)
        self.charts.set_hexpand(True)
        self.grid.add(self.charts)

    def view_changed(self, combobox):
        viewid = int(combobox.get_active_id())

        if self.charts:
            self.grid.remove(self.charts)

        self.charts = self.views[viewid]
        self.charts.set_vexpand(True)
        self.charts.set_hexpand(True)

        self.grid.add(self.charts)
        self.charts.run()

    def run(self):
        self.charts.run()
        self.show_all()


class GoalScorers(Gtk.ScrolledWindow):
    def __init__(self):
        Gtk.ScrolledWindow.__init__(self)

        self.liststore = Gtk.ListStore(str, str, int)

        treeview = Gtk.TreeView()
        treeview.set_model(self.liststore)
        treeview.set_enable_search(False)
        treeview.set_search_column(-1)
        treeselection = treeview.get_selection()
        treeselection.set_mode(Gtk.SelectionMode.NONE)
        self.add(treeview)

        treeviewcolumn = widgets.TreeViewColumn(title="Name", column=0)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Club", column=1)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Goals", column=2)
        treeview.append_column(treeviewcolumn)

    def run(self):
        self.liststore.clear()

        values = sorted(goals.chart.goalscorers,
                         key=goals.chart.goalscorers.get,
                         reverse=True)

        for playerid in values[:25]:
            playerObject = player.get_player(playerid)
            name = playerObject.get_name(mode=1)
            club = game.clubs[player.club].name

            self.liststore.append([name, club, game.goalscorers[playerid]])

        self.show_all()


class Assists(Gtk.ScrolledWindow):
    def __init__(self):
        Gtk.ScrolledWindow.__init__(self)

        self.liststore = Gtk.ListStore(str, str, int)

        treeview = Gtk.TreeView()
        treeview.set_model(self.liststore)
        treeview.set_enable_search(False)
        treeview.set_search_column(-1)
        treeselection = treeview.get_selection()
        treeselection.set_mode(Gtk.SelectionMode.NONE)
        self.add(treeview)

        treeviewcolumn = widgets.TreeViewColumn(title="Name", column=0)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Club", column=1)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Assists", column=2)
        treeview.append_column(treeviewcolumn)

    def run(self):
        self.liststore.clear()

        values = sorted(assists.chart.assisters,
                         key=assists.chart.assisters.get,
                         reverse=True)

        for playerid in values[:25]:
            player = game.players[playerid]
            name = player.get_name(mode=1)
            club = game.clubs[player.club].name

            self.liststore.append([name, club, game.assists[playerid]])

        self.show_all()


class Cards(Gtk.ScrolledWindow):
    def __init__(self):
        Gtk.ScrolledWindow.__init__(self)

        self.liststore = Gtk.ListStore(str, str, int, int, int)
        treemodelsort = Gtk.TreeModelSort(self.liststore)
        treemodelsort.set_sort_column_id(4, Gtk.SortType.DESCENDING)

        treeview = Gtk.TreeView()
        treeview.set_model(treemodelsort)
        treeview.set_enable_search(False)
        treeview.set_search_column(-1)
        treeselection = treeview.get_selection()
        treeselection.set_mode(Gtk.SelectionMode.NONE)
        self.add(treeview)

        treeviewcolumn = widgets.TreeViewColumn(title="Name", column=0)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Club", column=1)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Yellow Cards", column=2)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Red Cards", column=3)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Points", column=4)
        treeview.append_column(treeviewcolumn)

    def run(self):
        self.liststore.clear()

        players = [key for key in sorted(game.cards, key=lambda x: game.cards[x].points, reverse=True)]

        for playerid in players[:25]:
            player = game.players[playerid]
            name = player.get_name(mode=1)
            club = player.get_club()
            cards = game.cards[playerid]

            self.liststore.append([name,
                                   club,
                                   cards.yellow_cards,
                                   cards.red_cards,
                                   cards.points])

        self.show_all()


class Transfers(Gtk.ScrolledWindow):
    def __init__(self):
        Gtk.ScrolledWindow.__init__(self)

        self.liststore = Gtk.ListStore(str, str, str, str)
        treemodelsort = Gtk.TreeModelSort(self.liststore)
        treemodelsort.set_sort_column_id(3, Gtk.SortType.DESCENDING)

        treeview = Gtk.TreeView()
        treeview.set_model(treemodelsort)
        treeview.set_enable_search(False)
        treeview.set_search_column(-1)
        treeselection = treeview.get_selection()
        treeselection.set_mode(Gtk.SelectionMode.NONE)
        self.add(treeview)

        treeviewcolumn = widgets.TreeViewColumn(title="Name", column=0)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Former Club", column=1)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Current Club", column=2)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Transfer Fee", column=3)
        treeview.append_column(treeviewcolumn)

    def run(self):
        self.liststore.clear()

        for transfer in game.transfers:
            self.liststore.append(transfer)

        self.show_all()


class Referees(Gtk.ScrolledWindow):
    def __init__(self):
        Gtk.ScrolledWindow.__init__(self)

        self.liststore = Gtk.ListStore(str, int, int, int, int)
        self.treemodelsort = Gtk.TreeModelSort(self.liststore)

        treeview = Gtk.TreeView()
        treeview.set_model(self.treemodelsort)
        treeview.set_enable_search(False)
        treeview.set_search_column(-1)
        treeview.set_headers_clickable(True)
        treeselection = treeview.get_selection()
        treeselection.set_mode(Gtk.SelectionMode.NONE)
        self.add(treeview)

        treeviewcolumn = widgets.TreeViewColumn(title="Name", column=0)
        treeviewcolumn.set_sort_column_id(0)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Matches", column=1)
        treeviewcolumn.set_sort_column_id(1)
        treeviewcolumn.set_fixed_width(75)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Fouls", column=2)
        treeviewcolumn.set_sort_column_id(2)
        treeviewcolumn.set_fixed_width(75)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Yellow Cards", column=3)
        treeviewcolumn.set_sort_column_id(3)
        treeviewcolumn.set_fixed_width(75)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Red Cards", column=4)
        treeviewcolumn.set_sort_column_id(4)
        treeviewcolumn.set_fixed_width(75)
        treeview.append_column(treeviewcolumn)

    def run(self):
        self.liststore.clear()

        if game.date.eventindex == 0:
            self.treemodelsort.set_sort_column_id(0, Gtk.SortType.ASCENDING)
        else:
            self.treemodelsort.set_sort_column_id(1, Gtk.SortType.DESCENDING)

        for referee in game.referees.values():
            self.liststore.append([referee.name,
                                   referee.matches,
                                   referee.fouls,
                                   referee.yellows,
                                   referee.reds])

        self.show_all()
