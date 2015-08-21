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


import game
import structures


stadiums = {}


class Stadium:
    def __init__(self):
        self.name = ""

        self.main = []
        self.corner = []

        self.condition = 100
        self.fines = 0
        self.warnings = 0

        self.buildings = []
        self.plots = 0

    def get_capacity(self):
        '''
        Return the stadium capacity.
        '''
        capacity = 0

        for stand in self.main:
            capacity += stand.capacity
            capacity += stand.box

        for stand in self.corner:
            capacity += stand.capacity

        return capacity

    def get_maintenance(self):
        '''
        Calculate cost of maintaining stadium.
        '''
        # Stadium maintenance cost
        cost = (stadium.maintenance * 0.01) * stadium.capacity * 0.5

        # Building maintenance cost
        for count, item in enumerate(constants.buildings):
            cost += (item[2] * 0.05) * stadium.buildings[count]

        return cost

    def pay_maintenance(self):
        '''
        Calculate cost for maintenance.
        '''
        cost = self.get_maintenance()

        self.accounts.withdraw(amount=cost, category="stadium")

class MainStand:
    def __init__(self):
        self.capacity = 0
        self.box = 0
        self.seating = False
        self.roof = False

    def get_box_permitted(self):
        '''
        Return True if box is allowed to be built.
        '''
        permitted = self.capacity >= 5000 and self.roof

        return permitted

class CornerStand:
    def __init__(self):
        self.capacity = 0
        self.seating = False
        self.roof = False

    def get_build_permitted(self):
        '''
        Return wheter the corner stand can be built.
        '''


def populate_data():
    '''
    Populate stadium data.
    '''
    game.database.cursor.execute("SELECT * FROM stadium, stadiumattr ON stadium.id = stadiumattr.stadium WHERE year = ?", (game.date.year,))
    data = game.database.cursor.fetchall()

    adjacent = (0, 1), (2, 0), (3, 2), (1, 3), # DO NOT REORDER/CHANGE!

    for item in data:
        stadium = Stadium()
        stadiumid = item[0]
        stadiums[stadiumid] = stadium

        stadium.name = item[1]

        for count, value in enumerate(item[5:9]):
            stand = MainStand()
            stand.capacity = value

            stand.box = item[13 + count]

            stadium.main.append(stand)

        for count, value in enumerate(item[9:13]):
            stand = CornerStand()
            stand.capacity = value
            stadium.corner.append(stand)

    '''
    stadium = self.Stadium()
    stadiumid = item[0]
    self.stadiums[stadiumid] = stadium

    stadium.name = item[1]
    stadium.condition = 100
    stadium.plots = 0
    stadium.capacity = sum(item[13:25])
    stadium.main = []
    stadium.corner = []

    for count, value in enumerate(item[13:25]):
        stand = structures.Stand()
        stand.capacity = value

        if stand.capacity > 0:
            stand.seating = bool(item[count + 17])
            stand.roof = bool(item[count + 25])

            if stand.capacity >= 5000 and stand.roof:
                stand.box = item[count + 13]
            else:
                stand.box = 0
        else:
            stand.seating = False
            stand.roof = False
            stand.box = 0

        stand.adjacent = adjacent[count]

        stadium.main.append(stand)

    for count, value in enumerate(item[9:13]):
        stand = structures.Stand()
        stand.capacity = value

        if stand.capacity > 0:
            stand.seating = bool(item[count + 21])
            stand.roof = bool(item[count + 29])
            stand.available = [False, False]
        else:
            stand.seating = False
            stand.roof = False
            stand.available = [False, False]

        stadium.corner.append(stand)

    stadium.buildings = list(item[33:41])
    '''

def perform_maintenance():
    for stadium in self.stadiums.values():
        stadium.pay_maintenance()
