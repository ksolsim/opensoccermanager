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


import random

import data
import structures.formations


class Squad:
    def __init__(self):
        self.clubid = None

        self.squad = []
        self.teamselection = TeamSelection()

        self.teamgenerator = TeamGenerator()

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

        for playerid in self.squad:
            player = data.players.get_player_by_id(playerid)
            age += player.get_age()

        age = age / self.get_squad_count()

        return age

    def generate_squad(self):
        '''
        Initiate handler class to generate squad selection.
        '''
        self.teamgenerator.clubid = self.clubid
        self.teamgenerator.squad = self.squad
        self.teamgenerator.teamselection = self.teamselection
        self.teamgenerator.generate_team_selection()


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
        count = sum(1 for playerid in self.team if playerid)

        return count

    def get_subs_count(self):
        '''
        Return number of substitutes selected.
        '''
        count = sum(1 for playerid in self.subs if playerid)

        return count

    def get_team_ids(self):
        '''
        Return list of player ids in team selection.
        '''
        team = [playerid for playerid in self.team if playerid]

        return team

    def get_player_for_position(self, positionid):
        '''
        Get player id for given position id.
        '''
        return self.team[positionid]

    def get_sub_player_for_position(self, positionid):
        '''
        Get substitute player id for given position id.
        '''
        return self.subs[positionid]


class TeamGenerator:
    def __init__(self):
        self.clubid = None

        self.formation = structures.formations.Formations()

    def generate_formation(self):
        '''
        Get formation for use by team.
        '''
        return random.randint(0, 6)

    def generate_team_selection(self):
        '''
        Generate eleven first team members.
        '''
        formationid = self.generate_formation()
        formation = self.formation.get_formation_by_index(formationid)

        selection = []

        for position in formation[1]:
            scores = {}

            for playerid in self.squad:
                if playerid not in selection:
                    player = data.players.get_player_by_id(playerid)

                    skills = player.get_skills()
                    score = sum(skills)

                    if position == player.position:
                        if position in ("GK"):
                            score = player.keeping * 2.5
                        elif position in ("DL", "DR", "DC", "D"):
                            score = player.tackling * 2.5
                        elif position in ("ML", "MR", "MC", "M"):
                            score = player.passing * 2.5
                        elif position in ("AS", "AF"):
                            score = player.shooting * 2.5
                    else:
                        score *= 0.1

                    scores[playerid] = score

            sorted_scores = sorted(scores, key=lambda x: scores[x], reverse=True)
            selection.append(sorted_scores[0])

        for count, playerid in enumerate(selection):
            self.teamselection.add_to_team(playerid, count)

    def generate_sub_selection(self):
        '''
        Generate five substitution members.
        '''
