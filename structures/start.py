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


import data
import structures.buildings
import structures.calendar
import structures.clubs
import structures.companies
import structures.computer
import structures.date
import structures.events
import structures.finances
import structures.injuries
import structures.leagues
import structures.loans
import structures.nations
import structures.negotiations
import structures.players
import structures.proceed
import structures.referees
import structures.seasons
import structures.stadiums
import structures.staff
import structures.user


class Start:
    '''
    Object initialisation for in-game data structures.
    '''
    def __init__(self, clubid, season):
        data.user = structures.user.User()

        data.calendar = structures.calendar.Calendar()
        data.date = structures.date.Date(season)
        data.continuegame = structures.proceed.ContinueGame()
        data.continuetomatch = structures.proceed.ContinueToMatch()

        data.companies = structures.companies.Companies()
        data.merchandise = structures.merchandise.Merchandise()
        data.catering = structures.catering.Catering()
        data.staff = structures.staff.Staff()
        data.buildings = structures.buildings.Buildings()
        data.negotiations = structures.negotiations.Negotiations()
        data.loans = structures.loans.Loans()
        data.injuries = structures.injuries.Injuries()
        data.suspensions = structures.suspensions.Suspensions()
        data.comparison = structures.comparison.Comparison()

        data.nations = structures.nations.Nations()
        data.leagues = structures.leagues.Leagues(season)
        data.referees = structures.referees.Referees(season)
        data.stadiums = structures.stadiums.Stadiums(season)
        data.clubs = structures.clubs.Clubs(season)
        data.players = structures.players.Players(season)

        data.events = structures.events.Events()

        data.injury = structures.computer.InjuryGenerator()
        data.advertising = structures.computer.AdvertHandler()

        data.user.set_club(clubid)

    def set_manager_name(self, name):
        '''
        Set passed manager name argument and add to names list.
        '''
        data.user.club.manager = name
        data.names.add_name(name)

    def setup_initial_values(self):
        '''
        Setup initial values for each club.
        '''
        data.leagues.generate_fixtures()

        data.user.club.hoardings.maximum = 48
        data.user.club.hoardings.generate_adverts(36)

        if data.user.club.reputation < 10:
            data.user.club.programmes.maximum = 36
        else:
            data.user.club.programmes.maximum = 48

        data.user.club.programmes.generate_adverts(24)

        if data.user.club.reputation < 13:
            data.user.club.stadium.buildings.maximum_plots = 60
        else:
            data.user.club.stadium.buildings.maximum_plots = 80

        data.user.club.coaches.generate_initial_staff()
        data.user.club.scouts.generate_initial_staff()

        data.user.club.tickets.set_initial_prices()
        data.user.club.tickets.set_initial_school_tickets()
        data.user.club.tickets.set_initial_season_tickets()

        self.publish_initial_news()

    def publish_initial_news(self):
        '''
        Publish initial news articles for user on starting new game.
        '''
        data.user.club.news.publish("MA01")

        initial1, initial2, initial3 = data.user.club.league.fixtures.get_initial_fixtures()

        data.user.club.news.publish("FX01", fixture1=initial1, fixture2=initial2, fixture3=initial3)
