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


class Goalscorers:
    '''
    Storage class for goals scored in game.
    '''
    def __init__(self):
        self.goals = {}

    def get_sorted_goals(self):
        '''
        Return sorted list of goalscorers.
        '''

    def get_goals_for_player(self, player):
        '''
        Return goals for given player.
        '''
        if player.playerid in self.goals:
            return self.goals[player.playerid]
        else:
            return None

    def add_goal(self, player, goals):
        '''
        Add player to goals chart.
        '''
        if player.playerid in self.goals:
            goal = Goal(player)
            goal.league += goals
            self.goals[player.player] = goal
        else:
            goal = self.goals[player.player]
            goal.league += goals

    def clear_goals(self):
        '''
        Clear list of goals for end of season.
        '''
        self.goals.clear()


class Goal:
    '''
    Individual goal object for each player.
    '''
    def __init__(self, player):
        self.player = player

        self.league = 0
