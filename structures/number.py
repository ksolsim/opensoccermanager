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


class Number:
    '''
    Ordinal number retrieval for dates and positions.
    '''
    def __init__(self):
        self.first = "st"
        self.second = "nd"
        self.third = "rd"
        self.other = "th"

    def get_ordinal_number(self, number):
        '''
        Return ordinal number for display as string.
        '''
        if number == 1:
            output = "%i%s" % (number, self.first)
        elif number == 2:
            output = "%i%s" % (number, self.second)
        elif number == 3:
            output = "%i%s" % (number, self.third)
        else:
            output = "%i%s" % (number, self.other)

        return output
