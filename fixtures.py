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


class Fixtures:
    def __init__(self):
        self.clubs = []
        self.fixtures = []

    def generate(self, teams):
        '''
        Generate the fixtures for the given teams.
        '''
        self.clubs = [team for team in teams]
        random.shuffle(self.clubs)

        rounds = len(self.clubs) - 1
        matches = len(self.clubs) * 0.5

        round_count = 0
        match_count = 0

        fixtures = []

        while round_count < rounds:
            fixtures.append([])

            while match_count < matches:
                home = (round_count + match_count) % rounds
                away = (len(self.clubs) - 1 - match_count + round_count) % rounds

                if match_count == 0:
                    away = rounds

                if round_count % 2 == 1:
                    fixtures[round_count].append([self.clubs[home], self.clubs[away]])
                else:
                    fixtures[round_count].append([self.clubs[away], self.clubs[home]])

                match_count += 1

            round_count += 1
            match_count = 0

        count = 0
        round_count = rounds

        while count < rounds:
            fixtures.append([])

            for match in fixtures[count]:
                teams = [match[1], match[0]]
                fixtures[round_count].append(teams)

            round_count += 1
            count += 1

        self.fixtures = fixtures

    def get_number_of_rounds(self):
        total = len(self.clubs) * 2 - 2

        return total
