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
import uigtk.shared


class Squad:
    def __init__(self, club):
        self.club = club

        self.squad = {}
        self.teamselection = TeamSelection()
        self.teamgenerator = TeamGenerator(club)

    def add_to_squad(self, player):
        '''
        Add player id to squad list.
        '''
        self.squad[player.playerid] = player

    def remove_from_squad(self, playerid):
        '''
        Remove passed player id from squad list.
        '''
        del self.squad[playerid]

    def get_player_in_squad(self, player):
        '''
        Return whether player id is in squad listing.
        '''
        return player in self.squad.values()

    def get_player_available(self, player):
        '''
        Get whether passed player is available to play.
        '''
        available = not player.injury.get_injured() and not player.suspension.get_suspended()

        return available

    def get_injured_players(self):
        '''
        Return list of injured players from squad.
        '''
        injured = []

        for playerid, player in self.squad.items():
            if player.injury.get_injured():
                injured.append(player)

        return injured

    def get_suspended_players(self):
        '''
        Return list of suspended players from squad.
        '''
        suspended = []

        for playerid, player in self.squad.items():
            if player.suspension.get_suspended():
                suspended.append(player)

        return suspended

    def get_squad(self):
        '''
        Return list of players in squad.
        '''
        return self.squad.items()

    def get_squad_count(self):
        '''
        Return number of players in squad.
        '''
        return len(self.squad)

    def get_release_permitted(self):
        '''
        Determine whether player can be released from club.
        '''
        if len(self.squad) < 17:
            uigtk.shared.SquadSize(1)
            return False
        elif len(self.squad) > 29:
            uigtk.shared.SquadSize(2)
            return False
        else:
            return True

    def get_reserves_count(self):
        '''
        Return list of players not in squad.
        '''
        return sum(1 for player in self.squad.keys() if player not in self.teamselection.team)

    def get_average_age(self):
        '''
        Return average age of players in squad.
        '''
        return sum(player.get_age() for player in self.squad.values()) / self.get_squad_count()

    def generate_squad(self):
        '''
        Initiate handler class to generate squad selection.
        '''
        self.teamgenerator.teamselection = self.teamselection
        self.teamgenerator.generate_team_selection()
        self.teamgenerator.generate_sub_selection()


class TeamSelection:
    def __init__(self):
        self.team = [None] * 11
        self.subs = [None] * 5

    def add_to_team(self, player, positionid):
        '''
        Add player to team or move if already in team.
        '''
        self.remove_from_team(player)

        self.team[positionid] = player

    def add_to_subs(self, player, positionid):
        '''
        Add player to substitutes or move if already in team.
        '''
        self.remove_from_team(player)

        self.subs[positionid] = player

    def remove_from_team(self, player):
        '''
        Remove player from team.
        '''
        if player in self.team:
            index = self.team.index(player)
            self.team[index] = None

        if player in self.subs:
            index = self.subs.index(player)
            self.subs[index] = None

        data.user.club.tactics.remove_responsiblity(player)

    def remove_from_team_by_position(self, positionid):
        '''
        Remove player from team for given position id.
        '''
        player = self.team[positionid]
        data.user.club.tactics.remove_responsiblity(player)
        self.team[positionid] = None

    def remove_from_subs_by_position(self, positionid):
        '''
        Remove player from subs for given position id.
        '''
        player = self.team[positionid]
        data.user.club.tactics.remove_responsiblity(player)
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
        return sum(1 for player in self.team if player)

    def get_subs_count(self):
        '''
        Return number of substitutes selected.
        '''
        return sum(1 for player in self.subs if player)

    def get_team_ids(self):
        '''
        Return list of player ids in team selection.
        '''
        return [player.playerid for player in self.team if player]

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

    def get_injured_players(self):
        '''
        Return list of injured players in team selection.
        '''
        injured = []

        for selection in (self.team, self.subs):
            for player in selection:
                if player:
                    if player.injury.get_injured():
                        injured.append(player)

        return injured

    def get_suspended_players(self):
        '''
        Return list of suspended players from squad.
        '''
        suspended = []

        for selection in (self.team, self.subs):
            for player in selection:
                if player:
                    if player.suspension.get_suspended():
                        suspended.append(player)

        return suspended

    def pay_win_bonus(self):
        '''
        Pay contract win bonus for players in team selection.
        '''
        total = sum(player.contract.winbonus for player in self.team if player)

        data.user.club.accounts.withdraw(amount=total, category="playerwage")


class TeamGenerator:
    def __init__(self, club):
        self.club = club

        self.formation = structures.formations.Formations()

    def generate_formation(self):
        '''
        Get formation for use by team.
        '''
        return random.randint(0, 6)

    def generate_team_selection(self):
        '''
        Generate eleven first team members and assign to first team.
        '''
        formationid = self.generate_formation()
        formation = self.formation.get_formation_by_id(formationid)

        selection = []

        for position in formation[1]:
            scores = {}

            for playerid, player in self.club.squad.get_squad():
                if player not in selection:
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

                    scores[player] = score

            sorted_scores = sorted(scores, key=lambda x: scores[x], reverse=True)
            selection.append(sorted_scores[0])

        for count, player in enumerate(selection):
            self.teamselection.add_to_team(player, count)

    def generate_sub_selection(self):
        '''
        Generate five substitution members and assign to substitutions.
        '''
        selection = []

        for count in range(0, 5):
            scores = {}

            for playerid, player in self.club.squad.get_squad():
                if player not in selection:
                    if player not in self.teamselection.get_team_selection():
                        skills = player.get_skills()
                        score = sum(skills)

                        if player.position in ("GK"):
                            score = player.keeping * 2.5
                        elif player.position in ("DL", "DR", "DC", "D"):
                            score = player.tackling * 2.5
                        elif player.position in ("ML", "MR", "MC", "M"):
                            score = player.passing * 2.5
                        elif player.position in ("AS", "AF"):
                            score = player.shooting * 2.5
                        else:
                            score *= 0.1

                        scores[player] = score

            sorted_scores = sorted(scores, key=lambda x: scores[x], reverse=True)
            selection.append(sorted_scores[0])

        for count, player in enumerate(selection):
            self.teamselection.add_to_subs(player, count)
