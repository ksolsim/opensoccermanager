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


import constants


class Tactics:
    def __init__(self):
        self.formation = 0

        self.captain = None
        self.penalty_taker = None
        self.free_kick_taker = None
        self.corner_taker = None

        self.style = 0
        self.tackling = 0
        self.passing = 0

        self.win_bonus = 0

    def get_formation_string(self):
        '''
        Return the formation string for display.
        '''
        formation = constants.formations[self.formation][0]

        return formation

    def get_formation_positions(self):
        '''
        Return the tuple of positions.
        '''
        formation = constants.formations[self.formation][1]

        return formation
