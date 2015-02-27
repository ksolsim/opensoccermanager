#!/usr/bin/env python3

from gi.repository import Gtk
import random

import constants
import display
import game
import news


class Cards:
    yellow_cards = 0
    red_cards = 0
    points = 0


def goalscorers(result, selection1, selection2):
    '''
    Determines the goalscorers for each club when passed both club
    team IDs and the score for both teams.
    '''
    def maximum_calculator(player):
        maximum = 0

        if player.position == "GK":
            maximum = 1
        elif player.position in ("DL", "DR", "DC", "D"):
            maximum = player.tackling
        elif player.position in ("ML", "MR", "MC", "M"):
            maximum = player.passing * 3
        elif player.position in ("AS", "AF"):
            maximum = player.shooting * 5

        return maximum

    players = [[], []]
    scorers = [[], []]

    for playerid in selection1[0]:
        if playerid != 0:
            player = game.players[playerid]

            maximum = maximum_calculator(player)

            for x in range(0, maximum):
                players[0].append(playerid)

    for playerid in selection1[1]:
        if playerid != 0:
            player = game.players[playerid]

            maximum = maximum_calculator(player)

            for x in range(0, maximum):
                players[0].append(playerid)

    for playerid in selection2[0]:
        if playerid != 0:
            player = game.players[playerid]

            maximum = maximum_calculator(player)

            for x in range(0, maximum):
                players[1].append(playerid)

    for playerid in selection2[1]:
        if playerid != 0:
            player = game.players[playerid]

            maximum = maximum_calculator(player)

            for x in range(0, maximum):
                players[1].append(playerid)

    random.shuffle(players[0])
    random.shuffle(players[1])

    for count in range(0, result[1]):
        choice = random.choice(players[0])

        scorers[0].append(choice)

    for count in range(0, result[2]):
        choice = random.choice(players[1])

        scorers[1].append(choice)

    return scorers


def assists(result, selection1, selection2, scorers):
    players = [[], []]

    for playerid in selection1[0]:
        if playerid != 0:
            players[0].append(playerid)

    for playerid in selection2[0]:
        if playerid != 0:
            players[1].append(playerid)

    for playerid in selection1[1]:
        if playerid != 0:
            players[0].append(playerid)

    for playerid in selection2[1]:
        if playerid != 0:
            players[1].append(playerid)

    assisters = []
    a = [[], []]

    for playerid in scorers[0]:
        for count in range(0, result[0]):
            for playerid in players[0]:
                player = game.players[playerid]

                maximum = 0

                if player.position == "GK":
                    maximum = 2
                elif player.position in ("DL", "DR", "DC", "D"):
                    maximum = player.shooting * 0.2
                elif player.position in ("ML", "MR", "MC", "M"):
                    maximum = player.shooting
                elif player.position in ("AS", "AF"):
                    maximum = player.shooting * 0.25

                for x in range(0, int(maximum)):
                    assisters.append(playerid)

        if result[0] > 0:
            choice = random.choice(assisters)
            a[0].append(choice)

    assisters = []

    for playerid in scorers[1]:
        for count in range(0, result[1]):
            for playerid in players[1]:
                player = game.players[playerid]

                maximum = 0

                if player.position == "GK":
                    maximum = 2
                elif player.position in ("DL", "DR", "DC", "D"):
                    maximum = player.shooting * 0.2
                elif player.position in ("ML", "MR", "MC", "M"):
                    maximum = player.shooting
                elif player.position in ("AS", "AF"):
                    maximum = player.shooting * 0.25

                for x in range(0, int(maximum)):
                    assisters.append(playerid)

        if result[1] > 0:
            choice = random.choice(assisters)
            a[1].append(choice)

    return a


def cards(club1, club2):
    '''
    Generate cards for each match based on tackling style. There is some
    randomness however, and in theory the likeliness of a card being
    issued diminishes as more cards are given.

    If a player receives a red, or two yellows, a suspension is also
    generated.
    '''
    def generate(clubid):
        match_cards = [{}, {}]

        multiplier = game.clubs[clubid].tactics[6] + 1

        fouls = random.randint(0, multiplier * 6) * 10
        yellow = random.randint(0, int(fouls * 0.5))
        red = random.randint(0, int(fouls / 8))

        count = 0

        while count < int(yellow):
            choice = random.randint(0, (100 * (10 - len(match_cards[0]))))

            if choice < int(yellow) and len(players[0]) > 0:
                playerid = random.choice(players[0])
                player = game.players[playerid]

                if playerid in match_cards[0]:
                    match_cards[0][playerid] += 1
                    match_cards[1][playerid] = 1
                    player.yellow_cards += 1
                    player.red_cards += 1

                    player.suspension_period = 1
                    player.suspension_type = 1

                    players[0].remove(playerid)
                    players[1].remove(playerid)

                    if player.club == game.teamid:
                        name = display.name(player, mode=1)
                        news.publish("SU01", player=name, period="1")
                else:
                    match_cards[0][playerid] = 1
                    player.yellow_cards += 1

                # Ban player for one match if five/ten/etc yellows
                if player.yellow_cards * 0.2 >= 1 and player.yellow_cards % 5 == 0:
                    player.suspension_period = 1
                    player.suspension_type = 9

                    if player.club == game.teamid:
                        name = display.name(player, mode=1)
                        news.publish("SU03", player=name, period="1", cards=player.yellow_cards)

                '''
                # Add card to chart
                if playerid not in game.cards.keys():
                    cards = Cards()
                    game.cards[playerid] = cards
                else:
                    cards = game.cards[playerid]

                cards.yellow_cards += 1
                '''

            count += 1

        count = 0

        while count < int(red):
            choice = random.randint(0, (100 * (10 - len(match_cards[0]))))

            if choice < int(red):
                playerid = random.choice(players[1])
                player = game.players[playerid]
                player.red_cards += 1

                suspensionid = random.choice(list(constants.suspensions.keys())[2:8])
                suspension = constants.suspensions[suspensionid]
                player.suspension_type = suspensionid
                player.suspension_period = random.randint(suspension[1], suspension[2])

                players[0].remove(playerid)
                players[1].remove(playerid)

                if player.club == game.teamid:
                    name = display.name(player, mode=1)
                    news.publish("SU02", player=name, period=player.suspension_period, suspension=suspension[0])

                '''
                # Add card to chart
                if playerid not in game.cards.keys():
                    cards = Cards()
                    game.cards[playerid] = cards
                else:
                    cards = game.cards[playerid]

                cards.red_cards += 1
                '''

            count += 1

        # Process cards and add to chart
        for playerid, amount in match_cards[0].items():
            if playerid not in game.cards.keys():
                cards = Cards()
                game.cards[playerid] = cards
            else:
                cards = game.cards[playerid]

            cards.yellow_cards += amount
            cards.points += amount * 1

        for playerid, amount in match_cards[1].items():
            if playerid not in game.cards.keys():
                cards = Cards()
                game.cards[playerid] = cards
            else:
                cards = game.cards[playerid]

            cards.red_cards += amount
            cards.points += 3

        return len(match_cards[0]), len(match_cards[1])

    players = [[], []]

    for playerid in game.clubs[club1.teamid].team.values():
        if playerid != 0:
            players[0].append(playerid)
            players[1].append(playerid)

    total1 = generate(club1.teamid)

    for playerid in game.clubs[club2.teamid].team.values():
        if playerid != 0:
            players[0].append(playerid)
            players[1].append(playerid)

    total2 = generate(club2.teamid)

    yellows = total1[0] + total2[0]
    reds = total1[1] + total2[1]

    return yellows, reds


def injury(teamid1, teamid2):
    for teamid in (teamid1.teamid, teamid2.teamid):
        team = game.clubs[teamid].team

        selection = []

        for playerid in team.values():
            if playerid != 0:
                player = game.players[playerid]

                if player.fitness == 100:
                    selection.append(playerid)
                else:
                    value = 100 - player.fitness
                    count = round(value % 4)

                    number = 0

                    while number < count:
                        selection.append(playerid)
                        number += 1

        random.shuffle(selection)

        if random.randint(0, 100) < 25:
            name = display.name(player, mode=1)

            injuryid = random.choice(list(constants.injuries.keys()))
            injury = constants.injuries[injuryid]

            weighting = []

            ranges = list(range(injury[4], injury[3] - 1, -1))
            count = 0

            for value in ranges:
                for x in range(0, count):
                    weighting.append(value)

                count += 1

            random.shuffle(weighting)

            period = random.choice(weighting)

            player.injury_type = injuryid
            player.injury_period = period
            player.fitness -= random.randint(10, 30)

            if teamid == game.teamid:
                news.publish("IN02", player=name, weeks=period, injury=injury[0])


def attendance(team1, team2):
    club = game.clubs[team1.teamid]

    capacity = game.stadiums[club.stadium].capacity
    base_capacity = (74000 * 0.05) * club.reputation

    capacity -= club.school_tickets

    attendance = 0

    if base_capacity > capacity:
        attendance += capacity * 0.5
    else:
        attendance += base_capacity * 0.5

    # Form
    points = 0

    for form in club.form:
        if form == "W":
            points += 3
        elif form == "D":
            points += 1

    attendance += (points / (len(club.form) * 3)) * (base_capacity * 0.5)

    # Reputation
    diff = club.reputation - game.clubs[team2.teamid].reputation

    if diff == 0:
        diff = 1

    attendance += (base_capacity * 0.5) / diff

    if attendance > capacity:
        attendance = capacity

    attendance += club.school_tickets

    attendance = int(attendance)

    return attendance


def rating(selection):
    '''
    Calculate player ratings for both teams at end of each match.
    '''
    ratings = {}

    for playerid in selection[0]:
        player = game.players[playerid]

        rating = random.randint(1, 10)
        player.rating.append(rating)

        ratings[playerid] = rating

    for playerid in selection[1]:
        player = game.players[playerid]

        rating = random.randint(1, 10)
        player.rating.append(rating)

        ratings[playerid] = rating

    return ratings
