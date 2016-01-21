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


class Cards:
    def __init__(self):
        self.cards = {}

    def add_player(self, playerid, card):
        '''
        Add player to card list with points total.
        '''
        if card == 0:
            points = 1
        else:
            points = 3

        if playerid not in self.cards.keys():
            self.cards[playerid] = points
        else:
            self.cards[playerid] += points

    def get_sorted_cards(self):
        '''
        Return list of player with most card points.
        '''
