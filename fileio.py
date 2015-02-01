#!/usr/bin/env python3

import sqlite3
import os

import constants
import database
import events
import game
import resources
import widgets


class Player:
    pass


class Club:
    pass


class Nation:
    pass


class Stadium:
    pass


class Stand:
    pass


class Negotiation:
    pass


def open_file(filename):
    # Clear existing data structures
    game.clubs = {}
    game.players = {}
    game.nations = {}
    game.stadiums = {}
    game.referees = {}
    game.surnames = []
    game.negotiations = {}
    game.loans = {}
    game.televised = []
    game.news = []
    game.transers = []
    game.fixtures = []
    game.results = []
    constants.buildings = []

    connection = sqlite3.connect(filename)
    connection.execute("PRAGMA foreign_keys = on")
    cursor = connection.cursor()

    # Main data and globals
    cursor.execute("SELECT * FROM main")
    data = cursor.fetchone()

    game.teamid = data[0]
    game.year = data[1]
    game.month = data[2]
    game.date = data[3]
    game.week = data[4]
    game.eventindex = data[5]
    game.dateindex = data[6]
    game.dateprev = data[7]
    game.fixturesindex = data[8]
    game.fixturespage = data[9]
    game.active_screen_id = data[10]

    widgets.date.update()

    # Nation
    for item in cursor.execute("SELECT * FROM nation"):
        nation = Nation()
        nationid = item[0]
        game.nations[nationid] = nation

        nation.name = item[1]
        nation.denonym = item[2]

    # Stadium
    for item in cursor.execute("SELECT * FROM stadium"):
        stadium = Stadium()
        stadiumid = item[0]
        game.stadiums[stadiumid] = stadium

        stadium.name = item[1]
        stadium.capacity = item[2]
        stadium.maintenance = 100
        stadium.condition = item[3]
        stadium.plots = item[4]
        stadium.main = []
        stadium.corner = []

        count = 0

        data = item[5:17]

        for value in range(0, 4):
            stand = Stand()
            stand.capacity = data[0 * value]
            stand.roof = data[1 * value]
            stand.seating = data[2 * value]
            stand.box = 0
            stand.adjacent = [False, False]
            stadium.main.append(stand)

            count += 1

        count = 0

        data = item[17:29]

        for value in range(0, 4):
            stand = Stand()
            stand.capacity = data[0 * value]
            stand.roof = data[1 * value]
            stand.seating = data[2 * value]
            stadium.corner.append(stand)

            count += 1

        stadium.buildings = list(item[29:37])

    # Club
    for item in cursor.execute("SELECT * FROM club"):
        club = Club()
        clubid = item[0]
        game.clubs[clubid] = club

        club.name = item[1]
        club.nickname = item[2]
        club.manager = item[3]
        club.chairman = item[4]
        club.stadium = item[5]
        club.reputation = item[6]
        club.form = []
        club.squad = []
        club.team = {}
        club.tactics = [item[7], item[8], item[9], item[10], item[11], item[12], item[13], item[14], item[15]]
        club.coaches_available = {}
        club.coaches_hired = {}
        club.scouts_available = {}
        club.scouts_hired = {}
        club.team_training = [0] * 42
        club.individual_training = {}
        club.tickets = [0] * 15
        club.season_tickets = item[16]
        club.school_tickets = item[17]
        club.accounts = [[0, 0] for x in range(20)]
        club.income = item[18]
        club.expenditure = item[19]
        club.balance = item[20]
        club.finances = [0, 0, 0, 0, 0, 0, 0, 0]
        club.sponsor_status = 0
        club.sponsor_offer = ()
        club.hoardings = [[], [], 0]
        club.programmes = [[], [], 0]
        club.shortlist = set()
        club.merchandise = []
        club.catering = []
        club.evaluation = [item[21], item[22], item[23], item[24], item[25]]
        club.statistics = [0] * 3
        club.form = []

    # Team
    for clubid, club in game.clubs.items():
        cursor.execute("SELECT * FROM team WHERE club=?", (clubid,))
        data = cursor.fetchone()

        for position, item in enumerate(data[1:]):
            club.team[position] = item

        cursor.execute("SELECT * FROM shortlist WHERE club=?", (clubid,))
        data = cursor.fetchall()

        for item in data:
            club.shortlist.add(item[1])

    # Player
    for item in cursor.execute("SELECT * FROM player"):
        player = Player()
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
        player.fitness = item[17]
        player.training = item[18]
        player.training_points = item[19]
        player.morale = item[20]
        player.injury_type = item[21]
        player.injury_period = item[22]
        player.suspension_type = item[23]
        player.suspension_period = item[24]
        player.suspension_points = item[25]
        player.value = item[26]
        player.wage = item[27]
        player.bonus = (item[28], item[29], item[30], item[31])
        player.contract = item[32]
        player.transfer = [item[33], item[34]]
        player.not_for_sale = item[35]
        player.appearances = item[36]
        player.substitute = item[37]
        player.missed = item[38]
        player.goals = item[39]
        player.assists = item[40]
        player.man_of_the_match = item[41]
        player.yellow_cards = item[42]
        player.red_cards = item[43]

        if item[44] == "":
            player.rating = []
        else:
            player.rating = item[44].split(",")

        player.age = events.age(item[4])

    # Squad
    for item in cursor.execute("SELECT * FROM squad"):
        clubid = item[0]
        playerid = item[1]

        game.clubs[clubid].squad.append(playerid)
        game.players[playerid].club = clubid

    # News
    for item in cursor.execute("SELECT * FROM news"):
        game.news.append(item[0:5])

    # Fixtures
    for item in range(0, 38):
        data = cursor.execute("SELECT * FROM fixtures WHERE week=?", (item,))
        game.fixtures.append([])

        for value in data:
            game.fixtures[value[0]].append([value[1], value[2]])

    # Results
    for item in cursor.execute("SELECT * FROM results"):
        if len(game.results) == item[0] + 1:
            game.results[item[0]].append(item[1:5])
        else:
            game.results.append([])
            game.results[item[0]].append(item[1:5])

    # Standings
    for item in cursor.execute("SELECT * FROM standings"):
        game.standings[item[0]] = item[1:10]

    # Negotiations
    for item in cursor.execute("SELECT * FROM negotiations"):
        negotiation = Negotiation()
        key = item[0]
        negotiation.playerid = item[1]
        negotiation.transfer_type = item[2]
        negotiation.timeout = item[3]
        negotiation.club = item[4]
        negotiation.status = item[5]
        negotiation.date = item[6]
        game.negotiations[key] = negotiation

    # Loans
    for item in cursor.execute("SELECT * FROM loans"):
        game.loans[item[0]] = [item[1], item[2]]

    # Charts
    for item in cursor.execute("SELECT * FROM transfers"):
        game.transfers.append(item)

    # Buildings
    for item in cursor.execute("SELECT * FROM buildings"):
        constants.buildings.append(item)

    resources.import_news()
    resources.import_evaluation()

    connection.close()


def save_file(filename):
    # Delete existing file if it exists
    if os.path.exists(filename):
        os.remove(filename)

    connection = sqlite3.connect(filename)
    connection.execute("PRAGMA foreign_keys = on")
    cursor = connection.cursor()

    cursor.execute("CREATE TABLE main (teamid, year, month, date, week, eventindex, dateindex, dateprev, fixturesindex, fixturespage, active_screen)")
    cursor.execute("CREATE TABLE nation (id PRIMARY KEY, name, denonym)")
    cursor.execute("CREATE TABLE stadium (id PRIMARY KEY, name, capacity, condition, plots, northcapacity, northroof, northseating, westcapacity, westroof, westseating, southcapacity, southroof, southseating, eastcapacity, eastroof, eastseating, northwestcapacity, northeastcapacity, southwestcapacity, southeastcapacity, northwestroof, northeastroof, southwestroof, southeastroof, northwestseating, northeastseating, southwestseating, southeastseating, stall, programme, smallshop, largeshop, bar, burgerbar, cafe, restaurant)")
    cursor.execute("CREATE TABLE club (id PRIMARY KEY, name, nickname, manager, chairman, stadium, reputation, tactics1, tactics2, tactics3, tactics4, tactics5, tactics6, tactics7, tactics8, tactics9, seasontickets, schooltickets, income, expenditure, balance, eval1, eval2, eval3, eval4, eval5)")
    cursor.execute("CREATE TABLE player (id PRIMARY KEY, firstname, secondname, commonname, dateofbirth, club, nation, position, keeping, tackling, passing, shooting, heading, pace, stamina, ballcontrol, setpieces, fitness, training, trainingpoints, morale, injurytype, injuryperiod, suspensiontype, suspensionperiod, suspensionpoints, value, wage, bonus0, bonus1, bonus2, bonus3, contract, transfer1, transfer2, notforsale, appearances, substitute, missed, goals, assists, manofthematch, yellowcards, redcards, rating FLOAT, FOREIGN KEY(club) REFERENCES club(id), FOREIGN KEY(nation) REFERENCES nation(id))")
    cursor.execute("CREATE TABLE squad (club, player, FOREIGN KEY(club) REFERENCES club(id), FOREIGN KEY(player) REFERENCES player(id))")
    cursor.execute("CREATE TABLE news (date, title, message, category, unread)")
    cursor.execute("CREATE TABLE fixtures (week, team1, team2)")
    cursor.execute("CREATE TABLE results (week, team1, result1, result2, team2)")
    cursor.execute("CREATE TABLE standings (club, played, won, drawn, lost, goalsfor, goalsagainst, goaldifference, points, FOREIGN KEY(club) REFERENCES club(id))")
    cursor.execute("CREATE TABLE referee (refereeid PRIMARY KEY, matches, fouls, yellow, red)")
    cursor.execute("CREATE TABLE team (club, pos1, pos2, pos3, pos4, pos5, pos6, pos7, pos8, pos9, pos10, pos11, pos12, pos13, pos14, pos15, pos16, FOREIGN KEY(club) REFERENCES club(id))")
    cursor.execute("CREATE TABLE shortlist (club, player, FOREIGN KEY(club) REFERENCES club(id), FOREIGN KEY(player) REFERENCES player(id))")
    cursor.execute("CREATE TABLE negotiations (negotiationid, player, transfertype, timeout, club, status, date, FOREIGN KEY(player) REFERENCES player(id), FOREIGN KEY(club) REFERENCES club(id))")
    cursor.execute("CREATE TABLE loans (player, club, period, FOREIGN KEY(player) REFERENCES player(id), FOREIGN KEY(club) REFERENCES club(id))")
    cursor.execute("CREATE TABLE transfers (player, oldclub, newclub, fee, FOREIGN KEY(player) REFERENCES player(id), FOREIGN KEY(oldclub) REFERENCES club(id), FOREIGN KEY(newclub) REFERENCES club(id))")
    cursor.execute("CREATE TABLE buildings (name, size, cost)")

    cursor.execute("INSERT INTO main VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (game.teamid, game.year, game.month, game.date, game.week, game.eventindex, game.dateindex, game.dateprev, game.fixturesindex, game.fixturespage, game.active_screen_id))

    for nationid, nation in game.nations.items():
        cursor.execute("INSERT INTO nation VALUES (?, ?, ?)", (nationid, nation.name, nation.denonym))

    for stadiumid, stadium in game.stadiums.items():
        details = []

        for stand in stadium.main:
            details.append(stand.capacity)
            details.append(stand.roof)
            details.append(stand.seating)

        for stand in stadium.corner:
            details.append(stand.capacity)
            details.append(stand.roof)
            details.append(stand.seating)

        buildings = stadium.buildings

        cursor.execute("INSERT INTO stadium VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (stadiumid, stadium.name, stadium.capacity, stadium.condition, stadium.plots, details[0], details[1], details[2], details[3], details[4], details[5], details[6], details[7], details[8], details[9], details[10], details[11], details[12], details[13], details[14], details[15], details[16], details[17], details[18], details[19], details[20], details[21], details[22], details[23], buildings[0], buildings[1], buildings[2], buildings[3], buildings[4], buildings[5], buildings[6], buildings[7]))

    for clubid, club in game.clubs.items():
        cursor.execute("INSERT INTO club VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (clubid, club.name, club.nickname, club.manager, club.chairman, club.stadium, club.reputation, club.tactics[0], club.tactics[1], club.tactics[2], club.tactics[3], club.tactics[4], club.tactics[5], club.tactics[6], club.tactics[7], club.tactics[8], club.season_tickets, club.school_tickets, club.income, club.expenditure, club.balance, club.evaluation[0], club.evaluation[1], club.evaluation[2], club.evaluation[3], club.evaluation[4]))

    for playerid, player in game.players.items():
        rating = ",".join(map(str, player.rating))

        cursor.execute("INSERT INTO player VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (playerid, player.first_name, player.second_name, player.common_name, player.date_of_birth, player.club, player.nationality, player.position, player.keeping, player.tackling, player.passing, player.shooting, player.heading, player.pace, player.stamina, player.ball_control, player.set_pieces, player.fitness, player.training, player.training_points, player.morale, player.injury_type, player.injury_period, player.suspension_type, player.suspension_period, player.suspension_points, player.value, player.wage, player.bonus[0], player.bonus[1], player.bonus[2], player.bonus[3], player.contract, player.transfer[0], player.transfer[1], player.not_for_sale, player.appearances, player.substitute, player.missed, player.goals, player.assists, player.man_of_the_match, player.yellow_cards, player.red_cards, rating))

    for clubid, club in game.clubs.items():
        for item in club.squad:
            cursor.execute("INSERT INTO squad VALUES (?, ?)", (clubid, item))

        cursor.execute("INSERT INTO team VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (clubid, club.team[0], club.team[1], club.team[2], club.team[3], club.team[4], club.team[5], club.team[6], club.team[7], club.team[8], club.team[9], club.team[10], club.team[11], club.team[12], club.team[13], club.team[14], club.team[15]))

        for item in club.shortlist:
            cursor.execute("INSERT INTO shortlist VALUES (?, ?)", (clubid, item))

    for item in game.news:
        cursor.execute("INSERT INTO news VALUES (?, ?, ?, ?, ?)", (item[0:5]))

    for week, match in enumerate(game.fixtures):
        for team in match:
            cursor.execute("INSERT INTO fixtures VALUES (?, ?, ?)", (week, team[0], team[1]))

    for week, match in enumerate(game.results):
        for team in match:
            cursor.execute("INSERT INTO results VALUES (?, ?, ?, ?, ?)", (week, team[0], team[1], team[2], team[3]))

    for clubid, item in game.standings.items():
        cursor.execute("INSERT INTO standings VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (clubid, item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7]))

    for key, negotiation in game.negotiations.items():
        cursor.execute("INSERT INTO negotiations VALUES (?, ?, ?, ?, ?, ?, ?)", (key, negotiation.playerid, negotiation.transfer_type, negotiation.timeout, negotiation.club, negotiation.status, negotiation.date))

    for key, loan in game.loans.items():
        cursor.execute("INSERT INTO loans VALUES (?, ?, ?)", (key, loan[0], loan[1]))

    for item in game.transfers:
        cursor.execute("INSERT INTO transfers VALUES (?, ?, ?, ?)", item)

    for item in constants.buildings:
        cursor.execute("INSERT INTO buildings VALUES (?, ?, ?)", item)

    connection.commit()
    connection.close()


def check_config():
    # Create data directory
    if not os.path.isdir(game.data_location):
        os.makedirs(game.data_location)

    # Create username file
    filepath = os.path.join(game.data_location, "users.txt")

    if not os.path.isfile(filepath):
        open(filepath, "w")

    # Create saves directory
    filepath = os.path.join(game.data_location, "saves")

    if not os.path.isdir(filepath):
        os.makedirs(filepath)


def read_names():
    filepath = os.path.join(game.data_location, "users.txt")
    names = []

    # Create username file if it does not already exist

    with open(filepath, "r") as fp:
        for item in fp.readlines():
            item = item.strip("\n")
            names.append(item)

    return names


def write_names(data, mode="w"):
    filepath = os.path.join(game.data_location, "users.txt")

    if mode == "w":
        with open(filepath, "w") as fp:
            for value in data:
                fp.write("%s\n" % (value))
    else:
        with open(filepath, "a") as fp:
            fp.write("%s\n" % (data))
