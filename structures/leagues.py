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
import structures.fixtures
import structures.standings


class Leagues:
    class League:
        def __init__(self, leagueid):
            self.leagueid = leagueid
            self.name = ""
            self.clubs = []
            self.referees = []

            self.fixtures = structures.fixtures.Fixtures()
            self.standings = structures.standings.Standings()

            self.televised = []

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

        def get_referees(self):
            '''
            Return list of referees associated with league.
            '''
            return self.referees

        def get_clubs(self):
            '''
            Return list of clubs associated with league.
            '''
            return self.clubs

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
        for leagueid, league in self.leagues.items():
            league.fixtures.generate_fixtures(league)

    def populate_data(self):
        data.database.cursor.execute("SELECT * FROM league \
                                     JOIN leagueattr \
                                     ON league.id = leagueattr.league \
                                     WHERE year = ?",
                                     (self.season,))

        for item in data.database.cursor.fetchall():
            leagueid = item[0]
            league = self.League(leagueid)
            league.name = item[1]
            self.leagues[leagueid] = league
