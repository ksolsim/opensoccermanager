#!/usr/bin/env python3

import data


class Suspensions:
    class Suspension:
        def __init__(self):
            self.suspension = None
            self.period = 0

    def __init__(self):
        self.suspensions = {}

        self.messages = SuspensionMessage()

    def get_suspensions(self):
        '''
        Return full dictionary of suspension objects.
        '''
        return self.suspensions


class SuspensionMessage:
    def __init__(self):
        self.messages = {}

        self.populate_data()

    def populate_data(self):
        data.database.cursor.execute("SELECT * FROM suspension")

        for item in data.database.cursor.fetchall():
            self.messages[item[0]] = item[1:4]
