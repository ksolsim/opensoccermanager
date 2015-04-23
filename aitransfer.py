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

import constants
import display
import game
import transfer


def identify():
    for clubid, club in game.clubs.items():
        if clubid != game.teamid:
            position = random.choice(constants.positions)

            other_average = 0
            squad_average = 0
            selected = 0

            potential = []

            for count, playerid in enumerate(game.clubs[clubid].squad, start=1):
                player = game.players[playerid]

                if position == player.position:
                    skills = player.skills()
                    squad_average += sum(skills) / count

                    if position == "GK":
                        squad_average = skills[0] * 2
                    elif position in ("DL", "DR", "DC", "D"):
                        squad_average = skills[1] * 2
                    elif position in ("ML", "MR", "MC", "M"):
                        squad_average = skills[2] * 2
                    elif position in ("AF", "AS"):
                        squad_average = skills[3] * 2

            for playerid, player in game.players.items():
                if position == player.position:
                    skills = player.skills()
                    other_average += sum(skills) / count

                    if position == "GK":
                        other_average = skills[0] * 2
                    elif position in ("DL", "DR", "DC", "D"):
                        other_average = skills[1] * 2
                    elif position in ("ML", "MR", "MC", "M"):
                        other_average = skills[2] * 2
                    elif position in ("AF", "AS"):
                        other_average = skills[3] * 2

                    if other_average > squad_average + 0 and other_average < squad_average + 100:
                        potential.append(playerid)

            if len(potential) > 0:
                playerid = random.choice(potential)

                game.negotiations[game.negotiationid] = Negotiation()
                game.negotiations[game.negotiationid].playerid = playerid
                game.negotiations[game.negotiationid].club = clubid
                game.negotiations[game.negotiationid].enquiry_initialise()
                game.negotiationid += 1

    print(game.negotiations)


class Negotiation:
    def __init__(self):
        self.playerid = 0
        self.status = 0
        self.timeout = 0
        self.transfer_type = 0
        self.club = 0
        self.date = "%i/%i/%i" % (game.year, game.month, game.date)

    def enquiry_initialise(self):
        '''
        Initiate the enquiry from the buying club.
        '''
        self.timeout = random.randint(1, 4)

    def enquiry_response(self):
        '''
        Determine the response whether the selling club is willing to part with
        the player.
        '''

    def offer_initialise(self):
        '''
        Set the offer details for the transfer.
        '''
        self.timeout = random.randint(1, 4)

    def offer_response(self):
        '''
        Selling club response to the offer for the player.
        '''

    def contract_initialise(self):
        '''
        Offer a contract to the player (transfer or free transfer only).
        '''
        self.timeout = random.randint(1, 4)

    def contract_response(self):
        '''
        Player response to the contract offer.
        '''

    def complete_transfer(self):
        '''
        Finialise the transfer move.
        '''

    def cancel_transfer(self):
        '''
        End the transfer negotiations and cleanup details.
        '''

    def update(self):
        '''
        Update the transfer status for negotiation.
        '''
        if self.timeout > 0:
            self.timeout -= 1
