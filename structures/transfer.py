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


class TransferType:
    def __init__(self):
        self.transfer_types = ("Purchase", "Loan", "Free Transfer")

    def get_transfer_types(self):
        '''
        Return list of transfer type strings.
        '''
        return self.transfer_types

    def get_transfer_type_for_index(self, index):
        '''
        Return transfer type string for given index value.
        '''
        return self.transfer_types[index]
