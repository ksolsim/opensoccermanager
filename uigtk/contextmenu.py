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
import structures.transfer
import uigtk.widgets


class ContextMenu1(Gtk.Menu):
    '''
    Context menu displayed for players belonging to user club.
    '''
    def __init__(self):
        Gtk.Menu.__init__(self)

        menuitem = uigtk.widgets.MenuItem("_Player Information")
        menuitem.connect("activate", self.on_player_information_clicked)
        self.append(menuitem)

        separator = Gtk.SeparatorMenuItem()
        self.append(separator)

        self.menuitemAddPurchase = uigtk.widgets.MenuItem("_Add To Purchase List")
        self.menuitemAddPurchase.connect("activate", self.on_purchase_list_clicked)
        self.append(self.menuitemAddPurchase)
        self.menuitemRemovePurchase = uigtk.widgets.MenuItem("_Remove From Purchase List")
        self.menuitemRemovePurchase.connect("activate", self.on_purchase_list_clicked)
        self.append(self.menuitemRemovePurchase)
        self.menuitemAddLoan = uigtk.widgets.MenuItem("_Add To Loan List")
        self.menuitemAddLoan.connect("activate", self.on_loan_list_clicked)
        self.append(self.menuitemAddLoan)
        self.menuitemRemoveLoan = uigtk.widgets.MenuItem("_Remove From Loan List")
        self.menuitemRemoveLoan.connect("activate", self.on_loan_list_clicked)
        self.append(self.menuitemRemoveLoan)
        menuitem = uigtk.widgets.MenuItem("_Renew Contract")
        menuitem.connect("activate", self.on_renew_contract_clicked)
        self.append(menuitem)
        menuitem = uigtk.widgets.MenuItem("_Terminate Contract")
        menuitem.connect("activate", self.on_terminate_contract_clicked)
        self.append(menuitem)
        self.menuitemNotForSale = uigtk.widgets.CheckMenuItem("_Not for Sale")
        self.menuitemNotForSale.connect("toggled", self.on_not_for_sale_clicked)
        self.append(self.menuitemNotForSale)

        separator = Gtk.SeparatorMenuItem()
        self.append(separator)

        menuitem = uigtk.widgets.MenuItem("Add To _Comparison")
        menuitem.connect("activate", self.on_comparison_clicked)
        self.append(menuitem)

    def on_player_information_clicked(self, *args):
        '''
        Launch player information screen for selected player.
        '''
        data.window.screen.change_visible_screen("playerinformation")
        data.window.screen.active.set_visible_player(self.player)

    def on_purchase_list_clicked(self, *args):
        '''
        Add player to the transfer list for sale.
        '''
        if data.purchase_list.get_player_listed(self.player):
            data.purchase_list.remove_from_list(self.player)
        else:
            listing = structures.transfer.PurchaseListing(self.player, self.player.value.get_value())
            data.purchase_list.add_to_list(listing)

        self.update_sensitivity()

        data.window.screen.refresh_visible_screen()

    def on_loan_list_clicked(self, *args):
        '''
        Add player to the transfer list for loan.
        '''
        if data.loan_list.get_player_listed(self.player):
            data.loan_list.remove_from_list(self.player)
        else:
            listing = structures.transfer.LoanListing(self.player)
            data.loan_list.add_to_list(listing)

        self.update_sensitivity()

        data.window.screen.refresh_visible_screen()

    def on_renew_contract_clicked(self, *args):
        '''
        Query user to renew contract of selected player.
        '''
        dialog = uigtk.squad.RenewContract(self.player)

        if dialog.show():
            data.window.screen.refresh_visible_screen()

    def on_terminate_contract_clicked(self, *args):
        '''
        Query user to terminate contract of selected player.
        '''
        dialog = uigtk.squad.TerminateContract(self.player)

        if dialog.show():
            self.player.contract.terminate_contract()
            data.window.screen.refresh_visible_screen()

    def on_not_for_sale_clicked(self, checkmenuitem):
        '''
        Toggle not for sale flag on player object.
        '''
        self.player.not_for_sale = checkmenuitem.get_active()

    def on_comparison_clicked(self, *args):
        '''
        Add player to stack for comparison.
        '''
        data.comparison.add_to_comparison(self.player)

    def update_sensitivity(self):
        '''
        Update menu item sensitivity for available options.
        '''
        self.menuitemAddPurchase.set_sensitive(not data.purchase_list.get_player_listed(self.player))
        self.menuitemRemovePurchase.set_sensitive(data.purchase_list.get_player_listed(self.player))
        self.menuitemAddLoan.set_sensitive(not data.loan_list.get_player_listed(self.player))
        self.menuitemRemoveLoan.set_sensitive(data.loan_list.get_player_listed(self.player))
        self.menuitemNotForSale.set_active(self.player.not_for_sale)

    def show(self):
        self.update_sensitivity()
        self.show_all()


class ContextMenu2(Gtk.Menu):
    '''
    Context menu for players out of contract or contracted to other clubs.
    '''
    def __init__(self):
        Gtk.Menu.__init__(self)

        menuitem = uigtk.widgets.MenuItem("_Player Information")
        menuitem.connect("activate", self.on_player_information_clicked)
        self.append(menuitem)

        separator = Gtk.SeparatorMenuItem()
        self.append(separator)

        self.menuitemPurchase = uigtk.widgets.MenuItem("Make Offer To _Purchase")
        self.menuitemPurchase.connect("activate", self.on_purchase_offer_clicked)
        self.append(self.menuitemPurchase)
        self.menuitemLoan = uigtk.widgets.MenuItem("Make Offer To _Loan")
        self.menuitemLoan.connect("activate", self.on_loan_offer_clicked)
        self.append(self.menuitemLoan)
        self.menuitemAddShortlist = uigtk.widgets.MenuItem("_Add To Shortlist")
        self.menuitemAddShortlist.connect("activate", self.on_add_to_shortlist_clicked)
        self.append(self.menuitemAddShortlist)
        self.menuitemRemoveShortlist = uigtk.widgets.MenuItem("_Remove From Shortlist")
        self.menuitemRemoveShortlist.connect("activate", self.on_remove_from_shortlist_clicked)
        self.append(self.menuitemRemoveShortlist)

        separator = Gtk.SeparatorMenuItem()
        self.append(separator)

        menuitem = uigtk.widgets.MenuItem("Add To _Comparison")
        menuitem.connect("activate", self.on_comparison_clicked)
        self.append(menuitem)

    def on_player_information_clicked(self, *args):
        '''
        Launch player information screen for selected player.
        '''
        data.window.screen.change_visible_screen("playerinformation")
        data.window.screen.active.set_visible_player(self.player)

    def on_purchase_offer_clicked(self, *args):
        '''
        Initiate purchase offer of selected player.
        '''
        data.negotiations.initialise_purchase(self.player)

    def on_loan_offer_clicked(self, *args):
        '''
        Initiate loan offer of selected player.
        '''
        data.negotiations.initialise_loan(self.player)

    def on_add_to_shortlist_clicked(self, *args):
        '''
        Add player to shortlist.
        '''
        data.user.club.shortlist.add_to_shortlist(self.player)
        self.update_sensitivity()

    def on_remove_from_shortlist_clicked(self, *args):
        '''
        Remove player from shortlist.
        '''
        dialog = uigtk.shortlist.RemoveShortlist()

        if dialog.show(self.player):
            data.user.club.shortlist.remove_from_shortlist(self.player)
            self.update_sensitivity()

    def on_comparison_clicked(self, *args):
        '''
        Add player to stack for comparison.
        '''
        data.comparison.add_to_comparison(self.player)

    def update_sensitivity(self):
        '''
        Update menu item sensitivity for available options.
        '''
        sensitive = data.user.club.shortlist.get_player_in_shortlist(self.player)
        self.menuitemAddShortlist.set_sensitive(not sensitive)
        self.menuitemRemoveShortlist.set_sensitive(sensitive)

        if self.player.club:
            self.menuitemPurchase.set_label("Make Offer to _Purchase")
            self.menuitemLoan.set_sensitive(True)
        else:
            self.menuitemPurchase.set_label("Make Offer to _Sign")
            self.menuitemLoan.set_sensitive(False)

    def show(self):
        self.update_sensitivity()
        self.show_all()
