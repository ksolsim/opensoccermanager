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


class Merchandise:
    def __init__(self):
        self.merchandise = []

        self.populate_data()

    def get_merchandise(self):
        '''
        Return list of merchandise items.
        '''
        return self.merchandise

    def populate_data(self):
        data.database.cursor.execute("SELECT * FROM merchandise")

        for item in data.database.cursor.fetchall():
            self.merchandise.append(item)
