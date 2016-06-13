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
import uigtk.widgets


class Charts(uigtk.widgets.Grid):
    __name__ = "charts"

    def __init__(self):
        self.views = {0: Goalscorers(),
                      1: Assisters(),
                      2: Cards(),
                      3: Transfers(),
                      4: Referees()}

        uigtk.widgets.Grid.__init__(self)

        buttonbox = uigtk.widgets.ButtonBox()
        buttonbox.set_layout(Gtk.ButtonBoxStyle.END)
        self.attach(buttonbox, 0, 0, 1, 1)

        label = uigtk.widgets.Label("Chart")
        label.set_alignment(1, 0.5)
        buttonbox.add(label)

        self.combobox = Gtk.ComboBoxText()
        self.combobox.connect("changed", self.on_view_changed)
        buttonbox.add(self.combobox)

        self.grid = uigtk.widgets.Grid()
        self.attach(self.grid, 0, 1, 1, 1)

        self.charts = self.views[0]
        self.grid.add(self.charts)

    def on_view_changed(self, combobox):
        '''
        Change the visible chart information.
        '''
        if combobox.get_active_id():
            if self.charts:
                self.grid.remove(self.charts)

            viewid = int(combobox.get_active_id())
            self.charts = self.views[viewid]
            self.grid.add(self.charts)

            self.charts.run()

            self.populate_data()

    def populate_charts(self):
        self.combobox.remove_all()

        for viewid, view in self.views.items():
            self.combobox.append(str(viewid), view.name)

        self.combobox.set_active_id("0")

    def populate_data(self):
        viewid = int(self.combobox.get_active_id())
        view = self.views[viewid]

        view.populate_data()

    def run(self):
        self.populate_charts()

        self.show_all()


class Leagues(uigtk.widgets.Grid):
    '''
    Visible league data selector.
    '''
    def __init__(self):
        uigtk.widgets.Grid.__init__(self)

        self.radiobuttonAll = uigtk.widgets.RadioButton("_All Leagues")
        self.radiobuttonAll.set_tooltip_text("Display data for all leagues.")
        self.radiobuttonAll.connect("toggled", self.on_view_toggled)
        self.attach(self.radiobuttonAll, 0, 0, 1, 1)
        self.radiobuttonSelected = uigtk.widgets.RadioButton("_Specific League")
        self.radiobuttonSelected.join_group(self.radiobuttonAll)
        self.radiobuttonSelected.set_tooltip_text("Display data for selected league.")
        self.radiobuttonSelected.connect("toggled", self.on_view_toggled)
        self.attach(self.radiobuttonSelected, 1, 0, 1, 1)

        self.liststore = Gtk.ListStore(str, str)
        treemodelsort = Gtk.TreeModelSort(self.liststore)
        treemodelsort.set_sort_column_id(1, Gtk.SortType.ASCENDING)

        for leagueid, league in data.leagues.get_leagues():
            self.liststore.append([str(leagueid), league.name])

        self.comboboxLeagues = uigtk.widgets.ComboBox(column=1)
        self.comboboxLeagues.set_model(treemodelsort)
        self.comboboxLeagues.set_id_column(0)
        self.comboboxLeagues.set_active(0)
        self.comboboxLeagues.set_sensitive(False)
        self.comboboxLeagues.set_tooltip_text("Select league to show visible fixtures.")
        self.attach(self.comboboxLeagues, 2, 0, 1, 1)

    def on_view_toggled(self, radiobutton):
        '''
        Toggle view of visible league data.
        '''
        if radiobutton is self.radiobuttonAll:
            self.comboboxLeagues.set_sensitive(not radiobutton.get_active())


class Display(uigtk.widgets.Grid):
    '''
    Base ScrolledWindow and TreeView for charts displaying player information.
    '''
    def __init__(self):
        uigtk.widgets.Grid.__init__(self)

        self.leagues = Leagues()
        self.attach(self.leagues, 0, 0, 1, 1)

        scrolledwindow = uigtk.widgets.ScrolledWindow()
        self.attach(scrolledwindow, 0, 1, 1, 1)

        self.treeview = uigtk.widgets.TreeView()
        self.treeview.set_hexpand(True)
        self.treeview.set_vexpand(True)
        self.treeview.connect("row-activated", self.on_row_activated)
        scrolledwindow.add(self.treeview)

    def on_row_activated(self, treeview, treepath, treeviewcolumn):
        '''
        Launch player information screen for selected player.
        '''
        model = sef.treeview.get_model()
        playerid = model[treepath][0]

        player = data.players.get_player_by_id(playerid)

        data.window.screen.change_visible_screen("playerinformation", player=player)


class Goalscorers(uigtk.widgets.Grid):
    name = "Goalscorers"

    def __init__(self):
        uigtk.widgets.Grid.__init__(self)

        self.display = Display()
        self.attach(self.display, 0, 0, 1, 1)

        self.liststore = Gtk.ListStore(int, str, str, str, int)
        self.display.treeview.set_model(self.liststore)

        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Player", column=1)
        self.display.treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Club", column=2)
        self.display.treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="League", column=3)
        self.display.treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Goals", column=4)
        self.display.treeview.append_column(treeviewcolumn)

    def populate_data(self):
        pass

    def run(self):
        self.show_all()


class Assisters(uigtk.widgets.Grid):
    name = "Assisters"

    def __init__(self):
        uigtk.widgets.Grid.__init__(self)

        self.display = Display()
        self.attach(self.display, 0, 0, 1, 1)

        self.liststore = Gtk.ListStore(int, str, str, str, int)
        self.display.treeview.set_model(self.liststore)

        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Player", column=1)
        self.display.treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Club", column=2)
        self.display.treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="League", column=3)
        self.display.treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Assists", column=4)
        self.display.treeview.append_column(treeviewcolumn)

    def populate_data(self):
        pass

    def run(self):
        self.show_all()


class Cards(uigtk.widgets.Grid):
    name = "Cards"

    def __init__(self):
        uigtk.widgets.Grid.__init__(self)

        self.display = Display()
        self.attach(self.display, 0, 0, 1, 1)

        self.liststore = Gtk.ListStore(int, str, str, str, int, int, int)
        self.display.treeview.set_model(self.liststore)

        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Player", column=1)
        self.display.treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Club", column=2)
        self.display.treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="League", column=3)
        self.display.treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Yellow Cards",
                                                      column=4)
        self.display.treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Red Cards",
                                                      column=5)
        self.display.treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Card Points",
                                                      column=6)
        self.display.treeview.append_column(treeviewcolumn)

    def populate_data(self):
        pass

    def run(self):
        self.show_all()


class Transfers(uigtk.widgets.Grid):
    name = "Transfers"

    def __init__(self):
        uigtk.widgets.Grid.__init__(self)

        self.display = Display()
        self.attach(self.display, 0, 0, 1, 1)

        self.liststore = Gtk.ListStore(int, str, str, str, str)
        self.display.treeview.set_model(self.liststore)

        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Player", column=1)
        self.display.treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Former Club",
                                                      column=2)
        self.display.treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Current Club",
                                                      column=3)
        self.display.treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Transfer Fee",
                                                      column=4)
        self.display.treeview.append_column(treeviewcolumn)

    def populate_data(self):
        pass

    def run(self):
        self.show_all()


class Referees(uigtk.widgets.Grid):
    name = "Referees"

    def __init__(self):
        uigtk.widgets.Grid.__init__(self)

        scrolledwindow = uigtk.widgets.ScrolledWindow()
        self.attach(scrolledwindow, 0, 0, 1, 1)

        self.liststore = Gtk.ListStore(int, str, str, int, int, int, int)

        treeview = uigtk.widgets.TreeView()
        treeview.set_vexpand(True)
        treeview.set_hexpand(True)
        treeview.set_model(self.liststore)
        scrolledwindow.add(treeview)

        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Referee", column=1)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="League", column=2)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Games", column=3)
        treeviewcolumn.set_fixed_width(80)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Yellow Cards",
                                                      column=4)
        treeviewcolumn.set_fixed_width(80)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Red Cards",
                                                      column=5)
        treeviewcolumn.set_fixed_width(80)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Card Points",
                                                      column=6)
        treeviewcolumn.set_fixed_width(80)
        treeview.append_column(treeviewcolumn)

    def populate_data(self):
        self.liststore.clear()

        for refereeid, referee in data.referees.get_referee_data():
            self.liststore.append([refereeid,
                                   referee.name,
                                   referee.league.name,
                                   0, 0, 0, 0])

    def run(self):
        self.populate_data()
        self.show_all()
