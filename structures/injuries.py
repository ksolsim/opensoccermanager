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


class Injuries:
    class Injury:
        def __init__(self):
            self.name = ""
            self.period = (0, 0)
            self.impact = (0, 0)

    def __init__(self):
        self.injuries = {}

        self.populate_data()

    def get_injury_by_id(self, injuryid):
        '''
        Return injury object for given injury id.
        '''
        return self.injuries[injuryid]

    def populate_data(self):
        data.database.cursor.execute("SELECT * FROM injury")

        for item in data.database.cursor.fetchall():
            injury = self.Injury()
            injury.name = item[1]
            injury.period = (item[2], item[3])
            injury.impact = (item[4], item[5])
            self.injuries[item[0]] = injury
