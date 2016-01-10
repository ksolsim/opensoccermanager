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
        Return complete list of shortlisted players.
        '''
        return self.shortlist

    def get_player_in_shortlist(self, playerid):
        '''
        Return whether given player id is already in the shortlist.
        '''
        return playerid in self.shortlist

    def add_to_shortlist(self, playerid):
        '''
        Add specified player id to the shortlist.
        '''
        self.shortlist.add(playerid)

    def remove_from_shortlist(self, playerid):
        '''
        Remove specified player id from shortlist.
        '''
        if playerid in self.shortlist:
            self.shortlist.remove(playerid)
