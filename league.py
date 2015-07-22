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


import fixtures
import game
import standings


class Leagues:
    class League:
        def __init__(self):
            self.name = ""
            self.teams = []
            self.referees = {}

            self.fixtures = fixtures.Fixtures()
            self.results = []
            self.standings = standings.Standings()

            self.televised = []

        def add_club(self, clubid):
            '''
            Add club to league and standings.
            '''
            self.teams.append(clubid)

            self.standings.add_item(clubid)

        def add_result(self, result):
            '''
            Update results with latest for given teams.
            '''
            self.results[game.date.fixturesindex].append(result)

        def generate_fixtures(self):
            '''
            Generate fixtures for list of teams.
            '''
            self.fixtures.generate(self.teams)

    def __init__(self):
        self.leagues = {}

        self.populate_data()

    def populate_data(self):
        '''
        Populate league data.
        '''
        game.database.cursor.execute("SELECT * FROM league JOIN leagueattr ON league.id = leagueattr.league WHERE year = ?", (game.date.year,))
        data = game.database.cursor.fetchall()

        for item in data:
            league = self.League()
            leagueid = item[0]
            self.leagues[leagueid] = league

            league.name = item[1]

    def generate_fixtures(self):
        '''
        Generate fixtures for all leagues.
        '''
        for league in self.leagues.values():
            league.generate_fixtures()

    def prize_money(self):
        '''
        Pay out prize money based on finishing position.
        '''
        for league in self.leagues.values():
            standings = league.standings.get_data()

            for position, standing in enumerate(standings, start=1):
                clubid = standing[0]
                club = club.clubitem.clubs[clubid]

                amount = 250000 * (21 - position)

                if position == 1:
                    amount += 2500000
                elif position == 2:
                    amount += 500000

                club.accounts.deposit(category="prizemoney", amount=amount)

                position = standings.get_position_string(clubid)
                game.news.publish("PZ01", amount=amount, position=position)
