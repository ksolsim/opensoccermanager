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


class Value:
    def __init__(self, player):
        self.player = player

    def get_value(self):
        '''
        Get player value for associated attributes.
        '''
        age = self.player.get_age()
        skills = self.player.get_skills()

        if self.player.position in ("GK"):
            primary = skills[0]
        elif self.player.position in ("DL", "DR", "DC", "D"):
            primary = skills[1]
        elif self.player.position in ("ML", "MR", "MC", "M"):
            primary = skills[2]
        elif self.player.position in ("AS", "AF"):
            primary = skills[3]

        average = sum(skills[0:6]) + (skills[8] * 1.5) + (skills[5] * 0.2) + (skills[6] * 0.2) + (skills[7] * 1.5)
        average += primary * 2
        average = average / 9

        if primary > 95:
            value_multiplier = 5.25
        elif primary >= 90:
            value_multiplier = 3.5
        elif primary > 85:
            value_multiplier = 2.5
        elif primary > 80:
            value_multiplier = 1.8
        elif primary > 75:
            value_multiplier = 1.5
        elif primary > 70:
            value_multiplier = 1.25
        elif primary > 60:
            value_multiplier = 0.9
        elif primary > 50:
            value_multiplier = 0.55
        elif primary > 40:
            value_multiplier = 0.25
        else:
            value_multiplier = 0.12

        # Age modifier
        if age >= 37:
            age_multiplier = 0.1
        elif age >= 34:
            age_multiplier = 0.25
        elif age >= 32:
            age_multiplier = 0.5
        elif age >= 30:
            age_multiplier = 0.75
        elif age == 29:
            age_multiplier = 0.9
        elif age >= 26:
            age_multiplier = 1
        elif age >= 24:
            age_multiplier = 0.9
        elif age >= 21:
            age_multiplier = 0.8
        elif age >= 18:
            age_multiplier = 0.7
        else:
            age_multiplier = 0.5

        value = ((average * 1000) * average) * value_multiplier * 0.25
        value = value * age_multiplier
        value = self.value_rounder(value)

        return value

    def get_value_as_string(self):
        '''
        Return player value with set currency as string.
        '''
        value = self.get_value()

        if value >= 1000000:
            value = "£%.1fM" % (value / 1000000)
        elif value >= 1000:
            value = "£%iK" % (value / 1000)

        return value

    def value_rounder(self, value):
        '''
        Round calculated player value to nearest divisor.
        '''
        if value >= 1000000:
            divisor = 100000
        elif value >= 10000:
            divisor = 1000

        value = value - (value % divisor)
        value = int(value)

        return value
