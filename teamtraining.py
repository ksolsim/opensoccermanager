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


import random

import game


class TeamTraining:
    def __init__(self):
        self.training = [0] * 42

        self.timeout = random.randint(8, 12)
        self.alert = 0

    def generate_schedule(self):
        '''
        Generate team training schedule.
        '''
        values = [count for count in range(2, 18)]
        random.shuffle(values)

        for count in range(0, 6):
            self.training[count * 6] = values[count * 2]
            self.training[count * 6 + 1] = values[count * 2 + 1]
            self.training[count * 6 + 2] = 1
            self.training[count * 6 + 3] = 0
            self.training[count * 6 + 4] = 0
            self.training[count * 6 + 5] = 0

    def get_sunday_training(self):
        '''
        Return True if team is training on Sunday.
        '''
        sunday = False

        for trainingid in self.training[36:42]:
            if trainingid != 0:
                sunday = True

        return sunday

    def get_overworked_training(self):
        '''
        Return True if the team is being overworked.
        '''
        count = 0

        for trainingid in game.clubs[game.teamid].team_training.training:
            if trainingid != 0:
                count += 1

        overwork = count > 18

        return overwork

    def update(self):
        '''
        Process countdown timers for team training updates.
        '''
        if self.timeout > 0:
            self.timeout -= 1
        else:
            self.timeout = random.randint(8, 12)

            game.news.publish("TT02")

        if self.alert == 0:
            if self.get_overworked_training():
                self.alert = random.randint(12, 18)

                club = game.clubs[game.teamid]

                for playerid in club.squad:
                    game.players[playerid].set_morale(-5)

                game.news.publish("TT04")

            if self.get_sunday_training():
                self.alert = random.randint(12, 18)

                for playerid in club.squad:
                    game.players[playerid].set_morale(-3)

                game.news.publish("TT03")
        else:
            self.alert -= 1


def get_schedule_set():
    '''
    Return whether a schedule has been set.
    '''
    schedule = not game.clubs[game.teamid].team_training.training != [0] * 42

    return schedule


def update_schedules():
    '''
    Generate team training schedules for all AI teams.
    '''
    for clubid, club in game.clubs.items():
        if clubid != game.teamid:
            club.team_training.generate_schedule()
