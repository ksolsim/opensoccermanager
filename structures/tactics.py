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
import structures.formations


class Tactics:
    def __init__(self, club):
        self.club = club
        self.formationid = 0

        self.offside_trap = False
        self.tackling_style = 1
        self.passing_style = 0
        self.playing_style = 1

        self.captain = None
        self.corner_taker = None
        self.free_kick_taker = None
        self.penalty_taker = None

        self.bonus = None

        self.formations = structures.formations.Formations()

    def get_formation_name(self):
        '''
        Get set formation as a string for display.
        '''
        return self.formations.get_formations()[0]

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

    def pay_bonus(self):
        '''
        Pay win bonus percentage specified on tactics screen.
        '''
        if self.bonus:
            bonus = 0

            for player in self.club.squad.teamselection.team:
                bonus += player.wage.get_wage()

            self.club.accounts.withdraw(bonus, "playerwage")
