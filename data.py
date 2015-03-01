#!/usr/bin/env python3

import random

import calculator
import constants
import evaluation
import events
import fixtures
import game
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
    database = game.database
    database.connect()

    game.clubs = {}
    game.players = {}
    game.nations = {}
    game.stadiums = {}
    game.negotiations = {}
    game.news = []

    game.date = 1
    game.month = 8
    game.week = 1

    game.year, database.version = database.importer("about")[0]

    widgets.date.update()

    # Import clubs and populate club data structure
    for item in database.importer("club"):
        club = structures.Club()
        clubid = item[0]
        game.clubs[clubid] = club

        club.name = item[1]
        club.nickname = item[2]
        club.manager = item[3]
        club.chairman = item[4]
        club.stadium = item[5]
        club.reputation = item[6]
        club.squad = []
        club.team = {}
        club.tactics = [0, 0, 0, 0, 0, 1, 1, 0, 0]
        club.coaches_available = {}
        club.coaches_hired = {}
        club.scouts_available = {}
        club.scouts_hired = {}
        club.team_training = [0] * 42
        club.individual_training = {}
        club.tickets = [0] * 15
        club.season_tickets = 40
        club.school_tickets = 0
        club.accounts = [[0, 0] for x in range(20)]
        club.income = 0
        club.expenditure = 0
        club.balance = 0
        club.finances = [0, 0, 0, 0, 0, 0, 0, 0]
        club.sponsor_status = 0
        club.sponsor_offer = ()
        club.hoardings = [[], [], 0]
        club.programmes = [[], [], 0]
        club.shortlist = set()
        club.merchandise = []
        club.catering = []
        club.sales = [[], []]
        club.evaluation = [0, 0, 0, 0, 0]
        club.statistics = [0] * 3
        club.form = []

        # Initialise playerid in team to 0
        for count in range(0, 16):
            club.team[count] = 0

        game.standings[clubid] = structures.League()

    # Import players
    for item in database.importer("player"):
        player = structures.Player()
        playerid = item[0]
        game.players[playerid] = player

        player.first_name = item[1]
        player.second_name = item[2]
        player.common_name = item[3]
        player.date_of_birth = item[4]
        player.club = item[5]
        player.nationality = item[6]
        player.position = item[7]
        player.keeping = item[8]
        player.tackling = item[9]
        player.passing = item[10]
        player.shooting = item[11]
        player.heading = item[12]
        player.pace = item[13]
        player.stamina = item[14]
        player.ball_control = item[15]
        player.set_pieces = item[16]
        player.fitness = 100
        player.training = item[17]
        player.training_points = 0
        player.morale = 10
        player.injury_type = 0
        player.injury_period = 0
        player.suspension_points = 0
        player.suspension_type = 0
        player.suspension_period = 0
        player.yellow_cards = 0
        player.red_cards = 0
        player.contract = random.randint(24, 260)
        player.transfer = [False, False]
        player.not_for_sale = False
        player.appearances = 0
        player.substitute = 0
        player.missed = 0
        player.goals = 0
        player.assists = 0
        player.man_of_the_match = 0
        player.rating = []

        player.age = events.age(item[4])
        player.value = calculator.value(item[0])
        player.wage = calculator.wage(item[0])
        player.bonus = calculator.bonus(player.wage)

        game.clubs[player.club].squad.append(playerid)

    # Import nations
    for item in database.importer("nation"):
        nation = structures.Nation()
        nationid = item[0]
        game.nations[nationid] = nation

        nation.name = item[1]
        nation.denonym = item[2]

    adjacent = (0, 1), (2, 0), (3, 2), (1, 3), # DO NOT REORDER/CHANGE!

    # Import stadiums
    for item in database.importer("stadium"):
        stadium = structures.Stadium()
        stadiumid = item[0]
        game.stadiums[stadiumid] = stadium

        stadium.name = item[1]
        stadium.condition = 100
        stadium.capacity = sum(item[2:14])
        stadium.main = []
        stadium.corner = []

        for count, value in enumerate(item[2:6]):
            stand = structures.Stand()
            stand.capacity = value

            if stand.capacity > 0:
                stand.seating = bool(item[count + 14])
                stand.roof = bool(item[count + 22])

                if stand.capacity >= 5000 and stand.roof:
                    stand.box = item[count + 10]
                else:
                    stand.box = 0
            else:
                stand.seating = False
                stand.roof = False
                stand.box = 0

            stand.adjacent = adjacent[count]

            stadium.main.append(stand)

        for count, value in enumerate(item[6:10]):
            stand = structures.Stand()
            stand.capacity = value

            if stand.capacity > 0:
                stand.seating = bool(item[count + 18])
                stand.roof = bool(item[count + 26])
                stand.available = [False, False]
            else:
                stand.seating = False
                stand.roof = False
                stand.available = [False, False]

            stadium.corner.append(stand)

        stadium.buildings = list(item[30:38])

    for clubid, club in game.clubs.items():
        stadium = game.stadiums[club.stadium]

        if club.reputation > 12:
            stadium.plots = 60
        else:
            stadium.plots = 40

    # Import injuries
    for item in database.importer("injury"):
        constants.injuries[item[0]] = item[1:]

    # Import suspensions
    for item in database.importer("suspension"):
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

    constants.buildings = database.importer("buildings")
    constants.merchandise = database.importer("merchandise")
    constants.catering = database.importer("catering")
    game.companies = database.importer("company")

    # Import surnames for staff
    surnames = database.importer("staff")
    game.surnames = [name[0] for name in surnames]

    # Import referees
    for item in database.importer("referee"):
        referee = structures.Referee()
        refereeid = item[0]
        referee.name = item[1]
        game.referees[refereeid] = referee


def dataloader(finances):
    club = game.clubs[game.teamid]

    if finances == -1:
        club.balance = club.reputation ** 3 * random.randint(985, 1025) * 3
    else:
        club.balance = constants.money[finances][0]

    # Generate coaches and scouts
    club.coaches_available = staff.generate(role=0, number=5)
    club.scouts_available = staff.generate(role=1, number=5)

    # Generate sponsorship offer
    club.sponsor_status = 0
    club.sponsor_offer = events.generate_sponsor(game.companies)

    # Generate advertising offers for hoardings/programmes
    club.hoardings[2] = 48

    if club.reputation > 10:
        club.programmes[2] = 24
    else:
        club.programmes[2] = 18

    events.generate_advertisement()
    game.advertising_timeout = random.randint(8, 12)

    # Produce initial interest rates
    game.bankloan = structures.Loan()
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

    # Initiate season ticket sales based on percentage of capacity
    club.season_tickets = events.season_tickets()
    game.season_tickets_status = 0

    # Calculate base ticket prices
    club.tickets = calculator.ticket_prices()

    # Calculate free school tickets
    tickets = int((20 - club.reputation) * 0.25) + 1  # Leave int to round
    club.school_tickets = tickets * 100

    # Initiate values for merchandise / catering
    [club.merchandise.append(100) for item in constants.merchandise]
    [club.catering.append(100) for item in constants.catering]

    # Import resources
    resources.import_news()
    resources.import_evaluation()

    evaluation.update()

    # Retrieve first three fixtures for news
    initial_fixtures = []
    for count, week in enumerate(game.fixtures):
        for match in week:
            if game.teamid in (match[0], match[1]) and count < 3:
                match = "%s - %s" % (game.clubs[match[0]].name, game.clubs[match[1]].name)
                initial_fixtures.append(match)

    # Publish initial news articles
    news.publish("MA01")
    news.publish("FX01",
                 fixture1=initial_fixtures[0],
                 fixture2=initial_fixtures[1],
                 fixture3=initial_fixtures[2],)
