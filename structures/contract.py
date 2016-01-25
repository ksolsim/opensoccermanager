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


class Contract:
    def __init__(self, player):
        self.player = player

        self.leaguechamp = 0
        self.leaguerunnerup = 0
        self.goalbonus = 0
        self.winbonus = 0

        self.contract = random.randint(24, 260)

        self.set_initial_wage()

    def set_initial_wage(self):
        '''
        Set initial wage values at beginning of the game.
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

        value = bonuses[index]

        if value >= 1000:
            bonus = "£%.1fK" % (value / 1000)
        elif value >= 100:
            bonus = "£%i" % (value)

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

    def set_contract(self, length):
        self.contract = 0

    def get_contract_renewal(self):
        '''
        Grab details for renewal of contract.
        '''
        # Calculate new expected wage for player
        # If new wage is <10% of old wage, ask for 10% rise
        # Determine contract length based on age/morale

    def get_termination_payout(self):
        '''
        Get the amount the player is owed if his contract is terminated.
        '''
        return self.contract * self.wage

    def decrement_contract_period(self):
        self.contract -= 1

        if self.contract == 0:
            print("Out of contract")
