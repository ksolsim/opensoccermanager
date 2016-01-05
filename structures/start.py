#!/usr/bin/env python3

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
    def __init__(self, teamid, season):
        data.user = structures.user.User()
        data.user.team = teamid

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

        self.club = data.clubs.get_club_by_id(data.user.team)

    def set_manager_name(self, name):
        '''
        Set passed manager name argument and add to names list.
        '''
        self.club.manager = name
        data.names.add_name(name)

    def setup_initial_values(self):
        '''
        Setup initial values for each club.
        '''
        data.leagues.generate_fixtures()

        stadium = data.stadiums.get_stadium_by_id(self.club.stadium)

        self.club.hoardings.maximum = 48
        self.club.hoardings.generate_adverts(36)

        if self.club.reputation < 10:
            self.club.programmes.maximum = 36
        else:
            self.club.programmes.maximum = 48

        self.club.programmes.generate_adverts(24)

        if self.club.reputation < 13:
            stadium.buildings.maximum_plots = 60
        else:
            stadium.buildings.maximum_plots = 80

        self.club.coaches.generate_initial_staff()
        self.club.scouts.generate_initial_staff()

        self.club.tickets.set_initial_school_tickets()
        self.club.tickets.set_initial_season_tickets()

        self.publish_initial_news()

    def publish_initial_news(self):
        '''
        Publish initial news articles for user on starting new game.
        '''
        self.club.news.publish("MA01")

        league = data.leagues.get_league_by_id(self.club.league)
        initial1, initial2, initial3 = league.fixtures.get_initial_fixtures()

        self.club.news.publish("FX01", fixture1=initial1, fixture2=initial2, fixture3=initial3)