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


class Contract:
    def __init__(self, player):
        self.player = player

        self.leaguechamp = 0
        self.leaguerunnerup = 0
        self.winbonus = 0
        self.goalbonus = 0

        self.contract = random.randint(24, 260)

        self.set_initial_bonus()

    def set_initial_bonus(self):
        '''
        Set initial bonus amounts based on starting player wage.
        '''
        self.leaguechamp = self.player.wage.get_wage() * 10
        self.leaguerunnerup = self.player.wage.get_wage() * 2
        self.goalbonus = self.player.wage.get_wage() * 0.1
        self.winbonus = self.player.wage.get_wage() * 0.1

    def get_bonus(self, index):
        '''
        Return player bonus value for given bonus index.
        '''
        bonuses = (self.leaguechamp, self.leaguerunnerup, self.goalbonus, self.winbonus)
        bonus = data.currency.get_rounded_amount(bonuses[index])

        return bonus

    def get_contract(self):
        '''
        Format the number of weeks on the contract remaining and return.
        '''
        if self.contract > 1:
            contract = "%i Weeks" % (self.contract)
        elif self.contract == 1:
            contract = "%i Week" % (self.contract)
        elif self.contract == 0:
            contract = "Out of Contract"

        return contract

    def get_contract_renewal(self):
        '''
        Grab details for renewal of contract.
        '''
        return self.player.wage.calculate_wage()

    def set_contract(self, contract):
        '''
        Define contract details for player from passed contract tuple.
        '''
        self.leaguechamp = contract[0]
        self.leaguerunnerup = contract[1]
        self.winbonus = contract[2]
        self.goalbonus = contract[3]

    def set_contract_length(self, length):
        '''
        Define length of contract in weeks from passed year value.
        '''
        self.contract = length * 52

    def get_termination_payout(self):
        '''
        Get the amount the player is owed if his contract is terminated.
        '''
        return self.contract * self.player.wage.get_wage()

    def terminate_contract(self):
        '''
        Run calls to terminate contract of player and cleanup actions.
        '''
        self.contract = 0

        club = data.clubs.get_club_by_id(self.player.squad)
        club.squad.remove_from_squad(self.player.playerid)
        club.individual_training.remove_from_training(self.player.playerid)

        self.player.squad = None

        self.player.transfer = [False, False]

    def decrement_contract_period(self):
        '''
        Decrease number of weeks remaining on contract.
        '''
        if self.contract > 0:
            self.contract -= 1

            club = data.clubs.get_club_by_id(data.user.team)

            if self.contract in (4, 8, 12):
                if self.player.squad == data.user.team:
                    club.news.publish("PC02", player=self.player.get_name(mode=1), weeks=self.contract)
            elif self.contract == 0:
                if self.player.squad == data.user.team:
                    club.news.publish("PC01", player=self.player.get_name(mode=1))
                elif club.shortlist.get_player_in_shortlist(self.player.playerid):
                    club.news.publish("SH01", player=self.player.get_name(mode=1))
