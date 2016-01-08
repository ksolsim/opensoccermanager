#!/usr/bin/env python3

import data

import structures.buildings


class Names:
    def __init__(self):
        self.names = ("North", "East", "South", "West", "North East", "South East", "South West", "North West")

    def get_names(self):
        return self.names


class Stadiums:
    class Stadium:
        def __init__(self):
            self.name = ""

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

            for stand in self.main_stands:
                capacity += stand.box

            return capacity

    def __init__(self, season):
        self.season = season
        self.stadiums = {}

        self.populate_data()

    def get_stadiums(self):
        '''
        Return full dictionary of stadiums.
        '''
        return self.stadiums

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
            stadiumid = item[0]
            self.stadiums[stadiumid] = stadium

            stadium.name = item[1]

            main_capacity = item[5:9]
            corner_capacity = item[9:13]
            box_capacity = item[13:17]
            roof = item[17:25]
            seating = item[25:33]
            building = item[33:]

            for count in range(0, 4):
                stand = MainStand()
                stand.capacity = main_capacity[count]
                stand.box = box_capacity[count]
                stand.roof = roof[count]
                stand.seating = seating[count]
                stadium.main_stands.append(stand)

            for count in range(0, 4):
                stand = CornerStand()
                stand.capacity = corner_capacity[count]
                stand.roof = roof[count + 4]
                stand.seating = seating[count + 4]
                stadium.corner_stands.append(stand)


class MainStand:
    def __init__(self):
        self.capacity = 0
        self.seating = False
        self.roof = False
        self.box = 0


class CornerStand:
    def __init__(self):
        self.capacity = 0
        self.seating = False
        self.roof = False
