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


import operator
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


def increment_goalscorers(scorers1, scorers2):
    '''
    Increment goals total for each player who scored, and increase the
    morale
    '''
    scorers = operator.concat(scorers1, scorers2)

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
    assists = operator.concat(assists1, assists2)

    for playerid in assists:
        player = game.players[playerid]
        player.assists += 1
        evaluation.morale(playerid, 1)

        if playerid in game.assists:
            game.assists[playerid] += 1
        else:
            game.assists[playerid] = 1


def increment_referee(refereeid, fouls=0, yellows=0, reds=0):
    referee = game.referees[refereeid]
    referee.matches += 1
    referee.fouls += fouls
    referee.yellows += yellows
    referee.reds += reds


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
    '''
    Generate injuries outside of a match, typically through training.
    '''
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
    for player in game.players.values():
        if player.injury_type == 0 and player.fitness < 100:
            if recovery == 0:
                recovery = random.randint(1, 5)

            player.fitness += recovery

            if player.fitness > 100:
                player.fitness = 100


def injury_period():
    '''
    Decrement injury period while player has injury. Clear injury once
    the period reaches zero, then publish news indicating player has
    returned to training (but may not be fully fit).
    '''
    for club in game.clubs.values():
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
                        del game.negotiations[negotiationid]

                    # Notify user contract has ended
                    if player.club == game.teamid:
                        news.publish("PC01", player=name)

                # Notify if shortlisted player contract ends
                if key in game.clubs[game.teamid].shortlist:
                    if player.contract == 0:
                        news.publish("SH01", player=name)

    for club in game.clubs.values():
        for coachid, coach in club.coaches_hired.items():
            if coach.contract > 0:
                coach.contract -= 1

                if coach.contract == 0:
                    news.publish("CC01", coach=coach.name)
                    del game.clubs[game.teamid].coaches_hired[coachid]
                elif coach.contract == 1:
                    news.publish("CC02", coach=coach.name)

        for scoutid, scout in club.scouts_hired.items():
            if scout.contract > 0:
                scout.contract -= 1

                if scout.contract == 0:
                    news.publish("SC01", scout=scout.name)
                    del game.clubs[game.teamid].scouts_hired[scoutid]
                elif scout.contract == 1:
                    news.publish("SC02", scout=scout.name)


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
            game.sponsor_timeout = random.randint(4, 6)


def update_advertising():
    '''
    Decrease number of weeks on purchased advertisements, and remove
    any that have expired. Also periodically refresh the advertisements
    that are available.
    '''
    for club in game.clubs.values():
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


def season_tickets():
    '''
    Calculate the default percentage of season tickets to be sold based
    on reputation of the club.
    '''
    percentage = game.clubs[game.teamid].reputation + 40

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

            for playerid in game.players.keys():
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

    # Reduce player skill when not individual training
    for playerid in club.squad:
        if playerid not in club.individual_training:
            player = game.players[playerid]

            reduction = random.randint(1, 3)
            player.training_points -= reduction

            if player.training_points <= 0:
                skill = random.randint(0, 9)

                if skill == 0:
                    player.keeping -= 1
                elif skill == 1:
                    player.tackling -= 1
                elif skill == 2:
                    player.passing -= 1
                elif skill == 3:
                    player.shooting -= 1
                elif skill == 4:
                    player.heading -= 1
                elif skill == 5:
                    player.pace -= 1
                elif skill == 6:
                    player.stamina -= 1
                elif skill == 7:
                    player.ball_control -= 1
                elif skill == 8:
                    player.set_pieces -= 1

                player.training_points = 99


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
        evaluation.morale(playerid, morale)
        adjust_fitness(recovery=fitness)


def expectation():
    '''
    Determine the expectations for the season by comparing to other club
    reputations and then publishing news article to notify player at the
    beginning of each season.
    '''
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

    midpoint = 20 - ((high_value - low_value) * 0.5)

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
    dialogs.end_of_season()

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
    for player in game.players.values():
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
        game.referees[referee].matches = 0
        game.referees[referee].fouls = 0
        game.referees[referee].yellows = 0
        game.referees[referee].reds = 0

    # Age staff at end of season
    for scout in game.clubs[game.teamid].scouts_hired.values():
        scout.age += 1

        if scout.age > 60:
            likeliness = (scout.age - 60) * 20
            value = random.randint(0, 100)

            if value <= likeliness:
                scout.retiring = True

        if scout.retiring and scout.contract == 0:
            del game.clubs[game.teamid].scouts_hired[scoutid]

    for coach in game.clubs[game.teamid].coaches_hired.values():
        coach.age += 1

        if coach.age > 60:
            likeliness = (coach.age - 60) * 20
            value = random.randint(0, 100)

            if value <= likeliness:
                coach.retiring = True

        if coach.retiring and coach.contract == 0:
            del game.clubs[game.teamid].coaches_hired[coachid]

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
        game.clubs[game.teamid].coaches_available = staff.generate(role=0, number=5)

        game.clubs[game.teamid].scouts_available = {}
        game.clubs[game.teamid].scouts_available = staff.generate(role=0, number=5)

        game.staff_timeout = random.randint(8, 12)

    game.staff_timeout -= 1


def update_records():
    position = display.find_position(game.teamid)
    season = display.season()

    details = game.standings[game.teamid]

    game.record[0] = ["%s" % (season),
                      details.played,
                      details.wins,
                      details.draws,
                      details.losses,
                      details.goals_for,
                      details.goals_against,
                      details.goal_difference,
                      details.points,
                      position
                     ]


def update_statistics(result):
    score = result.final_score

    if result.clubid1 == game.teamid:
        if score[0] > score[1]:
            if score > game.statistics.win[1]:
                game.statistics.win = (result.clubid2, score)
        elif score[1] > score[0]:
            if score > game.statistics.loss[1]:
                game.statistics.loss = (result.clubid2, score)
    elif result.clubid2 == game.teamid:
        if score[0] < score[1]:
            if score > game.statistics.win[1]:
                game.statistics.win = (result.clubid1, score)
        elif score[1] < score[0]:
            if score > game.statistics.loss[1]:
                game.statistics.loss = (result.clubid1, score)

    game.statistics.yellows += result.yellows
    game.statistics.reds += result.reds


def renew_contract(playerid):
    '''
    Logic for whether player is willing to agree to a new contract.
    '''
    points = 0

    player = game.players[playerid]

    points += player.morale

    overall = evaluation.calculate_overall()
    points += overall - 25

    if points >= 0:
        state = True
    else:
        state = False

    return state


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
    stadium.condition = stadium.maintenance + random.randint(-1, 2)

    if stadium.condition > 100:
        stadium.condition = 100
    elif stadium.condition < 0:
        stadium.condition = 0

    # Publish news article
    if stadium.condition <= 25:
        news.publish("SM01")

        stadium.warnings += 1
    elif stadium.condition <= 50:
        news.publish("SM02")

        stadium.warnings += 1

    # Issue FA fine
    if stadium.warnings == 3:
        fine = (stadium.capacity * 3) * (stadium.fines + 1)
        money.withdraw(fine, 9)

        news.publish("SM03", amount=fine)

        stadium.fines += 1
        stadium.warnings = 0


def update_maintenance():
    '''
    Calculate the cost of stadium and building maintenance.
    '''
    cost = calculator.maintenance()

    money.withdraw(cost, 10)
