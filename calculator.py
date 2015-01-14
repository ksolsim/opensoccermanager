#!/usr/bin/env python3

import game
import news
import constants
import random


def value(playerid):
    '''
    Calculate player value.
    '''
    player = game.players[playerid]

    position = player.position
    age = player.age
    skills = (player.keeping,
              player.tackling,
              player.passing,
              player.shooting,
              player.heading,
              player.pace,
              player.stamina,
              player.ball_control,
              player.set_pieces)

    if position in ("GK"):
        primary = skills[0]
    elif position in ("DL", "DR", "DC", "D"):
        primary = skills[1]
    elif position in ("ML", "MR", "MC", "M"):
        primary = skills[2]
    elif position in ("AS", "AF"):
        primary = skills[3]

    average = sum(skills[0:6]) + (skills[8] * 1.5) + (skills[5] * 0.2) + (skills[6] * 0.2) + (skills[7] * 1.5)
    average += primary * 2
    average = average / 9

    if primary > 95:
        value_multiplier = 5.25
    elif primary >= 90:
        value_multiplier = 3.5
    elif primary > 85:
        value_multiplier = 2.5
    elif primary > 80:
        value_multiplier = 1.8
    elif primary > 75:
        value_multiplier = 1.5
    elif primary > 70:
        value_multiplier = 1.25
    elif primary > 60:
        value_multiplier = 0.9
    elif primary > 50:
        value_multiplier = 0.55
    elif primary > 40:
        value_multiplier = 0.25
    else:
        value_multiplier = 0.12

    # Age modifier
    if age >= 37:
        age_multiplier = 0.1
    elif age >= 34:
        age_multiplier = 0.25
    elif age >= 32:
        age_multiplier = 0.5
    elif age >= 30:
        age_multiplier = 0.75
    elif age == 29:
        age_multiplier = 0.9
    elif age >= 26:
        age_multiplier = 1
    elif age >= 24:
        age_multiplier = 0.9
    elif age >= 21:
        age_multiplier = 0.8
    elif age >= 18:
        age_multiplier = 0.7
    else:
        age_multiplier = 0.5

    value = ((average * 1000) * average) * value_multiplier / 4
    value = value * age_multiplier
    value = value_rounder(value)

    return value


def wage(playerid):
    '''
    Calculate player wage
    '''
    player = game.players[playerid]

    position = player.position
    skills = (player.keeping,
              player.tackling,
              player.passing,
              player.shooting,
              player.heading,
              player.pace,
              player.stamina,
              player.ball_control,
              player.set_pieces)
    value = player.value

    if position in ("GK"):
        primary = skills[0]
    elif position in ("DL", "DR", "DC", "D"):
        primary = skills[1]
    elif position in ("ML", "MR", "MC", "M"):
        primary = skills[2]
    elif position in ("AS", "AF"):
        primary = skills[3]

    average = sum(skills[0:6]) + (skills[8] * 1.5) + (skills[5] * 0.2) + (skills[6] * 0.2) + (skills[7] * 1.5)
    average += primary
    average = average / 9

    if primary >= 95:
        wage_divider = 390
        value_multiplier = 5
    elif primary >= 90:
        wage_divider = 310
        value_multiplier = 3.25
    elif primary >= 85:
        wage_divider = 255
        value_multiplier = 2.2
    elif primary >= 80:
        wage_divider = 225
        value_multiplier = 1.8
    elif primary >= 75:
        wage_divider = 195
        value_multiplier = 1.5
    elif primary >= 70:
        wage_divider = 165
        value_multiplier = 1.1
    elif primary >= 60:
        wage_divider = 140
        value_multiplier = 0.75
    elif primary >= 50:
        wage_divider = 120
        value_multiplier = 0.55
    elif primary >= 40:
        wage_divider = 100
        value_multiplier = 0.25
    else:
        wage_divider = 100
        value_multiplier = 0.12

    value = (((average * 1000) * average) * value_multiplier) * 0.25
    wage = value / wage_divider
    wage = wage_rounder(wage)

    return wage


def bonus(wage):
    '''
    Calculate player bonus from existing wage.
    '''
    leaguewin = wage * 2
    leaguerunnerup = wage * 0.25
    winbonus = wage * 0.1
    goalbonus = wage * 0.1

    return leaguewin, leaguerunnerup, winbonus, goalbonus


def value_rounder(value):
    if value >= 10000:
        divisor = 10000
    elif value >= 1000:
        divisor = 1000
    elif value >= 100:
        divisor = 100
    else:
        divisor = 10

    return value - (value % divisor)


def wage_rounder(value):
    if value >= 1000:
        divisor = 100
    else:
        divisor = 10

    return value - (value % divisor)


def ticket_prices():
    club = game.clubs[game.teamid]

    tickets = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

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


def maintenance():
    club = game.clubs[game.teamid]
    stadium = game.stadiums[club.stadium]

    # Stadium maintenance cost
    cost = (game.maintenance * 0.01) * stadium.capacity * 0.5

    # Building maintenance cost
    for count, item in enumerate(constants.buildings):
        cost += (item[2] * 0.05) * stadium.buildings[count]

    return cost
