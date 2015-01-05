#!/usr/bin/env python

import game


def league_update(result, standings):
    '''
    Received both the teams and results of each game, along with the standings
    list which is to be updated.
    '''
    team1 = result[0]
    team2 = result[3]

    # Increment games played
    standings[team1][0] += 1
    standings[team2][0] += 1

    if result[1] > result[2]:
        standings[team1][1] += 1
        standings[team2][3] += 1
        standings[team1][4] += result[1]
        standings[team1][5] += result[2]
        standings[team1][6] = standings[team1][4] - standings[team1][5]
        standings[team2][4] += result[2]
        standings[team2][5] += result[1]
        standings[team2][6] = standings[team2][4] - standings[team2][5]
        standings[team1][7] += 3

        game.clubs[team1].form.append("W")
        game.clubs[team2].form.append("L")
    elif result[2] > result[1]:
        standings[team2][1] += 1
        standings[team1][3] += 1
        standings[team2][4] += result[2]
        standings[team2][5] += result[1]
        standings[team2][6] = standings[team2][4] - standings[team2][5]
        standings[team1][4] += result[1]
        standings[team1][5] += result[2]
        standings[team1][6] = standings[team1][4] - standings[team1][5]
        standings[team2][7] += 3

        game.clubs[team1].form.append("L")
        game.clubs[team2].form.append("W")
    else:
        standings[team1][2] += 1
        standings[team2][2] += 1
        standings[team1][4] += result[1]
        standings[team1][5] += result[2]
        standings[team1][6] = standings[team1][4] - standings[team1][5]
        standings[team2][4] += result[2]
        standings[team2][5] += result[1]
        standings[team2][6] = standings[team2][4] - standings[team2][5]
        standings[team1][7] += 1
        standings[team2][7] += 1

        game.clubs[team1].form.append("D")
        game.clubs[team2].form.append("D")

    # Remove form items if more than six
    if len(game.clubs[team1].form) > 6:
        game.clubs[team1].form.pop(0)

    if len(game.clubs[team2].form) > 6:
        game.clubs[team2].form.pop(0)

    return standings
