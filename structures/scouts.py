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
import structures.staff


class Scouts(structures.staff.Staff):
    def __init__(self):
        structures.staff.Staff.__init__(self)

        self.scoutid = 0

    def get_scoutid(self):
        '''
        Return unique scout id.
        '''
        self.scoutid += 1

        return self.scoutid

    def get_scout_by_id(self, scoutid):
        '''
        Return hired scout for given scout id.
        '''
        return self.hired[scoutid]

    def generate_initial_staff(self):
        '''
        Generate the first five staff members.
        '''
        for count in range(0, 5):
            scoutid = self.get_scoutid()
            self.available[scoutid] = Scout(scoutid)

    def update_contracts(self):
        '''
        Decrement hired scout contract and remove any whose contract expired.
        '''
        delete = []

        for scoutid, scout in self.hired.items():
            scout.contract -= 1

            if scout.contract in (4, 8, 12):
                data.user.club.news.publish("SC03", scout=scout.name, period=scout.contract)
            elif scout.contract == 0:
                data.user.club.news.publish("SC01", scout=scout.name)

                delete.append(scoutid)

        for scoutid in delete:
            del self.hired[scoutid]

    def hire_staff(self, scoutid):
        '''
        Add given scout id to hired staff listing.
        '''
        self.hired[scoutid] = self.available[scoutid]
        del self.available[scoutid]

    def fire_staff(self, scoutid):
        '''
        Remove given scout id from hired staff listing and pay off contract.
        '''
        scout = self.hired[scoutid]

        data.user.club.accounts.withdraw(amount=scout.get_payout(), category="staffwage")
        del self.hired[scoutid]


class Scout(structures.staff.Member):
    def __init__(self, scoutid):
        structures.staff.Member.__init__(self)
        self.scoutid = scoutid


class ScoutReport:
    def __init__(self):
        self.report = {0: "The scouting team report that %s would not be a good signing.",
                       1: "%s would be considered a good signing by the scouting staff.",
                       2: "After some scouting, %s would be an excellent addition to the squad.",
                       3: "The scouts report that %s would be a top prospect for the future."}

    def get_scout_report(self, reportid):
        '''
        Get scout reporting string for given report id.
        '''
        return self.report[reportid]
