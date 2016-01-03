#!/usr/bin/env python3

import structures.formations


class Tactics:
    def __init__(self):
        self.formationid = 0

        self.offside_trap = False
        self.tackling_style = 1
        self.passing_style = 0
        self.playing_style = 1

        self.captain = None
        self.corner_taker = None
        self.free_kick_taker = None
        self.penalty_taker = None

        self.formations = structures.formations.Formations()

    def get_formation_name(self):
        '''
        Get set formation as a string for display.
        '''
        formation = self.formations.get_formations()[0]

        return formation

    def get_formation_positions(self):
        '''
        Get set positions for currently active formation.
        '''
        return self.formations.get_positions(self.formationid)

    def remove_responsiblity(self, playerid):
        '''
        Removes specified player id from role of responsibility.
        '''
        if playerid == self.captain:
            self.captain = None

        if playerid == self.corner_taker:
            self.corner_taker = None

        if playerid == self.free_kick_taker:
            self.free_kick_taker = None

        if playerid == self.penalty_taker:
            self.penalty_taker = None
