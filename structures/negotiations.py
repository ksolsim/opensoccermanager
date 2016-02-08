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

    def get_player_in_negotiations(self, playerid):
        '''
        Return whether the given player id is already in transfer negotiations.
        '''
        status = False

        for negotiation in self.negotiations.values():
            if playerid == negotiation.playerid:
                if data.user.team == negotiation.clubid:
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

    def initialise_purchase(self, playerid):
        '''
        Create purchase transfer negotiation object.
        '''
        if not self.get_player_in_negotiations(playerid):
            dialog = uigtk.negotiations.PurchaseApproach()

            player = data.players.get_player_by_id(playerid)
            club = data.clubs.get_club_by_id(player.squad)

            if dialog.show(club, player) == 1:
                negotiationid = self.get_negotiationid()

                negotiation = Negotiation(negotiationid, playerid)
                negotiation.clubid = data.user.team
                self.negotiations[negotiationid] = negotiation

                club = data.clubs.get_club_by_id(data.user.team)
                club.shortlist.add_to_shortlist(playerid)

    def initialise_loan(self, playerid):
        '''
        Create loan transfer negotiation object.
        '''
        if not self.get_player_in_negotiations(playerid):
            dialog = uigtk.negotiations.LoanApproach()

            player = data.players.get_player_by_id(playerid)
            club = data.clubs.get_club_by_id(player.squad)

            if dialog.show(club, player) == 1:
                negotiationid = self.get_negotiationid()

                negotiation = Negotiation(negotiationid, playerid)
                negotiation.clubid = data.user.team
                negotiation.transfer_type = 1
                self.negotiations[negotiationid] = negotiation

                club = data.clubs.get_club_by_id(data.user.team)
                club.shortlist.add_to_shortlist(playerid)

    def end_negotiation(self, negotiationid):
        '''
        Call negotiation for passed negotiation id.
        '''
        del self.negotiations[negotiationid]

    def get_user_incoming(self):
        '''
        Return dict of players which the user is negotiating to purchase/loan.
        '''
        incoming = {}

        for negotiationid, negotiation in self.negotiations.items():
            if negotiation.clubid == data.user.team:
                incoming[negotiationid] = negotiation

        return incoming.items()

    def get_user_outgoing(self):
        '''
        Return dict of players which the user is negotiating to sell/loan.
        '''
        outgoing = {}

        for negotiationid, negotiation in self.negotiations.items():
            if negotiation.clubid != data.user.team:
                outgoing[negotationid] = negotation

        return outgoing.items()


class Negotiation:
    def __init__(self, negotiationid, playerid):
        self.negotiationid = negotiationid
        self.playerid = playerid
        self.clubid = None
        self.transfer_type = 0
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
        if self.clubid == data.user.team:
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
        player = data.players.get_player_by_id(self.playerid)
        club = data.clubs.get_club_by_id(player.squad)

        if self.statusid in (1, 4, 7):
            uigtk.negotiations.NegotiationRejected()
        elif self.statusid in (0, 3, 6):
            uigtk.negotiations.AwaitingResponse(player, club)
        elif self.statusid == 2:
            dialog = uigtk.negotiations.PurchaseOffer(player, club)

            if dialog.show():
                self.set_status(3)
                Negotiations.inbound.populate_data(data.negotiations.get_user_incoming())
            else:
                data.negotiations.end_negotiation(self.negotiationid)
        elif self.statusid == 5:
            dialog = uigtk.negotiations.ContractNegotiation(self.playerid)

            if dialog.show() == 1:
                self.set_status(6)
            else:
                data.negotiations.end_negotiation(self.negotiationid)

    def consider_enquiry(self):
        '''
        Determine whether parent club wishes to negotiate for player.
        '''
        return random.choice((True, False))

    def consider_offer(self):
        '''
        Determine whether parent club wishes to agree to the offer.
        '''
        return random.choice((True, False))

    def consider_contract(self):
        '''
        Determine whether player wishes to move clubs.
        '''
        return random.choice((True, False))
