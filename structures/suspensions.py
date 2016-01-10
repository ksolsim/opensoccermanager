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
            self.suspension = None
            self.period = 0

    def __init__(self):
        self.suspensions = {}

        self.messages = SuspensionMessage()

    def get_suspensions(self):
        '''
        Return full dictionary of suspension objects.
        '''
        return self.suspensions


class SuspensionMessage:
    def __init__(self):
        self.messages = {}

        self.populate_data()

    def populate_data(self):
        data.database.cursor.execute("SELECT * FROM suspension")

        for item in data.database.cursor.fetchall():
            self.messages[item[0]] = item[1:4]
