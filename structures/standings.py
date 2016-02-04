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
import structures.number


class Standings:
    def __init__(self):
        self.standings = {}

        self.number = structures.number.Number()

    def add_club(self, clubid):
        '''
        Adds passed clubid to standing with new object.
        '''
        self.standings[clubid] = Standing()

    def get_data(self):
        '''
        Return the sorted league standings.
        '''
        standings = []

        for clubid, standing in self.standings.items():
            club = data.clubs.get_club_by_id(clubid)
            item = standing.get_standing_data()

            item.insert(0, clubid)

            standings.append(item)

        if data.calendar.event == 0:
            standings = sorted(standings,
                               key=lambda item: data.clubs.get_club_by_id(item[0]).name)
        else:
            standings = sorted(standings,
                               key=lambda item: (item[8], item[7], item[5], item[6]),
                               reverse=True)

        return standings

    def get_standing_for_club(self, clubid):
        '''
        Get standing data list for given club id.
        '''
        for standing in self.get_data():
            if clubid == standing[0]:
                return standing[1:8]

    def get_position_for_club(self, clubid):
        '''
        Return the position for the given club id.
        '''
        for position, standing in enumerate(self.get_data(), start=1):
            if clubid == standing[0]:
                return self.number.get_ordinal_number(position)

    def get_club_for_position(self, position):
        '''
        Return the clubid for the given position.
        '''
        standings = self.get_data()
        clubid = standings[position - 1]

        return clubid

    def update_standing(self, fixture):
        '''
        Update standings for given fixture object.
        '''
        home = self.standings[fixture.home.clubid]
        away = self.standings[fixture.away.clubid]

        home.played += 1
        away.played += 1

        if fixture.result[0] > fixture.result[1]:
            home.wins += 1
            away.losses += 1
            home.goals_for += fixture.result[0]
            home.goals_against += fixture.result[1]
            away.goals_for += fixture.result[1]
            away.goals_against += fixture.result[0]
            home.goal_difference = home.goals_for - home.goals_against
            away.goal_difference = away.goals_for - away.goals_against
            home.points += 3
        elif fixture.result[0] < fixture.result[1]:
            away.wins += 1
            home.losses += 1
            home.goals_for += fixture.result[0]
            home.goals_against += fixture.result[1]
            away.goals_for += fixture.result[1]
            away.goals_against += fixture.result[0]
            home.goal_difference = home.goals_for - home.goals_against
            away.goal_difference = away.goals_for - away.goals_against
            away.points += 3
        else:
            home.draws += 1
            away.draws += 1
            home.goals_for += fixture.result[0]
            home.goals_against += fixture.result[1]
            away.goals_for += fixture.result[1]
            away.goals_against += fixture.result[0]
            home.goal_difference = home.goals_for - home.goals_against
            away.goal_difference = away.goals_for - away.goals_against
            home.points += 1
            away.points += 1

    def clear_standings(self):
        '''
        Completely empty standings list.
        '''
        self.standings.clear()


class Standing:
    def __init__(self):
        self.played = 0
        self.wins = 0
        self.draws = 0
        self.losses = 0
        self.goals_for = 0
        self.goals_against = 0
        self.goal_difference = 0
        self.points = 0

    def get_standing_data(self):
        '''
        Return the standing data as a list.
        '''
        data = [self.played,
                self.wins,
                self.draws,
                self.losses,
                self.goals_for,
                self.goals_against,
                self.goal_difference,
                self.points]

        return data
