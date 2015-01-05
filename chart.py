#!/usr/bin/env python

from gi.repository import Gtk

import game
import display


class GoalScorers(Gtk.ScrolledWindow):
    def __init__(self):
        Gtk.ScrolledWindow.__init__(self)

        self.liststore = Gtk.ListStore(str, str, int)

        treeview = Gtk.TreeView()
        treeselection = treeview.get_selection()
        treeselection.set_mode(Gtk.SelectionMode.NONE)
        treeview.set_model(self.liststore)
        self.add(treeview)

        cellrenderertext = Gtk.CellRendererText()
        treeviewcolumn = Gtk.TreeViewColumn("Name", cellrenderertext, text=0)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Club", cellrenderertext, text=1)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Goals", cellrenderertext, text=2)
        treeview.append_column(treeviewcolumn)

    def run(self):
        self.liststore.clear()

        goalscorers = sorted(game.goalscorers, key=game.goalscorers.get, reverse=True)

        for playerid in goalscorers[:25]:
            player = game.players[playerid]
            name = display.name(player, mode=1)
            club = game.clubs[player.club].name

            self.liststore.append([name, club, game.goalscorers[playerid]])

        self.show_all()


class Assists(Gtk.ScrolledWindow):
    def __init__(self):
        Gtk.ScrolledWindow.__init__(self)

        self.liststore = Gtk.ListStore(str, str, int)

        treeview = Gtk.TreeView()
        treeview.set_model(self.liststore)
        treeselection = treeview.get_selection()
        treeselection.set_mode(Gtk.SelectionMode.NONE)
        self.add(treeview)

        cellrenderertext = Gtk.CellRendererText()
        treeviewcolumn = Gtk.TreeViewColumn("Name", cellrenderertext, text=0)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Club", cellrenderertext, text=1)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Assists", cellrenderertext, text=2)
        treeview.append_column(treeviewcolumn)

    def run(self):
        self.liststore.clear()

        assists = sorted(game.assists, key=game.assists.get, reverse=True)

        for playerid in assists[:25]:
            player = game.players[playerid]
            name = display.name(player, mode=1)
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
        self.add(treeview)

        cellrenderertext = Gtk.CellRendererText()
        treeviewcolumn = Gtk.TreeViewColumn("Name", cellrenderertext, text=0)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Club", cellrenderertext, text=1)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Yellow Cards", cellrenderertext, text=2)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Red Cards", cellrenderertext, text=3)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Points", cellrenderertext, text=4)
        treeview.append_column(treeviewcolumn)

    def run(self):
        self.liststore.clear()

        cards = sorted(game.cards, key=game.cards.get, reverse=True)

        for playerid in cards[:25]:
            player = game.players[playerid]
            name = display.name(player, mode=1)
            club = game.clubs[player.club].name
            yellow = player.yellow_cards
            red = player.red_cards
            points = player.suspension_points

            self.liststore.append([name, club, yellow, red, points])

        self.show_all()


class Transfers(Gtk.Grid):
    def __init__(self):
        Gtk.Grid.__init__(self)
        self.set_row_spacing(5)
        self.set_column_spacing(5)

        self.liststore = Gtk.ListStore(str, str, str, str)

        treemodelsort = Gtk.TreeModelSort(self.liststore)
        treemodelsort.set_sort_column_id(3, Gtk.SortType.DESCENDING)

        treeview = Gtk.TreeView()
        treeview.set_vexpand(True)
        treeview.set_hexpand(True)
        treeview.set_model(treemodelsort)
        self.attach(treeview, 0, 0, 2, 1)
        treeselection = treeview.get_selection()
        treeselection.set_mode(Gtk.SelectionMode.NONE)

        cellrenderertext = Gtk.CellRendererText()
        treeviewcolumn = Gtk.TreeViewColumn("Name", cellrenderertext, text=0)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Former Club", cellrenderertext, text=1)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Current Club", cellrenderertext, text=2)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Transfer Fee", cellrenderertext, text=3)
        treeview.append_column(treeviewcolumn)

    def run(self):
        self.liststore.clear()

        for item in game.transfers:
            self.liststore.append(item)

        self.show_all()


class Referees(Gtk.ScrolledWindow):
    def __init__(self):
        Gtk.ScrolledWindow.__init__(self)

        self.liststore = Gtk.ListStore(str, int, int, int, int)
        self.treemodelsort = Gtk.TreeModelSort(self.liststore)

        treeview = Gtk.TreeView()
        treeview.set_model(self.treemodelsort)
        self.add(treeview)
        treeselection = treeview.get_selection()
        treeselection.set_mode(Gtk.SelectionMode.NONE)

        cellrenderertext = Gtk.CellRendererText()
        treeviewcolumn = Gtk.TreeViewColumn("Name", cellrenderertext, text=0)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Matches", cellrenderertext, text=1)
        treeviewcolumn.set_fixed_width(75)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Fouls", cellrenderertext, text=2)
        treeviewcolumn.set_fixed_width(75)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Yellow Cards", cellrenderertext, text=3)
        treeviewcolumn.set_fixed_width(75)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Red Cards", cellrenderertext, text=4)
        treeviewcolumn.set_fixed_width(75)
        treeview.append_column(treeviewcolumn)

    def run(self):
        self.liststore.clear()

        if game.eventindex == 0:
            self.treemodelsort.set_sort_column_id(0, Gtk.SortType.ASCENDING)
        else:
            self.treemodelsort.set_sort_column_id(1, Gtk.SortType.DESCENDING)

        for refereeid, referee in game.referees.items():
            name = referee[0]
            matches = referee[1]
            yellows = referee[3]
            reds = referee[4]

            self.liststore.append([name, matches, 0, yellows, reds])

        self.show_all()
