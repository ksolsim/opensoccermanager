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


import operator

import game


class Standings:
    class Item:
        def __init__(self):
            self.played = 0
            self.wins = 0
            self.draws = 0
            self.losses = 0
            self.goals_for = 0
            self.goals_against = 0
            self.goal_difference = 0
            self.points = 0

        def get_data(self):
            data = [self.played,
                    self.wins,
                    self.draws,
                    self.losses,
                    self.goals_for,
                    self.goals_against,
                    self.goal_difference,
                    self.points
                   ]

            return data

        def reset_data(self):
            self.played = 0
            self.wins = 0
            self.draws = 0
            self.losses = 0
            self.goals_for = 0
            self.goals_against = 0
            self.goal_difference = 0
            self.points = 0

    def __init__(self):
        self.clubs = {}

    def add_item(self, clubid):
        '''
        Create initial data item for given club.
        '''
        self.clubs[clubid] = self.Item()

        return self.clubs[clubid]

    def update_item(self, result):
        '''
        Update information for specified club.
        '''
        team1 = result[0]
        team2 = result[3]

        self.clubs[team1].played += 1
        self.clubs[team2].played += 1

        if result[1] > result[2]:
            self.clubs[team1].wins += 1
            self.clubs[team2].losses += 1
            self.clubs[team1].goals_for += result[1]
            self.clubs[team1].goals_against += result[2]
            self.clubs[team1].goal_difference = self.clubs[team1].goals_for - self.clubs[team1].goals_against
            self.clubs[team2].goals_for += result[2]
            self.clubs[team2].goals_against += result[1]
            self.clubs[team2].goal_difference = self.clubs[team2].goals_for - self.clubs[team2].goals_against
            self.clubs[team1].points += 3

            game.clubs[team1].form.append("W")
            game.clubs[team2].form.append("L")
        elif result[2] > result[1]:
            self.clubs[team2].wins += 1
            self.clubs[team1].losses += 1
            self.clubs[team2].goals_for += result[2]
            self.clubs[team2].goals_against += result[1]
            self.clubs[team2].goal_difference = self.clubs[team2].goals_for - self.clubs[team2].goals_against
            self.clubs[team1].goals_for += result[1]
            self.clubs[team1].goals_against += result[2]
            self.clubs[team1].goal_difference = self.clubs[team1].goals_for - self.clubs[team1].goals_against
            self.clubs[team2].points += 3

            game.clubs[team1].form.append("L")
            game.clubs[team2].form.append("W")
        else:
            self.clubs[team1].draws += 1
            self.clubs[team2].draws += 1
            self.clubs[team1].goals_for += result[1]
            self.clubs[team1].goals_against += result[2]
            self.clubs[team1].goal_difference = self.clubs[team1].goals_for - self.clubs[team1].goals_against
            self.clubs[team2].goals_for += result[2]
            self.clubs[team2].goals_against += result[1]
            self.clubs[team2].goal_difference = self.clubs[team2].goals_for - self.clubs[team2].goals_against
            self.clubs[team1].points += 1
            self.clubs[team2].points += 1

            game.clubs[team1].form.append("D")
            game.clubs[team2].form.append("D")

    def reset_standings(self):
        '''
        Clear information back to defaults.
        '''
        for item in self.clubs.values():
            item.reset_data()

    def get_data(self):
        '''
        Return the sorted league standings.
        '''
        standings = []

        for key, value in self.clubs.items():
            item = []

            club = game.clubs[key]
            item = value.get_data()

            form = "".join(club.form[-6:])

            item.insert(0, key)
            item.insert(1, club.name)
            item.append(form)

            standings.append(item)

        if game.date.eventindex > 0:
            standings = sorted(standings,
                                key=operator.itemgetter(9, 8, 6, 7),
                                reverse=True
                               )
        else:
            standings = sorted(standings,
                                key=operator.itemgetter(1)
                               )

        return standings

    def find_champion(self):
        '''
        Return club which is top of the league.
        '''
        standings = self.get_data()
        champion = standings[0]

        return champion

    def find_position(self, teamid):
        '''
        Return position for given club.
        '''
        standings = self.get_data()

        position = 0

        for count, item in enumerate(standings, start=1):
            if item[0] == teamid:
                position = count

        return position

    def get_position_string(self, teamid):
        '''
        Return position as a display position.
        '''
        position = self.find_position(teamid)

        if position == 1:
            output = "%ist" % (position)
        elif position == 2:
            output = "%ind" % (position)
        elif position == 3:
            output = "%ird" % (position)
        elif position >= 4:
            output = "%ith" % (position)

        return output
