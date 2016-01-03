#!/usr/bin/env python3

import data


class Seasons:
    def __init__(self):
        self.seasons = []

        self.populate_data()

    def get_seasons(self):
        return self.seasons

    def populate_data(self):
        data.database.cursor.execute("SELECT * FROM year")

        self.seasons = [item[0] for item in data.database.cursor.fetchall()]
