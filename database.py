#!/usr/bin/env python

import sqlite3
import os

class Database:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self, filepath):
        '''
        Connect to supplied filepath.
        '''
        connected = False

        if os.path.exists(filepath):
            self.connection = sqlite3.connect(filepath)
            self.cursor = self.connection.cursor()
            self.cursor.execute("PRAGMA foreign_keys = on")

            connected = True

        return connected

    def close(self):
        '''
        Close database connection.
        '''
        self.connection.close()
