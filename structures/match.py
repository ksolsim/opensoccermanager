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


class Score:
    def __init__(self, fixture):
        self.fixture = fixture

        self.calculate_skills()

    def calculate_skills(self):
        '''
        Calculate player scores for team selection from skill attributes.
        '''
        self.weights = [1, 1] #0, 0

        for count, club in enumerate((data.clubs.get_club_by_id(self.fixture.home.clubid),
                                      data.clubs.get_club_by_id(self.fixture.away.clubid))):
            for playerid in club.squad.teamselection.team:
                if playerid:
                    player = data.players.get_player_by_id(playerid)

                    skills = player.get_skills()
                    self.weights[count] = sum(skills)

        self.total = sum(self.weights)

        self.calculate_percentages()

    def home_advantage(self):
        '''
        Determine home advantage score based on form and fan morale.
        '''
        club = data.clubs.get_club_by_id(self.fixture.home.clubid)

        points = 0

        for item in club.form.get_form_for_length(6):
            if item == "W":
                points += 3
            elif item == "D":
                points += 1
            elif item == "L":
                points -= 1

        return points

    def calculate_percentages(self):
        '''
        Determine percentage chance of win, loss, and draw for each team.
        '''
        club = data.clubs.get_club_by_id(self.fixture.home.clubid)

        percent1 = ((self.weights[0] / self.total) + self.home_advantage()) * 100
        percent1 = (percent1 * 0.05) * club.reputation
        self.percent1 = round(percent1)

        club = data.clubs.get_club_by_id(self.fixture.away.clubid)

        percent2 = (self.weights[0] / self.total) * 100
        percent2 = (percent2 * 0.05) * club.reputation
        self.percent2 = round(percent2)

        self.determine_result()

    def determine_result(self):
        '''
        Produce final result for match.
        '''
        if self.percent1 > self.percent2:
            draw = self.percent1 - self.percent2
        elif self.percent1 < self.percent2:
            draw = self.percent2 - self.percent1
        else:
            draw = 0

        ranges = [[], [], []]
        ranges[0] = [0, self.percent1]
        ranges[1] = [ranges[0][1], self.percent1 + draw]
        ranges[2] = [ranges[1][1], ranges[1][1] + self.percent2]

        if ranges == [[0, 0], [0, 0], [0, 0]]:
            ranges = [[1, 2], [3, 4], [5, 6]]

        print(ranges)

        [list(map(int, item)) for item in ranges]

        choice = random.randrange(0, int(ranges[2][1]))

        if choice < ranges[0][1]:
            score = self.generate_goals()
        elif choice < ranges[1][1]:
            score = self.generate_goals()
            score = score[0], score[0]
        elif choice < ranges[2][1]:
            score = self.generate_goals()
            score = score[1], score[0]

        self.fixture.result = score

    def generate_goals(self):
        '''
        Generate goals scored for both teams.
        '''
        score1 = 1

        club = data.clubs.get_club_by_id(self.fixture.home.clubid)

        if club.tactics.playing_style == 0:
            start = 35
        elif club.tactics.playing_style == 1:
            start = 50
        elif club.tactics.playing_style == 2:
            start = 65

        for x in range(2, 9):
            if random.randint(0, 100) < start:
                score1 += 1
                start = int(start * 0.5)

                if start < 1:
                    start = 1

        score2 = random.randint(0, score1 - 1)

        return score1, score2


class Substitutes:
    pass


class Injuries:
    pass


class Suspensions:
    pass


class Goalscorers:
    pass
