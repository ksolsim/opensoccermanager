#!/usr/bin/env python3

import sqlite3
import os

import game


class DB:
    def connect(self, filename=None):
        if not filename:
            game.preferences.readfile()

        filepath = os.path.join("databases", game.database_filename)

        self.connection = sqlite3.connect(filepath)
        self.connection.execute("PRAGMA foreign_keys = on")
        self.cursor = self.connection.cursor()

    def importer(self, table):
        self.cursor.execute("SELECT * FROM %s" % (table))
        data = self.cursor.fetchall()

        return data


class SaveFile:
    def connect(self, filepath):
        self.connection = sqlite3.connect(filepath)
        self.connection.execute("PRAGMA foreign_keys = on")
        self.cursor = self.connection.cursor()

    def load(self, table):
        self.cursor.execute("SELECT * FROM %s" % (table))
        data = self.cursor.fetchall()

        return data
