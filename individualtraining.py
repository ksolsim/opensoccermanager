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


class IndividualTraining:
    class Item:
        def __init__(self):
            self.playerid = 0
            self.coachid = 0
            self.skill = 0
            self.intensity = 1
            self.start_value = 0
            self.timeout = 0

        def get_status(self):
            '''
            Return the individual training status.
            '''
            player = game.players[self.playerid]
            skills = player.get_skills()

            if self.start_value == skills[self.skill]:
                status = "Training has just started."
            elif self.timeout == 0:
                status = "Player is no longer improving."

            return status

    def __init__(self):
        self.individual_training = {}

    def update(self):
        '''
        Update timeout.
        '''
        for item in self.individual_training.values():
            item.timeout -= 1


