#!/usr/bin/env python3

import random

import data


class Fixtures:
    class Fixture:
        def __init__(self):
            self.week = 0

            self.home = None
            self.away = None
            self.result = None

            self.attendance = 0
            self.refereeid = None

        def get_home_name(self):
            '''
            Return name of home side for fixture.
            '''
            club = data.clubs.get_club_by_id(self.home)

            return club.name

        def get_away_name(self):
            '''
            Return name of away side for fixture.
            '''
            club = data.clubs.get_club_by_id(self.away)

            return club.name

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

    def generate_fixtures(self, clubs):
        '''
        Generate season fixture list for passed clubs argument.
        '''
        random.shuffle(clubs)

        self.clubs = clubs

        rounds = len(self.clubs) - 1
        matches = int(len(self.clubs) * 0.5)

        for round_count in range(0, rounds):
            week = round_count

            for match_count in range(0, matches):
                home = (round_count + match_count) % rounds
                away = (len(self.clubs) - 1 - match_count + round_count) % rounds

                if match_count == 0:
                    away = rounds

                fixture = self.Fixture()
                fixture.week = week

                if round_count % 2 == 1:
                    fixture.home = self.clubs[home]
                    fixture.away = self.clubs[away]
                else:
                    fixture.home = self.clubs[away]
                    fixture.away = self.clubs[home]

                fixtureid = self.get_fixtureid()
                self.fixtures[fixtureid] = fixture

        half_season = self.fixtures.copy()

        for item in half_season.values():
            fixtureid = self.get_fixtureid()

            fixture = self.Fixture()
            fixture.week = round_count + item.week + 1
            fixture.home = item.away
            fixture.away = item.home
            self.fixtures[fixtureid] = fixture

    def get_fixtures(self):
        '''
        Return complete list of fixtures.
        '''
        return self.fixtures

    def get_fixture_for_id(self, fixtureid):
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
        total = len(self.clubs) * 2 - 2

        return total

    def get_initial_fixtures(self):
        '''
        Return name and venue of first three first of the season.
        '''
        fixtures = []
        initial = []

        for fixture in self.fixtures.values():
            if fixture.week in (0, 1, 2):
                if data.user.team in (fixture.home, fixture.away):
                    fixtures.append([fixture.home, fixture.away])

        for teams in fixtures:
            for count, team in enumerate(teams):
                if team != data.user.team:
                    club = data.clubs.get_club_by_id(team)
                    location = ("A", "H")[count]

                    fixture = "%s (%s)" % (club.name, location)
                    initial.append(fixture)

        return initial
