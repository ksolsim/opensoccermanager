#!/usr/bin/env python3

import sqlite3
import os

import game
import preferences


class DB:
    def __init__(self):
        self.prefs = preferences.Preferences()

    def connect(self):
        self.prefs.readfile()

        filepath = os.path.join("databases", game.database_filename)

        self.connection = sqlite3.connect(filepath)
        self.connection.execute("PRAGMA foreign_keys = on")
        self.connection.commit()
        self.cursor = self.connection.cursor()

    def importer(self, table):
        self.cursor.execute("SELECT * FROM %s" % (table))
        data = self.cursor.fetchall()

        return data

    def disconnect(self):
        self.connection.close()
