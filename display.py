#!/usr/bin/env python

from gi.repository import Gtk
import operator
import statistics

import game
import constants
import calculator
import money


def name(player, mode=0):
    '''
    Return the player name in the requested format depending on whether
    it should be displayed as first/second or second/first name.
    '''
    if player.common_name is None:
        player.common_name = ""

    if player.common_name is not "":
        name = player.common_name
    else:
        if mode == 0:
            name = "%s, %s" % (player.second_name, player.first_name)
        elif mode == 1:
            name = "%s %s" % (player.first_name, player.second_name)

    return name


def format_position(value):
    '''
    Format position with ordinal for display to player.

    * Will clearly cause problems if league table is longer than 20
    teams, e.g. 21th, 32th. Needs to be fixed.
    '''
    if value == 1:
        output = "%ist" % (value)
    elif value == 2:
        output = "%ind" % (value)
    elif value == 3:
        output = "%ird" % (value)
    elif value >= 4:
        output = "%ith" % (value)

    return output


def find_champion():
    '''
    Returns clubid of the team at the top of the league.
    '''
    standings = []

    for clubid, club in game.standings.items():
        item = (clubid, club[0], club[1], club[2], club[3], club[4], club[5], club[6], club[7])
        standings.append(item)

    standings = sorted(standings,
                       key = operator.itemgetter(8, 7, 5, 6),
                       reverse = True)

    champion = standings[0][0]

    return champion


def find_position(teamid, ordinal=True):
    '''
    Returns the position in standings of specified club.
    '''
    standings = []

    for clubid, club in game.standings.items():
        item = (clubid, club[0], club[1], club[2], club[3], club[4], club[5], club[6], club[7])
        standings.append(item)

    standings = sorted(standings,
                       key = operator.itemgetter(8, 7, 5, 6),
                       reverse = True)

    position = 1

    for item in standings:
        if item[0] == teamid:
            break

        position += 1

    if ordinal:
        position = format_position(position)

    return position


def top_scorer():
    top = [0, 0]

    for playerid, player in game.players.items():
        if player.goals > top[1]:
            top[0] = playerid
            top[1] = player.goals

    return top


def top_assister():
    top = [0, 0]

    for playerid, player in game.players.items():
        if player.assists > top[1]:
            top[0] = playerid
            top[1] = player.assists

    return top


def player_of_the_season():
    top = [0, 0]

    for playerid, player in game.players.items():
        if player.man_of_the_match > top[1]:
            top[0] = playerid
            top[1] = statistics.mean(player.rating)

    return top


def player_morale(value):
    '''
    Return the string indicating the players morale value.
    '''
    status = ""

    if value >= 85:
        status = constants.morale[8]
    elif value >= 70:
        status = constants.morale[7]
    elif value >= 45:
        status = constants.morale[6]
    elif value >= 20:
        status = constants.morale[5]
    elif value >= 0:
        status = constants.morale[4]
    elif value >= -25:
        status = constants.morale[3]
    elif value >= -50:
        status = constants.morale[2]
    elif value >= -75:
        status = constants.morale[1]
    elif value >= -100:
        status = constants.morale[0]

    return status


def staff_morale(value):
    status = constants.morale[value - 1]

    return status


def value(value):
    value = calculator.value_rounder(value)
    currency = constants.currency[game.currency][0]
    exchange = constants.currency[game.currency][1]

    if value >= 1000000:
        amount = (value / 1000000) * exchange
        value = "%s%.1fM" % (currency, amount)
    elif value >= 1000:
        amount = (value / 1000) * exchange
        value = "%s%iK" % (currency, amount)

    return value


def wage(wage):
    wage = calculator.wage_rounder(wage)
    currency = constants.currency[game.currency][0]
    exchange = constants.currency[game.currency][1]

    if wage >= 1000:
        amount = (wage / 1000) * exchange
        wage = "%s%.1fK" % (currency, amount)
    elif wage >= 100:
        amount = wage * exchange
        wage = "%s%i" % (currency, amount)

    return wage


def currency(amount, mode=0):
    currency = constants.currency[game.currency][0]
    amount *= constants.currency[game.currency][1]

    if mode == 0:
        amount = "%s%i" % (currency, amount)
    elif mode == 1:
        amount = "%s%.2f" % (currency, amount)

    return amount


def contract(period):
    if period > 1:
        text = "%i Weeks" % (period)
    elif contract == 1:
        text = "%i Week" % (period)
    elif contract == 0:
        text = "Out of Contract"

    return text


def club(clubid):
    '''
    Used for players who are out of contract
    '''
    if clubid == 0:
        text = ""
    else:
        text = game.clubs[clubid].name

    return text


def nation(nationid):
    text = game.nations[nationid].name

    return text


def injury(value):
    if value == 1:
        text = "%i Week" % (value)
    else:
        text = "%i Weeks" % (value)

    return text


def suspension(value):
    if value == 1:
        text = "%i Match" % (value)
    else:
        text = "%i Matches" % (value)

    return text


def rating(player):
    if player.rating != []:
        rating = "%.1f" % (statistics.mean(player.rating))
    else:
        rating = "0.0"

    return rating


def season():
    season = "%i/%i" % (game.year, game.year + 1)

    return season
