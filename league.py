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


def update(result):
    '''
    Received both the teams and results of each game, along with the standings
    list which is to be updated.
    '''
    team1 = result[0]
    team2 = result[3]

    # Increment games played
    game.standings[team1].played += 1
    game.standings[team2].played += 1

    if result[1] > result[2]:
        game.standings[team1].wins += 1
        game.standings[team2].losses += 1
        game.standings[team1].goals_for += result[1]
        game.standings[team1].goals_against += result[2]
        game.standings[team1].goal_difference = game.standings[team1].goals_for - game.standings[team1].goals_against
        game.standings[team2].goals_for += result[2]
        game.standings[team2].goals_against += result[1]
        game.standings[team2].goal_difference = game.standings[team2].goals_for - game.standings[team2].goals_against
        game.standings[team1].points += 3

        game.clubs[team1].form.append("W")
        game.clubs[team2].form.append("L")
    elif result[2] > result[1]:
        game.standings[team2].wins += 1
        game.standings[team1].losses += 1
        game.standings[team2].goals_for += result[2]
        game.standings[team2].goals_against += result[1]
        game.standings[team2].goal_difference = game.standings[team2].goals_for - game.standings[team2].goals_against
        game.standings[team1].goals_for += result[1]
        game.standings[team1].goals_against += result[2]
        game.standings[team1].goal_difference = game.standings[team1].goals_for - game.standings[team1].goals_against
        game.standings[team2].points += 3

        game.clubs[team1].form.append("L")
        game.clubs[team2].form.append("W")
    else:
        game.standings[team1].draws += 1
        game.standings[team2].draws += 1
        game.standings[team1].goals_for += result[1]
        game.standings[team1].goals_against += result[2]
        game.standings[team1].goal_difference = game.standings[team1].goals_for - game.standings[team1].goals_against
        game.standings[team2].goals_for += result[2]
        game.standings[team2].goals_against += result[1]
        game.standings[team2].goal_difference = game.standings[team2].goals_for - game.standings[team2].goals_against
        game.standings[team1].points += 1
        game.standings[team2].points += 1

        game.clubs[team1].form.append("D")
        game.clubs[team2].form.append("D")
