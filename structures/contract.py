#!/usr/bin/env python3

import random


class Contract:
    def __init__(self):
        self.wage = 0

        self.leaguechamp = 0
        self.leaguerunnerup = 0
        self.goalbonus = 0
        self.winbonus = 0

        self.contract = random.randint(24, 260)

    def set_initial_wage(self, wage):
        '''
        Set initial wage values at beginning of the game.
        '''
        self.wage = wage

        self.leaguechamp = wage * 10
        self.leaguerunnerup = wage * 2
        self.goalbonus = wage * 0.1
        self.winbonus = wage * 0.1

    def get_wage(self):
        '''
        Fetch the player wage and return with appropriate currency.
        '''
        if self.wage >= 1000:
            wage = "£%.1fK" % (self.wage / 1000)
        elif self.wage >= 100:
            wage = "£%i" % (self.wage)

        return wage

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
