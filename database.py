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


import os


class Database:
    def __init__(self):
        try:
            import sqlite3
            self.initialise(sqlite3, "python-sqlite2")
            self.binding.version = sqlite3.version
        except ImportError:
            try:
                import apsw
                self.initialise(apsw, "apsw")
                self.binding.version = apsw.apswversion()
            except ImportError:
                print("Requires python-sqlite2 or apsw for the database.")
                exit()

    def initialise(self, binding, name):
        '''
        Initialise connection and cursor objects.
        '''
        self.binding = binding
        self.binding.name = name

        self.connection = None
        self.cursor = None

    def connect(self, filepath):
        '''
        Connect to supplied filepath.
        '''
        connected = False

        if os.path.exists(filepath):
            self.connection = self.binding.Connection(filepath)
            self.cursor = self.connection.cursor()
            self.cursor.execute("PRAGMA foreign_keys = on")

            connected = True

        return connected

    def close(self):
        '''
        Close database connection.
        '''
        self.connection.close()
