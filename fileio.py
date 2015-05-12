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


import os

import constants
import database
import display
import events
import game
import resources
import staff
import structures
import widgets


db = database.DB()


def open_file(filename):
    db.connect(filename)

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
    game.companies = []
    game.surnames = []
    game.standings = {}
    game.records = [[], []]
    constants.buildings = []
    constants.merchandise = []
    constants.catering = []

    db.connect(filename)

    # Main data and globals
    db.cursor.execute("SELECT * FROM main")
    data = db.cursor.fetchone()

    game.teamid = int(data[0])
    game.year = int(data[1])
    game.month = int(data[2])
    game.date = int(data[3])
    game.week = int(data[4])
    game.eventindex = int(data[5])
    game.dateindex = int(data[6])
    game.dateprev = data[7]
    game.fixturesindex = int(data[8])
    game.fixturespage = int(data[9])
    game.televised = list(map(int, data[10].split(",")))
    game.active_screen_id = game.start_screen

    '''
    The following variables in each class need correctly saving and
    restoring from the save game file.
    '''
    game.flotation = structures.Flotation()
    game.flotation.timeout = 0
    game.flotation.status = 0
    game.flotation.amount = 0

    game.overdraft = structures.Overdraft()
    game.overdraft.amount = 0
    game.overdraft.timeout = 0
    game.overdraft.maximum = 0
    game.overdraft.rate = 0

    game.bankloan = structures.BankLoan()
    game.bankloan.amount = 0
    game.bankloan.maximum = 0
    game.bankloan.rate = 0

    game.grant = structures.Grant()
    game.grant.timeout = 0
    game.grant.status = False
    game.grant.maximum = 0

    game.season_tickets_status = 0

    widgets.date.update()

    # Nation
    for item in db.importer("nation"):
        nation = structures.Nation()
        nationid = item[0]
        game.nations[nationid] = nation

        nation.name = item[1]
        nation.denonym = item[2]

    # Stadium
    for item in db.importer("stadium"):
        stadium = structures.Stadium()
        stadiumid = item[0]
        game.stadiums[stadiumid] = stadium

        stadium.name = item[1]
        stadium.capacity = item[2]
        stadium.maintenance = 100
        stadium.condition = item[3]
        stadium.warnings = item[4]
        stadium.plots = item[5]
        stadium.main = []
        stadium.corner = []

        data = item[6:18]
        count = 0

        for value in range(0, 4):
            stand = structures.Stand()
            stand.capacity = data[0 * value]
            stand.roof = data[1 * value]
            stand.seating = data[2 * value]
            stand.box = 0
            stand.adjacent = [False, False]
            stadium.main.append(stand)

            count += 1

        data = item[18:30]
        count = 0

        for value in range(0, 4):
            stand = structures.Stand()
            stand.capacity = data[0 * value]
            stand.roof = data[1 * value]
            stand.seating = data[2 * value]
            stadium.corner.append(stand)

            count += 1

        stadium.buildings = list(item[30:38])

    # Club
    for item in db.importer("club"):
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
        club.tactics = list(item[7:16])
        club.team_training = list(map(int, item[30].split(",")))
        club.individual_training = {}
        club.tickets = list(map(int, item[31].split(",")))
        club.season_tickets = item[16]
        club.school_tickets = item[17]
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
        club.evaluation = list(item[21:26])
        club.form = []
        club.sales = [[], []]
        club.coaches_available = {}
        club.coaches_hired = {}
        club.scouts_available = {}
        club.scouts_hired = {}
        club.accounts = []

        if item[26]:
            merchandise = item[26].split(",")

            if len(merchandise) > 1:
                club.merchandise = list(map(int, merchandise))

        if item[27]:
            catering = item[27].split(",")

            if len(catering) > 1:
                club.catering = list(map(int, catering))

        club.sponsor_status = item[28]

        if item[29]:
            club.sponsor_offer = item[29].split(",")
            club.sponsor_offer[1] = int(club.sponsor_offer[1])
            club.sponsor_offer[2] = int(club.sponsor_offer[2])

        for value in item[32].split(","):
            category = value.split("|")
            category[0] = int(category[0])
            category[1] = int(category[1])
            club.accounts.append(category)

        club.form = item[33].split(",")

        if item[34] != "":
            attendances = item[34].split(",")
            club.attendances = list(map(int, attendances))
        else:
            club.attendances = []

    # Team
    for clubid, club in game.clubs.items():
        db.cursor.execute("SELECT * FROM team WHERE club=?", (clubid,))
        data = db.cursor.fetchone()

        for position, item in enumerate(data[1:]):
            club.team[position] = item

        db.cursor.execute("SELECT * FROM shortlist WHERE club=?", (clubid,))
        data = db.cursor.fetchall()

        for item in data:
            club.shortlist.add(item[1])

    # Player
    for item in db.importer("player"):
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
        player.rating = []

        player.age = player.get_age()

    # Squad
    for item in db.importer("squad"):
        clubid = item[0]
        playerid = item[1]

        game.clubs[clubid].squad.append(playerid)
        game.players[playerid].club = clubid

    # News
    for item in db.importer("news"):
        game.news.append(item[0:5])

    # Fixtures
    for item in range(0, 38):
        data = db.cursor.execute("SELECT * FROM fixtures WHERE week=?", (item,))
        game.fixtures.append([])

        for value in data:
            game.fixtures[value[0]].append([value[1], value[2]])

    # Results
    for item in db.cursor.execute("SELECT * FROM results"):
        if len(game.results) == item[0] + 1:
            game.results[item[0]].append(item[1:5])
        else:
            game.results.append([])
            game.results[item[0]].append(item[1:5])

    # Standings
    for item in db.importer("standings"):
        item = list(map(int, item))
        clubid = item[0]
        game.standings[clubid] = structures.League()
        game.standings[clubid].played = item[1]
        game.standings[clubid].wins = item[2]
        game.standings[clubid].draws = item[3]
        game.standings[clubid].losses = item[4]
        game.standings[clubid].goals_for = item[5]
        game.standings[clubid].goals_against = item[6]
        game.standings[clubid].goal_difference = item[7]
        game.standings[clubid].points = item[8]

    # Negotiations
    for item in db.importer("negotiations"):
        negotiation = structures.Negotiation()
        key = item[0]
        negotiation.playerid = item[1]
        negotiation.transfer_type = item[2]
        negotiation.timeout = item[3]
        negotiation.club = item[4]
        negotiation.status = item[5]
        negotiation.date = item[6]
        game.negotiations[key] = negotiation

    # Loans
    for item in db.importer("loans"):
        game.loans[item[0]] = [item[1], item[2]]

    # Charts
    for item in db.importer("transfers"):
        game.transfers.append(item)

    # Buildings
    for item in db.importer("buildings"):
        constants.buildings.append(item)

    # Injuries
    for item in db.importer("injuries"):
        constants.injuries[item[0]] = item[1:]

    # Suspensions
    for item in db.importer("suspensions"):
        constants.suspensions[item[0]] = item[1:]

    # Companies
    for item in db.importer("companies"):
        game.companies.append(item)

    # Surnames
    for item in db.importer("surnames"):
        game.surnames.append(item[0])

    # Merchandise
    for item in db.importer("merchandise"):
        constants.merchandise.append(item)

    # Catering
    for item in db.importer("catering"):
        constants.catering.append(item)

    club = game.clubs[game.teamid]

    # Staff
    for item in db.importer("coachavailable"):
        coach = staff.Staff(staff_type=0)
        coach.name = item[1]
        coach.age = item[2]
        coach.ability = item[3]
        coach.speciality = item[4]
        coach.wage = item[5]
        coach.contract = item[6]

        coachid = item[0]
        club.coaches_available[coachid] = coach

    for item in db.importer("coachhired"):
        coach = staff.Staff(staff_type=0)
        coach.name = item[1]
        coach.age = item[2]
        coach.ability = item[3]
        coach.speciality = item[4]
        coach.wage = item[5]
        coach.contract = item[6]
        coach.morale = item[7]
        coach.retiring = bool(item[8])

        coachid = item[0]
        club.coaches_hired[coachid] = coach

    for item in db.importer("scoutavailable"):
        scout = staff.Staff(staff_type=1)
        scout.name = item[1]
        scout.age = item[2]
        scout.ability = item[3]
        scout.wage = item[4]
        scout.contract = item[5]

        scoutid = item[0]
        club.scouts_available[scoutid] = scout

    for item in db.importer("scouthired"):
        scout = staff.Staff(staff_type=1)
        scout.name = item[1]
        scout.age = item[2]
        scout.ability = item[3]
        scout.wage = item[4]
        scout.contract = item[5]
        scout.morale = item[6]
        scout.retiring = bool(item[7])

        scoutid = item[0]
        club.scouts_hired[scoutid] = scout

    # Referees
    for item in db.importer("referee"):
        referee = structures.Referee()
        referee.name = item[1]
        referee.matches = item[2]
        referee.fouls = item[3]
        referee.yellows = item[4]
        referee.reds = item[5]

        refereeid = item[0]
        game.referees[refereeid] = referee

    club = game.clubs[game.teamid]

    # Advertising
    for item in db.importer("hoardingsavailable"):
        club.hoardings[0].append(item)

    for item in db.importer("hoardingscurrent"):
        club.hoardings[1].append(item)

    for item in db.importer("programmesavailable"):
        club.programmes[0].append(item)

    for item in db.importer("programmescurrent"):
        club.programmes[1].append(item)

    # Records
    season = "%s/%s" % (game.year, game.year + 1)
    position = display.find_position(game.teamid)
    standings = game.standings[game.teamid]
    game.record[0] = [season,
                      standings.played,
                      standings.wins,
                      standings.draws,
                      standings.losses,
                      standings.goals_for,
                      standings.goals_against,
                      standings.goal_difference,
                      standings.points,
                      position
                     ]

    game.statistics = structures.Statistics()

    for item in db.importer("statistics"):
        if item[0] != "":
            win = item[0].split(",")
            win = list(map(int, win))
            game.statistics.win = (win[0], (win[1], win[2]))

        if item[1] != "":
            loss = item[1].split(",")
            loss = list(map(int, loss))
            game.statistics.loss = (loss[0], (loss[1], loss[2]))

        game.statistics.yellows = item[2]
        game.statistics.reds = item[3]

    club.hoardings[2] = 48
    club.programmes[2] = 36

    resources.import_news()
    resources.import_evaluation()

    db.connection.close()


def save_file(filename):
    # Delete existing file if it exists
    if os.path.exists(filename):
        os.remove(filename)

    db.connect(filename)

    db.cursor.execute("CREATE TABLE main (teamid, year, month, date, week, eventindex, dateindex, dateprev, fixturesindex, fixturespage, televised)")
    db.cursor.execute("CREATE TABLE nation (id PRIMARY KEY, name, denonym)")
    db.cursor.execute("CREATE TABLE stadium (id PRIMARY KEY, name, capacity, condition, warnings, plots, northcapacity, northroof, northseating, westcapacity, westroof, westseating, southcapacity, southroof, southseating, eastcapacity, eastroof, eastseating, northwestcapacity, northeastcapacity, southwestcapacity, southeastcapacity, northwestroof, northeastroof, southwestroof, southeastroof, northwestseating, northeastseating, southwestseating, southeastseating, stall, programme, smallshop, largeshop, bar, burgerbar, cafe, restaurant)")
    db.cursor.execute("CREATE TABLE club (id PRIMARY KEY, name, nickname, manager, chairman, stadium, reputation, tactics1, tactics2, tactics3, tactics4, tactics5, tactics6, tactics7, tactics8, tactics9, seasontickets, schooltickets, income, expenditure, balance, eval1, eval2, eval3, eval4, eval5, merchandise, catering, sponsorstatus, sponsoroffer, teamtraining, tickets, accounts, form, attendances)")
    db.cursor.execute("CREATE TABLE player (id PRIMARY KEY, firstname, secondname, commonname, dateofbirth, club, nation, position, keeping, tackling, passing, shooting, heading, pace, stamina, ballcontrol, setpieces, fitness, training, trainingpoints, morale, injurytype, injuryperiod, suspensiontype, suspensionperiod, suspensionpoints, value, wage, bonus0, bonus1, bonus2, bonus3, contract, transfer1, transfer2, notforsale, appearances, substitute, missed, goals, assists, manofthematch, yellowcards, redcards, rating, FOREIGN KEY(club) REFERENCES club(id), FOREIGN KEY(nation) REFERENCES nation(id))")
    db.cursor.execute("CREATE TABLE squad (club, player, FOREIGN KEY(club) REFERENCES club(id), FOREIGN KEY(player) REFERENCES player(id))")
    db.cursor.execute("CREATE TABLE news (date, title, message, category, unread)")
    db.cursor.execute("CREATE TABLE fixtures (week, team1, team2)")
    db.cursor.execute("CREATE TABLE results (week, team1, result1, result2, team2)")
    db.cursor.execute("CREATE TABLE standings (club, played, won, drawn, lost, goalsfor, goalsagainst, goaldifference, points, FOREIGN KEY(club) REFERENCES club(id))")
    db.cursor.execute("CREATE TABLE referee (refereeid PRIMARY KEY, name, matches, fouls, yellow, red)")
    db.cursor.execute("CREATE TABLE team (club, pos1, pos2, pos3, pos4, pos5, pos6, pos7, pos8, pos9, pos10, pos11, pos12, pos13, pos14, pos15, pos16, FOREIGN KEY(club) REFERENCES club(id))")
    db.cursor.execute("CREATE TABLE shortlist (club, player, FOREIGN KEY(club) REFERENCES club(id), FOREIGN KEY(player) REFERENCES player(id))")
    db.cursor.execute("CREATE TABLE negotiations (negotiationid, player, transfertype, timeout, club, status, date, FOREIGN KEY(player) REFERENCES player(id), FOREIGN KEY(club) REFERENCES club(id))")
    db.cursor.execute("CREATE TABLE loans (player, club, period, FOREIGN KEY(player) REFERENCES player(id), FOREIGN KEY(club) REFERENCES club(id))")
    db.cursor.execute("CREATE TABLE transfers (player, oldclub, newclub, fee, FOREIGN KEY(player) REFERENCES player(id), FOREIGN KEY(oldclub) REFERENCES club(id), FOREIGN KEY(newclub) REFERENCES club(id))")
    db.cursor.execute("CREATE TABLE individualtraining (name, coach, skill, intensity, start, current, notes)")
    db.cursor.execute("CREATE TABLE hoardingsavailable (name, quantity, period, cost)")
    db.cursor.execute("CREATE TABLE programmesavailable (name, quantity, period, cost)")
    db.cursor.execute("CREATE TABLE hoardingscurrent (name, quantity, period)")
    db.cursor.execute("CREATE TABLE programmescurrent (name, quantity, period)")
    db.cursor.execute("CREATE TABLE buildings (name, size, cost)")
    db.cursor.execute("CREATE TABLE merchandise (name, cost, percentage)")
    db.cursor.execute("CREATE TABLE catering (name, cost, percentage)")
    db.cursor.execute("CREATE TABLE injuries (injuryid PRIMARY KEY, name, minperiod, maxperiod, minfitness, maxfitness)")
    db.cursor.execute("CREATE TABLE suspensions (suspensionid PRIMARY KEY, name, minperiod, maxperiod)")
    db.cursor.execute("CREATE TABLE companies (name)")
    db.cursor.execute("CREATE TABLE surnames (name)")
    db.cursor.execute("CREATE TABLE coachavailable (id PRIMARY KEY, name, age, rating, speciality, wage, contract)")
    db.cursor.execute("CREATE TABLE scoutavailable (id PRIMARY KEY, name, age, rating, wage, contract)")
    db.cursor.execute("CREATE TABLE coachhired (id PRIMARY KEY, name, age, rating, speciality, wage, contract, morale, retiring)")
    db.cursor.execute("CREATE TABLE scouthired (id PRIMARY KEY, name, age, rating, wage, contract, morale, retiring)")
    db.cursor.execute("CREATE TABLE records (season, played, won, drawn, lost, goalsfor, goalsagainst, goaldifference, points, position)")
    db.cursor.execute("CREATE TABLE statistics (win, loss, yellow, red)")

    if game.statistics.win[0] != 0:
        win = ",".join(str(item) for item in (game.statistics.win[0], game.statistics.win[1][0], game.statistics.win[1][1]))
    else:
        win = ""

    if game.statistics.loss[0] != 0:
        loss = ",".join(str(item) for item in (game.statistics.loss[0], game.statistics.loss[1][0], game.statistics.loss[1][1]))
    else:
        loss = ""

    yellow = game.statistics.yellows
    red = game.statistics.reds

    db.cursor.execute("INSERT INTO statistics VALUES (?, ?, ?, ?)", (win, loss, yellow, red))

    televised = ",".join(str(item) for item in game.televised)

    db.cursor.execute("INSERT INTO main VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (game.teamid, game.year, game.month, game.date, game.week, game.eventindex, game.dateindex, game.dateprev, game.fixturesindex, game.fixturespage, televised))

    for nationid, nation in game.nations.items():
        db.cursor.execute("INSERT INTO nation VALUES (?, ?, ?)", (nationid, nation.name, nation.denonym))

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

        db.cursor.execute("INSERT INTO stadium VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (stadiumid, stadium.name, stadium.capacity, stadium.condition, stadium.warnings, stadium.plots, details[0], details[1], details[2], details[3], details[4], details[5], details[6], details[7], details[8], details[9], details[10], details[11], details[12], details[13], details[14], details[15], details[16], details[17], details[18], details[19], details[20], details[21], details[22], details[23], buildings[0], buildings[1], buildings[2], buildings[3], buildings[4], buildings[5], buildings[6], buildings[7]))

    for clubid, club in game.clubs.items():
        if club.merchandise:
            merchandise = ",".join(str(item) for item in club.merchandise)
        else:
            merchandise = None

        if club.catering:
            catering = ",".join(str(item) for item in club.catering)
        else:
            catering = None

        if club.sponsor_offer != ():
            sponsor_offer = ",".join(str(item) for item in club.sponsor_offer)
        else:
            sponsor_offer = None

        team_training = ",".join(str(item) for item in club.team_training)
        tickets = ",".join(str(item) for item in club.tickets)

        accounts = []

        for item in club.accounts:
            accounts.append("%i|%i" % (item[0], item[1]))

        new = ",".join(str(item) for item in accounts)

        accounts = new

        form = ",".join(item for item in club.form)
        attendances = ",".join(str(item) for item in club.attendances)

        db.cursor.execute("INSERT INTO club VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (clubid, club.name, club.nickname, club.manager, club.chairman, club.stadium, club.reputation, club.tactics[0], club.tactics[1], club.tactics[2], club.tactics[3], club.tactics[4], club.tactics[5], club.tactics[6], club.tactics[7], club.tactics[8], club.season_tickets, club.school_tickets, club.income, club.expenditure, club.balance, club.evaluation[0], club.evaluation[1], club.evaluation[2], club.evaluation[3], club.evaluation[4], merchandise, catering, club.sponsor_status, sponsor_offer, team_training, tickets, accounts, form, attendances))

    for playerid, player in game.players.items():
        rating = ",".join(map(str, player.rating))

        db.cursor.execute("INSERT INTO player VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (playerid, player.first_name, player.second_name, player.common_name, player.date_of_birth, player.club, player.nationality, player.position, player.keeping, player.tackling, player.passing, player.shooting, player.heading, player.pace, player.stamina, player.ball_control, player.set_pieces, player.fitness, player.training, player.training_points, player.morale, player.injury_type, player.injury_period, player.suspension_type, player.suspension_period, player.suspension_points, player.value, player.wage, player.bonus[0], player.bonus[1], player.bonus[2], player.bonus[3], player.contract, player.transfer[0], player.transfer[1], player.not_for_sale, player.appearances, player.substitute, player.missed, player.goals, player.assists, player.man_of_the_match, player.yellow_cards, player.red_cards, rating))

    for clubid, club in game.clubs.items():
        for item in club.squad:
            db.cursor.execute("INSERT INTO squad VALUES (?, ?)", (clubid, item))

        db.cursor.execute("INSERT INTO team VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (clubid, club.team[0], club.team[1], club.team[2], club.team[3], club.team[4], club.team[5], club.team[6], club.team[7], club.team[8], club.team[9], club.team[10], club.team[11], club.team[12], club.team[13], club.team[14], club.team[15]))

        for item in club.shortlist:
            db.cursor.execute("INSERT INTO shortlist VALUES (?, ?)", (clubid, item))

    for item in game.news:
        db.cursor.execute("INSERT INTO news VALUES (?, ?, ?, ?, ?)", (item[0:5]))

    for week, match in enumerate(game.fixtures):
        for team in match:
            db.cursor.execute("INSERT INTO fixtures VALUES (?, ?, ?)", (week, team[0], team[1]))

    for week, match in enumerate(game.results):
        for team in match:
            db.cursor.execute("INSERT INTO results VALUES (?, ?, ?, ?, ?)", (week, team[0], team[1], team[2], team[3]))

    for clubid, item in game.standings.items():
        db.cursor.execute("INSERT INTO standings VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (clubid, item.played, item.wins, item.draws, item.losses, item.goals_for, item.goals_against, item.goal_difference, item.points))

    for refereeid, referee in game.referees.items():
        db.cursor.execute("INSERT INTO referee VALUES (?, ?, ?, ?, ?, ?)", (refereeid, referee.name, referee.matches, referee.fouls, referee.yellows, referee.reds))

    for key, negotiation in game.negotiations.items():
        db.cursor.execute("INSERT INTO negotiations VALUES (?, ?, ?, ?, ?, ?, ?)", (key, negotiation.playerid, negotiation.transfer_type, negotiation.timeout, negotiation.club, negotiation.status, negotiation.date))

    for key, loan in game.loans.items():
        db.cursor.execute("INSERT INTO loans VALUES (?, ?, ?)", (key, loan[0], loan[1]))

    for item in game.transfers:
        db.cursor.execute("INSERT INTO transfers VALUES (?, ?, ?, ?)", item)

    for item in constants.buildings:
        db.cursor.execute("INSERT INTO buildings VALUES (?, ?, ?)", item)

    for injuryid, injury in constants.injuries.items():
        db.cursor.execute("INSERT INTO injuries VALUES (?, ?, ?, ?, ?, ?)", (injuryid, injury[0], injury[1], injury[2], injury[3], injury[4]))

    for suspensionid, suspension in constants.suspensions.items():
        db.cursor.execute("INSERT INTO suspensions VALUES (?, ?, ?, ?)", (suspensionid, suspension[0], suspension[1], suspension[2]))

    for company in game.companies:
        db.cursor.execute("INSERT INTO companies VALUES (?)", (company[0],))

    for surname in game.surnames:
        db.cursor.execute("INSERT INTO surnames VALUES (?)", (surname,))

    for item in constants.merchandise:
        db.cursor.execute("INSERT INTO merchandise VALUES (?, ?, ?)", item[0:])

    for item in constants.catering:
        db.cursor.execute("INSERT INTO catering VALUES (?, ?, ?)", item[0:])

    club = game.clubs[game.teamid]

    for coachid, coach in club.coaches_available.items():
        db.cursor.execute("INSERT INTO coachavailable VALUES (?, ?, ?, ?, ?, ?, ?)", (coachid, coach.name, coach.age, coach.ability, coach.speciality, coach.wage, coach.contract))

    for scoutid, scout in club.scouts_available.items():
        db.cursor.execute("INSERT INTO scoutavailable VALUES (?, ?, ?, ?, ?, ?)", (scoutid, scout.name, scout.age, scout.ability, scout.wage, scout.contract))

    for coachid, coach in club.coaches_hired.items():
        db.cursor.execute("INSERT INTO coachhired VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (coachid, coach.name, coach.age, coach.ability, coach.speciality, coach.wage, coach.contract, coach.morale, coach.retiring))

    for scoutid, scout in club.scouts_hired.items():
        db.cursor.execute("INSERT INTO scouthired VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (scoutid, scout.name, scout.age, scout.ability, scout.wage, scout.contract, scout.morale, scout.retiring))

    for item in club.hoardings[0]:
        db.cursor.execute("INSERT INTO hoardingsavailable VALUES (?, ?, ?, ?)", item[0:4])

    for item in club.hoardings[1]:
        db.cursor.execute("INSERT INTO hoardingscurrent VALUES (?, ?, ?)", item[0:3])

    for item in club.programmes[0]:
        db.cursor.execute("INSERT INTO programmesavailable VALUES (?, ?, ?, ?)", item[0:4])

    for item in club.programmes[1]:
        db.cursor.execute("INSERT INTO programmescurrent VALUES (?, ?, ?)", item[0:3])

    for item in game.record[1]:
        db.cursor.execute("INSERT INTO records VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", item)

    db.connection.commit()
    db.connection.close()


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

    if mode is "w":
        with open(filepath, "w") as fp:
            for value in data:
                fp.write("%s\n" % (value))
    else:
        with open(filepath, "a") as fp:
            fp.write("%s\n" % (data))
