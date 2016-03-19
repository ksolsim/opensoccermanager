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
import structures.buildings


class Names:
    def __init__(self):
        self.names = ("North",
                      "East",
                      "South",
                      "West",
                      "North East",
                      "South East",
                      "South West",
                      "North West")

    def get_names(self):
        '''
        Return tuple of stadium stand names.
        '''
        return self.names


class Stadiums:
    class Stadium:
        def __init__(self):
            self.name = ""
            self.condition = 100
            self.maintenance = 100
            self.warnings = 0
            self.fines = 0

            self.main_stands = []
            self.corner_stands = []

            self.buildings = structures.buildings.Buildings()

        def get_capacity(self):
            '''
            Return total stadium capacity.
            '''
            capacity = 0

            for stands in (self.main_stands, self.corner_stands):
                for stand in stands:
                    capacity += stand.capacity

            capacity += self.get_box_capacity()

            return capacity

        def get_box_capacity(self):
            '''
            Return total number of executive box seats.
            '''
            return sum(stand.box for stand in self.main_stands)

        def get_standing_uncovered(self):
            '''
            Return whether stadium has any uncovered standing areas.
            '''
            for stands in (self.main_stands, self.corner_stands):
                for stand in stands:
                    if stand.capacity > 0 and not stand.roof and not stand.seating:
                        return True

            return False

        def get_standing_covered(self):
            '''
            Return whether stadium has any covered standing areas.
            '''
            for stands in (self.main_stands, self.corner_stands):
                for stand in stands:
                    if stand.capacity > 0 and stand.roof and not stand.seating:
                        return True

            return False

        def get_seating_uncovered(self):
            '''
            Return whether stadium has any uncovered seating areas.
            '''
            for stands in (self.main_stands, self.corner_stands):
                for stand in stands:
                    if stand.capacity > 0 and not stand.roof and stand.seating:
                        return True

            return False

        def get_seating_covered(self):
            '''
            Return whether stadium has any covered seating areas.
            '''
            for stands in (self.main_stands, self.corner_stands):
                for stand in stands:
                    if stand.capacity > 0 and stand.roof and stand.seating:
                        return True

            return False

        def get_executive_box(self):
            '''
            Return whether the stadium has any executive boxes.
            '''
            for stands in (self.main_stands, self.corner_stands):
                for stand in stands:
                    if stand.box > 0:
                        return True

            return False

        def get_maintenance_cost(self):
            '''
            Calculate cost of maintaining current stadium and buildings.
            '''
            cost = (self.maintenance * 0.01) * self.get_capacity() * 0.5

            for building in self.buildings.get_buildings():
                cost += (building.cost * 0.05) * building.number

            return cost

        def update_condition(self):
            '''
            Update the current condition of the stadium.
            '''
            data.user.club.stadium.condition = data.user.club.stadium.maintenance + random.randint(-1, 2)

            if data.user.club.stadium.condition > 100:
                data.user.club.stadium.condition = 100
            elif data.user.club.stadium.condition < 0:
                data.user.club.stadium.condition = 0

            if data.user.club.stadium.condition <= 25:
                data.user.club.news.publish("SM01")

                self.warnings += 1
            elif data.user.club.stadium.condition <= 50:
                data.user.club.news.publish("SM02")

                self.warnings += 1

            if data.user.club.stadium.warnings == 3:
                fine = self.get_capacity() * 3 * (self.fines + 1)
                data.user.club.accounts.withdraw(amount=fine, category="fines")

                data.user.club.news.publish("SM03", amount=fine)

                self.fines += 1
                self.warnings = 0

    def __init__(self, season):
        self.season = season
        self.stadiums = {}

        self.populate_data()

    def get_stadiums(self):
        '''
        Return full dictionary of stadiums.
        '''
        return self.stadiums.items()

    def get_stadium_by_id(self, stadiumid):
        '''
        Get stadium object for given stadium id.
        '''
        return self.stadiums[stadiumid]

    def populate_data(self):
        data.database.cursor.execute("SELECT * FROM stadium \
                                     JOIN stadiumattr \
                                     ON stadium.id = stadiumattr.stadium \
                                     WHERE year = ?",
                                     (self.season,))

        for item in data.database.cursor.fetchall():
            stadium = self.Stadium()
            stadium.stadiumid = item[0]
            self.stadiums[stadium.stadiumid] = stadium

            stadium.name = item[1]

            main_capacity = item[5:9]
            corner_capacity = item[9:13]
            box_capacity = item[13:17]
            roof = item[17:25]
            seating = item[25:33]
            shops = item[33:]

            for count in range(0, 4):
                stand = MainStand()
                stand.capacity = main_capacity[count]
                stand.set_roof(roof[count])
                stand.set_seating(seating[count])
                stand.set_box(box_capacity[count])
                stadium.main_stands.append(stand)

            for count in range(0, 4):
                stand = CornerStand()
                stand.capacity = corner_capacity[count]
                stand.set_roof(roof[count + 4])
                stand.set_seating(seating[count + 4])
                stadium.corner_stands.append(stand)

            for count, shop in enumerate(shops):
                building = stadium.buildings.get_building_by_index(count)
                building.number = shop


class MainStand:
    def __init__(self):
        self.capacity = 0
        self.seating = False
        self.roof = False
        self.box = 0

    def set_seating(self, seating):
        '''
        Set seating boolean if set and capacity is greater than zero.
        '''
        if seating and self.capacity > 0:
            self.seating = True

    def set_roof(self, roof):
        '''
        Set roof boolean if set and capacity is greater than zero.
        '''
        if roof and self.capacity > 0:
            self.roof = True

    def set_box(self, box):
        '''
        Set box capacity if roof is set and capacity is greater than 4000.
        '''
        if box > 0 and self.roof and self.capacity > 4000:
            self.box = box


class CornerStand:
    def __init__(self):
        self.capacity = 0
        self.seating = False
        self.roof = False

    def set_seating(self, seating):
        '''
        Set seating boolean if set and capacity is greater than zero.
        '''
        if seating and self.capacity > 0:
            self.seating = True

    def set_roof(self, roof):
        '''
        Set roof boolean if set and capacity is greater than zero.
        '''
        if roof and self.capacity > 0:
            self.roof = True
