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


active_screen = None        # Track screen currently in view
database = None
proceed = True
unreadnews = False          # Unread news notification

# Audio
music = None                # Music player object

# Filters
player_filter = (True, 0, (0, 20000000), (16, 50), 0, (0, 99), (0, 99), (0, 99), (0, 99), (0, 99), (0, 99), (0, 99), (0, 99), (0, 99))
squad_filter = (0, False)
comparison = [None, None]

teamid = 0                  # Team that player has selected

date = 1                    # Game day
month = 8                   # Game month
year = 2014                 # Game year
week = 1                    # Week number

fixturespage = 0            # Page showing on fixtures page
fixturesindex = 0           # Index number of which fixture the game is on
eventindex = 0              # Position in relation to events
dateindex = 1               # Position in relation to dates
dateprev = 0

staff_timeout = 1
coachid = 1
scoutid = 1
negotiationid = 1

# Data
clubs = {}
players = {}
nations = {}
stadiums = {}
referees = {}
injuries = {}
suspensions = {}
surnames = []
negotiations = {}
loans = {}
televised = []

# Information
fixtures = []
results = []
record = [[], []]
news = []

# Charts
goalscorers = {}
assists = {}
cleansheets = {}
cards = {}
transfers = []

team_training_alert = 0
team_training_timeout = 12
sponsor_timeout = 0
advertising_alert = 4
advertising_timeout = 0
advertising_assistant = False  # Toggle assistant handling advertising
