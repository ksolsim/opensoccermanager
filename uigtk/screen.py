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
        screens = (uigtk.accounts.Accounts(),
                   uigtk.advertising.Advertising(),
                   uigtk.buildings.Buildings(),
                   uigtk.catering.Catering(),
                   uigtk.charts.Charts(),
                   uigtk.clubinformation.ClubInformation(),
                   uigtk.clubsearch.ClubSearch(),
                   uigtk.evaluation.Evaluation(),
                   uigtk.finances.Finances(),
                   uigtk.fixtures.Fixtures(),
                   uigtk.individualtraining.IndividualTraining(),
                   uigtk.match.Match(),
                   uigtk.merchandise.Merchandise(),
                   uigtk.nationsearch.NationSearch(),
                   uigtk.negotiations.Negotiations(),
                   uigtk.news.News(),
                   uigtk.playerinformation.PlayerInformation(),
                   uigtk.playersearch.PlayerSearch(),
                   uigtk.result.Result(),
                   uigtk.shortlist.Shortlist(),
                   uigtk.staff.Staff(),
                   uigtk.squad.Squad(),
                   uigtk.stadium.Stadium(),
                   uigtk.standings.Standings(),
                   uigtk.tactics.Tactics(),
                   uigtk.teamtraining.TeamTraining(),
                   uigtk.tickets.Tickets(),
                   uigtk.trainingcamp.TrainingCamp(),
                   uigtk.unavailable.Unavailable())

        self.screens = {}

        for screen in screens:
            self.screens[screen.__name__] = screen

    def change_visible_screen(self, name):
        '''
        Change visible screen being displayed to the user.
        '''
        if self.active:
            self.previous = self.active
            self.remove(self.active)

        self.active = self.screens[name]
        self.active.name = name
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

        self.show_all()
