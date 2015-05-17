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


import statistics

import calculator
import constants
import game


def format_position(value):
    '''
    Format position with ordinal for display to player.
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
    '''
    Find player with the highest performance ratings for the season, and return
    as the 'Player of the Year'.
    '''
    top = [0, 0]

    for playerid, player in game.players.items():
        if player.man_of_the_match > top[1]:
            if len(player.rating) > 0:
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


def value(value):
    value = calculator.value_rounder(value)
    currency, exchange = constants.currency[game.currency]

    if value >= 1000000:
        amount = (value / 1000000) * exchange
        value = "%s%.1fM" % (currency, amount)
    elif value >= 1000:
        amount = (value / 1000) * exchange
        value = "%s%iK" % (currency, amount)

    return value


def currency(amount, mode=0):
    '''
    Format the amount into the selected currency and convert to appropriate
    exchange rate.
    '''
    currency = constants.currency[game.currency][0]
    amount *= constants.currency[game.currency][1]

    if mode == 0:
        amount = "%s%i" % (currency, amount)
    elif mode == 1:
        amount = "%s%.2f" % (currency, amount)

    return amount


def club(clubid):
    '''
    Return club name for the specified id or nothing when player is unattached.
    '''
    if clubid == 0:
        text = ""
    else:
        text = game.clubs[clubid].name

    return text


def season():
    '''
    Return the season in yyyy/yyyy format.
    '''
    season = "%i/%i" % (game.year, game.year + 1)

    return season
