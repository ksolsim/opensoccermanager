#!/usr/bin/env python3


class Ability:
    def __init__(self):
        self.abilities = {0: "Average",
                          1: "Good",
                          2: "Superb"}

    def get_abilities(self):
        '''
        Return full dictionary of abilities.
        '''
        return self.abilities

    def get_ability_for_id(self, abilityid):
        '''
        Return ability string for given id value.
        '''
        return self.abilities[abilityid]
