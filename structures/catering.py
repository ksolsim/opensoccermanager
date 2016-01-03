#!/usr/bin/env python3

import data


class Catering:
    def __init__(self):
        self.catering = []

        self.populate_data()

    def get_catering(self):
        return self.catering

    def populate_data(self):
        data.database.cursor.execute("SELECT * FROM catering")

        for item in data.database.cursor.fetchall():
            self.catering.append(item)
