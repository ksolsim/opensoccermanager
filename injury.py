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


class Injuries:
    class Injury:
        def __init__(self):
            self.name = ""
            self.min_period = 0
            self.max_period = 0
            self.min_fitness = 0
            self.max_fitness = 0

    def __init__(self):
        self.injuries = {}

        self.populate_data()

    def get_random_injury(self):
        '''
        Return a random injury ID.
        '''
        injuryid = list(self.injuries.keys())
        injury = random.choice(injuryid)

        return injuryid

    def populate_data(self):
        '''
        Populate injury data.
        '''
        for item in game.database.importer("injury"):
            self.injuries[item[0]] = item[1:]
