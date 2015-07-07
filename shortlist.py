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


import game


class Shortlist:
    def __init__(self):
        self.players = []

    def add_player(self, playerid):
        '''
        Add passed playerid to shortlisted players.
        '''
        if playerid not in self.players:
            self.players.append(playerid)

    def remove_player(self, playerid):
        '''
        Remove passed playerid from shortlisted players.
        '''
        if playerid in self.players:
            self.players.remove(playerid)

    def get_player_in_shortlist(self, playerid):
        '''
        Return whether a player is currently shortlisted.
        '''
        state = playerid in self.players

        return state
