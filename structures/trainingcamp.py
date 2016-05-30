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


class TrainingCamp:
    def __init__(self):
        self.options = TrainingCampOptions()

    def get_player_cost(self):
        '''
        Return cost of training camp for a single player.
        '''
        quality = ((self.options.quality + 1) * 550) * self.options.quality
        location = ((self.options.location + 1) * 425) * self.options.location
        purpose = (self.options.purpose + 1) * 350

        cost = (quality + location + purpose) * self.options.days

        return cost

    def get_first_team_cost(self):
        '''
        Return cost of training camp for first team.
        '''
        return self.get_player_cost() * 16

    def get_reserve_team_cost(self):
        '''
        Return cost of training camp for reserve team.
        '''
        return self.get_player_cost() * data.user.club.squad.get_reserves_count()

    def get_total_cost(self):
        '''
        Return total training camp cost for selected team members.
        '''
        if self.options.squad == 0:
            squad = data.user.club.squad.get_squad_count()
        elif self.options.squad == 1:
            squad = 16
        elif self.options.squad == 2:
            squad = data.user.club.squad.get_reserves_count()

        cost = squad * self.get_player_cost()

        return cost

    def apply_options(self):
        pass

    def revert_options(self):
        pass


class TrainingCampOptions:
    def __init__(self):
        self.days = 1
        self.quality = 0
        self.location = 0
        self.purpose = 0
        self.squad = 0
