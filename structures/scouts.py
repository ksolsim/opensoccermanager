#!/usr/bin/env python3

import structures.staff


class Scouts(structures.staff.Staff):
    def __init__(self):
        structures.staff.Staff.__init__(self)

        self.scoutid = 0

    def get_scoutid(self):
        self.scoutid += 1

        return self.scoutid

    def get_scout_by_id(self, scoutid):
        return self.hired[scoutid]

    def generate_initial_staff(self):
        '''
        Generate the first five staff members.
        '''
        for count in range(0, 5):
            scout = Scout()
            scoutid = self.get_scoutid()
            self.available[scoutid] = scout

    def update_contracts(self):
        '''
        Decrement hired scout contract and remove any whose contract expired.
        '''
        for scoutid, scout in self.hired.items():
            scout.contract -= 1

            if scout.contract in (4, 8, 12):
                print("Scout contract ending soon")
            elif scout.contract == 0:
                del self.hired[scoutid]


class Scout(structures.staff.Member):
    def __init__(self):
        structures.staff.Member.__init__(self)


class ScoutReport:
    def __init__(self):
        self.report = {0: "The scouting team report that %s would not be a good signing.",
                       1: "%s would be considered a good signing by the scouting staff.",
                       2: "After some scouting, %s would be an excellent addition to the squad.",
                       3: "The scouts report that %s would be a top prospect for the future.",
                      }

    def get_scout_report(self, reportid):
        '''
        Get scout reporting string for given report id.
        '''
        return self.report[reportid]
