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


from gi.repository import Gtk
import os

from uigtk import accounts
from uigtk import advertising
from uigtk import buildings
from uigtk import catering
from uigtk import charts
from uigtk import details
from uigtk import evaluation
from uigtk import fixtures
from uigtk import individualtraining
from uigtk import injsus
from uigtk import interface
from uigtk import mainmenu
from uigtk import merchandise
from uigtk import negotiations
from uigtk import news
from uigtk import results
from uigtk import screen
from uigtk import search
from uigtk import shortlist
from uigtk import squad
from uigtk import staff
from uigtk import standings
from uigtk import statistics
from uigtk import tactics
from uigtk import teamtraining
from uigtk import tickets
from uigtk import trainingcamp
from uigtk import venue

import fileio
import finances
import game
import match
import music
import preferences
import version


class Window(Gtk.Window):
    def __init__(self):
        preferences.preferences.readfile()

        iconpath = os.path.join("resources", "logo.svg")

        Gtk.Window.__init__(self)
        self.set_title(version.NAME)
        self.set_icon_from_file(iconpath)
        self.set_default_size(preferences.preferences.width,
                              preferences.preferences.height)

        if preferences.preferences.maximized:
            self.maximize()
        else:
            self.move(preferences.preferences.xposition,
                      preferences.preferences.yposition)

        self.connect("window-state-event", self.window_state_event)
        self.connect("delete-event", self.exit_game)

        game.accelgroup = Gtk.AccelGroup()
        self.add_accel_group(game.accelgroup)

    def window_state_event(self, widget, event):
        if self.is_maximized():
            self.move(preferences.preferences.xposition,
                      preferences.preferences.yposition)

    def screen_loader(self, index):
        screens = {1: self.screenSquad,
                   2: self.screenFixtures,
                   3: self.screenNews,
                   4: self.screenTactics,
                   5: self.screenStandings,
                   6: self.screenResults,
                   7: self.screenTeamTraining,
                   8: self.screenTrainingCamp,
                   9: self.screenIndividualTraining,
                   10: self.screenStadium,
                   11: self.screenFinances,
                   12: self.screenAccounts,
                   14: self.screenBuildings,
                   16: self.screenAdvertising,
                   17: self.screenMerchandise,
                   18: self.screenCatering,
                   19: self.screenTickets,
                   20: self.screenSearch,
                   21: self.screenNegotiations,
                   22: self.screenShortlist,
                   23: self.screenStaff,
                   24: self.screenInjSus,
                   25: self.screenEvaluation,
                   29: self.screenStatistics,
                   30: self.screenCharts,
                   99: self.screenMatch,
                  }

        if game.active_screen:
            game.window.screenGame.remove(game.active_screen)

        game.active_screen = screens[index]
        game.active_screen_id = index
        game.window.screenGame.attach(game.active_screen, 0, 1, 1, 1)

        game.active_screen.set_border_width(5)
        game.active_screen.set_hexpand(True)
        game.active_screen.set_vexpand(True)

        game.active_screen.run()

    def exit_game(self, widget=None, event=None):
        def update_window_config():
            '''
            Save the window size and state to preferences when quitting.
            '''
            if game.window.is_maximized():
                preferences.preferences["INTERFACE"]["Maximized"] = "True"
            else:
                preferences.preferences["INTERFACE"]["Maximized"] = "False"

                width, height = game.window.get_size()
                preferences.preferences["INTERFACE"]["Width"] = str(width)
                preferences.preferences["INTERFACE"]["Height"] = str(height)

                xposition, yposition = game.window.get_position()
                preferences.preferences["INTERFACE"]["XPosition"] = str(xposition)
                preferences.preferences["INTERFACE"]["YPosition"] = str(yposition)

            preferences.preferences.writefile()

        if game.teamid is None:
            update_window_config()
            Gtk.main_quit()
        else:
            exit_dialog = interface.ExitDialog()
            state = exit_dialog.display()

            if not state:
                update_window_config()
                Gtk.main_quit()

            return state

    def run(self):
        self.screenMain = mainmenu.MainMenu()
        self.screenDetails = details.Details()
        self.screenGame = screen.ScreenGame()

        self.screenSquad = squad.Squad()
        self.screenNews = news.News()
        self.screenEvaluation = evaluation.Evaluation()
        self.screenCharts = charts.Charts()
        self.screenStatistics = statistics.Statistics()
        self.screenFixtures = fixtures.Fixtures()
        self.screenResults = results.Results()
        self.screenStandings = standings.Standings()
        self.screenNegotiations = negotiations.Negotiations()
        self.screenShortlist = shortlist.Shortlist()
        self.screenInjSus = injsus.InjSus()
        self.screenTeamTraining = teamtraining.TeamTraining()
        self.screenIndividualTraining = individualtraining.IndividualTraining()
        self.screenTrainingCamp = trainingcamp.TrainingCamp()
        self.screenTickets = tickets.Tickets()
        self.screenStaff = staff.Staff()
        self.screenTactics = tactics.Tactics()
        self.screenAccounts = accounts.Accounts()
        self.screenMatch = match.Match()
        self.screenAdvertising = advertising.Advertising()
        self.screenMerchandise = merchandise.Merchandise()
        self.screenCatering = catering.Catering()
        self.screenBuildings = buildings.Buildings()
        self.screenSearch = search.Search()
        self.screenFinances = finances.Finances()
        self.screenStadium = venue.Stadium()

        self.add(self.screenMain)

        fileio.check_config()

        self.show_all()

        if music.music.playing:
            music.music.play()
