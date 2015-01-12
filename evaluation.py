#!/usr/bin/env python3

import game


def morale(playerid, amount):
    player = game.players[playerid]

    player.morale += amount

    if player.morale > 100:
        player.morale = 100
    elif player.morale < -100:
        player.morale = -100


def value(amount, category):
    '''
    Update evaluation category value by specified amount, ensuring that
    we never go above 100 or below 0.
    '''
    current = game.clubs[game.teamid].evaluation[category]
    current += amount

    if current > 100:
        current = 100
    elif current < 0:
        current = 0

    game.clubs[game.teamid].evaluation[category] = current


def indexer(index):
    '''
    Determine appropriate message to display for each evaluation item.
    '''
    if 0 <= index < 10:
        value = 0
    elif 10 <= index < 25:
        value = 1
    elif 25 <= index < 40:
        value = 2
    elif 40 <= index < 55:
        value = 3
    elif 55 <= index < 70:
        value = 4
    elif 70 <= index < 85:
        value = 5
    elif 85 <= index < 100:
        value = 6

    return value


def calculate_overall():
    club = game.clubs[game.teamid]

    total = sum(club.evaluation)

    if club.evaluation[4] == 0:
        multiplier = 0.25
    else:
        multiplier = 0.2

    total = total * multiplier

    return total
