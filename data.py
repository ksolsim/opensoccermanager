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


import random

import ai
import calculator
import constants
import evaluation
import events
import fixtures
import game
import money
import news
import resources
import staff
import structures
import widgets


def datainit():
    '''
    Populate data for game, including clubs, players and generate fixtures for
    the season. Initially used to populate details screen for collecting player
    information.
    '''
    # Clear data structures and reset date
    game.clubs = {}
    game.players = {}
    game.nations = {}
    game.stadiums = {}
    game.negotiations = {}
    game.referees = {}
    game.injuries = {}
    game.suspensions = {}
    game.televised = []
    game.surnames = []

    game.goalscorers = {}
    game.assists = {}
    game.cleansheets = {}
    game.cards = {}
    game.transfers = []

    game.standings = {}
    game.fixtures = []
    game.results = []
    game.record = [[], []]
    game.news = []

    game.date = 1
    game.month = 8
    game.week = 1

    widgets.date.update()

    # Import clubs and populate club data structure
    game.database.cursor.execute("SELECT * FROM club JOIN clubattr ON club.id = clubattr.club WHERE year = ?", (game.year,))
    data = game.database.cursor.fetchall()

    for item in data:
        club = structures.Club()
        clubid = item[0]
        game.clubs[clubid] = club

        club.name = item[1]
        club.nickname = item[2]
        club.manager = item[6]
        club.chairman = item[7]
        club.stadium = item[8]
        club.reputation = item[9]

        # Initialise playerid in team to 0
        for count in range(0, 16):
            club.team[count] = 0

        club.base_attendance = (74000 / (40 - club.reputation)) * club.reputation
        club.base_attendance = int(club.base_attendance * 0.9)

        game.standings[clubid] = structures.League()

    # Import players
    game.database.cursor.execute("SELECT * FROM player JOIN playerattr ON player.id = playerattr.player WHERE year = ?", (game.year,))
    data = game.database.cursor.fetchall()

    for item in data:
        player = structures.Player()
        playerid = item[0]
        game.players[playerid] = player

        player.first_name = item[1]
        player.second_name = item[2]
        player.common_name = item[3]
        player.date_of_birth = item[4]
        player.nationality = item[5]
        player.club = item[9]
        player.position = item[10]
        player.keeping = item[11]
        player.tackling = item[12]
        player.passing = item[13]
        player.shooting = item[14]
        player.heading = item[15]
        player.pace = item[16]
        player.stamina = item[17]
        player.ball_control = item[18]
        player.set_pieces = item[19]
        player.training = item[20]
        player.contract = random.randint(24, 260)

        player.age = player.get_age()
        player.value = calculator.value(item[0])
        player.wage = calculator.wage(item[0])
        player.bonus = calculator.bonus(player.wage)

        game.clubs[player.club].squad.append(playerid)

    # Import nations
    for item in game.database.importer("nation"):
        nation = structures.Nation()
        nationid = item[0]
        game.nations[nationid] = nation

        nation.name = item[1]
        nation.denonym = item[2]

    adjacent = (0, 1), (2, 0), (3, 2), (1, 3), # DO NOT REORDER/CHANGE!

    # Import stadiums
    game.database.cursor.execute("SELECT * FROM stadium JOIN stadiumattr, clubattr ON clubattr.stadium = stadium.id WHERE clubattr.year = ?", (game.year,))
    data = game.database.cursor.fetchall()

    for item in data:
        stadium = structures.Stadium()
        stadiumid = item[0]
        game.stadiums[stadiumid] = stadium

        stadium.name = item[1]
        stadium.condition = 100
        stadium.plots = 0
        stadium.capacity = sum(item[5:17])
        stadium.main = []
        stadium.corner = []

        for count, value in enumerate(item[5:9]):
            stand = structures.Stand()
            stand.capacity = value

            if stand.capacity > 0:
                stand.seating = bool(item[count + 17])
                stand.roof = bool(item[count + 25])

                if stand.capacity >= 5000 and stand.roof:
                    stand.box = item[count + 13]
                else:
                    stand.box = 0
            else:
                stand.seating = False
                stand.roof = False
                stand.box = 0

            stand.adjacent = adjacent[count]

            stadium.main.append(stand)

        for count, value in enumerate(item[9:13]):
            stand = structures.Stand()
            stand.capacity = value

            if stand.capacity > 0:
                stand.seating = bool(item[count + 21])
                stand.roof = bool(item[count + 29])
                stand.available = [False, False]
            else:
                stand.seating = False
                stand.roof = False
                stand.available = [False, False]

            stadium.corner.append(stand)

        stadium.buildings = list(item[33:41])

    for club in game.clubs.values():
        stadium = game.stadiums[club.stadium]

        if club.reputation > 12:
            stadium.plots = 60
        else:
            stadium.plots = 40

    # Import injuries
    for item in game.database.importer("injury"):
        constants.injuries[item[0]] = item[1:]

    # Import suspensions
    for item in game.database.importer("suspension"):
        constants.suspensions[item[0]] = item[1:]

    # Setup fixture list
    game.fixtures = fixtures.generate(game.clubs)

    # Televised matches
    home = []

    for count, week in enumerate(game.fixtures):
        home.append([])

        for match in week:
            home[count].append(match[0])

    for week in home:
        team = random.choice(week)
        game.televised.append(team)

    constants.buildings = game.database.importer("buildings")
    constants.merchandise = game.database.importer("merchandise")
    constants.catering = game.database.importer("catering")
    game.companies = game.database.importer("company")

    # Import surnames for staff
    surnames = game.database.importer("staff")
    game.surnames = [name[0] for name in surnames]

    # Import referees
    game.database.cursor.execute("SELECT id, name FROM referee WHERE year = ?", (game.year,))
    data = game.database.cursor.fetchall()

    for item in data:
        referee = structures.Referee()
        refereeid = item[0]
        referee.name = item[1]
        game.referees[refereeid] = referee


def dataloader(finances):
    '''
    Load remaining data attributes for user selected club. This includes the
    finances, sponsorship and advertising, and publishing initial new articles.
    '''
    club = game.clubs[game.teamid]

    if finances == -1:
        club.balance = club.reputation ** 3 * random.randint(985, 1025) * 3
    else:
        club.balance = constants.money[finances][0]

    # Generate coaches and scouts
    for count in range(5):
        coach = staff.Staff(staff_type=0)
        club.coaches_available[coach.staffid] = coach

    for count in range(5):
        scout = staff.Staff(staff_type=1)
        club.scouts_available[scout.staffid] = scout

    # Generate sponsorship offer
    club.sponsor_status = 0
    club.sponsor_offer = events.generate_sponsor(game.companies)

    # Generate advertising offers for hoardings/programmes
    club.hoardings[2] = 48

    if club.reputation > 10:
        club.programmes[2] = 36
    else:
        club.programmes[2] = 24

    events.generate_advertisement()
    game.advertising_timeout = random.randint(8, 12)

    # Produce initial interest rates
    game.bankloan = structures.BankLoan()
    game.bankloan.amount = 0
    game.bankloan.rate = random.randint(4, 15)
    game.bankloan.timeout = random.randint(4, 16)

    # Overdraft
    game.overdraft = structures.Overdraft()
    game.overdraft.amount = 0
    game.overdraft.rate = random.randint(4, 15)
    game.overdraft.timeout = random.randint(4, 16)

    # Grant
    game.grant = structures.Grant()
    game.grant.maximum = 0
    game.grant.status = False
    game.grant.timeout = 0

    # Flotation
    game.flotation = structures.Flotation()
    game.flotation.amount = 0
    game.flotation.timeout = 0
    game.flotation.status = 0

    # Statistics
    game.statistics = structures.Statistics()

    # Initiate season ticket sales based on percentage of capacity
    club.season_tickets = events.season_tickets()
    game.season_tickets_status = 0

    # Calculate base ticket prices
    club.tickets = calculator.ticket_prices()

    # Calculate free school tickets
    tickets = int((20 - club.reputation) * 0.5) + 1  # Leave int to round
    club.school_tickets = tickets * 100

    # Initiate values for merchandise / catering
    club.merchandise = [100] * len(constants.merchandise)
    club.catering = [100] * len(constants.catering)

    # Import resources
    resources.import_news()
    resources.import_evaluation()

    evaluation.update()

    money.calculate_loan()
    money.calculate_overdraft()
    money.calculate_grant()
    money.flotation()
    events.update_records()
    events.expectation()
    ai.transfer_list()
    ai.loan_list()
    ai.team_training()

    # Retrieve first three fixtures for news
    initial_fixtures = []

    for count, week in enumerate(game.fixtures):
        for match in week:
            if game.teamid in (match[0], match[1]) and count < 3:
                match = "%s - %s" % (game.clubs[match[0]].name,
                                     game.clubs[match[1]].name)
                initial_fixtures.append(match)

    # Publish initial news articles
    news.publish("MA01")
    news.publish("FX01",
                 fixture1=initial_fixtures[0],
                 fixture2=initial_fixtures[1],
                 fixture3=initial_fixtures[2],)
