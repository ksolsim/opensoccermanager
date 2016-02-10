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


class Referees:
    class Referee:
        def __init__(self):
            self.name = ""
            self.league = None

            self.games = 0
            self.yellow_cards = 0
            self.red_cards = 0

        def get_points(self):
            '''
            Calculate points for cards issued by referee.
            '''
            return (self.yellow_cards * 1) + (self.red_cards * 3)

    def __init__(self, season):
        self.referees = {}
        self.season = season

        self.populate_data()

    def get_referees(self):
        '''
        Return dictionary items for all referees.
        '''
        return self.referees.items()

    def get_referee_by_id(self, refereeid):
        '''
        Fetch referee for given referee id.
        '''
        return self.referees[refereeid]

    def get_referee_data(self):
        '''
        Return sorted list of referee data.
        '''
        referees = []

        for refereeid, referee in self.get_referees():
            referees.append([refereeid,
                             referee.name,
                             referee.league,
                             referee.games,
                             referee.yellow_cards,
                             referee.red_cards,
                             referee.get_points()])

        if data.calendar.event == 0:
            referees = sorted(referees,
                               key=lambda item: data.referees.get_referee_by_id(item[0]).name)
        else:
            referees = sorted(referees,
                               key=lambda item: (item[5], item[4], item[3], item[2]),
                               reverse=True)

        return referees

    def populate_data(self):
        data.database.cursor.execute("SELECT * FROM referee \
                                     JOIN refereeattr \
                                     ON referee.id = refereeattr.referee \
                                     WHERE refereeattr.year = ?",
                                     (self.season,))

        for item in data.database.cursor.fetchall():
            referee = self.Referee()
            refereeid = item[0]
            self.referees[refereeid] = referee

            referee.name = item[1]
            referee.league = item[5]

            league = data.leagues.get_league_by_id(referee.league)
            league.add_referee(refereeid)
