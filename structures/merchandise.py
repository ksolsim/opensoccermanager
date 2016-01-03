#!/usr/bin/env python3

import data


class Merchandise:
    def __init__(self):
        self.merchandise = []

        self.populate_data()

    def get_merchandise(self):
        return self.merchandise

    def populate_data(self):
        data.database.cursor.execute("SELECT * FROM merchandise")

        for item in data.database.cursor.fetchall():
            self.merchandise.append(item)
