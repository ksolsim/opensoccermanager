#!/usr/bin/env python3

import random

class TeamTraining(list):
    def __init__(self):
        for count in range(0, 42):
            self.append(0)

        self.timeout = random.randint(8, 12)

    def get_random_schedule(self):
        '''
        Apply new random schedule for team training.
        '''
        values = [count for count in range(2, 18)]
        random.shuffle(values)

        for count in range(0, 6):
            self[count * 6] = values[count * 2]
            self[count * 6 + 1] = values[count * 2 + 1]
            self[count * 6 + 2] = 1
            self[count * 6 + 3] = 0
            self[count * 6 + 4] = 0
            self[count * 6 + 5] = 0

    def get_sunday_training(self):
        '''
        Return True if team is training on Sunday.
        '''
        sunday = False

        for trainingid in self[36:42]:
            if trainingid != 0:
                sunday = True

        return sunday

    def get_overworked_training(self):
        '''
        Return True if the team is being overworked.
        '''
        count = 0

        for trainingid in self:
            if trainingid != 0:
                count += 1

        overwork = count > 18

        return overwork

    def get_schedule_set(self):
        '''
        Return whether a schedule has been set.
        '''
        state = self != [0] * 42

        return state

    def get_individual_set(self):
        '''
        Return whether individual training has been assigned.
        '''
        state = 1 in self

        return state

    def update_schedule(self):
        '''
        Generate new training schedule and apply.
        '''
        if self.timeout == 0:
            self.get_random_schedule()
            self.timeout = random.randint(8, 12)
        else:
            self.timeout -= 1
