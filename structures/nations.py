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


class Nations:
    class Nation:
        def __init__(self):
            self.name = ""
            self.denonym = ""

            self.players = []

        def add_to_nation(self, player):
            '''
            Add player to national list.
            '''
            self.players.append(player.playerid)

        def get_national_team(self):
            '''
            Return nested list of players to display in national team.
            '''
            goalkeepers = []
            defenders = []
            midfielders = []
            attackers = []

            for count, playerid in enumerate(self.players):
                player = data.players.get_player_by_id(playerid)

                if player.position == "GK":
                    goalkeepers.append(playerid)

                if player.position in ("DL", "DR", "DC", "D"):
                    defenders.append(playerid)

                if player.position in ("ML", "MR", "MC", "M"):
                    midfielders.append(playerid)

                if player.position in ("AF", "AS"):
                    attackers.append(playerid)

            players = (goalkeepers, defenders, midfielders, attackers)

            return players

        def get_players(self):
            '''
            Return tuple of all players associated with nation.
            '''
            return tuple(self.players)

    def __init__(self):
        self.nations = {}

        self.populate_data()

    def get_nation_by_id(self, nationid):
        '''
        Return the nation object for the given id.
        '''
        return self.nations[nationid]

    def get_nations(self):
        '''
        Return complete dictionary of nations.
        '''
        return self.nations.items()

    def populate_data(self):
        data.database.cursor.execute("SELECT * FROM nation")

        for item in data.database.cursor.fetchall():
            nation = self.Nation()
            nation.nationid = item[0]
            nation.name = item[1]
            nation.denonym = item[2]
            self.nations[nation.nationid] = nation
