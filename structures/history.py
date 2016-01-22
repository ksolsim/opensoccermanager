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


import data


class History:
    def __init__(self, playerid):
        self.history = []

        self.playerid = playerid

    def get_current_season(self):
        '''
        Return tuple of current season history data.
        '''
        player = data.players.get_player_by_id(self.playerid)
        club = data.clubs.get_club_by_id(player.squad)

        current = (data.date.get_season(),
                   club.name,
                   "",
                   player.appearances,
                   player.goals,
                   player.assists,
                   "%i/%i" % (player.yellow_cards, player.red_cards),
                   player.man_of_the_match)

        return current

    def add_season(self, season):
        '''
        Add season data to history list.
        '''
        self.history.append(season)

    def get_history(self):
        '''
        Return history in descending order by season.
        '''
        return sorted(self.history, reverse=True)
