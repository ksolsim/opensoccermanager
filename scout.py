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


import game


def individual(shortlist_playerid):
    '''
    Analyses each individual player to match suitability
    '''
    shortlist_position = game.players[shortlist_playerid].position

    equivalents = []

    for playerid in game.clubs[game.teamid].squad:
        player = game.players[playerid]

        if player.position:
            if shortlist_position == "GK":
                equivalents.append(playerid)
            elif shortlist_position in ("DL", "DR", "DC", "D"):
                equivalents.append(playerid)
            elif shortlist_position in ("ML", "MR", "MC", "M"):
                equivalents.append(playerid)
            elif shortlist_position in ("AF", "AS"):
                equivalents.append(playerid)

    averages = []

    for playerid in equivalents:
        player = game.players[playerid]
        skills = player.get_skills()

        average = sum(skills[0:6]) + (skills[8] * 1.5) + (skills[5] * 0.2) + (skills[6] * 0.2) + (skills[7] * 1.5)
        average = average / 9

        averages.append(average)

    position_average = sum(averages) / len(averages)

    player = game.players[shortlist_playerid]
    skills = player.get_skills()

    average = sum(skills[0:6]) + (skills[8] * 1.5) + (skills[5] * 0.2) + (skills[6] * 0.2) + (skills[7] * 1.5)
    average = average / 9

    status = average < position_average

    return status


def recommends():
    '''
    Iterates through all players and displays those which are suitable.
    '''
    recommended = {}

    for playerid, player in game.players.items():
        if individual(playerid):
            recommended[playerid] = player

    return recommended
