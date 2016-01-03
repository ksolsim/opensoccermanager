#!/usr/bin/env python3

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
        training.start_value = player.get_skills()[skill]
        self.individual_training[playerid] = training

    def remove_from_training(self, playerid):
        '''
        Remove passed player id from individual training.
        '''
        del self.individual_training[playerid]

    def get_player_in_training(self, playerid):
        '''
        Return whether passed player id is individual training.
        '''
        return playerid in self.individual_training
