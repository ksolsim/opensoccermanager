#!/usr/bin/env python3

from gi.repository import Gtk

import data
import uigtk.accounts
import uigtk.advertising
import uigtk.buildings
import uigtk.catering
import uigtk.charts
import uigtk.clubinformation
import uigtk.clubsearch
import uigtk.evaluation
import uigtk.finances
import uigtk.fixtures
import uigtk.individualtraining
import uigtk.match
import uigtk.merchandise
import uigtk.nationsearch
import uigtk.negotiations
import uigtk.news
import uigtk.playerinformation
import uigtk.playersearch
import uigtk.result
import uigtk.shortlist
import uigtk.squad
import uigtk.stadium
import uigtk.staff
import uigtk.standings
import uigtk.tactics
import uigtk.teamtraining
import uigtk.tickets
import uigtk.trainingcamp
import uigtk.unavailable


class Screen(Gtk.Grid):
    def __init__(self):
        Gtk.Grid.__init__(self)
        self.set_vexpand(True)
        self.set_hexpand(True)

        self.previous = None
        self.active = None

    def screen_initialiser(self):
        '''
        Screen object loading class.
        '''
        self.accounts = uigtk.accounts.Accounts()
        self.finances = uigtk.finances.Finances()
        self.squad = uigtk.squad.Squad()
        self.tactics = uigtk.tactics.Tactics()
        self.staff = uigtk.staff.Staff()
        self.playersearch = uigtk.playersearch.PlayerSearch()
        self.clubsearch = uigtk.clubsearch.ClubSearch()
        self.nationsearch = uigtk.nationsearch.NationSearch()
        self.playerinformation = uigtk.playerinformation.PlayerInformation()
        self.clubinformation = uigtk.clubinformation.ClubInformation()
        self.news = uigtk.news.News()
        self.shortlist = uigtk.shortlist.Shortlist()
        self.negotiations = uigtk.negotiations.Negotiations()
        self.charts = uigtk.charts.Charts()
        self.evaluation = uigtk.evaluation.Evaluation()
        self.tickets = uigtk.tickets.Tickets()
        self.fixtures = uigtk.fixtures.Fixtures()
        self.result = uigtk.result.Result()
        self.advertising = uigtk.advertising.Advertising()
        self.teamtraining = uigtk.teamtraining.TeamTraining()
        self.individualtraining = uigtk.individualtraining.IndividualTraining()
        self.trainingcamp = uigtk.trainingcamp.TrainingCamp()
        self.merchandise = uigtk.merchandise.Merchandise()
        self.catering = uigtk.catering.Catering()
        self.standings = uigtk.standings.Standings()
        self.stadium = uigtk.stadium.Stadium()
        self.buildings = uigtk.buildings.Buildings()
        self.unavailable = uigtk.unavailable.Unavailable()
        self.match = uigtk.match.Match()

    def change_visible_screen(self, name):
        '''
        Change visible screen being displayed to the user.
        '''
        if self.active:
            self.previous = self.active
            self.remove(self.active)

        self.active = self.screens[name]
        self.add(self.active)
        self.active.run()

    def get_visible_screen(self):
        '''
        Retrieve visible screen object.
        '''
        return self.active

    def return_previous_screen(self):
        '''
        Return to previously visible screen.
        '''
        self.remove(self.active)
        self.active = self.previous
        self.add(self.active)
        self.active.run()

    def refresh_visible_screen(self):
        '''
        Refresh the visible screen currently on display.
        '''
        if self.active:
            self.active.run()

    def run(self):
        self.screen_initialiser()

        self.screens = {"accounts": self.accounts,
                        "finances": self.finances,
                        "squad": self.squad,
                        "tactics": self.tactics,
                        "staff": self.staff,
                        "playersearch": self.playersearch,
                        "clubsearch": self.clubsearch,
                        "nationsearch": self.nationsearch,
                        "playerinformation": self.playerinformation,
                        "clubinformation": self.clubinformation,
                        "news": self.news,
                        "shortlist": self.shortlist,
                        "negotiations": self.negotiations,
                        "fixtures": self.fixtures,
                        "result": self.result,
                        "charts": self.charts,
                        "evaluation": self.evaluation,
                        "tickets": self.tickets,
                        "advertising": self.advertising,
                        "teamtraining": self.teamtraining,
                        "individualtraining": self.individualtraining,
                        "trainingcamp": self.trainingcamp,
                        "merchandise": self.merchandise,
                        "catering": self.catering,
                        "standings": self.standings,
                        "stadium": self.stadium,
                        "buildings": self.buildings,
                        "unavailable": self.unavailable,
                        "match": self.match}

        self.show_all()
