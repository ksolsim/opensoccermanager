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

import advertising
import ai
import calculator
import club
import constants
import evaluation
import events
import fixtures
import flotation
import game
import grant
import injury
import league
import loan
import money
import nation
import news
import overdraft
import player
import referee
import stadium
import statistics
import structures
import suspension
import teamtraining
import user
import widgets


def datainit():
    '''
    Populate data for game, including clubs, players and generate fixtures for
    the season. Initially used to populate details screen for collecting player
    information.
    '''
    # Import surnames for staff
    surnames = game.database.importer("staff")
    game.surnames = [name[0] for name in surnames]

    # Clear data structures and reset date
    game.negotiations = {}
    game.injuries = {}
    game.suspensions = {}

    game.goalscorers = {}
    game.assists = {}
    game.cleansheets = {}
    game.cards = {}
    game.transfers = []

    game.news = news.News()
    game.statistics = statistics.Statistics()

    widgets.date.update()

    # Import extra data
    constants.buildings = game.database.importer("buildings")
    constants.merchandise = game.database.importer("merchandise")
    constants.catering = game.database.importer("catering")
    game.companies = game.database.importer("company")

    # Import nations
    nation.populate_data()

    # Import leagues
    league.leagueitem = league.Leagues()

    # Import clubs
    club.clubitem = club.Clubs()
    club.clubitem.populate_data()

    # Import players
    player.populate_data()

    # Import referees
    referee.referees = referee.Referees()

    # Import stadiums
    stadium.stadiumitem = stadium.Stadiums()
    stadium.stadiumitem.populate_data()

    '''
    adjacent = (0, 1), (2, 0), (3, 2), (1, 3), # DO NOT REORDER/CHANGE!

    game.database.cursor.execute("SELECT * FROM stadium JOIN stadiumattr, clubattr ON clubattr.stadium = stadium.id WHERE clubattr.year = ?", (game.date.year,))
    data = game.database.cursor.fetchall()

    for item in data:
        stadium = stadiums.Stadium()
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
    '''

    for clubobj in club.clubitem.clubs.values():
        stadiumobj = stadium.stadiumitem.stadiums[clubobj.stadium]

        if clubobj.reputation > 12:
            stadiumobj.plots = 60
        else:
            stadiumobj.plots = 40

    # Import injuries
    injury.injuryitem = injury.Injuries()

    # Import suspensions
    suspension.suspensionitem = suspension.Suspensions()

    # Setup fixture list
    league.leagueitem.generate_fixtures()
    '''
    for leagueid, league in game.leagues.items():
        league.fixtures.generate(league.teams)

        league.televised = []

        for count, week in enumerate(league.fixtures.fixtures):
            league.televised.append(random.randint(0, len(week) - 1))'''

    # Create financial objects
    game.bankloan = loan.Loan()
    game.overdraft = overdraft.Overdraft()
    game.grant = grant.Grant()
    game.flotation = flotation.Flotation()


def dataloader(finances):
    '''
    Load remaining data attributes for user selected club. This includes the
    finances, sponsorship and advertising, and publishing initial new articles.
    '''
    club = user.get_user_club()

    if finances == -1:
        club.accounts.balance = club.reputation ** 3 * random.randint(985, 1025) * 3
    else:
        club.accounts.balance = constants.money[finances][0]

    # Generate advertising offers for hoardings/programmes
    club.hoardings.initialise()
    club.programmes.initialise()

    #evaluation.update()

    ai.transfer_list()
    ai.loan_list()
    teamtraining.update_schedules()

    # Publish initial news articles
    game.news.publish("MA01")

    initial = league.leagueitem.leagues[club.league].fixtures.get_initial_fixtures()

    game.news.publish("FX01",
                      fixture1=initial[0],
                      fixture2=initial[1],
                      fixture3=initial[2],
                     )

    #events.expectation()
