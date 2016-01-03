#!/usr/bin/env python3

import random

import data
import structures.staff


class Coaches(structures.staff.Staff):
    def __init__(self):
        structures.staff.Staff.__init__(self)

        self.coachid = 0

    def get_coachid(self):
        '''
        Return unique coach id.
        '''
        self.coachid += 1

        return self.coachid

    def get_coach_by_id(self, coachid):
        '''
        Return hired coach for given coach id.
        '''
        return self.hired[coachid]

    def generate_initial_staff(self):
        '''
        Generate the first five staff members.
        '''
        for count in range(0, 5):
            coachid = self.get_coachid()
            coach = Coach(coachid)
            self.available[coachid] = coach

    def update_contracts(self):
        '''
        Decrement hired coach contract and remove any whose contract expired.
        '''
        for coachid, coach in self.hired.items():
            coach.contract -= 1

            if coach.contract == 0:
                del self.hired[coachid]

    def hire_staff(self, coachid):
        self.hired[coachid] = self.available[coachid]
        del self.available[coachid]

    def fire_staff(self, coachid):
        coach = self.hired[coachid]
        club = data.clubs.get_club_by_id(data.user.team)

        club.accounts.withdraw(coach.get_payout(), "staffwage")
        del self.hired[coachid]


class Coach(structures.staff.Member):
    def __init__(self, coachid):
        structures.staff.Member.__init__(self)
        self.coachid = coachid
        self.speciality = random.randint(0, 5)

    def count_players_training(self):
        '''
        Return number of players being individually trained by coach.
        '''
        club = data.clubs.get_club_by_id(data.user.team)

        count = 0

        for trainingid, training in club.individual_training.get_individual_training():
            if self.coachid == training.coachid:
                count += 1

        return count
