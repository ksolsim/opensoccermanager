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


import os

import club
import game


class Names:
    '''
    User names entered previously by players.
    '''
    def __init__(self):
        self.names = []

        self.filepath = os.path.join(game.data_location, "users.txt")

    def add_name(self, name):
        '''
        Add name to
        '''
        if name in self.names:
            self.names.remove(name)

        self.names.insert(0, name)

        self.write_names()

    def read_names(self):
        '''
        Read existing names from file.
        '''
        self.names = []

        with open(self.filepath, "r") as fp:
            for item in fp.readlines():
                item = item.strip("\n")
                self.names.append(item)

        return self.names

    def write_names(self):
        '''
        Write new names to file.
        '''
        with open(self.filepath, "w") as fp:
            for name in self.names:
                fp.write("%s\n" % (name))


def get_user_club():
    '''
    Return the user club object.
    '''
    clubobj = club.clubitem.clubs[game.teamid]

    return clubobj
