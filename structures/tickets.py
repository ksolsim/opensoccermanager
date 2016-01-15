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


import data


class Tickets:
    def __init__(self):
        self.tickets = TicketCategories()

        self.school_tickets = 0

        self.season_tickets = 0
        self.season_tickets_available = True

    def set_initial_prices(self):
        '''
        Define initial ticket prices used at start of game.
        '''
        self.tickets.add_ticket_price(0, 1)
        self.tickets.add_ticket_price(1, 2)
        self.tickets.add_ticket_price(2, 3)
        self.tickets.add_ticket_price(3, 4)
        self.tickets.add_ticket_price(4, 30)

    def set_initial_school_tickets(self):
        '''
        Set initial number of school tickets to be made available.
        '''
        club = data.clubs.get_club_by_id(data.user.team)
        self.school_tickets = 100 * (int((20 - club.reputation) * 0.5) + 1)

    def set_initial_season_tickets(self):
        '''
        Return percentage capacity allocted to season tickets.
        '''
        club = data.clubs.get_club_by_id(data.user.team)
        self.season_tickets = 40 + club.reputation


class TicketCategories:
    def __init__(self):
        self.categories = [None] * 5

    def add_ticket_price(self, ticket, multiplier):
        '''
        Add ticket price object for stadium category.
        '''
        self.categories[ticket] = TicketPrices(multiplier)

    def remove_ticket_price(self, ticket):
        '''
        Remove passed ticket price category.
        '''
        self.categories[ticket] = None


class TicketPrices:
    def __init__(self, multiplier):
        self.club = data.clubs.get_club_by_id(data.user.team)

        self.prices = [multiplier + self.club.reputation,
                       multiplier + self.club.reputation + (self.club.reputation * 0.25),
                       (multiplier + self.club.reputation) * 15]

        self.prices = list(map(int, self.prices))
