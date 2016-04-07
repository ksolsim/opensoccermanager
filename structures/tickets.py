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

        self.school_tickets = 100

        self.season_tickets = 40
        self.season_tickets_available = True

    def get_ticket_prices(self):
        '''
        Return nested list of ticket prices.
        '''
        return self.tickets.categories

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
        self.school_tickets = 100 * (int((20 - data.user.club.reputation) * 0.5) + 1)

    def set_initial_season_tickets(self):
        '''
        Return percentage capacity allocted to season tickets.
        '''
        self.season_tickets = 40 + data.user.club.reputation

    def toggle_season_ticket_availability(self):
        '''
        Switch between season tickets available or not.
        '''
        self.season_tickets_available = not self.season_tickets_available

    def check_season_ticket_availability(self):
        '''
        Disable season ticket availability for season.
        '''
        if data.date.get_date_for_event() == (16, 8):
            self.toggle_season_ticket_availability()

            self.calculate_season_tickets()

    def calculate_season_tickets(self):
        '''
        Determine number of season tickets sold in pre-season.
        '''
        capacity = data.user.club.stadium.get_capacity() - data.user.club.stadium.get_box_capacity() - self.school_tickets

        # Calculate season ticket sales
        available = (capacity * 0.01) * self.season_tickets

        total = 0

        if data.user.club.stadium.get_standing_uncovered():
            capacity = (data.user.club.stadium.get_standing_uncovered_capacity() * 0.01) * self.season_tickets
            total += self.get_ticket_prices()[0].prices[2] * capacity

        if data.user.club.stadium.get_standing_covered():
            capacity = (data.user.club.stadium.get_standing_covered_capacity() * 0.01) * self.season_tickets
            total += self.get_ticket_prices()[1].prices[2] * capacity

        if data.user.club.stadium.get_seating_uncovered():
            capacity = (data.user.club.stadium.get_seating_uncovered_capacity() * 0.01) * self.season_tickets
            total += self.get_ticket_prices()[2].prices[2] * capacity

        if data.user.club.stadium.get_seating_covered():
            capacity = (data.user.club.stadium.get_seating_covered_capacity() * 0.01) * self.season_tickets
            total += self.get_ticket_prices()[3].prices[2] * capacity

        # Calculate box season ticket sales
        sales = (data.user.club.stadium.get_box_capacity() * 0.01) * self.season_tickets

        box = self.get_ticket_prices()[4]
        total += sales * box.prices[2]

        data.user.club.accounts.deposit(amount=total, category="tickets")


class TicketCategories:
    def __init__(self):
        self.categories = [None] * 5

    def set_ticket_price(self, index1, index2, amount):
        '''
        Set passed amount on ticket type.
        '''
        self.categories[index1].set_price(index2, amount)

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
        self.set_initial_prices(multiplier)

    def set_initial_prices(self, multiplier):
        '''
        Set initial ticket prices for league, cup, and season tickets.
        '''
        prices = [multiplier + data.user.club.reputation,
                  multiplier + data.user.club.reputation + (data.user.club.reputation * 0.25),
                  (multiplier + data.user.club.reputation) * 15]

        self.prices = list(map(int, prices))
        self.base = list(map(int, prices))

    def set_price(self, index, amount):
        '''
        Set amount as price for given index.
        '''
        self.prices[index] = int(amount)
