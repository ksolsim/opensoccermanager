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

import calculator
import constants
import game
import money


def season_tickets():
    '''
    Determine number of season tickets to be sold prior to first game of
    the season, and calculate the amount of income from those sales.
    '''
    club = game.clubs[game.teamid]
    stadium = game.stadiums[club.stadium]

    capacity = 0

    for stand in stadium.main:
        capacity += stand.capacity

    for stand in stadium.corner:
        capacity += stand.capacity

    max_season_tickets = (capacity * 0.01) * club.season_tickets

    base_tickets = calculator.ticket_prices()
    minmax = base_tickets[11] * 0.1

    upper = minmax + base_tickets[11]
    lower = base_tickets[11] - minmax

    if club.tickets[11] > upper:
        diff = (club.tickets[11] - base_tickets[11]) / minmax
        sold = (capacity * 0.01 * club.season_tickets) / diff
    elif club.tickets[11] < lower:
        diff = (base_tickets[11] - club.tickets[11]) / minmax
        sold = ((capacity * 0.01) * (club.season_tickets * (10 / diff)))
    else:
        sold = max_season_tickets

    if sold > max_season_tickets:
        sold = max_season_tickets

    sales = sold * club.tickets[11]

    capacity = 0

    for stand in stadium.main:
        capacity += stand.box

    box_sales = (capacity * 0.01) * club.season_tickets * club.tickets[14]

    total = sales + box_sales

    club.accounts.deposit(total, "tickets")


def matchday_tickets(attendance):
    club = game.clubs[game.teamid]
    stadium = game.stadiums[club.stadium]

    percentage = 100 - club.season_tickets

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

        amount += club.tickets[count * 3] * available

    # Calculate box sales
    capacity = 0

    for stand in stadium.main:
        capacity += stand.box

    available = (percentage * 0.01) * capacity
    amount += club.tickets[12] * available

    club.accounts.deposit(total, "tickets")


def merchandise(attendance):
    club = game.clubs[game.teamid]
    club.sales[0] = []

    for count, profit_percentage in enumerate(club.merchandise):
        multiplier = constants.merchandise[count][2]
        multiplier += random.randint(-3, 3)

        potential_sales = attendance * (multiplier * 0.01)
        sale_percentage = 200 - profit_percentage

        if sale_percentage < 0:
            sale_percentage = 0

        sales = int((potential_sales * 0.25 * 0.01) * sale_percentage)

        income = sales * (constants.merchandise[count][1] + (constants.merchandise[count][1] * (profit_percentage * 0.01)))
        profit = income - (sales * constants.merchandise[count][1])
        cost = income - profit

        club.sales[0].append([sales, income, profit])

        club.accounts.deposit(total, "merchandise")
        club.accounts.withdraw(cost, "merchandise")


def catering(attendance):
    club = game.clubs[game.teamid]
    club.sales[1] = []

    for count, profit_percentage in enumerate(club.catering):
        multiplier = constants.catering[count][2]
        multiplier += random.randint(-3, 3)

        potential_sales = attendance * (multiplier * 0.01)
        sale_percentage = 200 - profit_percentage

        if sale_percentage < 0:
            sale_percentage = 0

        sales = int((potential_sales * 0.25 * 0.01) * sale_percentage)

        income = sales * (constants.catering[count][1] + (constants.catering[count][1] * (profit_percentage * 0.01)))
        profit = income - (sales * constants.catering[count][1])
        cost = income - profit

        club.sales[1].append([sales, income, profit])

        club.accounts.deposit(total, "catering")
        club.accounts.withdraw(cost, "catering")
