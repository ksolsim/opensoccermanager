#!/usr/bin/env python3

import data


class Injuries:
    class Injury:
        def __init__(self):
            self.name = ""
            self.period = (0, 0)
            self.impact = (0, 0)

    def __init__(self):
        self.injuries = {}

        self.populate_data()

    def get_injury_by_id(self, injuryid):
        return self.injuries[injuryid]

    def populate_data(self):
        data.database.cursor.execute("SELECT * FROM injury")

        for item in data.database.cursor.fetchall():
            injury = self.Injury()
            injury.name = item[1]
            injury.period = (item[2], item[3])
            injury.impact = (item[4], item[5])
            self.injuries[item[0]] = injury
