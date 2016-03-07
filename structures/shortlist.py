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


class Shortlist:
    '''
    Class handling shortlisted players via user add or transfer negotiation.
    '''
    def __init__(self):
        self.shortlist = set()

    def get_shortlist(self):
        '''
        Return complete set of shortlisted players.
        '''
        return self.shortlist

    def get_player_in_shortlist(self, player):
        '''
        Return whether given player id is already in the shortlist.
        '''
        return player in self.shortlist

    def add_to_shortlist(self, player):
        '''
        Add specified player id to the shortlist.
        '''
        self.shortlist.add(player)

    def remove_from_shortlist(self, player):
        '''
        Remove specified player id from shortlist.
        '''
        if player in self.shortlist:
            self.shortlist.remove(player)
