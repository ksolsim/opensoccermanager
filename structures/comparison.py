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


import uigtk.comparison


class Comparison:
    def __init__(self):
        self.comparison = []

    def add_to_comparison(self, playerid):
        '''
        Add player to comparison list.
        '''
        if playerid not in self.comparison:
            self.comparison.insert(0, playerid)

            del self.comparison[2:]

    def get_comparison(self):
        '''
        Return list of two players for comparison.
        '''
        return self.comparison

    def get_comparison_valid(self):
        '''
        Return True if comparison contains two players.
        '''
        return len(self.comparison) == 2

    def get_comparison_count(self):
        '''
        Return number of players stored for comparison.
        '''
        return len(self.comparison)

    def set_show_comparison(self):
        '''
        Show comparison of two players, or error if unable.
        '''
        if self.get_comparison_valid():
            uigtk.comparison.ComparisonDialog()
        else:
            uigtk.comparison.ComparisonError()
