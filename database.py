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

import game
import preferences

try:
    import sqlite3
except ImportError:
    try:
        import apsw
    except ImportError:
        pass


class Database:
    class SQLiteDatabase:
        def __init__(self):
            self.connection = None
            self.cursor = None

        def connect(self, filename=None):
            if not filename:
                preferences.preferences.readfile()
                filepath = os.path.join("databases", game.database_filename)

                if not os.path.isfile(filepath):
                    return False
            else:
                filepath = filename

            self.connection = sqlite3.connect(filepath)
            self.connection.execute("PRAGMA foreign_keys = on")
            self.cursor = self.connection.cursor()

            return True

        def importer(self, table):
            self.cursor.execute("SELECT * FROM %s" % (table))
            data = self.cursor.fetchall()

            return data

    class APSWDatabase:
        def __init__(self):
            self.connection = None
            self.cursor = None

        def connect(self, filename=None):
            if not filename:
                preferences.preferences.readfile()
                filepath = os.path.join("databases", game.database_filename)

                if not os.path.isfile(filepath):
                    return False
            else:
                filepath = filename

            self.connection = apsw.Connection(filepath)
            self.cursor = self.connection.cursor()

            return True

        def importer(self, table):
            self.cursor.execute("SELECT * FROM %s" % (table))
            data = self.cursor.fetchall()

            return data

    def __init__(self):
        self.database = None

        if "sqlite3" in globals():
            self.database = self.SQLiteDatabase()
        else:
            self.database = self.APSWDatabase()

    def get_database_object(self):
        return self.database
