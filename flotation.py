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


import game


class Flotation:
    def __init__(self):
        self.status = 0
        self.timeout = 0

    def get_float_amount(self):
        '''
        Return the amount raised on floating of club.
        '''
        club = game.clubs[game.teamid]

        amount = club.reputation ** 2 * 100000

        form_affected = amount * 0.25
        amount -= form_affected

        points = 0
        form_length = len(club.form)

        if form_length > 12:
            form_length = 12

        for count in range(0, form_length):
            if club.form[count] == "W":
                points += 3
            elif club.form[count] == "D":
                points += 1

        if form_length >= 6:
            amount += (form_affected / form_length) * ((form_length * 3) - points)

        return amount

    def update_float(self):
        '''
        Countdown timer to flotation completion.
        '''
        if self.timeout > 0:
            self.timeout -= 1
        else:
            self.complete_float()

    def complete_float(self):
        '''
        Complete the flotation procedure.
        '''
        club = game.clubs[game.teamid]

        amount = self.get_float_amount()
        club.accounts.deposit(amount=amount, category=None)
        game.news.publish("FL01")

        self.status = 2

    def start_float(self):
        '''
        Start the procedure for floating the club.
        '''
        self.status = 1
        self.timeout = random.randint(12, 16)

        # Publish news article here
