#!/usr/bin/env python3

import data
import structures.fixtures
import structures.standings


class Leagues:
    class League:
        def __init__(self):
            self.name = ""
            self.clubs = []
            self.referees = []

            self.fixtures = structures.fixtures.Fixtures()
            self.standings = structures.standings.Standings()

            self.televisied = []

        def add_club(self, clubid):
            '''
            Add club to league and standings.
            '''
            self.clubs.append(clubid)
            self.standings.add_club(clubid)

        def add_referee(self, refereeid):
            '''
            Add referee to list of league referees.
            '''
            self.referees.append(refereeid)

    def __init__(self, season):
        self.leagues = {}
        self.season = season

        self.populate_data()

    def get_leagues(self):
        '''
        Return dictionary items for all leagues.
        '''
        return self.leagues.items()

    def get_league_by_id(self, leagueid):
        '''
        Return league object for passed league id.
        '''
        return self.leagues[leagueid]

    def generate_fixtures(self):
        '''
        Generate fixtures for each of the leagues.
        '''
        for league in self.leagues.values():
            league.fixtures.generate_fixtures(league.clubs)

    def populate_data(self):
        data.database.cursor.execute("SELECT * FROM league \
                                     JOIN leagueattr \
                                     ON league.id = leagueattr.league \
                                     WHERE year = ?",
                                     (self.season,))

        for item in data.database.cursor.fetchall():
            league = self.League()
            leagueid = item[0]
            league.name = item[1]
            self.leagues[leagueid] = league
