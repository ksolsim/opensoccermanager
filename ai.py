#!/usr/bin/env python

import random

import calculator
import constants
import display
import game
import money
import news


def team_training():
    '''
    Generate team training schedules for all teams. Sets mix of training
    for two hours in the morning, and also an individual session except
    on Sunday.
    '''
    for clubid, club in game.clubs.items():
        if clubid != game.teamid:
            values = [count for count in range(2, 17)]
            random.shuffle(values)

            for x in range(0, 6):
                club.team_training[x * 6] = values[x * 2]
                club.team_training[x * 6 + 1] = values[x * 2 + 1]
                club.team_training[x * 6 + 2] = 1
                club.team_training[x * 6 + 3] = 0
                club.team_training[x * 6 + 4] = 0
                club.team_training[x * 6 + 5] = 0


def renew_contract():
    for playerid, player in game.players.items():
        if player.club != game.teamid:
            if 0 < player.contract < 24:
                value = random.randint(0, 100)

                if value < 20:
                    wage = calculator.wage(playerid)
                    player.wage = calculator.wage_rounder(wage)

                    if player.age < 33:
                        contract = random.randint(2, 4)
                    else:
                        contract = random.randint(1, 3)

                    player.contract = contract * 52

                    announce = random.choice((True, False))

                    # Announce big name player contract renewals
                    if player.value > 5000000 and announce:
                        name = display.name(player, mode=1)
                        club = game.clubs[player.club].name

                        news.publish("RC01", player=name,
                                             team=club,
                                             period=contract)


def transfer_list():
    for clubid, club in game.clubs.items():
        if clubid != game.teamid:
            score = {}
            average = 0

            for count, playerid in enumerate(club.squad, start=1):
                player = game.players[playerid]

                skills = (player.keeping,
                          player.tackling,
                          player.passing,
                          player.shooting,
                          player.heading,
                          player.pace,
                          player.stamina,
                          player.ball_control,
                          player.set_pieces)

                score[playerid] = sum(skills) * random.randint(1, 3)

                average += score[playerid] / count

            for playerid in score:
                player = game.players[playerid]

                choice = random.choice((False, True))

                if score[playerid] < average * 0.125 and choice:
                    player.transfer[0] = True


def loan_list():
    for clubid, club in game.clubs.items():
        if clubid != game.teamid:
            score = {}
            average = 0

            for count, playerid in enumerate(club.squad, start=1):
                player = game.players[playerid]

                skills = (player.keeping,
                          player.tackling,
                          player.passing,
                          player.shooting,
                          player.heading,
                          player.pace,
                          player.stamina,
                          player.ball_control,
                          player.set_pieces)

                score[playerid] = sum(skills) * random.randint(1, 3)

                if player.age < 24:
                    score[playerid] += 24 - player.age * player.age

                average += score[playerid] / count

            for playerid in score:
                player = game.players[playerid]

                choice = random.choice((False, True))

                if score[playerid] < average * 0.125 and choice:
                    player.transfer[1] = True


def generate_team(clubid):
    formationid = random.randint(0, 6)
    game.clubs[clubid].tactics[0] = formationid
    formation = constants.formations[formationid]

    squad = game.clubs[clubid].squad
    team = game.clubs[clubid].team

    selection = []
    substitutes = []

    for position in formation[1]:
        scores = {}

        for playerid in squad:
            if playerid not in selection:
                player = game.players[playerid]

                skills = (player.keeping,
                          player.tackling,
                          player.passing,
                          player.shooting,
                          player.heading,
                          player.pace,
                          player.stamina,
                          player.ball_control,
                          player.set_pieces)
                score = sum(skills)

                if position == player.position:
                    if position in ("GK"):
                        score = player.keeping * 2.5
                    elif position in ("DL", "DR", "DC", "D"):
                        score = player.tackling * 2.5
                    elif position in ("ML", "MR", "MC", "M"):
                        score = player.passing * 2.5
                    elif position in ("AS", "AF"):
                        score = player.shooting * 2.5
                else:
                    score *= 0.1

                scores[playerid] = score

        sorted_scores = sorted(scores, key = lambda x: scores[x], reverse = True)

        selection.append(sorted_scores[0])

    for count in range(0, 5):
        scores = {}

        for playerid in squad:
            if playerid not in selection and playerid not in substitutes:
                player = game.players[playerid]
                skills = (player.keeping,
                          player.tackling,
                          player.passing,
                          player.shooting,
                          player.heading,
                          player.pace,
                          player.stamina,
                          player.ball_control,
                          player.set_pieces)
                score = sum(skills)

                if position == player.position:
                    if position in ("GK"):
                        score = player.keeping * 2.5
                    elif position in ("DL", "DR", "DC", "D"):
                        score = player.tackling * 2.5
                    elif position in ("ML", "MR", "MC", "M"):
                        score = player.passing * 2.5
                    elif position in ("AS", "AF"):
                        score = player.shooting * 2.5
                else:
                    score *= 0.1

                scores[playerid] = score

        sorted_scores = sorted(scores, key = lambda x: scores[x], reverse = True)

        try:
            substitutes.append(sorted_scores[0])
        except KeyError:
            print("Key error")

    for count, player in enumerate(selection):
        team[count] = player

    for count, player in enumerate(substitutes, start = 11):
        team[count] = player


def generate_result(clubid1, clubid2):
    club1 = game.clubs[clubid1]
    club2 = game.clubs[clubid2]

    team1 = club1.team
    team2 = club2.team

    reputation1 = club1.reputation
    reputation2 = club2.reputation

    sums = [0, 0]

    for positionid, playerid in team1.items():
        if playerid != 0:
            player = game.players[playerid]

            skills = (player.keeping, player.tackling, player.passing, player.shooting, player.heading, player.pace, player.stamina, player.ball_control, player.set_pieces)
            sums[0] = sum(skills)

    for positionid, playerid in team2.items():
        if playerid != 0:
            player = game.players[playerid]

            skills = (player.keeping, player.tackling, player.passing, player.shooting, player.heading, player.pace, player.stamina, player.ball_control, player.set_pieces)
            sums[1] = sum(skills)

    total_score = sum(sums)

    home_adv = random.randint(1, 5)

    percent1 = round((sums[0] / total_score) * 100)
    percent1 = ((percent1 + home_adv) / 20) * reputation1
    percent2 = round((sums[1] / total_score) * 100)
    percent2 = ((percent2 - home_adv) / 20) * reputation2

    if percent1 > percent2:
        draw = percent1 - percent2
    elif percent2 > percent1:
        draw = percent2 - percent1
    else:
        draw = 0

    draw += 100 - draw - percent1 - percent2

    ranges = [[], [], []]
    ranges[0] = [0.0, percent1]
    ranges[1] = [ranges[0][1], percent1 + draw]
    ranges[2] = [ranges[1][1], ranges[1][1] + percent2]

    for item in ranges:
        list(map(int, item))

    # Score
    def generate_score(ranges):
        def generate_goals(club):
            score1 = 1

            if club.tactics[5] == 0:
                start = 35
            elif club.tactics[5] == 1:
                start = 50
            elif club.tactics[5] == 2:
                start = 65

            for x in range(2, 9):
                if random.randint(0, 100) < start:
                    score1 += 1
                    start = int(start / 2)

                    if start < 1:
                        start = 1

            score2 = random.randint(0, score1 - 1)

            return score1, score2

        choice = random.randrange(0, int(ranges[2][1]))

        if choice < ranges[0][1]:
            r1, r2 = generate_goals(club1)
        elif choice < ranges[1][1]:
            r1, r2 = generate_goals(club1)
            r2 = r1
        elif choice < ranges[2][1]:
            r2, r1 = generate_goals(club2)

        return r1, r2

    result1, result2 = generate_score(ranges)

    return clubid1, result1, result2, clubid2


def advertising():
    '''
    Allow assistant manager to handle advertising by adding adverts to
    hoardings and programmes on each turn when there is space for them
    to be added.
    '''
    if game.advertising_assistant:
        club = game.clubs[game.teamid]

        # Programmes
        current_quantity = 0

        for item in club.hoardings[1]:
            current_quantity += item[1]

        position = 0

        for item in club.hoardings[0]:
            if current_quantity + item[1] <= club.hoardings[2]:
                club.hoardings[1].append(item[0:4])
                current_quantity += item[1]
                del(club.hoardings[0][position])

                money.deposit(item[3], 2)

            position += 1

        # Hoardings
        current_quantity = 0

        for item in club.programmes[1]:
            current_quantity += item[1]

        position = 0

        for item in club.programmes[0]:
            if current_quantity + item[1] <= club.programmes[2]:
                club.programmes[1].append(item[0:4])
                current_quantity += item[1]
                del(club.programmes[0][position])

                money.deposit(item[3], 2)

            position += 1
