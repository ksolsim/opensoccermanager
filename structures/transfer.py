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


class TransferType:
    def __init__(self):
        self.transfer_types = ("Purchase", "Loan", "Free Transfer")

    def get_transfer_types(self):
        '''
        Return list of transfer type strings.
        '''
        return self.transfer_types

    def get_transfer_type_for_index(self, index):
        '''
        Return transfer type string for given index value.
        '''
        return self.transfer_types[index]


class PurchaseList:
    def __init__(self):
        self.listed = []

        self.refresh_purchase_list()

    def refresh_purchase_list(self):
        '''
        Update players listed for purchase.
        '''
        for clubid, club in data.clubs.get_clubs():
            if clubid != data.user.clubid:
                score = {}
                average = 0

                for count, (playerid, player) in enumerate(club.squad.get_squad(), start=1):
                    player = data.players.get_player_by_id(playerid)

                    skills = player.get_skills()
                    score[playerid] = sum(skills) * random.randint(1, 3)

                    average += score[playerid] / count

                for playerid in score:
                    player = data.players.get_player_by_id(playerid)

                    choice = random.choice((False, True))

                    if score[playerid] < average * 0.125 and choice:
                        player.transfer[0] = True


class LoanList:
    def __init__(self):
        self.listed = []

        self.refresh_list()

    def refresh_list(self):
        '''
        Update players listed for loan.
        '''
        for clubid, club in data.clubs.get_clubs():
            if clubid != data.user.clubid:
                score = {}
                average = 0

                for count, (playerid, player) in enumerate(club.squad.get_squad(), start=1):
                    player = data.players.get_player_by_id(playerid)

                    skills = player.get_skills()
                    score[playerid] = sum(skills) * random.randint(1, 3)

                    age = player.get_age()

                    if age < 24:
                        score[playerid] += 24 - age * age

                    average += score[playerid] / count

                for playerid in score:
                    player = data.players.get_player_by_id(playerid)

                    choice = random.choice((False, True))

                    if score[playerid] < average * 0.125 and choice:
                        player.transfer[1] = True
