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


import database
import game


class Nations:
    class Nation:
        def __init__(self):
            self.name = ""
            self.denonym = ""

    def __init__(self):
        self.nations = {}

        self.populate_data()

    def populate_data(self):
        '''
        Populate nation data.
        '''
        for item in game.database.importer("nation"):
            nation = self.Nation()
            nationid = item[0]
            self.nations[nationid] = nation

            nation.name = item[1]
            nation.denonym = item[2]


def get_nation(nationid):
    '''
    Return the nation for the given ID.
    '''
    name = nationitem.nations[nationid].name

    return name
