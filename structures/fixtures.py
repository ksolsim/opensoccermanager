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

import data


class Fixtures:
    def __init__(self):
        self.fixtures = {}
        self.fixtureid = 0

        self.events = (16, 8), (23, 8), (30, 8), (13, 9), (20, 9), (27, 9), (4, 10), (18, 10), (25, 10), (1, 11), (8, 11), (22, 11), (29, 11), (2, 12), (6, 12), (13, 12), (20, 12), (26, 12), (28, 12), (1, 1), (10, 1), (17, 1), (31, 1), (7, 2), (10, 2), (21, 2), (28, 2), (3, 3), (14, 3), (21, 3), (4, 4), (11, 4), (18, 4), (25, 4), (2, 5), (9, 5), (16, 5), (24, 5),

    def get_fixtureid(self):
        '''
        Return unique fixture id.
        '''
        self.fixtureid += 1

        return self.fixtureid

    def generate_fixtures(self, league):
        '''
        Generate season fixture list for passed clubs argument.
        '''
        self.league = league
        clubs = league.clubs
        self.clubs = clubs

        random.shuffle(clubs)

        rounds = len(self.clubs) - 1
        matches = int(len(self.clubs) * 0.5)

        for week in range(0, rounds):
            referees = self.get_referee_list()

            for match in range(0, matches):
                home = (week + match) % rounds
                away = (len(self.clubs) - 1 - match + week) % rounds

                if match == 0:
                    away = rounds

                fixture = Fixture()
                fixture.leagueid = self.league.leagueid
                fixture.week = week
                fixture.referee = data.referees.get_referee_by_id(referees[match])

                if week % 2 == 1:
                    fixture.home.clubid = self.clubs[home]
                    fixture.away.clubid = self.clubs[away]
                else:
                    fixture.home.clubid = self.clubs[away]
                    fixture.away.clubid = self.clubs[home]

                fixture.fixtureid = self.get_fixtureid()
                self.fixtures[fixture.fixtureid] = fixture

        for week in range(0, rounds):
            referees = self.get_referee_list()

            for match in range(0, matches):
                home = ((rounds + week) + match) % rounds
                away = (len(self.clubs) - 1 - match + (rounds + week)) % rounds

                if match == 0:
                    away = rounds

                fixture = Fixture()
                fixture.leagueid = self.league.leagueid
                fixture.week = rounds + week
                fixture.referee = data.referees.get_referee_by_id(referees[match])

                if (rounds + week) % 2 == 1:
                    fixture.home.clubid = self.clubs[home]
                    fixture.away.clubid = self.clubs[away]
                else:
                    fixture.away.clubid = self.clubs[away]
                    fixture.home.clubid = self.clubs[home]

                fixture.fixtureid = self.get_fixtureid()
                self.fixtures[fixture.fixtureid] = fixture

    def get_referee_list(self):
        '''
        Return randomly ordered list of referees for assignment to fixture.
        '''
        referees = self.league.get_referees()
        random.shuffle(referees)

        return referees

    def get_fixtures(self):
        '''
        Return complete list of fixtures.
        '''
        return self.fixtures

    def get_fixture_by_id(self, fixtureid):
        '''
        Get fixture object for given fixture id.
        '''
        return self.fixtures[fixtureid]

    def get_fixtures_for_week(self, week):
        '''
        Return list of fixtures for passed week value.
        '''
        fixtures = {}

        for fixtureid, fixture in self.fixtures.items():
            if fixture.week == week:
                fixtures[fixtureid] = fixture

        return fixtures

    def get_number_of_rounds(self):
        '''
        Return the number of rounds in the season.
        '''
        return len(self.clubs) * 2 - 2

    def get_initial_fixtures(self):
        '''
        Return name and venue of first three first of the season.
        '''
        fixtures = []
        initial = []

        for fixture in self.fixtures.values():
            if fixture.week in (0, 1, 2):
                if data.user.clubid in (fixture.home.clubid, fixture.away.clubid):
                    fixtures.append([fixture.home.clubid, fixture.away.clubid])

        for teams in fixtures:
            for count, team in enumerate(teams):
                if team != data.user.clubid:
                    club = data.clubs.get_club_by_id(team)
                    location = ("A", "H")[count]

                    fixture = "%s (%s)" % (club.name, location)
                    initial.append(fixture)

        return initial


class Fixture:
    '''
    Fixture object representing match to be played.
    '''
    def __init__(self):
        self.week = 0
        self.played = False

        self.home = FixtureTeam()
        self.away = FixtureTeam()
        self.result = None

        self.attendance = 0
        self.referee = None
        self.leagueid = None

    def get_home_name(self):
        '''
        Return name of home side for fixture.
        '''
        club = data.clubs.get_club_by_id(self.home.clubid)

        return club.name

    def get_away_name(self):
        '''
        Return name of away side for fixture.
        '''
        club = data.clubs.get_club_by_id(self.away.clubid)

        return club.name

    def increment_player_appearances(self):
        '''
        Increment appearances for both clubs registered to fixture object.
        '''
        self.home.increment_player_appearances()
        self.away.increment_player_appearances()

    def store_team_selection(self):
        '''
        Save selected first team and substitutions into fixture object.
        '''
        self.home.team_played[0] = self.home.team_selection[0]
        self.away.team_played[0] = self.away.team_selection[0]


class FixtureTeam:
    '''
    Fixture team object storing squad, events, match statistics, and more.
    '''
    def __init__(self):
        self.clubid = None

        self.team_selection = [[], []]
        self.team_played = [[], []]

        self.team = []
        self.subs = []

        self.formationid = 0

        self.yellow_cards = []
        self.red_cards = []

    def increment_player_appearances(self):
        '''
        Increment appearances for each player in team.
        '''
        for player in self.team_played[0]:
            if player:
                player.appearances += 1

        for player in self.team_played[1]:
            if player:
                player.appearances += 1
