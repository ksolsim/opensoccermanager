#!/usr/bin/env python3


class Loans:
    class Loan:
        def __init__(self):
            self.playerid = None
            self.period = 0

    def __init__(self):
        self.loans = {}

        self.loanid = 0

    def get_loanid(self):
        self.loanid += 1

        return self.loanid

    def end_loan(self, playerid):
        '''
        End the loan contract and return player to parent club.
        '''

    def on_update(self):
        '''
        Update loan object and return any players at end of their loan spell.
        '''
        for loan in game.loans.values():
            loan.period -= 1
