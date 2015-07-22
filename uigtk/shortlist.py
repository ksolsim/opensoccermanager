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

import game
import user
import widgets


class Shortlist(Gtk.Grid):
    __name__ = "shortlist"

    def __init__(self):
        Gtk.Grid.__init__(self)
        self.set_row_spacing(5)

        self.liststorePlayers = Gtk.ListStore(int, str, int, str,
                                              str, str, str, str)

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_policy(Gtk.PolicyType.NEVER,
                                  Gtk.PolicyType.AUTOMATIC)
        scrolledwindow.set_vexpand(True)
        scrolledwindow.set_hexpand(True)
        self.attach(scrolledwindow, 0, 0, 1, 1)

        treeview = Gtk.TreeView()
        treeview.set_model(self.liststorePlayers)
        treeview.set_activate_on_single_click(True)
        treeview.set_enable_search(False)
        treeview.set_search_column(-1)
        self.treeselection = treeview.get_selection()
        self.treeselection.connect("changed", self.selection_changed)
        scrolledwindow.add(treeview)

        treeviewcolumn = widgets.TreeViewColumn(title="Name", column=1)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Age", column=2)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Club", column=3)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Nationality", column=4)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Position", column=5)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Value", column=6)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Wage", column=7)
        treeview.append_column(treeviewcolumn)

        buttonbox = Gtk.ButtonBox()
        buttonbox.set_layout(Gtk.ButtonBoxStyle.END)
        buttonbox.set_spacing(5)
        self.attach(buttonbox, 0, 1, 1, 1)

        self.buttonScout = widgets.Button("_Scout Report")
        self.buttonScout.set_sensitive(False)
        self.buttonScout.connect("clicked", self.scout_report)
        buttonbox.add(self.buttonScout)
        self.buttonBuy = widgets.Button("_Buy")
        self.buttonBuy.set_sensitive(False)
        self.buttonBuy.connect("clicked", self.make_transfer_offer, 0)
        buttonbox.add(self.buttonBuy)
        self.buttonLoan = widgets.Button("_Loan")
        self.buttonLoan.set_sensitive(False)
        self.buttonLoan.connect("clicked", self.make_transfer_offer, 1)
        buttonbox.add(self.buttonLoan)
        self.buttonRemove = widgets.Button("_Remove")
        self.buttonRemove.set_sensitive(False)
        self.buttonRemove.connect("clicked", self.remove_from_shortlist)
        buttonbox.add(self.buttonRemove)

    def selection_changed(self, treeselection):
        model, treeiter = self.treeselection.get_selected()

        if treeiter:
            playerid = model[treeiter][0]
            player = game.players[playerid]

            club = user.get_user_club()

            if club.scouts.get_number_of_scouts() > 0:
                self.buttonScout.set_sensitive(True)

            if playerid in game.loans:
                self.buttonBuy.set_sensitive(False)
                self.buttonLoan.set_sensitive(False)
            else:
                self.buttonBuy.set_sensitive(True)
                self.buttonLoan.set_sensitive(True)

                if not player.club:
                    self.buttonLoan.set_sensitive(False)

            self.buttonRemove.set_sensitive(True)
        else:
            self.buttonScout.set_sensitive(False)
            self.buttonBuy.set_sensitive(False)
            self.buttonLoan.set_sensitive(False)
            self.buttonRemove.set_sensitive(False)

    def remove_from_shortlist(self, button):
        model, treeiter = self.treeselection.get_selected()
        playerid = model[treeiter][0]

        if dialogs.remove_from_shortlist(playerid):
            club = user.get_user_club()
            club.shortlist.remove_player(playerid)

            self.populate_data()

    def scout_report(self, button):
        model, treeiter = self.treeselection.get_selected()
        playerid = model[treeiter][0]

        status = scout.individual(playerid)
        name = game.players[playerid].get_name(mode=1)

        dialogs.scout_report(name, status)

    def make_transfer_offer(self, menuitem, transfer_type):
        model, treeiter = self.treeselection.get_selected()
        playerid = model[treeiter][0]

        # Set to free transfer if player has no club
        if game.players[playerid].club is None:
            transfer_type = 2

        transfer.make_enquiry(playerid, transfer_type)

    def populate_data(self):
        self.liststorePlayers.clear()

        club = user.get_user_club()

        for playerid in club.shortlist.players:
            player = game.players[playerid]

            self.liststorePlayers.append([playerid,
                                          player.get_name(),
                                          player.get_age(),
                                          player.get_club(),
                                          player.get_nationality(),
                                          player.position,
                                          player.get_value(),
                                          player.get_wage()])

    def run(self):
        self.populate_data()

        self.show_all()
