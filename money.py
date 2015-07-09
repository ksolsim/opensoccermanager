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


import math
import random

import calculator
import game
import news


def pay_bonus():
    '''
    Calculate the user-specified win bonus on the tactics screen.
    '''
    if game.clubs[game.teamid].tactics.win_bonus != 0:
        total = 0

        for playerid in game.clubs[game.teamid].team:
            if playerid != 0:
                total += game.players[playerid].wage

        bonus = total * (game.clubs[game.teamid].tactics.win_bonus * 0.1)
        game.clubs[game.teamid].accounts.withdraw(bonus, "playerwage")

        game.clubs[game.teamid].tactics.win_bonus = 0


def pay_win_bonus():
    '''
    Pay the win bonus amount defined within the players contract.
    '''
    for playerid in game.clubs[game.teamid].team.values():
        if playerid != 0:
            amount = game.players[playerid].bonus[2]
            game.clubs[game.teamid].accounts.withdraw(amount, "playerwage")


def prize_money(position):
    '''
    Handed out at end of season based on position, plus bonus for a
    first or second place finish.
    '''
    amount = 250000 * (21 - position)

    if position == 1:
        amount += 2500000
    elif position == 2:
        amount += 500000

    return amount
