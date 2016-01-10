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
