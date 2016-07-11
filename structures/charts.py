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
        goals = sorted(self.goals.items(),
                       key=lambda item: (item[1].league),
                       reverse=True)

        print(goals[:25])

        return goals[:25]

    def get_goals_for_player(self, player):
        '''
        Return goals for given player.
        '''
        goals = 0

        if player.playerid in self.goals:
            goal = self.goals[player.playerid]
            goals = goal.league

        return goals

    def add_goal(self, player, goals):
        '''
        Add player to goals chart.
        '''
        if player.playerid not in self.goals.keys():
            self.goals[player.playerid] = self.Goal(player)

        goal = self.goals[player.playerid]
        goal.league += goals

    def clear_goals(self):
        '''
        Clear list of goals for end of season.
        '''
        self.goals.clear()


class Assists:
    '''
    Storage class for assists made in game.
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
            return None

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


class Cards:
    '''
    Storage class for cards received in game.
    '''
    class Card:
        '''
        Individual card record for each player with cards.
        '''
        def __init__(self, player):
            self.player = player
            self.yellow = 0
            self.red = 0

        def get_points(self):
            '''
            Return points count for card totals.
            '''
            return self.yellow + (self.red * 3)

    def __init__(self):
        self.cards = {}

    def get_sorted_cards(self):
        '''
        Return list of player with most card points.
        '''

    def get_cards_for_player(self, player):
        '''
        Return cards for given player.
        '''
        if player.playerid in self.cards:
            return self.cards[player.playerid]
        else:
            return None

    def get_cards_string_for_player(self, player):
        '''
        Return cards for given player as string.
        '''
        cards = self.get_cards_for_player(player)

        if cards:
            cards = "%i / %i" % (cards.yellow, cards.red)
        else:
            cards = "0 / 0"

        return cards

    def add_card(self, player, yellow=0, red=0):
        '''
        Add player to card list with points total.
        '''
        if player not in self.cards.values():
            card = Card()
            card.yellow += yellow
            card.red += red
            self.cards[player.playerid] = card
        else:
            card = self.cards[player.playerid]
            card.yellow += yellow
            card.red += red

    def clear_cards(self):
        '''
        Clear list of cards for season.
        '''
        self.cards.clear()
