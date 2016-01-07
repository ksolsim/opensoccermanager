#!/usr/bin/env python3

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
                      4: Referees()
                     }

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

    def populate_charts(self):
        self.combobox.remove_all()

        for viewid, view in self.views.items():
            self.combobox.append(str(viewid), view.name)

        self.combobox.set_active_id("0")

    def run(self):
        self.populate_charts()

        self.show_all()


class TreeView(Gtk.TreeView):
    '''
    Base TreeView class for charts displaying player information.
    '''
    def __init__(self):
        Gtk.TreeView.__init__(self)
        self.set_hexpand(True)
        self.set_vexpand(True)
        self.connect("row-activated", self.on_row_activated)

    def on_row_activated(self, treeview, treepath, treeviewcolumn):
        '''
        Launch player information screen for selected player.
        '''
        model = treeview.get_model()
        playerid = model[treepath][0]

        data.window.screen.change_visible_screen("playerinformation")
        data.window.screen.active.set_visible_player(playerid)


class Goalscorers(uigtk.widgets.Grid):
    name = "Goalscorers"

    def __init__(self):
        uigtk.widgets.Grid.__init__(self)

        scrolledwindow = uigtk.widgets.ScrolledWindow()
        self.attach(scrolledwindow, 0, 0, 1, 1)

        treeview = TreeView()
        scrolledwindow.add(treeview)

        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Player", column=1)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Club", column=2)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="League", column=3)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Goals", column=4)
        treeview.append_column(treeviewcolumn)

    def populate_data(self):
        pass

    def run(self):
        self.show_all()


class Assisters(uigtk.widgets.Grid):
    name = "Assisters"

    def __init__(self):
        uigtk.widgets.Grid.__init__(self)

        scrolledwindow = uigtk.widgets.ScrolledWindow()
        self.attach(scrolledwindow, 0, 0, 1, 1)

        treeview = TreeView()
        scrolledwindow.add(treeview)

        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Player", column=1)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Club", column=2)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="League", column=3)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Assists", column=4)
        treeview.append_column(treeviewcolumn)

    def populate_data(self):
        pass

    def run(self):
        self.show_all()


class Cards(uigtk.widgets.Grid):
    name = "Cards"

    def __init__(self):
        uigtk.widgets.Grid.__init__(self)

        scrolledwindow = uigtk.widgets.ScrolledWindow()
        self.attach(scrolledwindow, 0, 0, 1, 1)

        treeview = TreeView()
        scrolledwindow.add(treeview)

        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Player", column=1)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Club", column=2)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="League", column=3)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Yellow Cards", column=4)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Red Cards", column=5)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Card Points", column=6)
        treeview.append_column(treeviewcolumn)

    def populate_data(self):
        pass

    def run(self):
        self.show_all()


class Transfers(uigtk.widgets.Grid):
    name = "Transfers"

    def __init__(self):
        uigtk.widgets.Grid.__init__(self)

        scrolledwindow = uigtk.widgets.ScrolledWindow()
        self.attach(scrolledwindow, 0, 0, 1, 1)

        self.liststore = Gtk.ListStore(int, str, str, str, str)

        treeview = TreeView()
        treeview.set_model(self.liststore)
        scrolledwindow.add(treeview)

        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Player", column=1)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Former Club", column=2)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Current Club", column=3)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Transfer Fee", column=4)
        treeview.append_column(treeviewcolumn)

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

        self.liststore = Gtk.ListStore(int, str, str, int, int, int)

        treeview = Gtk.TreeView()
        treeview.set_vexpand(True)
        treeview.set_hexpand(True)
        treeview.set_model(self.liststore)
        scrolledwindow.add(treeview)

        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Referees", column=1)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="League", column=2)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Yellow Cards", column=3)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Red Cards", column=4)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Card Points", column=5)
        treeview.append_column(treeviewcolumn)

    def populate_data(self):
        self.liststore.clear()

        for refereeid, referee in data.referees.get_referees():
            league = data.leagues.get_league_by_id(referee.league)
            self.liststore.append([refereeid, referee.name, league.name, 0, 0, 0])

    def run(self):
        self.populate_data()
        self.show_all()
