#!/usr/bin/env python

import game


def individual(shortlist_playerid):
    '''
    Analyses each individual player to match suitability
    '''
    shortlist_position = game.players[shortlist_playerid].position

    equivalents = []

    for playerid in game.clubs[game.teamid].squad:
        player = game.players[playerid]

        if player.position == "GK" and shortlist_position == "GK":
            equivalents.append(playerid)
        elif player.position in ("DL", "DR", "DC", "D") and shortlist_position in ("DL", "DR", "DC", "D"):
            equivalents.append(playerid)
        elif player.position in ("ML", "MR", "MC", "M") and shortlist_position in ("ML", "MR", "MC", "M"):
            equivalents.append(playerid)
        elif player.position in ("AF", "AS") and shortlist_position in ("AF", "AS"):
            equivalents.append(playerid)

    averages = []

    for playerid in equivalents:
        player = game.players[playerid]
        skills = (player.keeping,
                  player.tackling,
                  player.passing,
                  player.shooting,
                  player.heading,
                  player.pace,
                  player.stamina,
                  player.ball_control,
                  player.set_pieces,)
        average = sum(skills[0:6]) + (skills[8] * 1.5) + (skills[5] * 0.2) + (skills[6] * 0.2) + (skills[7] * 1.5)
        average = average / 9

        averages.append(average)

    position_average = sum(averages) / len(averages)

    player = game.players[shortlist_playerid]
    skills = (player.keeping,
              player.tackling,
              player.passing,
              player.shooting,
              player.heading,
              player.pace,
              player.stamina,
              player.ball_control,
              player.set_pieces,)
    average = sum(skills[0:6]) + (skills[8] * 1.5) + (skills[5] * 0.2) + (skills[6] * 0.2) + (skills[7] * 1.5)
    average = average / 9

    if average < position_average:
        status = 0
    else:
        status = 1

    return status


def recommends():
    '''
    Iterates through all players and displays those which are suitable
    '''
    recommended = []

    for playerid, player in game.players.items():
        status = individual(playerid)

        if status == 1:
            recommended.append(playerid)

    return recommended
