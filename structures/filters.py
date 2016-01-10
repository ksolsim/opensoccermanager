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


import collections


class Squad:
    attributes = {"availableonly": False,
                  "position": 0}

    def __init__(self):
        self.options = {}

        self.reset_filter()

    def reset_filter(self):
        '''
        Restore default filtering attributes.
        '''
        for key, value in self.attributes.items():
            self.options[key] = value

    def get_filter_active(self):
        '''
        Return whether a filter is currently applied.
        '''
        return self.attributes != self.options


class Player:
    defaults = (("own_players", True),
                ("position", 0),
                ("value", [0, 20000000]),
                ("age", [16, 50]),
                ("status", 0),
                ("keeping", [0, 99]),
                ("tackling", [0, 99]),
                ("passing", [0, 99]),
                ("shooting", [0, 99]),
                ("heading", [0, 99]),
                ("pace", [0, 99]),
                ("stamina", [0, 99]),
                ("ball_control", [0, 99]),
                ("set_pieces", [0, 99]))
    defaults = collections.OrderedDict(defaults)

    def __init__(self):
        self.options = {}

        self.reset_filter()

    def reset_filter(self):
        '''
        Restore default filtering attributes.
        '''
        self.options = collections.OrderedDict(self.defaults)

    def get_filter_active(self):
        '''
        Return whether a filter is currently applied.
        '''
        return self.options != self.defaults
