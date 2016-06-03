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


class Assists:
    '''
    Storage class for assists.
    '''
    class Assist:
        '''
        Individual assist record for each player with an assist.
        '''
        def __init__(self, player):
            self.player = player

            self.league = 0

    def __init__(self):
        self.assists = {}

    def get_sorted_assists(self):
        '''
        Return sorted list of assisters.
        '''

    def get_assists_for_player(self, player):
        '''
        Return assists for given player.
        '''
        if player.playerid in self.assists:
            return self.assists[player.playerid]
        else:
            return 0

    def add_assist(self, player, assists):
        '''
        Add player to assists chart.
        '''
        if player.playerid in self.assists:
            assist = self.Assist(player)
            assist.league += assists
            self.assists[player.playerid] = assist
        else:
            assist = self.assists[player.playerid]
            assist.league += assists

    def clear_assists(self):
        '''
        Clear list of goals for end of season.
        '''
        self.assists.clear()


class Goalscorers:
    '''
    Storage class for goals scored in game.
    '''
    class Goal:
        '''
        Individual goal record for each player with a goal.
        '''
        def __init__(self, player):
            self.player = player

            self.league = 0

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
            return 0

    def add_goal(self, player, goals):
        '''
        Add player to goals chart.
        '''
        if player.playerid in self.goals:
            goal = self.Goal(player)
            goal.league += goals
            self.goals[player.playerid] = goal
        else:
            goal = self.goals[player.playerid]
            goal.league += goals

    def clear_goals(self):
        '''
        Clear list of goals for end of season.
        '''
        self.goals.clear()
