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


class IndividualTraining:
    class Item:
        def __init__(self):
            self.coachid = None
            self.skill = None
            self.intensity = 1
            self.start_value = 0
            self.status = 0

    def __init__(self):
        self.individual_training = {}

    def get_individual_training(self):
        '''
        Return dictionary items for individual training.
        '''
        return self.individual_training.items()

    def add_to_training(self, training):
        '''
        Add player along with details to individual training.
        '''
        playerid, coachid, skill, intensity = training

        player = data.players.get_player_by_id(playerid)

        training = self.Item()
        training.coachid = coachid
        training.skill = skill
        training.intensity = intensity
        training.start_value = player.get_skill_by_index(skill)
        self.individual_training[playerid] = training

    def remove_from_training(self, playerid):
        '''
        Remove passed player id from individual training.
        '''
        if playerid in self.individual_training:
            del self.individual_training[playerid]

    def get_player_in_training(self, playerid):
        '''
        Return whether passed player id is individual training.
        '''
        return playerid in self.individual_training

    def get_individual_training_by_playerid(self, playerid):
        '''
        Return individual training object for given player id.
        '''
        return self.individual_training[playerid]


class Status:
    def __init__(self):
        self.status = {0: "Just started training.",
                       1: "Improving slowly.",
                       2: "Making good progress.",
                       3: "Quickly developing.",
                       4: "No longer progressing."}

    def get_status(self, index):
        '''
        Get status string for given index.
        '''
        return self.status[index]
