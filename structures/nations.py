#!/usr/bin/env python3

import data


class Nations:
    class Nation:
        def __init__(self):
            self.name = ""
            self.denonym = ""

            self.players = []

        def add_to_nation(self, playerid):
            '''
            Add player to national list.
            '''
            self.players.append(playerid)

        def get_national_team(self):
            '''
            Return tuple of players to display in national team.
            '''

        def get_players(self):
            '''
            Return tuple of all players associated with nation.
            '''
            return tuple(self.players)

    def __init__(self):
        self.nations = {}

        self.populate_data()

    def populate_data(self):
        data.database.cursor.execute("SELECT * FROM nation")

        for item in data.database.cursor.fetchall():
            nationid = item[0]

            nation = self.Nation()
            nation.name = item[1]
            nation.denonym = item[2]
            self.nations[nationid] = nation

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
