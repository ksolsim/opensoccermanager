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
import structures.negotiations
import uigtk.widgets


class Negotiations(Gtk.Grid):
    __name__ = "negotiations"

    class Negotiation(Gtk.Grid):
        def __init__(self, label):
            Gtk.Grid.__init__(self)
            self.set_row_spacing(5)

            label = uigtk.widgets.Label("<b>%s</b>" % (label), leftalign=True)
            self.attach(label, 0, 0, 1, 1)

            scrolledwindow = uigtk.widgets.ScrolledWindow()
            self.attach(scrolledwindow, 0, 1, 1, 1)

            self.liststore = Gtk.ListStore(int, int, str, str, str, str, str)

            self.treeview = uigtk.widgets.TreeView()
            self.treeview.set_vexpand(True)
            self.treeview.set_hexpand(True)
            self.treeview.set_model(self.liststore)
            self.treeview.connect("row-activated", self.on_row_activated)
            self.treeview.treeselection.connect("changed", self.on_selection_changed)
            scrolledwindow.add(self.treeview)

            treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Name",
                                                          column=2)
            treeviewcolumn.set_expand(True)
            self.treeview.append_column(treeviewcolumn)
            treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Offer Date",
                                                          column=3)
            self.treeview.append_column(treeviewcolumn)
            treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Offer Type",
                                                          column=4)
            self.treeview.append_column(treeviewcolumn)
            treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Club",
                                                          column=5)
            self.treeview.append_column(treeviewcolumn)
            treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Status",
                                                          column=6)
            self.treeview.append_column(treeviewcolumn)

            buttonbox = Gtk.ButtonBox()
            buttonbox.set_layout(Gtk.ButtonBoxStyle.END)
            self.attach(buttonbox, 0, 2, 1, 1)
            self.buttonEnd = uigtk.widgets.Button("End Negotiations")
            self.buttonEnd.set_sensitive(False)
            self.buttonEnd.set_tooltip_text("End transfer negotiations for selected player.")
            self.buttonEnd.connect("clicked", self.on_end_transfer)
            buttonbox.add(self.buttonEnd)

        def on_end_transfer(self, *args):
            '''
            Ask to end transfer for selected players.
            '''
            model, treeiter = self.treeview.treeselection.get_selected()

            negotiationid = model[treeiter][0]
            negotiation = data.negotiations.get_negotiation(negotiationid)
            player = data.players.get_player_by_id(negotiation.playerid)

            dialog = EndTransfer(player.get_name(mode=1))

            if dialog.show():
                data.negotiations.end_negotiation(negotiationid)
                self.populate_data(data.negotiations.get_user_incoming())

        def on_row_activated(self, treeview, treepath, treeviewcolumn):
            '''
            Display visible player information screen.
            '''
            model = treeview.get_model()

            playerid = model[treepath][1]

            data.window.screen.change_visible_screen("playerinformation")
            data.window.screen.active.set_visible_player(playerid)

        def on_selection_changed(self, treeselection):
            '''
            Update end transfer button sensitivity when item is selected.
            '''
            model, treeiter = treeselection.get_selected()

            if treeiter:
                self.buttonEnd.set_sensitive(True)
            else:
                self.buttonEnd.set_sensitive(False)

        def populate_data(self, negotiations):
            self.liststore.clear()

            for negotiationid, negotiation in negotiations.items():
                player = data.players.get_player_by_id(negotiation.playerid)
                transfer_type = ("Purchase", "Loan")[negotiation.transfer_type]
                club = data.clubs.get_club_by_id(player.squad)

                self.liststore.append([negotiationid,
                                       negotiation.playerid,
                                       player.get_name(mode=1),
                                       negotiation.offer_date,
                                       transfer_type,
                                       club.name,
                                       negotiation.get_status_message()])

    def __init__(self):
        Gtk.Grid.__init__(self)
        self.set_column_homogeneous(True)
        self.set_column_spacing(5)

        self.inbound = self.Negotiation(label="Inbound Transfers")
        self.attach(self.inbound, 0, 0, 1, 1)

        self.outbound = self.Negotiation(label="Outbound Transfers")
        self.attach(self.outbound, 0, 1, 1, 1)

    def populate_outgoing_data(self):
        self.negotiationOutbound.liststore.clear()

        outgoing = data.negotiations.get_user_outgoing()

        for negotiationid, negotiation in outgoing.items():
            player = data.players.get_player_by_id(negotiation.playerid)
            transfer_type = ("Purchase", "Loan")[negotiation.transfer_type]
            club = data.clubs[negotiation.clubid]

            self.negotiationOutbound.liststore.append([negotiationid,
                                                       player.get_name(mode=1),
                                                       "%i/%i/%i" % (negotiation.offer_date),
                                                       transfer_type,
                                                       club.name,
                                                       ""])

    def run(self):
        self.inbound.populate_data(data.negotiations.get_user_incoming())
        #self.populate_outgoing_data()
        self.show_all()


class TransferApproach(Gtk.MessageDialog):
    '''
    Message dialog base class confirming whether to approach for a player.
    '''
    def __init__(self):
        Gtk.MessageDialog.__init__(self)
        self.set_transient_for(data.window)
        self.set_title("Transfer Offer")
        self.set_property("message-type", Gtk.MessageType.QUESTION)
        self.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("_Approach", Gtk.ResponseType.OK)
        self.set_default_response(Gtk.ResponseType.CANCEL)


class PurchaseApproach(TransferApproach):
    '''
    Dialog displayed on approaching player for a purchase.
    '''
    def __init__(self):
        TransferApproach.__init__(self)

    def show(self, club, player):
        self.set_markup("Approach %s for the purchase of %s?" % (club.name, player.get_name(mode=1)))

        state = 0

        if self.run() == Gtk.ResponseType.OK:
            state = 1

        self.destroy()

        return state


class LoanApproach(TransferApproach):
    '''
    Dialog displayed on approaching player for a loan.
    '''
    def __init__(self):
        TransferApproach.__init__(self)

    def show(self, club, player):
        self.set_markup("Approach %s for the loan of %s?" % (club.name, player.get_name(mode=1)))

        state = 0

        if self.run() == Gtk.ResponseType.OK:
            state = 1

        self.destroy()

        return state


class FreeApproach(TransferApproach):
    '''
    Dialog displayed on approaching player who is out of contract.
    '''
    def __init__(self):
        TransferApproach.__init__(self)

    def show(self, player):
        self.set_markup("Approach %s to join on a free transfer?" % (player.get_name(mode=1)))

        state = 0

        if self.run() == Gtk.ResponseType.OK:
            state = 1

        self.destroy()


class EndTransfer(Gtk.MessageDialog):
    '''
    Message dialog to confirm cancellation of ongoing negotiation.
    '''
    def __init__(self, name):
        Gtk.MessageDialog.__init__(self)
        self.set_transient_for(data.window)
        self.set_title("End Transfer")
        self.set_markup("Do you want to end the transfer negotiations for %s?" % (name))
        self.set_property("message-type", Gtk.MessageType.WARNING)
        self.add_button("_Do Not End", Gtk.ResponseType.CANCEL)
        self.add_button("_End Transfer", Gtk.ResponseType.OK)
        self.set_default_response(Gtk.ResponseType.CANCEL)

    def show(self):
        state = self.run() == Gtk.ResponseType.OK
        self.destroy()

        return state


class InProgress(Gtk.MessageDialog):
    '''
    Message dialog display when transfer negotiations already in progress.
    '''
    def __init__(self):
        Gtk.MessageDialog.__init__(self)
        self.set_transient_for(data.window)
        self.set_title("Transfer Status")
        self.set_markup("Transfer negotiations for this player are already in progress.")
        self.set_property("message-type", Gtk.MessageType.ERROR)
        self.add_button("_Close", Gtk.ResponseType.CLOSE)
        self.connect("response", self.on_response)

        self.show()

    def on_response(self, *args):
        self.destroy()
