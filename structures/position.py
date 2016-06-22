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


class Position:
    def __init__(self):
        self.positions = {"GK": "Goalkeeper",
                          "DL": "Left-Sided Defender",
                          "DR": "Right-Sided Defender",
                          "DC": "Central Defender",
                          "D": "Defender",
                          "ML": "Left-Sided Midfielder",
                          "MR": "Right-Sided Midfielder",
                          "MC": "Central Midfielder",
                          "M": "Midfielder",
                          "AF": "Forward",
                          "AS": "Striker"}

    def get_position_name_by_positionid(self, positionid):
        '''
        Return position string for given position id.
        '''
        return self.positions[positionid]
