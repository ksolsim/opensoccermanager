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


import random

import data
import uigtk.negotiations


class TransferStatus:
    def __init__(self):
        self.inbound = {0: "Awaiting response to your enquiry",
                        1: "Enquiry rejected by club",
                        2: "Enquiry accepted by club",
                        3: "Awaiting response to your offer",
                        4: "Offer rejected by club",
                        5: "Offer accepted by club",
                        6: "Awaiting reponse to your contract offer",
                        7: "Offer rejected by player",
                        8: "Offer accepted by player",
                        9: "Enquiry rejected by player",
                        10: "Enquiry accepted by player"}

        self.outbound = {0: "Awaiting your response to enquiry",
                         1: "Awaiting offer from club",
                         2: "Awaiting your response to offer",
                         3: "Player is negotiating with club",
                         4: "Player has accepted the offer",
                         5: "Player has rejected the offer"}

    def get_inbound_status(self, statusid):
        '''
        Return inbound status message for given status id.
        '''
        return self.inbound[statusid]

    def get_outbound_status(self, statusid):
        '''
        Return outbound status message for given status id.
        '''
        return self.outbound[statusid]


class Negotiations:
    def __init__(self):
        self.negotiations = {}
        self.negotiationid = 0

    def get_negotiationid(self):
        '''
        Return unqiue negotiation id.
        '''
        self.negotiationid += 1

        return self.negotiationid

    def get_negotiation_by_id(self, negotiationid):
        '''
        Return negotiation object for given negotiation id.
        '''
        return self.negotiations[negotiationid]

    def get_player_in_negotiations(self, player):
        '''
        Return whether the given player id is already in transfer negotiations.
        '''
        status = False

        for negotiation in self.negotiations.values():
            if player.playerid == negotiation.player.playerid:
                if data.user.clubid == negotiation.club.clubid:
                    uigtk.negotiations.InProgress()
                    status = True

        return status

    def update_negotiations(self):
        '''
        Update countdown on negotiations in progress.
        '''
        for negotiation in self.negotiations.values():
            negotiation.timeout -= 1

            if negotiation.timeout == 0:
                if negotiation.transfer_type == 0:
                    self.update_purchases(negotiation)
                elif negotiation.transfer_type == 1:
                    self.update_loans(negotiation)
                elif negotiation.transfer_type == 2:
                    self.update_free_transfers(negotiation)

    def update_purchases(self, negotiation):
        '''
        Update status of purchase from player or club response.
        '''
        if negotiation.statusid == 0:
            if negotiation.consider_enquiry():
                negotiation.statusid = 2
            else:
                negotiation.statusid = 1
        elif negotiation.statusid == 3:
            if negotiation.consider_offer():
                negotiation.statusid = 5
            else:
                negotiation.statusid = 4
        elif negotiation.statusid == 6:
            if negotiation.consider_contract():
                negotiation.statusid = 8
            else:
                negotiation.statusid = 7

    def update_loans(self, negotiation):
        '''
        Update status of loan from club response.
        '''
        if negotiation.statusid == 0:
            if negotiation.consider_enquiry():
                negotiation.statusid = 2
            else:
                negotiation.statusid = 1
        elif negotiation.statusid == 3:
            if negotiation.consider_offer():
                negotiation.statusid = 5
            else:
                negotiation.statusid = 4

    def update_free_transfers(self, negotiation):
        '''
        Update status of free transfer from player response.
        '''
        if negotiation.statusid == 0:
            if negotiation.consider_enquiry():
                negotiation.statusid = 10
            else:
                negotiation.statusid = 9
        elif negotiation.statusid == 6:
            if negotiation.consider_contract():
                negotiation.statusid = 8
            else:
                negotiation.statusid = 7

    def initialise_purchase(self, player):
        '''
        Create purchase transfer negotiation object.
        '''
        if not self.get_player_in_negotiations(player):
            if player.club:
                dialog = uigtk.negotiations.PurchaseEnquiry()
                state = dialog.show(player)
            else:
                dialog = uigtk.negotiations.FreeEnquiry()
                state = dialog.show(player)

            if state:
                negotiationid = self.get_negotiationid()

                if player.club:
                    negotiation = PurchaseNegotiation(negotiationid, player)
                else:
                    negotiation = FreeNegotiation(negotiationid, player)

                negotiation.club = data.user.club
                self.negotiations[negotiationid] = negotiation

                data.user.club.shortlist.add_to_shortlist(player)

    def initialise_loan(self, player):
        '''
        Create loan transfer negotiation object.
        '''
        if not self.get_player_in_negotiations(player):
            dialog = uigtk.negotiations.LoanEnquiry()

            if dialog.show(player) == 1:
                negotiationid = self.get_negotiationid()

                negotiation = LoanNegotiation(negotiationid, player)
                negotiation.club = data.user.club
                self.negotiations[negotiationid] = negotiation

                data.user.club.shortlist.add_to_shortlist(player)

    def end_negotiation(self, negotiation):
        '''
        Remove negotiation for passed negotiation id.
        '''
        del self.negotiations[negotiation.negotiationid]

    def get_user_incoming(self):
        '''
        Return dict of players which the user is negotiating to purchase/loan.
        '''
        incoming = {}

        for negotiationid, negotiation in self.negotiations.items():
            if negotiation.club.clubid == data.user.clubid:
                incoming[negotiationid] = negotiation

        return incoming.items()

    def get_user_outgoing(self):
        '''
        Return dict of players which the user is negotiating to sell/loan.
        '''
        outgoing = {}

        for negotiationid, negotiation in self.negotiations.items():
            if negotiation.club.clubid != data.user.clubid:
                outgoing[negotationid] = negotation

        return outgoing.items()


class Negotiation:
    def __init__(self, negotiationid, player):
        self.negotiationid = negotiationid
        self.player = player
        self.club = None
        self.offer_date = data.date.get_date_as_string()
        self.statusid = 0
        self.status = TransferStatus()

        self.update_timeout()

    def set_status(self, statusid):
        '''
        Set status id and update timeout.
        '''
        self.statusid = statusid
        self.update_timeout()

    def get_status_message(self):
        '''
        Retrieve current transfer status message for given status id.
        '''
        if self.club.clubid == data.user.clubid:
            return self.status.get_inbound_status(self.statusid)
        else:
            return self.status.get_outbound_status(self.statusid)

    def update_timeout(self):
        '''
        Set new timeout counter.
        '''
        self.timeout = random.randint(3, 8)

    def respond_to_negotiation(self):
        '''
        Handle user wanting a response to negotiation.
        '''
        if self.transfer_type == 0:
            self.respond_to_purchase()
        elif self.transfer_type == 1:
            self.respond_to_loan()
        elif self.transfer_type == 2:
            self.respond_to_free_transfer()


class PurchaseNegotiation(Negotiation):
    def __init__(self, negotiationid, player):
        Negotiation.__init__(self, negotiationid, player)
        self.transfer_type = 0

    def respond_to_purchase(self):
        '''
        Handle response for purchase transfer types.
        '''
        if self.statusid == 1:
            uigtk.negotiations.EnquiryRejection(self)
            data.negotiations.end_negotiation(self)
        elif self.statusid == 4:
            uigtk.negotiations.OfferRejection(self)
            data.negotiations.end_negotiation(self)
        elif self.statusid == 7:
            uigtk.negotiations.ContractRejection(self)
            data.negotiations.end_negotiation(self)
        elif self.statusid in (0, 3, 6):
            uigtk.negotiations.AwaitingResponse(self)
        elif self.statusid == 2:
            dialog = uigtk.negotiations.PurchaseOffer(self)
            amount = dialog.show()

            if amount:
                self.amount = amount
                self.set_status(3)
            else:
                data.negotiations.end_negotiation(self)
        elif self.statusid == 5:
            dialog = uigtk.negotiations.ContractNegotiation(self)
            dialog.player = self.player

            if dialog.show():
                self.set_status(6)
            else:
                data.negotiations.end_negotiation(self)
        elif self.statusid == 8:
            dialog = uigtk.negotiations.CompleteTransfer(self)

            if dialog.show():
                self.complete_purchase()

    def consider_enquiry(self):
        '''
        Determine whether parent club wishes to negotiate for player.
        '''
        status = False

        if data.purchase_list.get_player_listed(self.player):
            status = True

        if status:
            data.user.club.news.publish("PT02",
                                        player=self.player.get_name(mode=1),
                                        team=self.player.club.name)
        else:
            data.user.club.news.publish("PT01",
                                        player=self.player.get_name(mode=1),
                                        team=self.player.club.name)

        if not status:
            status = random.choice((True, False))

        return status

    def consider_offer(self):
        '''
        Determine whether parent club wishes to agree to the offer.
        '''
        status = False

        if data.purchase_list.get_player_listed(self.player):
            if self.amount >= self.player.value.get_value() * round(random.uniform(0.85, 0.99), 2):
                status = True

        if not status:
            status = random.choice((True, False))

        if status:
            data.user.club.news.publish("PT04",
                                        player=self.player.get_name(mode=1),
                                        team=self.player.club.name)
        else:
            data.user.club.news.publish("PT03",
                                        player=self.player.get_name(mode=1),
                                        team=self.player.club.name)

        return status

    def consider_contract(self):
        '''
        Determine whether player wishes to move clubs.
        '''
        status = random.choice((True, False))

        if status:
            data.user.club.news.publish("PT06",
                                        player=self.player.get_name(mode=1),
                                        team=self.player.club.name)
        else:
            data.user.club.news.publish("PT05",
                                        player=self.player.get_name(mode=1),
                                        team=self.player.club.name)

        return status

    def complete_transfer(self):
        '''
        Complete purchase transfer of player.
        '''
        print(self.player.get_name())

        if self.club.accounts.request(self.offer):
            self.club.accounts.withdraw(amount=self.offer, category="transfers")


class LoanNegotiation(Negotiation):
    def __init__(self, negotiationid, player):
        Negotiation.__init__(self, negotiationid, player)
        self.transfer_type = 1

    def respond_to_loan(self):
        '''
        Handle response for loan transfer types.
        '''
        if self.statusid == 1:
            uigtk.negotiations.EnquiryRejection(self)
            data.negotiations.end_negotiation(self)
        elif self.statusid == 4:
            uigtk.negotiations.OfferRejection(self)
            data.negotiations.end_negotiation(self)
        elif self.statusid in (0, 3):
            uigtk.negotiations.AwaitingResponse(self)
        elif self.statusid == 2:
            dialog = uigtk.negotiations.LoanOffer(self)

            if dialog.show():
                self.set_status(3)
            else:
                data.negotiations.end_negotiation(self)
        elif self.statusid == 5:
            dialog = uigtk.negotiations.CompleteTransfer(self)

            if dialog.show():
                print("Complete move")

    def consider_enquiry(self):
        '''
        Determine whether parent club wishes to negotiation for player.
        '''
        status = False

        if data.loan_list.get_player_listed(self.player):
            status = True

        if status:
            data.user.club.news.publish("LT02",
                                        player=self.player.get_name(mode=1),
                                        team=self.player.club.name)
        else:
            data.user.club.news.publish("LT01",
                                        player=self.player.get_name(mode=1),
                                        team=self.player.club.name)

        if not status:
            status = random.choice((True, False))

        return status

    def consider_offer(self):
        '''
        Determine whether parent club wishes to agree to the offer.
        '''
        return random.choice((True, False))

    def complete_transfer(self):
        '''
        Complete loan of player.
        '''
        print(self.player.get_name())


class FreeNegotiation(Negotiation):
    def __init__(self, negotiationid, player):
        Negotiation.__init__(self, negotiationid, player)
        self.transfer_type = 2

    def respond_to_free_transfer(self):
        '''
        Handle response for free transfer types.
        '''
        if self.statusid == 9:
            uigtk.negotiations.EnquiryRejection(self)
            data.negotiations.end_negotiation(self)
        elif self.statusid == 7:
            uigtk.negotiations.ContractRejection(self)
            data.negotiations.end_negotiation(self)
        elif self.statusid in (0, 3):
            uigtk.negotiations.AwaitingResponse(self)
        elif self.statusid == 10:
            dialog = uigtk.negotiations.ContractNegotiation(self)
            dialog.player = self.player

            if dialog.show():
                self.set_status(6)
            else:
                data.negotiations.end_negotiation(self)
        elif self.statusid == 8:
            dialog = uigtk.negotiations.CompleteTransfer(self)

            if dialog.show():
                print("Complete move")

    def consider_enquiry(self):
        '''
        Determine whether player wishes to negotiation contract.
        '''
        status = random.choice((True, False))

        if status:
            data.user.club.news.publish("FT02",
                                        player=self.player.get_name(mode=1))
        else:
            data.user.club.news.publish("FT01",
                                        player=self.player.get_name(mode=1))

        return status

    def consider_contract(self):
        '''
        Determine whether player wishes to move clubs.
        '''
        status = random.choice((True, False))

        if status:
            data.user.club.news.publish("FT04",
                                        player=self.player.get_name(mode=1))
        else:
            data.user.club.news.publish("FT03",
                                        player=self.player.get_name(mode=1))

        return status

    def complete_transfer(self):
        '''
        Complete free transfer of player.
        '''
        print(self.player.get_name())
