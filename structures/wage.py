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


class Wage:
    def __init__(self, player):
        self.player = player
        self.wage = self.calculate_wage()

    def calculate_wage(self):
        '''
        Get player wage for associated attributes.
        '''
        skills = self.player.get_skills()

        value = self.player.value.get_value()

        if self.player.position in ("GK"):
            primary = skills[0]
        elif self.player.position in ("DL", "DR", "DC", "D"):
            primary = skills[1]
        elif self.player.position in ("ML", "MR", "MC", "M"):
            primary = skills[2]
        elif self.player.position in ("AS", "AF"):
            primary = skills[3]

        average = sum(skills[0:6]) + (skills[8] * 1.5) + (skills[5] * 0.2) + (skills[6] * 0.2) + (skills[7] * 1.5)
        average += primary
        average = average / 9

        if primary >= 95:
            wage_divider = 390
            value_multiplier = 5
        elif primary >= 90:
            wage_divider = 310
            value_multiplier = 3.25
        elif primary >= 85:
            wage_divider = 255
            value_multiplier = 2
        elif primary >= 80:
            wage_divider = 225
            value_multiplier = 1.25
        elif primary >= 75:
            wage_divider = 195
            value_multiplier = 1
        elif primary >= 70:
            wage_divider = 165
            value_multiplier = 0.75
        elif primary >= 60:
            wage_divider = 140
            value_multiplier = 0.55
        elif primary >= 50:
            wage_divider = 120
            value_multiplier = 0.35
        elif primary >= 40:
            wage_divider = 100
            value_multiplier = 0.22
        else:
            wage_divider = 100
            value_multiplier = 0.12

        value = (((average * 1000) * average) * value_multiplier) * 0.25
        wage = value / wage_divider
        wage = self.wage_rounder(wage)

        return wage

    def get_wage(self):
        '''
        Return player wage as value.
        '''
        return self.wage

    def get_wage_as_string(self):
        '''
        Return player wage with set currency as string.
        '''
        if self.wage >= 1000:
            wage = "£%.1fK" % (self.wage / 1000)
        elif self.wage >= 100:
            wage = "£%i" % (self.wage)

        return wage

    def wage_rounder(self, wage):
        '''
        Round calculated player wage to nearest divisor.
        '''
        if wage >= 10000:
            divisor = 100
        else:
            divisor = 10

        wage = int(wage - (wage % divisor))

        return wage
