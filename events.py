#!/usr/bin/env python3

from gi.repository import Gtk
import random

import calculator
import constants
import dialogs
import display
import evaluation
import fixtures
import game
import money
import news
import staff
import widgets


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


def increment_appearances(team1, team2):
    '''
    Update the number of appearances made by each player on the team.
    '''
    # Team 1
    selection1 = [[], []]
    subs = []

    for key, playerid in game.clubs[team1].team.items():
        if playerid != 0 and key < 11:
            selection1[0].append(playerid)

        if playerid != 0 and key >= 11:
            subs.append(playerid)

    for count in range(1, 4):
        if len(subs) > 0:
            choice = random.choice(subs)
            selection1[1].append(choice)
            subs.remove(choice)

    for playerid in selection1[0]:
        player = game.players[playerid]
        player.appearances += 1
        evaluation.morale(playerid, 3)

    for playerid in selection1[1]:
        player = game.players[playerid]
        player.substitute += 1

    for playerid in game.clubs[team1].squad:
        if playerid not in selection1[0] and playerid not in selection1[1]:
            player = game.players[playerid]
            player.missed += 1
            evaluation.morale(playerid, 3)

    # Team 2
    selection2 = [[], []]
    subs = []

    for key, playerid in game.clubs[team2].team.items():
        if playerid != 0 and key < 11:
            selection2[0].append(playerid)

        if playerid != 0 and key >= 11:
            subs.append(playerid)

    for count in range(1, 4):
        if len(subs) > 0:
            choice = random.choice(subs)
            selection2[1].append(choice)
            subs.remove(choice)

    for playerid in selection2[0]:
        player = game.players[playerid]
        player.appearances += 1
        evaluation.morale(playerid, 3)

    for playerid in selection2[1]:
        player = game.players[playerid]
        player.substitute += 1

    for playerid in game.clubs[team2].squad:
        if playerid not in selection2[0] and playerid not in selection2[1]:
            player = game.players[playerid]
            player.missed += 1
            evaluation.morale(playerid, 3)

    return selection1, selection2


def increment_goalscorers(scorers1, scorers2):
    '''
    Increment goals total for each player who scored, and increase the
    morale
    '''
    scorers = scorers1 + scorers2  # Cat lists, not a sum

    for playerid in scorers:
        player = game.players[playerid]
        player.goals += 1
        evaluation.morale(playerid, 3)

        if playerid in game.goalscorers:
            game.goalscorers[playerid] += 1
        else:
            game.goalscorers[playerid] = 1


def increment_assists(assists1, assists2):
    '''
    Increments assists for players, and increase morale
    '''
    assists = assists1 + assists2  # Cat lists, not a sum

    for playerid in assists:
        player = game.players[playerid]
        player.assists += 1
        evaluation.morale(playerid, 1)

        if playerid in game.assists:
            game.assists[playerid] += 1
        else:
            game.assists[playerid] = 1


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

    team1 = result[0]
    team2 = result[3]
    score = result[1], result[2]

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

        player = game.players[choice]
        name = display.name(player)

        scorers[0].append(choice)

    for count in range(0, result[2]):
        choice = random.choice(players[1])

        player = game.players[choice]
        name = display.name(player)

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
        cards = [{}, {}]

        multiplier = game.clubs[clubid].tactics[6] + 1

        fouls = random.randint(0, multiplier * 6) * 10
        yellow = random.randint(0, int(fouls * 0.5))
        red = random.randint(0, int(fouls / 8))

        count = 0

        while count < int(yellow):
            choice = random.randint(0, (100 * (10 - len(cards[0]))))

            if choice < int(yellow) and len(players[0]) > 0:
                playerid = random.choice(players[0])
                player = game.players[playerid]

                if playerid in cards[0]:
                    cards[0][playerid] += 1
                    cards[1][playerid] = 1
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
                    cards[0][playerid] = 1
                    player.yellow_cards += 1

                # Ban player for one match if five/ten/etc yellows
                if player.yellow_cards * 0.2 >= 1 and player.yellow_cards % 5 == 0:
                    player.suspension_period = 1
                    player.suspension_type = 9

                    if player.club == game.teamid:
                        name = display.name(player, mode=1)
                        news.publish("SU03", player=name, period="1", cards=player.yellow_cards)

                # Add card to chart
                if playerid in game.cards:
                    game.cards[playerid][0] += 1
                else:
                    game.cards[playerid] = [0, 0]
                    game.cards[playerid][0] = 1

            count += 1

        count = 0

        while count < int(red):
            choice = random.randint(0, (100 * (10 - len(cards[0]))))

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

                # Add card to chart
                if playerid in game.cards:
                    game.cards[playerid][1] += 1
                else:
                    game.cards[playerid] = [0, 0]
                    game.cards[playerid][1] = 1

            count += 1

        return len(cards[0]), len(cards[1])

    players = [[], []]

    for positionid, playerid in game.clubs[club1].team.items():
        if playerid != 0:
            players[0].append(playerid)
            players[1].append(playerid)

    total1 = generate(club1)

    for positionid, playerid in game.clubs[club2].team.items():
        if playerid != 0:
            players[0].append(playerid)
            players[1].append(playerid)

    total2 = generate(club2)

    yellows = total1[0] + total2[0]
    reds = total1[1] + total2[1]

    return yellows, reds


def age(date_of_birth):
    '''
    Determine the age of player at the start of the game.
    '''
    year, month, day = date_of_birth.split("-")
    age = game.year - int(year)

    if (game.month, game.date) < (int(month), int(day)):
        age -= 1

    return age


def morale(playerid, amount):
    value = game.players[playerid].morale

    if amount > 0:
        if value + amount <= 100:
            value += amount
        elif value + amount > 100:
            value = 100
    elif amount < 0:
        if value + amount >= -100:
            value += amount
        elif value + amount < -100:
            value = -100


def injury():
    for clubid, club in game.clubs.items():
        number = random.randint(0, 100)

        if number < 2:
            selection = []

            for playerid in club.squad:
                if game.players[playerid].injury_type == 0:
                    selection.append(playerid)

                    if game.players[playerid].fitness < 100:
                        count = (100 - game.players[playerid].fitness) / 5

                        for x in range(0, int(count)):
                            selection.append(playerid)

            random.shuffle(selection)

            playerid = random.choice(selection)
            player = game.players[playerid]
            name = display.name(player, mode=1)

            injuryid = random.choice(list(constants.injuries.keys()))
            injury = constants.injuries[injuryid]

            weighting = []

            l = list(range(injury[4], injury[3] - 1, -1))
            count = 0

            for value in l:
                for x in range(0, count):
                    weighting.append(value)

                count += 1

            random.shuffle(weighting)

            period = random.choice(weighting)

            player.injury_type = injuryid
            player.injury_period = period
            player.fitness -= random.randint(10, 30)

            if clubid == game.teamid:
                news.publish("IN01", player=name, weeks=period, injury=injury[0])

    adjust_fitness()


def adjust_fitness(recovery=0):
    '''
    Restore player fitness by specified amount, or by a random amount.
    '''
    for playerid, player in game.players.items():
        if player.injury_type == 0 and player.fitness < 100:
            if recovery == 0:
                recovery = random.randint(1, 5)

            player.fitness += recovery

            if player.fitness > 100:
                player.fitness = 100


def match_injury(teamid1, teamid2):
    for teamid in (teamid1, teamid2):
        team = game.clubs[teamid].team

        selection = []

        for positionid, playerid in team.items():
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


def injury_period():
    '''
    Decrement injury period while player has injury. Clear injury once
    the period reaches zero, then publish news indicating player has
    returned to training (but may not be fully fit).
    '''
    for clubid, club in game.clubs.items():
        for playerid in club.squad:
            player = game.players[playerid]

            if player.injury_period > 0:
                player.injury_period -= 1

                if player.injury_period == 0:
                    name = display.name(player, mode=1)
                    injury = constants.injuries[player.injury_type]

                    if player.club == game.teamid:
                        news.publish("IN03", player=name, injury=injury[0])

                    player.injury_type = 0


def pay_wages():
    '''
    Pay wages for both players and staff.
    '''
    total = 0

    club = game.clubs[game.teamid]

    for playerid in club.squad:
        total += game.players[playerid].wage

    money.withdraw(total, 12)

    total = 0

    for staffid in club.coaches_hired:
        total += club.coaches_hired[staffid].wage

    for staffid in club.scouts_hired:
        total += club.scouts_hired[staffid].wage

    money.withdraw(total, 11)


def pay_bonus():
    '''
    Calculates the win bonus on top of wages, then resets the bonus
    statement.
    '''
    if game.clubs[game.teamid].tactics[8] != 0:
        total = 0

        for playerid in game.clubs[game.teamid].team:
            if playerid != 0:
                total += game.players[playerid].wage

        bonus = total * (game.clubs[game.teamid].tactics[8] * 0.1)
        money.withdraw(bonus, 12)

        game.clubs[game.teamid].tactics[8] = 0


def update_contracts():
    '''
    Decrement weeks on contracts, and notify of players and staff who
    are due to reach the end of their contract.
    '''
    for key, player in game.players.items():
        if player.club != 0:
            name = display.name(player, mode=1)

            if player.contract > 0:
                player.contract -= 1

                # Notify user about player contract ending
                if player.club == game.teamid:
                    if player.contract == 12:
                        news.publish("PC02", player=name, weeks=12)
                    elif player.contract == 8:
                        news.publish("PC02", player=name, weeks=8)
                    elif player.contract == 4:
                        news.publish("PC02", player=name, weeks=4)

                if player.contract == 0:
                    # Remove player from squad
                    game.clubs[player.club].squad.remove(key)
                    player.club = 0

                    # Cancel in progress negotiations for player
                    delete = False

                    for negotiationid, negotiation in game.negotiations.items():
                        if negotiation.playerid == key:
                            delete = True

                    if delete:
                        del(game.negotiations[negotiationid])

                    # Notify user contract has ended
                    if player.club == game.teamid:
                        news.publish("PC01", player=name)

                # Notify if shortlisted player contract ends
                if key in game.clubs[game.teamid].shortlist:
                    if player.contract == 0:
                        news.publish("SH01", player=name)

    for clubid, club in game.clubs.items():
        for coachid, coach in club.coaches_hired.items():
            if coach.contract > 0:
                coach.contract -= 1

                if coach.contract == 0:
                    news.publish("CC01", coach=coach.name)

        for scoutid, scout in club.scouts_hired.items():
            if scout.contract > 0:
                scout.contract -= 1

                if scout.contract == 0:
                    news.publish("SC01", scout=scout.name)


def update_sponsorship():
    '''
    When the sponsorship status is set to 0, the club has not received
    an offer and the timeout is decremented each week. Once the timeout
    hits 0, an offer is made and the club is free to accept or reject.
    Each week, the timeout decreases again, and if at 0, the offer is
    withdrawn.
    '''
    if game.clubs[game.teamid].sponsor_status == 0:
        if game.sponsor_timeout == 0:
            game.clubs[game.teamid].sponsor_status = 1
            game.clubs[game.teamid].sponsor_offer = generate_sponsor(game.companies)

            news.publish("BS01")
            game.sponsor_timeout = random.randint(4, 6)
        elif game.sponsor_timeout > 0:
            game.sponsor_timeout -= 1
    elif game.clubs[game.teamid].sponsor_status == 1:
        if game.sponsor_timeout > 0:
            game.sponsor_timeout -= 1
        elif game.sponsor_timeout == 0:
            game.clubs[game.teamid].sponsor_status = 0

            news.publish("BS03")
            evaluation.value(-5, 0)
            game.sponsor_timeout = random.randint(4, 6)


def update_advertising():
    '''
    Decrease number of weeks on purchased advertisements, and remove
    any that have expired. Also periodically refresh the advertisements
    that are available.
    '''
    for clubid, club in game.clubs.items():
        for advert in club.hoardings[1]:
            advert[2] -= 1

            if advert[2] == 0:
                club.hoardings[1].remove(advert)

        for advert in club.programmes[1]:
            advert[2] -= 1

            if advert[2] == 0:
                club.programmes[1].remove(advert)

    # Generate news alert if advertising needs looking at by user
    if game.advertising_alert == 0:
        club = game.clubs[game.teamid]

        if len(club.hoardings[1]) + len(club.programmes[1]) < 12:
            evaluation.value(-3, 0)
            news.publish("BS04")

        game.advertising_alert = random.randint(10, 16)

    game.advertising_alert -= 1

    if game.advertising_timeout > 0:
        game.advertising_timeout -= 1

        if game.advertising_timeout == 0:
            generate_advertisement()
            game.advertising_timeout = random.randint(8, 12)


def generate_sponsor(companies):
    companies = random.choice(companies)
    company = companies[0]

    period = random.randint(1, 5)
    reputation = game.clubs[game.teamid].reputation
    cost = (reputation * random.randrange(950, 1100, 10)) * reputation ** 2

    return company, period, cost


def generate_advertisement():
    club = game.clubs[game.teamid]

    club.hoardings[0] = []
    club.programmes[0] = []

    random.shuffle(game.companies)

    for item in game.companies[0:30]:
        name = item[0]
        amount = random.randint(1, 6)
        period = random.randint(4, 12)
        cost = (club.reputation + random.randint(-5, 5)) * 100

        club.hoardings[0].append([name, amount, period, cost])

    random.shuffle(game.companies)

    for item in game.companies[0:20]:
        name = item[0]
        amount = random.randint(1, 6)
        period = random.randint(4, 12)
        cost = (club.reputation + random.randint(-5, 5)) * 50

        club.programmes[0].append([name, amount, period, cost])


def season_tickets(clubid):
    '''
    Calculate the default percentage of season tickets to be sold based
    on reputation of the club.
    '''
    percentage = game.clubs[clubid].reputation + 40

    return percentage


def team_training():
    # Refresh team training
    if game.team_training_timeout > 0:
        game.team_training_timeout -= 1
    elif game.team_training_timeout == 0:
        news.publish("TT02")

        game.team_training_timeout = 4

    # Check training on Sunday or if player being overworked
    sunday = 0
    overwork = 0

    for trainingid in game.clubs[game.teamid].team_training[36:42]:
        if trainingid != 0:
            sunday += 1

    for trainingid in game.clubs[game.teamid].team_training:
        if trainingid != 0:
            overwork += 1

    if game.team_training_alert == 0:
        if sunday > 0 or overwork > 18:
            game.team_training_alert = random.randint(12, 18)

            for playerid, player in game.players.items():
                evaluation.morale(playerid, -5)
    else:
        game.team_training_alert -= 1

        if game.team_training_alert == 0:
            if overwork > 18:
                news.publish("TT04")
            elif sunday > 0:
                news.publish("TT03")


def individual_training():
    club = game.clubs[game.teamid]

    for playerid in club.individual_training:
        player = game.players[playerid]

        training = club.individual_training[playerid]

        coachid = training[0]
        skill = training[1]
        intensity = training[2] + 1

        coach = club.coaches_hired[coachid]

        if coach.skill == "Average":
            ability = 1
        elif coach.skill == "Good":
            ability = 2
        elif coach.skill == "Superb":
            ability = 3

        # Speciality
        if coach.speciality == "Goalkeeping":
            if skill == 0:
                speciality = 1
            else:
                speciality = 0.1
        elif coach.speciality == "Defensive":
            if skill in (1, 6):
                speciality = 1
            else:
                speciality = 0.1
        elif coach.speciality == "Midfield":
            if skill in (2, 7):
                speciality = 1
            else:
                speciality = 0.1
        elif coach.speciality == "Attacking":
            if skill == 3:
                speciality = 1
            else:
                speciality = 0.1
        elif coach.speciality == "Fitness":
            if skill in (9, 6, 7):
                speciality = 1
            else:
                speciality = 0.1
        elif coach.speciality == "All":
            speciality = 1

        sessions = 0.0

        for value in club.team_training:
            if value == 1:
                sessions += 0.4

        points = (ability * intensity * speciality * sessions) * (player.training * 0.1)

        player.training_points += points
        player.training_points = int(player.training_points)

        if player.training_points >= 100:
            if skill == 0:
                player.keeping += 1
            elif skill == 1:
                player.tackling += 1
            elif skill == 2:
                player.passing += 1
            elif skill == 3:
                player.shooting += 1
            elif skill == 4:
                player.heading += 1
            elif skill == 5:
                player.pace += 1
            elif skill == 6:
                player.stamina += 1
            elif skill == 7:
                player.ball_control += 1
            elif skill == 8:
                player.set_pieces += 1
            elif skill == 9:
                player.fitness += 1

            player.training_points -= 100


def training_camp(options):
    days = options[0]

    # Determine players to take on training camp
    squad = []

    if options[4] == 0:
        for playerid in game.clubs[game.teamid].team.values():
            if playerid != 0:
                squad.append(playerid)
    elif options[4] == 1:
        for playerid in game.clubs[game.teamid].squad:
            if playerid not in game.clubs[game.teamid].team.values():
                squad.append(playerid)
    else:
        squad = [playerid for playerid in game.clubs[game.teamid].squad]

    if options[3] == 0:
        # Leisure
        morale = (options[1] + 1) + (options[2] + 1) * days
        morale = morale * 3
        fitness = 1
    elif options[3] == 1:
        # Schedule
        morale = (options[1] + 1) + (options[2] + 1) * days
        morale = morale * 1.5
        individual_training()
        fitness = 3
    elif options[3] == 2:
        # Intensive
        morale = (-options[1] + 1) + (-options[2] + 1) * -days
        morale = -morale * 2
        fitness = 8

    for playerid in squad:
        player = game.players[playerid]
        evaluation.morale(playerid, morale)
        adjust_fitness(recovery=fitness)


def expectation():
    '''
    Determine the expectations for the season by comparing to other club
    reputations and then publishing news article to notify player at the
    beginning of each season.
    '''
    team_count = len(game.clubs)
    team_ids = [item for item in game.clubs.keys()]

    positions = [[], [], []]

    high_value = 0
    high_id = 0
    low_value = 20
    low_id = 0

    for clubid, club in game.clubs.items():
        if club.reputation > high_value:
            high_value = club.reputation
            high_id = clubid
            positions[0] = [clubid]

    for clubid, club in game.clubs.items():
        if club.reputation < low_value:
            low_value = club.reputation
            low_id = clubid
            positions[2] = [clubid]

    midpoint = 20 - (high_value - low_value) / 2

    team_ids.remove(high_id)
    team_ids.remove(low_id)

    for item in team_ids:
        if game.clubs[item].reputation == midpoint:
            positions[1].append(item)
        elif game.clubs[item].reputation > midpoint:
            if game.clubs[item].reputation > high_value - (high_value - midpoint) * .5:
                positions[0].append(item)
            else:
                positions[1].append(item)
        elif game.clubs[item].reputation < midpoint:
            if game.clubs[item].reputation < midpoint - (midpoint - low_value) * .5:
                positions[2].append(item)
            else:
                positions[1].append(item)

    publish = ("EX01", "EX02", "EX03")
    category = 0

    for idlist in positions:
        for clubid in idlist:
            if clubid == game.teamid:
                news.publish(publish[category], chairman=game.clubs[game.teamid].chairman)

        category += 1


def reset_accounts():
    '''
    Reset weekly accounts for each category to zero.
    '''
    for item in game.clubs[game.teamid].accounts:
        item[0] = 0


def end_of_season():
    '''
    Process end of season events, particularly clearing standings, regen
    of fixtures, clear results, player information, etc.

    Also pay out prize money for finish on previous season.
    '''
    position = display.find_position(game.teamid, ordinal=False)

    dialogs.end_of_season()
    #print("You finished in position %i" % (position))

    # Reset and increment all values where appropriate
    game.date = 1
    game.month = 8
    game.season = "%s/%s" % (game.year, game.year + 1)
    game.week = 1

    widgets.date.update()

    game.eventindex = 0
    game.dateindex = 1
    game.dateprev = 0
    game.fixturesindex = 0

    # Generate new fixture list
    game.fixtures = fixtures.generate(game.clubs)

    # Clear previous season results
    game.results = []

    # Result league standings
    for clubid in game.standings:
        game.standings[clubid] = [0, 0, 0, 0, 0, 0, 0, 0]

    # Reset player statistics
    for playerid, player in game.players.items():
        player.appearances = 0
        player.missed = 0
        player.substitute = 0
        player.goals = 0
        player.assists = 0
        player.man_of_the_match = 0
        player.rating = []

    # Reset club details
    for clubid, club in game.clubs.items():
        club.form = []
        club.accounts = [[0, 0] for x in range(20)]

    # Reset referee stats
    for referee in game.referees:
        game.referees[referee][1] = 0
        game.referees[referee][2] = 0
        game.referees[referee][3] = 0
        game.referees[referee][4] = 0

    # Age staff at end of season
    for key, scout in game.clubs[game.teamid].scouts_hired.items():
        scout.age += 1

    for key, coach in game.clubs[game.teamid].coaches_hired.items():
        coach.age += 1

    # Reset charts
    game.goalscorers = {}
    game.assists = {}
    game.cleansheets = {}
    game.cards = {}
    game.transfers = []

    # Update statistics
    game.record[1].insert(0, game.record[0])
    game.record[0] = []

    update_records()

    # Pay out on prize money for previous season
    prize_money = money.prize_money(position)
    position = display.format_position(position)

    money.deposit(prize_money, 0)
    amount = display.currency(prize_money)
    news.publish("PZ01", amount=amount, position=position)


def refresh_staff():
    '''
    Regenerate the list of scouts and coaches every 8-12 weeks when
    timer reaches zero.
    '''
    if game.staff_timeout == 0:
        game.clubs[game.teamid].coaches_available = {}
        game.clubs[game.teamid].coaches_available = staff.generate(5, "coach")

        game.clubs[game.teamid].scouts_available = {}
        game.clubs[game.teamid].scouts_available = staff.generate(5, "scout")

        game.staff_timeout = random.randint(8, 12)

    game.staff_timeout -= 1


def update_records():
    position = display.find_position(game.teamid)
    season = display.season()

    game.record[0] = game.standings[game.teamid][0:]
    game.record[0].insert(0, "%s" % (season))
    game.record[0].append(position)


def update_statistics(result):
    if result[0] == game.teamid:
        if result[1] > result[2]:
            if [result[1], result[2]] > game.statistics[0][1]:
                game.statistics[0][0] = result[3]
                game.statistics[0][1] = [result[1], result[2]]
        elif result[2] > result[1]:
            if [result[1], result[2]] > game.statistics[1][1]:
                game.statistics[1][0] = result[3]
                game.statistics[1][1] = [result[1], result[2]]
    elif result[3] == game.teamid:
        if result[1] < result[2]:
            if [result[2], result[1]] > game.statistics[0][1]:
                game.statistics[0][0] = result[0]
                game.statistics[0][1] = [result[1], result[2]]
        elif result[2] < result[1]:
            if [result[2], result[1]] > game.statistics[1][1]:
                game.statistics[1][0] = result[0]
                game.statistics[1][1] = [result[1], result[2]]


def attendance(team1, team2):
    club = game.clubs[team1]

    capacity = game.stadiums[club.stadium].capacity

    amount = 0
    amount += club.reputation ** 2 * 100
    amount += game.clubs[team2].reputation ** 2 * 100

    points = 0

    for form in club.form:
        if form == "W":
            points += 3
        elif form == "D":
            points += 1

    value = points / len(club.form) * 3

    amount += value * 1000
    amount += random.randint(-amount * 0.1, amount * 0.1)

    if amount > capacity:
        amount = capacity

    amount = int(amount)

    return amount


def renew_contract(playerid):
    '''
    Logic for whether player is willing to agree to a new contract.
    '''
    points = 0

    player = game.players[playerid]
    club = game.clubs[player.club]

    points += player.morale

    overall = evaluation.calculate_overall()
    points += overall - 50

    if points > 0:
        return True
    else:
        return False


def update_morale(clubid, amount):
    '''
    Increase or decrease player morale based on result.
    '''
    for playerid in game.clubs[clubid].squad:
        evaluation.morale(playerid, amount)

        # Add two points for captain
        if playerid == int(game.clubs[clubid].tactics[1]):
            evaluation.morale(playerid, 2)


def update_condition():
    '''
    Update the current condition of the stadium.
    '''
    club = game.clubs[game.teamid]
    stadium = game.stadiums[club.stadium]

    # Adjust stadium condition
    stadium.condition = game.maintenance + random.randint(-1, 2)

    if stadium.condition > 100:
        stadium.condition = 100
    elif stadium.condition < 0:
        stadium.condition = 0

    # Publish news article
    if stadium.condition <= 25:
        news.publish("SM01")
    elif stadium.condition <= 50:
        news.publish("SM02")


def update_maintenance():
    '''
    Calculate the cost of stadium and building maintenance.
    '''
    cost = calculator.maintenance()

    money.withdraw(cost, 10)


def float_club():
    '''
    Complete floating of club once timeout has been reached.
    '''
    if game.flotation.timeout > 0 and game.flotation.status == 1:
        game.flotation.timeout -= 1

        if game.flotation.timeout == 0:
            money.deposit(game.flotation.amount)
            news.publish("FL01")
