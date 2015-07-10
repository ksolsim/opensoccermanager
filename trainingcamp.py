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


import game


class TrainingCamp:
    def __init__(self):
        self.days = 1
        self.quality = 1
        self.location = 1
        self.purpose = 1
        self.squad = 0

    def get_player_total(self):
        '''
        Calculate cost per player of training camp with current options.
        '''
        quality = (self.quality * 550) * self.quality
        location = (self.location * 425) * self.location
        purpose = self.purpose * 350

        cost = (quality + location + purpose) * self.days

        return cost

    def get_total(self):
        '''
        Calculate cost of training camp for current options.
        '''
        player = self.get_player_total()

        if self.squad == 0:
            squad = 16
        elif self.squad == 1:
            count = 0

            for item in game.clubs[game.teamid].squad:
                if item not in game.clubs[game.teamid].team.values():
                    count += 1

            squad = count
        elif self.squad == 2:
            squad = len(game.clubs[game.teamid].squad)

        total = player * squad

        return total

    def revert_options(self):
        '''
        Reset selected options back to defaults.
        '''
        self.days = 1
        self.quality = 1
        self.location = 1
        self.purpose = 1
        self.squad = 0

    def get_options(self):
        '''
        Return a tuple of the current options.
        '''
        options = self.days, self.quality, self.location, self.purpose, self.squad

        return options

    def apply_training(self):
        '''
        Take options provided by training camp screen and determine player changes.
        '''
        # Determine players to take on training camp
        squad = []

        if self.squad == 0:
            for playerid in game.clubs[game.teamid].team.values():
                if playerid != 0:
                    squad.append(playerid)
        elif self.squad == 1:
            for playerid in game.clubs[game.teamid].squad:
                if playerid not in game.clubs[game.teamid].team.values():
                    squad.append(playerid)
        else:
            squad = [playerid for playerid in game.clubs[game.teamid].squad]

        if self.purpose == 1:
            # Leisure
            morale = (self.quality) + (self.location) * self.days
            morale = morale * 3
            fitness = 1
        elif self.purpose == 2:
            # Schedule
            morale = (self.quality) + (self.location) * self.days
            morale = morale * 1.5
            individual_training()
            fitness = 3
        elif self.purpose == 3:
            # Intensive
            morale = (-self.quality) + (-self.location) * -self.days
            morale = -morale * 2
            fitness = 8

        for playerid in squad:
            player = game.players[playerid]
            player.set_morale(morale)
            events.adjust_fitness(recovery=fitness)
