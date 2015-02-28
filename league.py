#!/usr/bin/env python3

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
