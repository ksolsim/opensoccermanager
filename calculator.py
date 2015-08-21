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


import constants
import game
import player


def value(playerid):
    '''
    Calculate player value.
    '''
    playeritem = player.get_player(playerid)

    age = playeritem.get_age()
    skills = playeritem.get_skills()

    if playeritem.position in ("GK"):
        primary = skills[0]
    elif playeritem.position in ("DL", "DR", "DC", "D"):
        primary = skills[1]
    elif playeritem.position in ("ML", "MR", "MC", "M"):
        primary = skills[2]
    elif playeritem.position in ("AS", "AF"):
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

    value = ((average * 1000) * average) * value_multiplier * 0.25
    value = value * age_multiplier
    value = value_rounder(value)

    return value


def wage(playerid):
    '''
    Calculate player wage
    '''
    playeritem = player.get_player(playerid)

    skills = playeritem.get_skills()
    value = playeritem.value

    if playeritem.position in ("GK"):
        primary = skills[0]
    elif playeritem.position in ("DL", "DR", "DC", "D"):
        primary = skills[1]
    elif playeritem.position in ("ML", "MR", "MC", "M"):
        primary = skills[2]
    elif playeritem.position in ("AS", "AF"):
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
    leaguewin = wage_rounder(wage * 2)
    leaguerunnerup = wage_rounder(wage * 0.25)
    winbonus = wage_rounder(wage * 0.1)
    goalbonus = wage_rounder(wage * 0.1)

    bonuses = list(map(int, (leaguewin, leaguerunnerup, winbonus, goalbonus)))

    return bonuses


def value_rounder(value):
    if value >= 1000000:
        divisor = 100000
    elif value >= 10000:
        divisor = 1000

    value = value - (value % divisor)
    value = int(value)

    return value


def wage_rounder(value):
    if value >= 10000:
        divisor = 100
    else:
        divisor = 10

    value = value - (value % divisor)
    value = int(value)

    return value


def ticket_prices():
    club = game.clubs[game.teamid]

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
