#!/usr/bin/env python3

import random


def generate(clubs):
    fixtures = []
    club_list = []

    for item in clubs:
        club_list.append(item)

    random.shuffle(club_list)

    clubs = club_list

    total_rounds = len(clubs) - 1
    matches_per_round = len(clubs) / 2

    round_count = 0
    match_count = 0

    while round_count < total_rounds:
        fixtures.append([])

        while match_count < matches_per_round:
            home = (round_count + match_count) % (len(clubs) - 1)
            away = (len(clubs) - 1 - match_count + round_count) % (len(clubs) - 1)

            if match_count == 0:
                away = len(clubs) - 1

            if round_count % 2 == 1:
                home = clubs[home]
                away = clubs[away]
                fixtures[round_count].append([home, away])
            else:
                home = clubs[home]
                away = clubs[away]
                fixtures[round_count].append([away, home])

            match_count += 1

        round_count += 1
        match_count = 0

    count = 0
    round_count = total_rounds

    while count < total_rounds:
        fixtures.append([])

        for match in fixtures[count]:
            teams = [match[1], match[0]]
            fixtures[round_count].append(teams)

        round_count += 1
        count += 1

    return fixtures
