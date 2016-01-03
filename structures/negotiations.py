#!/usr/bin/env python3

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
    class Negotiation:
        def __init__(self, playerid):
            self.playerid = playerid
            self.clubid = None
            self.transfer_type = 0
            self.offer_date = data.date.get_date_as_string()
            self.statusid = 0
            self.status = TransferStatus()
            self.timeout = random.randint(1, 4)

        def get_status_message(self):
            '''
            Retrieve current transfer status message for given status id.
            '''
            return self.status.get_inbound_status(self.statusid)

    def __init__(self):
        self.negotiations = {}

        self.negotiationid = 0

    def get_negotiationid(self):
        '''
        Return unqiue negotiation id.
        '''
        self.negotiationid += 1

        return self.negotiationid

    def get_negotiation(self, negotiationid):
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

                negotiation = self.Negotiation(playerid)
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

                negotiation = self.Negotiation(playerid)
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

        return incoming

    def get_user_outgoing(self):
        '''
        Return dict of players which the user is negotiating to sell/loan.
        '''
        outgoing = {}

        return outgoing
