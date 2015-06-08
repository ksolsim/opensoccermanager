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


teamid = None               # Team that player has selected
active_screen = None        # Track screen currently in view

fixturespage = 0            # Page showing on fixtures page
fixturesindex = 0           # Index number of which fixture the game is on
eventindex = 0              # Position in relation to events
dateindex = 1               # Position in relation to dates
dateprev = 0

staff_timeout = 1
coachid = 1
scoutid = 1
negotiationid = 1
team_training_alert = 0
team_training_timeout = 12
sponsor_timeout = 0
advertising_alert = 4
advertising_timeout = 0
advertising_assistant = False  # Toggle assistant handling advertising

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

# Charts
goalscorers = {}
assists = {}
cleansheets = {}
cards = {}
transfers = []
