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


import calculator
import game
import stadium
import user


class Tickets:
    def __init__(self):
        self.tickets = [0] * 15

        self.season_tickets = 0
        self.season_tickets_available = True

        self.school_tickets = 0

    def calculate_season_tickets(self):
        '''
        Determine number of season tickets to be sold prior to first game.
        '''
        club = user.get_user_club()
        stadiumobj = stadium.get_stadium(club.stadium)

        capacity = stadiumobj.get_capacity()

        max_season_tickets = (capacity * 0.01) * self.season_tickets

        base_tickets = self.get_ticket_prices()
        minmax = base_tickets[11] * 0.1

        upper = minmax + base_tickets[11]
        lower = base_tickets[11] - minmax

        if self.tickets[11] > upper:
            diff = (self.tickets[11] - base_tickets[11]) / minmax
            sold = (capacity * 0.01 * self.season_tickets) / diff
        elif self.tickets[11] < lower:
            diff = (base_tickets[11] - self.tickets[11]) / minmax
            sold = ((capacity * 0.01) * (self.season_tickets * (10 / diff)))
        else:
            sold = max_season_tickets

        if sold > max_season_tickets:
            sold = max_season_tickets

        sales = sold * self.tickets[11]

        capacity = 0

        for stand in stadiumobj.main:
            capacity += stand.box

        box_sales = (capacity * 0.01) * self.season_tickets * self.tickets[14]

        total = sales + box_sales

        club.accounts.deposit(amount=total, category="tickets")

    def get_ticket_prices(self):
        club = user.get_user_club()

        tickets = [0] * 15

        tickets[0] = 1 + club.reputation
        tickets[1] = 1 + club.reputation + (club.reputation * 0.25)
        tickets[2] = (1 + club.reputation) * 15
        tickets[3] = 2 + club.reputation
        tickets[4] = 2 + club.reputation + (club.reputation * 0.25)
        tickets[5] = (2 + club.reputation) * 15
        tickets[6] = 3 + club.reputation
        tickets[7] = 3 + club.reputation + (club.reputation * 0.25)
        tickets[8] = (3 + club.reputation) * 15
        tickets[9] = 4 + club.reputation
        tickets[10] = 4 + club.reputation + (club.reputation * 0.25)
        tickets[11] = (4 + club.reputation) * 15
        tickets[12] = 30 + club.reputation
        tickets[13] = 30 + club.reputation + (club.reputation * 0.25)
        tickets[14] = (30 + club.reputation) * 15

        tickets = list(map(int, tickets))

        return tickets


def calculate_matchday_tickets(attendance):
    '''
    Determine the number of tickets sold on matchday.
    '''
    for club in game.clubs.values():
        stadium = game.stadiums[club.stadium]

        percentage = 100 - club.tickets.season_tickets

        amount = 0

        # Calculate sales
        capacity = [0, 0, 0, 0]

        for stand in stadium.main:
            if not stand.seating and not stand.roof:
                capacity[0] += stand.capacity
            elif not stand.seating and stand.roof:
                capacity[1] += stand.capacity
            elif stand.seating and not stand.roof:
                capacity[2] += stand.capacity
            elif stand.seating and stand.roof:
                capacity[3] += stand.capacity

        for stand in stadium.corner:
            if not stand.seating and not stand.roof:
                capacity[0] += stand.capacity
            elif not stand.seating and stand.roof:
                capacity[1] += stand.capacity
            elif stand.seating and not stand.roof:
                capacity[2] += stand.capacity
            elif stand.seating and stand.roof:
                capacity[3] += stand.capacity

        for count, value in enumerate(capacity):
            available = (percentage * 0.01) * value

            amount += club.tickets.tickets[count * 3] * available

        # Calculate box sales
        capacity = 0

        for stand in stadium.main:
            capacity += stand.box

        available = (percentage * 0.01) * capacity
        amount += club.tickets.tickets[12] * available

        club.accounts.deposit(amount=amount, category="tickets")
