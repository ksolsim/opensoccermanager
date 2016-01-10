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

import database
import music
import preferences
import structures.currency
import structures.suspensions
import structures.user


# User information class
user = None

# Main window
window = None

# Global objects
music = music.Music()                        # Music player object
preferences = preferences.Preferences()      # Preferences configuration object
database = database.Database()               # Database connection object
names = structures.user.Names()              # Names object
currency = structures.currency.Currency()    # Currency object

# In-game data handling objects
players = None
clubs = None
stadiums = None
leagues = None
referees = None
nations = None
companies = None
buildings = None
merchandise = None
catering = None

# In-game dynamic data handling objects
date = None             # Date object
negotiations = None     # Negotiations handler class
loans = None            # Loans handler class
comparison = None       # Comparison object
calendar = None         # Calendar object
