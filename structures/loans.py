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
