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
from gi.repository import Gdk

import data
import structures.negotiations
import uigtk.shared
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
            self.treeview.connect("button-press-event", self.on_button_press_event)
            self.treeview.connect("key-press-event", self.on_key_press_event)
            self.treeview.treeselection.connect("changed", self.on_treeselection_changed)
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

            buttonbox = uigtk.widgets.ButtonBox()
            buttonbox.set_layout(Gtk.ButtonBoxStyle.END)
            self.attach(buttonbox, 0, 2, 1, 1)

            self.buttonRespond = uigtk.widgets.Button("_Respond")
            self.buttonRespond.set_sensitive(False)
            self.buttonRespond.set_tooltip_text("Respond to negotiations for selected player.")
            self.buttonRespond.connect("clicked", self.on_respond_clicked)
            buttonbox.add(self.buttonRespond)
            self.buttonEnd = uigtk.widgets.Button("_End")
            self.buttonEnd.set_sensitive(False)
            self.buttonEnd.set_tooltip_text("End transfer negotiations for selected player.")
            self.buttonEnd.connect("clicked", self.on_end_clicked)
            buttonbox.add(self.buttonEnd)

            self.contextmenu = ContextMenu()

        def on_key_press_event(self, treeview, event):
            '''
            Key event when right-click menu is pressed on keyboard.
            '''
            if Gdk.keyval_name(event.keyval) == "Menu":
                event.button = 3
                self.on_context_menu_event(event)

        def on_button_press_event(self, treeview, event):
            '''
            Button event when right-click on mouse is made.
            '''
            model, treeiter = self.treeview.treeselection.get_selected()

            if treeiter:
                if event.button == 3:
                    self.on_context_menu_event(event)

        def on_context_menu_event(self, event):
            model, treeiter = self.treeview.treeselection.get_selected()

            self.contextmenu.negotiationid = model[treeiter][0]
            self.contextmenu.show_all()
            self.contextmenu.popup(None,
                                   None,
                                   None,
                                   None,
                                   event.button,
                                   event.time)

        def on_respond_clicked(self, *args):
            '''
            Respond to negotiations for selected player.
            '''
            model, treeiter = self.treeview.treeselection.get_selected()
            negotiationid = model[treeiter][0]
            negotiation = data.negotiations.get_negotiation_by_id(negotiationid)
            negotiation.respond_to_negotiation()

            self.populate_data()

        def on_end_clicked(self, *args):
            '''
            End negotiations for selected player.
            '''
            model, treeiter = self.treeview.treeselection.get_selected()
            negotiationid = model[treeiter][0]
            negotiation = data.negotiations.get_negotiation_by_id(negotiationid)
            player = data.players.get_player_by_id(negotiation.playerid)

            dialog = EndTransfer(player.get_name(mode=1))

            if dialog.show():
                data.negotiations.end_negotiation(negotiationid)
                self.populate_data()

        def on_row_activated(self, treeview, treepath, treeviewcolumn):
            '''
            Display visible player information screen.
            '''
            negotiationid = self.liststore[treepath][0]
            negotiation = data.negotiations.get_negotiation_by_id(negotiationid)
            negotiation.respond_to_negotiation()

            self.populate_data()

        def on_treeselection_changed(self, treeselection):
            '''
            Update end transfer button sensitivity when item is selected.
            '''
            model, treeiter = treeselection.get_selected()

            if treeiter:
                self.buttonRespond.set_sensitive(True)
                self.buttonEnd.set_sensitive(True)
            else:
                self.buttonRespond.set_sensitive(False)
                self.buttonEnd.set_sensitive(False)

        def populate_data(self):
            self.liststore.clear()

            for negotiationid, negotiation in self.negotiations():
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

    def run(self):
        self.inbound.negotiations = data.negotiations.get_user_incoming
        self.inbound.populate_data()
        self.outbound.negotiations = data.negotiations.get_user_outgoing
        self.outbound.populate_data()

        self.show_all()


class ContextMenu(Gtk.Menu):
    def __init__(self):
        Gtk.Menu.__init__(self)

        menuitem = uigtk.widgets.MenuItem("_End Transfer")
        menuitem.connect("activate", self.on_end_clicked)
        self.append(menuitem)
        separator = Gtk.SeparatorMenuItem()
        self.append(separator)
        menuitem = uigtk.widgets.MenuItem("_Player Information")
        menuitem.connect("activate", self.on_player_information_clicked)
        self.append(menuitem)

    def on_end_clicked(self, *args):
        negotiation = data.negotiations.get_negotiation_by_id(self.negotiationid)
        player = data.players.get_player_by_id(negotiation.playerid)
        dialog = EndTransfer(player.get_name(mode=1))

        if dialog.show():
            data.negotiations.end_negotiation(self.negotiationid)

    def on_player_information_clicked(self, *args):
        pass


class PurchaseEnquiry(uigtk.shared.TransferEnquiry):
    '''
    Dialog displayed on approaching player for a purchase.
    '''
    def __init__(self):
        uigtk.shared.TransferEnquiry.__init__(self)

    def show(self, club, player):
        self.set_markup("Approach %s for the purchase of %s?" % (club.name, player.get_name(mode=1)))

        state = 0

        if self.run() == Gtk.ResponseType.OK:
            state = 1

        self.destroy()

        return state


class LoanEnquiry(uigtk.shared.TransferEnquiry):
    '''
    Dialog displayed on approaching player for a loan.
    '''
    def __init__(self):
        uigtk.shared.TransferEnquiry.__init__(self)

    def show(self, club, player):
        self.set_markup("Approach %s for the loan of %s?" % (club.name, player.get_name(mode=1)))

        state = 0

        if self.run() == Gtk.ResponseType.OK:
            state = 1

        self.destroy()

        return state


class FreeEnquiry(uigtk.shared.TransferEnquiry):
    '''
    Dialog displayed on approaching player who is out of contract.
    '''
    def __init__(self):
        uigtk.shared.TransferEnquiry.__init__(self)

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
        self.add_button("_End Negotiation", Gtk.ResponseType.OK)
        self.set_default_response(Gtk.ResponseType.CANCEL)

    def show(self):
        state = self.run() == Gtk.ResponseType.OK
        self.destroy()

        return state


class PurchaseOffer(Gtk.Dialog):
    '''
    Dialog to request offer amount for player when purchasing.
    '''
    def __init__(self, player, club):
        Gtk.Dialog.__init__(self)
        self.set_transient_for(data.window)
        self.set_modal(True)
        self.set_title("Purchase Offer")
        self.add_button("_Withdraw", Gtk.ResponseType.REJECT)
        self.add_button("_Offer", Gtk.ResponseType.ACCEPT)
        self.set_default_response(Gtk.ResponseType.ACCEPT)
        self.vbox.set_border_width(5)

        grid = uigtk.widgets.Grid()
        self.vbox.add(grid)

        label = uigtk.widgets.Label("The offer for %s has been accepted.\n%s would like to negotiate a fee for the transfer." % (player.get_name(mode=1), club.name))
        grid.attach(label, 0, 0, 2, 1)
        label = uigtk.widgets.Label("Enter the amount to offer for the player:")
        grid.attach(label, 0, 1, 1, 1)
        spinbuttonAmount = Gtk.SpinButton.new_with_range(0, 999999999, 100000)
        #spinbuttonAmount.set_value(player.value * 1.10)
        grid.attach(spinbuttonAmount, 1, 1, 1, 1)

    def show(self):
        self.show_all()

        state = self.run() == Gtk.ResponseType.ACCEPT
        self.destroy()

        return state


class LoanOffer(Gtk.Dialog):
    '''
    Dialog to request period for player when loaning.
    '''
    def __init__(self, player, club):
        Gtk.Dialog.__init__(self)
        self.set_transient_for(data.window)
        self.set_default_size(300, -1)
        self.set_modal(True)
        self.set_title("Loan Offer")
        self.add_button("_Withdraw", Gtk.ResponseType.REJECT)
        self.add_button("_Offer", Gtk.ResponseType.ACCEPT)
        self.set_default_response(Gtk.ResponseType.ACCEPT)
        self.vbox.set_border_width(5)

        grid = uigtk.widgets.Grid()
        self.vbox.add(grid)

        label = uigtk.widgets.Label("The loan offer for %s has been accepted. %s would like to negotiate a loan period for the player." % (player.get_name(mode=1), club.name))
        label.set_line_wrap(True)
        grid.attach(label, 0, 0, 3, 1)
        label = uigtk.widgets.Label("Loan Period in Weeks")
        grid.attach(label, 0, 1, 1, 1)
        self.spinbuttonPeriod = Gtk.SpinButton()
        grid.attach(self.spinbuttonPeriod, 1, 1, 1, 1)
        self.checkbuttonSeason = uigtk.widgets.CheckButton("_End of Season")
        self.checkbuttonSeason.set_hexpand(True)
        self.checkbuttonSeason.connect("toggled", self.on_season_loan_toggled)
        grid.attach(self.checkbuttonSeason, 2, 1, 1, 1)

    def on_season_loan_toggled(self, checkbutton):
        '''
        Update spin button sensitivity when season-long loan toggled on.
        '''
        active = checkbutton.get_active()
        self.spinbuttonPeriod.set_sensitive(not active)

    def show(self):
        self.spinbuttonPeriod.set_range(1, 48)
        self.spinbuttonPeriod.set_value(4)
        self.spinbuttonPeriod.set_increments(1, 4)

        self.show_all()

        if self.run() == Gtk.ResponseType.ACCEPT:
            if self.checkbuttonSeason.get_active():
                period = -1
            else:
                period = self.spinbuttonPeriod.get_value_as_int()
        else:
            return False

        self.destroy()

        return period


class EnquiryRejection(Gtk.MessageDialog):
    def __init__(self, player, club):
        Gtk.MessageDialog.__init__(self)
        self.set_transient_for(data.window)
        self.set_modal(True)
        self.set_title("Enquiry Rejected")
        self.set_property("message-type", Gtk.MessageType.INFO)
        self.set_markup("The enquiry for %s has been rejected by %s." % (player.get_name(mode=1), club.name))
        self.add_button("_Close", Gtk.ResponseType.CLOSE)

        self.run()
        self.destroy()


class OfferRejection(Gtk.MessageDialog):
    def __init__(self, player, club):
        Gtk.MessageDialog.__init__(self)
        self.set_transient_for(data.window)
        self.set_modal(True)
        self.set_title("Offer Rejected")
        self.set_property("message-type", Gtk.MessageType.INFO)
        self.set_markup("The offer for %s has been rejected by %s." % (player.get_name(mode=1), club.name))
        self.add_button("_Close", Gtk.ResponseType.CLOSE)

        self.run()
        self.destroy()


class ContractRejection(Gtk.MessageDialog):
    def __init__(self, player):
        Gtk.MessageDialog.__init__(self)
        self.set_transient_for(data.window)
        self.set_modal(True)
        self.set_title("Transfer Rejected")
        self.set_property("message-type", Gtk.MessageType.INFO)
        self.set_markup("The contract offered to %s has been rejected." % (player.get_name(mode=1)))
        self.add_button("_Close", Gtk.ResponseType.CLOSE)

        self.run()
        self.destroy()


class ContractNegotiation(uigtk.shared.ContractNegotiation):
    def __init__(self, playerid):
        player = data.players.get_player_by_id(playerid)

        uigtk.shared.ContractNegotiation.__init__(self)
        self.set_title("Contract Negotiation")
        self.add_button("_Negotiate", Gtk.ResponseType.OK)

        self.labelContract.set_label("Contract negotiation details for %s." % (player.get_name(mode=1)))


class CompleteTransfer(Gtk.MessageDialog):
    def __init__(self):
        Gtk.MessageDialog.__init__(self)
        self.set_transient_for(data.window)
        self.set_modal(True)
        self.set_title("Complete Transfer")
        self.add_button("_Cancel Transfer", Gtk.ResponseType.CANCEL)
        self.add_button("Complete _Transfer", Gtk.ResponseType.OK)
        self.set_default_response(Gtk.ResponseType.OK)
        self.set_property("message-type", Gtk.MessageType.QUESTION)
        self.set_markup("<span size='12000'><b>Complete transfer of %s to %s?</b></span>")
        self.format_secondary_text("The transfer can be delayed for a short time if necessary.")

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

        self.run()
        self.destroy()


class AwaitingResponse(Gtk.MessageDialog):
    def __init__(self, player, club):
        Gtk.MessageDialog.__init__(self)
        self.set_transient_for(data.window)
        self.set_title("Awaiting Response")
        self.set_property("message-type", Gtk.MessageType.INFO)
        self.set_markup("We are currently awaiting a response from %s for %s." % (club.name, player.get_name(mode=1)))
        self.add_button("_Close", Gtk.ResponseType.CLOSE)

        self.run()
        self.destroy()
