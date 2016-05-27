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
            self.available[coachid] = Coach(coachid)

    def update_contracts(self):
        '''
        Decrement hired coach contract and remove any whose contract expired.
        '''
        delete = []

        for coachid, coach in self.hired.items():
            coach.contract -= 1

            if coach.contract in (4, 8, 12):
                data.user.club.news.publish("CC03", coach=coach.name, period=coach.contract)
            elif coach.contract == 0:
                data.user.club.news.publish("CC01", coach=coach.name)

                delete.append(coachid)

        for coachid in delete:
            remove = []

            for trainingid, training in club.individual_training.get_individual_training():
                if coachid == training.coachid:
                    remove.append(playerid)

            for playerid in remove:
                club.individual_training.remove_from_training(playerid)

            del self.hired[coachid]

    def hire_staff(self, coachid):
        '''
        Add given coach id to hired staff listing.
        '''
        self.hired[coachid] = self.available[coachid]
        del self.available[coachid]

    def fire_staff(self, coachid):
        '''
        Remove given coach id from hired staff listing and pay off contract.
        '''
        coach = self.hired[coachid]

        data.user.club.accounts.withdraw(amount=coach.get_payout(), category="staffwage")
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
        count = 0

        for trainingid, training in data.user.club.individual_training.get_individual_training():
            if self.coachid == training.coach.coachid:
                count += 1

        return count
