#!/usr/bin/env python3

from gi.repository import Gtk

import data
import uigtk.widgets


class Match(uigtk.widgets.Grid):
    '''
    Interface handling display of match related widgets.
    '''
    def __init__(self):
        uigtk.widgets.Grid.__init__(self)

        buttonbox = uigtk.widgets.ButtonBox()
        buttonbox.set_orientation(Gtk.Orientation.VERTICAL)
        buttonbox.set_layout(Gtk.ButtonBoxStyle.START)
        self.attach(buttonbox, 0, 0, 1, 1)

        self.buttonStart = uigtk.widgets.Button("_Start Match")
        buttonbox.add(self.buttonStart)

        self.buttonHomeTactics = uigtk.widgets.Button()
        buttonbox.add(self.buttonHomeTactics)
        self.buttonAwayTactics = uigtk.widgets.Button()
        buttonbox.add(self.buttonAwayTactics)

        grid = Gtk.Grid()
        grid.set_hexpand(True)
        grid.set_column_homogeneous(True)
        self.attach(grid, 1, 0, 1, 1)

        self.score = Score()
        grid.attach(self.score, 0, 0, 1, 1)

        self.information = Information()
        self.score.attach(self.information, 0, 1, 1, 1)

    def update_match_details(self, fixtureid=0):
        '''
        Set match details for given fixture.
        '''
        teams = ("Real Madrid", "Barcelona")

        self.score.set_teams(teams)

        self.set_tactics_buttons(teams)

    def set_tactics_buttons(self, teams):
        '''
        Update label on tactics buttons to display club names.
        '''
        self.buttonHomeTactics.set_label("_%s\nTactics" % (teams[0]))
        self.buttonAwayTactics.set_label("_%s\nTactics" % (teams[1]))

    def run(self):
        self.show_all()


class Score(Gtk.Grid):
    '''
    Class to display and update both teams and scores.
    '''
    def __init__(self):
        Gtk.Grid.__init__(self)
        self.set_hexpand(True)
        self.set_column_homogeneous(True)

        self.labelHomeTeam = uigtk.widgets.Label()
        self.labelHomeTeam.set_hexpand(True)
        self.attach(self.labelHomeTeam, 0, 0, 1, 1)

        self.labelScore = uigtk.widgets.Label()
        self.labelScore.set_hexpand(True)
        self.attach(self.labelScore, 1, 0, 1, 1)

        self.labelAwayTeam = uigtk.widgets.Label()
        self.labelAwayTeam.set_hexpand(True)
        self.attach(self.labelAwayTeam, 2, 0, 1, 1)

    def set_teams(self, teams):
        '''
        Set competing team names and 0-0 scoreline.
        '''
        self.labelHomeTeam.set_markup("<span size='24000'><b>%s</b></span>" % (teams[0]))
        self.labelAwayTeam.set_markup("<span size='24000'><b>%s</b></span>" % (teams[1]))
        self.set_score((0, 0))

    def set_score(self, score):
        '''
        Set current score on label.
        '''
        self.labelScore.set_markup("<span size='24000'><b>%i - %i</b></span>" % (score))


class Information(Gtk.Grid):
    '''
    Information display of match venue and chosen referee.
    '''
    def __init__(self):
        Gtk.Grid.__init__(self)
        self.set_hexpand(True)
        self.set_row_spacing(5)

        label = uigtk.widgets.Label("Stadium", leftalign=True)
        self.attach(label, 0, 0, 1, 1)

        self.labelStadium = uigtk.widgets.Label(leftalign=True)
        self.labelStadium.set_hexpand(True)
        self.attach(self.labelStadium, 1, 0, 1, 1)

        label = uigtk.widgets.Label("Referee", leftalign=True)
        self.attach(label, 0, 1, 1, 1)

        self.labelReferee = uigtk.widgets.Label(leftalign=True)
        self.labelReferee.set_hexpand(True)
        self.attach(self.labelReferee, 1, 1, 1, 1)

    def set_information(self, stadium, referee):
        '''
        Update stadium and referee information.
        '''
        self.labelStadium.set_label(stadium)
        self.labelReferee.set_label(referee)


class ProceedToMatch(Gtk.MessageDialog):
    '''
    Message dialog asking to confirm continuance to next match.
    '''
    def __init__(self, opposition):
        Gtk.MessageDialog.__init__(self)
        self.set_transient_for(data.window)
        self.set_title("Proceed To Match")
        self.set_markup("Proceed to match against %s?" % (opposition))
        self.set_property("message-type", Gtk.MessageType.QUESTION)
        self.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("_Proceed", Gtk.ResponseType.OK)
        self.set_default_response(Gtk.ResponseType.OK)

    def show(self):
        state = self.run() == Gtk.ResponseType.OK
        self.destroy()

        return state


class NotEnoughPlayers(Gtk.MessageDialog):
    '''
    Error dialog displayed when there aren't enough selected players.
    '''
    def __init__(self, count):
        Gtk.MessageDialog.__init__(self)
        self.set_transient_for(data.window)
        self.set_title("Not Enough Players")

        if count == 0:
            message = "No players have been selected for this match."
        else:
            message = "You have selected only %i of the required 11 players." % (count)

        self.set_markup(message)
        self.set_property("message-type", Gtk.MessageType.ERROR)
        self.add_button("_Close", Gtk.ResponseType.CANCEL)
        self.set_default_response(Gtk.ResponseType.CANCEL)
        self.connect("response", self.on_response)

        self.run()

    def on_response(self, *args):
        self.destroy()


class NotEnoughSubs(Gtk.MessageDialog):
    '''
    Confirmation dialog on whether to proceed with less than five substitutes.
    '''
    def __init__(self, count):
        Gtk.MessageDialog.__init__(self)
        self.set_transient_for(data.window)
        self.set_title("Not Enough Substitutes")

        if count == 0:
            message = "No substitutes have been selected for this match."
        else:
            message = "You have selected only %i of 5 substitutes." % (count)

        self.set_markup("<span size='12000'><b>%s</b></span>" % (message))
        self.format_secondary_text("Do you wish to proceed to the game anyway?")
        self.set_property("message-type", Gtk.MessageType.WARNING)
        self.add_button("_Do Not Proceed", Gtk.ResponseType.CANCEL)
        self.add_button("_Proceed", Gtk.ResponseType.OK)
        self.set_default_response(Gtk.ResponseType.CANCEL)

    def show(self):
        state = self.run() == Gtk.ResponseType.OK
        self.destroy()

        return state
