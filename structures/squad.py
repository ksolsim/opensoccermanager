#!/usr/bin/env python3

import data


class Squad:
    def __init__(self):
        self.squad = []
        self.teamselection = TeamSelection()

    def add_to_squad(self, playerid):
        '''
        Add player id to squad list.
        '''
        self.squad.append(playerid)

    def remove_from_squad(self, playerid):
        '''
        Remove passed player id from squad list.
        '''
        self.squad.remove(playerid)

    def get_available_players(self):
        '''
        Return a tuple of all players which are available to play.
        '''

    def get_unavailable_players(self):
        '''
        Return tuple of all players which are injured, suspended or out on loan.
        '''

    def get_squad(self):
        '''
        Return list of players in squad.
        '''
        return self.squad

    def get_squad_count(self):
        '''
        Return number of players in squad.
        '''
        return len(self.squad)

    def get_average_age(self):
        '''
        Return average age of players in squad.
        '''
        age = 0

        for count, playerid in enumerate(self.squad, start=1):
            player = data.players.get_player_by_id(playerid)
            age += player.get_age()

        age = age / count

        return age


class TeamSelection:
    def __init__(self):
        self.team = [None] * 11
        self.subs = [None] * 5

    def add_to_team(self, playerid, positionid):
        '''
        Add player to team or move if already in team.
        '''
        self.remove_from_team(playerid)

        self.team[positionid] = playerid

    def add_to_subs(self, playerid, positionid):
        '''
        Add player to substitutes or move if already in team.
        '''
        self.remove_from_team(playerid)

        self.subs[positionid] = playerid

    def remove_from_team(self, playerid):
        '''
        Remove player from team.
        '''
        if playerid in self.team:
            index = self.team.index(playerid)
            self.team[index] = None

        if playerid in self.subs:
            index = self.subs.index(playerid)
            self.subs[index] = None

    def remove_from_team_by_position(self, positionid):
        '''
        Remove player from team for given position id.
        '''
        self.team[positionid] = None

    def remove_from_subs_by_position(self, positionid):
        '''
        Remove player from subs for given position id.
        '''
        self.subs[positionid] = None

    def get_team_selection(self):
        '''
        Return team selection list.
        '''
        return self.team

    def get_subs_selection(self):
        '''
        Return substitutes selection list.
        '''
        return self.subs

    def get_team_count(self):
        '''
        Return number of team players selected.
        '''
        count = 0

        for playerid in self.team:
            if playerid:
                count += 1

        return count

    def get_subs_count(self):
        '''
        Return number of substitutes selected.
        '''
        count = 0

        for playerid in self.subs:
            if playerid:
                count += 1

        return count

    def get_team_ids(self):
        '''
        Return list of player ids in team selection.
        '''
        team = [playerid for playerid in self.team if playerid]

        return team

    def get_position_for_player(self, playerid):
        '''
        Get position string for given player id.
        '''
        pass

    def get_player_for_position(self, positionid):
        '''
        Get player id for given position id.
        '''
        pass
