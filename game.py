#!/usr/bin/env python3

active_screen = None        # Track screen currently in view
database = None
proceed = True
unreadnews = False          # Unread news notification

# Audio
music = False
player = None

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
standings = {}
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
