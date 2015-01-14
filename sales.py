#!/usr/bin/env python3

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

    money.deposit(total, 5)


def merchandise(attendance):
    club = game.clubs[game.teamid]

    for count, profit_percentage in enumerate(club.merchandise):
        multiplier = constants.merchandise[count][2]
        potential_sales = attendance * (multiplier * 0.01)
        sale_percentage = 100 - (profit_percentage - 100)
        sales = (potential_sales * 0.01) * sale_percentage

        revenue = sales * constants.merchandise[count][1]
        cost = (revenue / (100 + profit_percentage)) * 100

        money.deposit(revenue, 3)
        money.withdraw(cost, 14)


def catering(attendance):
    club = game.clubs[game.teamid]

    for count, profit_percentage in enumerate(club.catering):
        multiplier = constants.catering[count][2]
        potential_sales = attendance * (multiplier * 0.01)
        sale_percentage = 100 - (profit_percentage - 100)
        sales = (potential_sales * 0.01) * sale_percentage

        revenue = sales * constants.merchandise[count][1]
        cost = (revenue / (100 + profit_percentage)) * 100

        money.deposit(revenue, 4)
        money.withdraw(cost, 15)
