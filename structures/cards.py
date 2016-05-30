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
    '''
    Storage class for assists.
    '''
    def __init__(self):
        self.cards = {}

    def add_player(self, player, card):
        '''
        Add player to card list with points total.
        '''
        if card == 0:
            points = 1
        else:
            points = 3

        if player not in self.cards.values():
            self.cards[player.playerid] = points
        else:
            self.cards[player.playerid] += points

    def get_sorted_cards(self):
        '''
        Return list of player with most card points.
        '''
