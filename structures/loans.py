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
    def __init__(self):
        self.loans = []

    def complete_loan(self, player, club, period):
        '''
        Complete loan transfer and join new club.
        '''
        loan = Loan(player, period)

        player.club.loan_out.add_loan_out(loan)
        club.loans_in.add_loan_in(loan)

        self.loans.append(loan)

    def extend_loan(self, player):
        '''
        Query loan extension for given player.
        '''

    def end_loan(self, player):
        '''
        End the loan contract and return player to parent club.
        '''
        self.loans.remove(player.playerid)

    def update_loans(self):
        '''
        Update loan object and return any players at end of their loan spell.
        '''
        for loan in self.loans:
            loan.period -= 1

            if loan.period in (4, 8, 12):
                data.user.club.news.publish("LA01",
                                            player=loan.player.get_name(mode=1),
                                            weeks=loan.period)
            elif loan.period == 0:
                self.end_loan()

    def get_player_on_loan(self, player):
        '''
        Return whether player is on loan.
        '''
        for loan in self.loans:
            if player is loan.player:
                return True

        return False


class Loan:
    '''
    Loan attribute information object.
    '''
    def __init__(self, player, period):
        self.player = player
        self.club = player.club

        self.period = period


class LoansIn:
    '''
    Players that have been loaned by the club from other clubs.
    '''
    def __init__(self):
        self.loans = []

    def add_loan_in(self, loan):
        self.loans.append(loan)


class LoansOut:
    '''
    Players that have been loaned out by the club to other clubs.
    '''
    def __init__(self):
        self.loans = []

    def add_loan_out(self):
        self.loans.append(loan)
