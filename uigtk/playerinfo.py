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

import display
import game
import widgets


class PlayerInfo(Gtk.Dialog):
    def __init__(self, playerid):
        self.playerid = playerid

        Gtk.Dialog.__init__(self)
        self.set_title("Player Information")
        self.set_transient_for(game.window)
        self.set_border_width(5)
        self.set_resizable(False)
        self.add_button("_Close", Gtk.ResponseType.CLOSE)
        self.vbox.set_spacing(5)

        grid = Gtk.Grid()
        self.vbox.add(grid)

        player = game.players[self.playerid]
        name = player.get_name(mode=1)

        label = widgets.AlignedLabel("%s" % (name))
        label.set_hexpand(True)
        grid.attach(label, 0, 0, 1, 1)

        if player.club == game.teamid:
            self.menu = Gtk.Menu()
            menuitem = widgets.MenuItem("_Recall From Loan")
            menuitem.set_sensitive(self.playerid in game.loans.keys())
            menuitem.connect("activate", self.recall_from_loan)
            self.menu.append(menuitem)

            menubutton = Gtk.MenuButton("Actions")
            menubutton.set_popup(self.menu)
            menubutton.connect("clicked", self.action_menu_popup)
            grid.attach(menubutton, 1, 0, 1, 1)

        notebook = Gtk.Notebook()
        self.vbox.add(notebook)

        grid1 = Gtk.Grid()
        grid1.set_border_width(5)
        grid1.set_row_spacing(5)
        grid1.set_column_spacing(5)
        label = widgets.Label("_Personal")
        notebook.append_page(grid1, label)

        commonframe = widgets.CommonFrame("Contract")
        grid1.attach(commonframe, 0, 0, 1, 1)

        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)
        commonframe.insert(grid)

        label = widgets.AlignedLabel("Win Bonus")
        grid.attach(label, 0, 0, 1, 1)
        label = widgets.AlignedLabel("Goal Bonus")
        grid.attach(label, 0, 1, 1, 1)
        label = widgets.AlignedLabel("League Champions Bonus")
        grid.attach(label, 0, 2, 1, 1)
        label = widgets.AlignedLabel("League Runners Up Bonus")
        grid.attach(label, 0, 3, 1, 1)

        if self.playerid:
            bonus = game.players[self.playerid].bonus

            amount = display.currency(bonus[2])
            label = widgets.AlignedLabel(amount)
            grid.attach(label, 1, 0, 1, 1)
            amount = display.currency(bonus[3])
            label = widgets.AlignedLabel(amount)
            grid.attach(label, 1, 1, 1, 1)
            amount = display.currency(bonus[0])
            label = widgets.AlignedLabel(amount)
            grid.attach(label, 1, 2, 1, 1)
            amount = display.currency(bonus[1])
            label = widgets.AlignedLabel(amount)
            grid.attach(label, 1, 3, 1, 1)

        commonframe = widgets.CommonFrame("Injuries / Suspensions")
        grid1.attach(commonframe, 0, 1, 1, 1)

        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)
        commonframe.insert(grid)

        label = widgets.AlignedLabel("Injury")
        grid.attach(label, 0, 0, 1, 1)
        label = widgets.AlignedLabel("Injury Period")
        grid.attach(label, 0, 1, 1, 1)
        label = widgets.AlignedLabel("Suspension")
        grid.attach(label, 0, 2, 1, 1)
        label = widgets.AlignedLabel("Suspension Period")
        grid.attach(label, 0, 3, 1, 1)

        if self.playerid:
            player = game.players[self.playerid]

            if player.injury_type == 0:
                injury_type = "None"
                injury_period = "N/A"
            else:
                injury_type = constants.injuries[injuryid][0]
                injury_period = player.get_injury()

            if player.suspension_type == 0:
                suspension_type = "None"
                suspension_period = "N/A"
            else:
                suspension_type = constants.suspensions[suspensionid][0]
                suspension_period = player.get_suspension()

            label = widgets.AlignedLabel("%s" % (injury_type))
            grid.attach(label, 1, 0, 1, 1)
            label = widgets.AlignedLabel("%s" % (injury_period))
            grid.attach(label, 1, 1, 1, 1)
            label = widgets.AlignedLabel("%s" % (suspension_type))
            grid.attach(label, 1, 2, 1, 1)
            label = widgets.AlignedLabel("%s" % (suspension_period))
            grid.attach(label, 1, 3, 1, 1)

        grid2 = Gtk.Grid()
        grid2.set_border_width(5)
        label = widgets.Label("_History")
        notebook.append_page(grid2, label)

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_policy(Gtk.PolicyType.NEVER,
                                  Gtk.PolicyType.AUTOMATIC)
        grid2.attach(scrolledwindow, 0, 0, 1, 1)

        player = game.players[self.playerid]
        club = player.get_club()
        season = game.date.get_season()
        games = player.get_appearances()

        liststore = Gtk.ListStore(str, str, str, int, int, int)
        liststore.append([season,
                          club,
                          games,
                          player.goals,
                          player.assists,
                          player.man_of_the_match])

        for item in player.history.history:
            liststore.append(item)

        treeview = Gtk.TreeView()
        treeview.set_vexpand(True)
        treeview.set_hexpand(True)
        treeview.set_model(liststore)
        treeview.set_enable_search(False)
        treeview.set_search_column(-1)
        scrolledwindow.add(treeview)

        treeselection = treeview.get_selection()
        treeselection.set_mode(Gtk.SelectionMode.NONE)

        treeviewcolumn = widgets.TreeViewColumn(title="Season", column=0)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Club", column=1)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Games", column=2)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Goals", column=3)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Assists", column=4)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="MOTM", column=5)
        treeview.append_column(treeviewcolumn)

        self.show_all()

    def recall_from_loan(self, menuitem):
        loan = game.loans[self.playerid]

        if loan.cancel_loan():
            loan.end_loan()

    def action_menu_popup(self, menubutton):
        self.menu.show_all()
