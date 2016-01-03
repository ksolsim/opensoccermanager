#!/usr/bin/env python3

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
