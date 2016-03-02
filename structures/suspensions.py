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


class Suspensions:
    class Suspension:
        def __init__(self):
            self.name = None
            self.period = None

    def __init__(self):
        self.suspensions = {}

        self.populate_data()

    def get_suspension_by_id(self, suspensionid):
        '''
        Return object for given suspension id.
        '''
        return self.suspensions[suspensionid]

    def get_random_suspension(self):
        '''
        Return random suspensions object.
        '''
        return random.choice(list(self.suspensions.values()))

    def populate_data(self):
        data.database.cursor.execute("SELECT * FROM suspension")

        for item in data.database.cursor.fetchall():
            suspension = self.Suspension()
            suspension.suspensionid = item[0]
            suspension.name = item[1]
            suspension.period = (item[2], item[3])
            self.suspensions[suspension.suspensionid] = suspension
