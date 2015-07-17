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


import game
import league


class Referees:
    class Referee:
        def __init__(self):
            self.name = ""
            self.matches = 0
            self.fouls = 0
            self.yellows = 0
            self.reds = 0

        def increment_appearance(self, fouls=0, yellows=0, reds=0):
            '''
            Increment referee appearances and match statistics.
            '''
            self.matches += 1
            self.fouls += fouls
            self.yellows += yellows
            self.reds += reds

        def reset_statistics(self):
            '''
            Clear statistics for referee.
            '''
            self.matches = 0
            self.fouls = 0
            self.yellows = 0
            self.reds = 0

    def __init__(self):
        self.referees = {}

        self.populate_data()

    def populate_data(self):
        '''
        Populate referee data.
        '''
        game.database.cursor.execute("SELECT * FROM referee WHERE year = ?", (game.date.year,))
        data = game.database.cursor.fetchall()

        for item in data:
            referee = self.Referee()
            refereeid = item[0]
            game.referees[refereeid] = referee

            referee.name = item[1]
            referee.league = item[2]

            league.leagueitem.leagues[referee.league].referees[refereeid] = referee

    def reset_data(self):
        '''
        Iterate through each referee and clear statistics.
        '''
        for referee in self.referees.values():
            referee.reset_statistics()
