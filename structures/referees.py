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

    def __init__(self, season):
        self.referees = {}
        self.season = season

        self.populate_data()

    def get_referees(self):
        '''
        Return dictionary items for all referees.
        '''
        return self.referees.items()

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
