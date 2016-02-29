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


class Buildings:
    class Building:
        def __init__(self):
            self.name = ""
            self.size = 0
            self.number = 0
            self.cost = 0
            self.filename = ""

    def __init__(self):
        self.buildings = []
        self.filenames = ("programmevendor",
                          "stall",
                          "burgerbar",
                          "bar",
                          "smallshop",
                          "largeshop",
                          "cafe",
                          "restaurant")

        self.populate_data()

    def get_buildings(self):
        '''
        Return list of building names and attribute information.
        '''
        return self.buildings

    def get_building_by_index(self, index):
        '''
        Return building object for given index value.
        '''
        return self.buildings[index]

    def get_used_plots(self):
        '''
        Return number of plots currently in use.
        '''
        return sum(shop.size * shop.number for shop in self.buildings)

    def populate_data(self):
        data.database.cursor.execute("SELECT * FROM buildings")

        for count, shop in enumerate(data.database.cursor.fetchall()):
            building = self.Building()
            building.name = shop[0]
            building.size = shop[1]
            building.cost = shop[2]
            building.filename = self.filenames[count]
            self.buildings.append(building)
