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
import widgets


class Negotiations(Gtk.Grid):
    __name__ = "negotiations"

    def __init__(self):
        Gtk.Grid.__init__(self)
        self.set_row_spacing(5)

        self.liststoreInbound = Gtk.ListStore(int, str, str, str, str, str)
        self.liststoreOutbound = Gtk.ListStore(int, str, str, str, str, str)

        # Inbound transfers
        label = widgets.AlignedLabel("<b>Inbound</b>")
        label.set_use_markup(True)
        self.attach(label, 0, 0, 1, 1)

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_vexpand(True)
        scrolledwindow.set_hexpand(True)
        self.attach(scrolledwindow, 0, 1, 1, 1)

        treeviewInbound = Gtk.TreeView()
        treeviewInbound.set_model(self.liststoreInbound)
        treeviewInbound.set_enable_search(False)
        treeviewInbound.set_search_column(-1)
        treeviewInbound.connect("row-activated", self.on_treeview_activated)
        treeviewInbound.connect("button-release-event", self.context_menu)
        self.treeselectionInbound = treeviewInbound.get_selection()
        scrolledwindow.add(treeviewInbound)

        treeviewcolumn = widgets.TreeViewColumn(title="Name", column=1)
        treeviewInbound.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Offer Date", column=2)
        treeviewInbound.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Offer Type", column=3)
        treeviewInbound.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Club", column=4)
        treeviewInbound.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Status", column=5)
        treeviewInbound.append_column(treeviewcolumn)

        # Outbound transfers
        label = widgets.AlignedLabel("<b>Outbound</b>")
        label.set_use_markup(True)
        self.attach(label, 0, 2, 1, 1)

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_vexpand(True)
        scrolledwindow.set_hexpand(True)
        self.attach(scrolledwindow, 0, 3, 1, 1)

        treeviewOutbound = Gtk.TreeView()
        treeviewOutbound.set_model(self.liststoreOutbound)
        treeviewOutbound.set_enable_search(False)
        treeviewOutbound.set_search_column(-1)
        treeviewOutbound.connect("row-activated", self.on_treeview_activated)
        treeviewOutbound.connect("button-release-event", self.context_menu)
        self.treeselectionOutbound = treeviewOutbound.get_selection()
        scrolledwindow.add(treeviewOutbound)

        treeviewcolumn = widgets.TreeViewColumn(title="Name", column=1)
        treeviewOutbound.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Offer Date", column=2)
        treeviewOutbound.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Offer Type", column=3)
        treeviewOutbound.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Club", column=4)
        treeviewOutbound.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Status", column=5)
        treeviewOutbound.append_column(treeviewcolumn)

        self.contextmenu = Gtk.Menu()
        menuitem = widgets.MenuItem("_Cancel Transfer")
        menuitem.connect("activate", self.cancel_transfer)
        self.contextmenu.append(menuitem)

    def cancel_transfer(self, menuitem):
        model, treeiter = self.treeselection.get_selected()

        negotiationid = model[treeiter][0]
        negotiation = game.negotiations[negotiationid]

        if negotiation.club == game.teamid:
            if dialogs.withdraw_transfer(negotiationid):
                del game.negotiations[negotiationid]
        else:
            if dialogs.cancel_transfer(negotiationid):
                del game.negotiations[negotiationid]

        self.populate_data()

    def on_treeview_activated(self, treeview, treepath, treeviewcolumn):
        model = treeview.get_model()

        negotiationid = model[treepath][0]
        negotiation = game.negotiations[negotiationid]

        negotiation.response()

        self.populate_data()

    def context_menu(self, treeview, event):
        if event.button == 3:
            treeselection = treeview.get_selection()
            model, treeiter = treeselection.get_selected()

            if treeiter:
                self.treeselection = treeselection
                self.contextmenu.show_all()
                self.contextmenu.popup(None, None, None, None, event.button, event.time)

    def populate_data(self):
        self.liststoreInbound.clear()
        self.liststoreOutbound.clear()

        for negotiationid, negotiation in game.negotiations.items():
            playerid = negotiation.playerid
            player = game.players[playerid]

            name = player.get_name(mode=1)
            transfer = ("Purchase", "Loan", "Free Transfer")[negotiation.transfer_type]

            if negotiation.club == game.teamid:
                club = player.get_club()
                status = constants.transfer_inbound_status[negotiation.status]

                self.liststoreInbound.append([negotiationid,
                                              name,
                                              negotiation.date,
                                              transfer,
                                              club,
                                              status])
            elif player.club == game.teamid:
                club = display.club(negotiation.club)
                status = constants.transfer_outbound_status[negotiation.status]

                self.liststoreOutbound.append([negotiationid,
                                               name,
                                               negotiation.date,
                                               transfer,
                                               club,
                                               status])

    def run(self):
        self.populate_data()

        self.show_all()
