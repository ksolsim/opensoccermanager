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

import data
import structures.match
import uigtk.widgets


class Match(uigtk.widgets.Grid):
    '''
    Interface handling display of match related widgets.
    '''
    __name__ = "match"

    def __init__(self):
        uigtk.widgets.Grid.__init__(self)

        buttonbox = uigtk.widgets.ButtonBox()
        buttonbox.set_orientation(Gtk.Orientation.VERTICAL)
        buttonbox.set_layout(Gtk.ButtonBoxStyle.START)
        self.attach(buttonbox, 0, 0, 1, 1)

        self.buttonStart = uigtk.widgets.Button("_Start Match")
        self.buttonStart.connect("clicked", self.on_start_match_clicked)
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
        self.score.attach(self.information, 1, 1, 1, 1)

        self.notebook = Gtk.Notebook()
        self.attach(self.notebook, 1, 1, 1, 1)

        self.teams = Teams()
        self.notebook.append_page(self.teams, uigtk.widgets.Label("_Teams"))

        self.statistics = Statistics()
        self.statistics.set_visible(False)
        self.notebook.append_page(self.statistics,
                                  uigtk.widgets.Label("_Statistics"))

    def update_match_details(self, fixture):
        '''
        Set match details for given fixture.
        '''
        self.fixture = fixture

        self.score.set_teams(fixture)
        self.set_tactics_buttons(fixture)

        self.information.set_information(fixture.home.club.stadium.name,
                                         fixture.referee.name)
        self.teams.set_teams_list(fixture.home.club, fixture.away.club)

        team = structures.match.Team(fixture)
        team.set_team_selection()

    def set_tactics_buttons(self, fixture):
        '''
        Update label on tactics buttons to display club names.
        '''
        self.buttonHomeTactics.set_label("_%s\nTactics" % (fixture.home.club.name))
        self.buttonHomeTactics.set_sensitive(True)
        self.buttonAwayTactics.set_label("_%s\nTactics" % (fixture.away.club.name))
        self.buttonAwayTactics.set_sensitive(True)

    def on_start_match_clicked(self, button):
        '''
        Call match engine to generate result, then enable interface elements.
        '''
        # Update user fixture
        structures.match.Score(self.fixture)

        self.score.set_result(self.fixture.result)

        self.score.eventsHomeTeam.update_events(self.fixture.home.goalscorers)
        self.score.eventsAwayTeam.update_events(self.fixture.away.goalscorers)

        attendance = structures.match.Attendance(self.fixture)
        self.statistics.set_attendance(attendance.get_attendance())

        self.fixture.league.standings.update_standing(self.fixture)

        data.events.process_end_of_match_events(self.fixture)

        # Update other fixtures
        for leagueid, league in data.leagues.get_leagues():
            for fixtureid in data.calendar.get_other_fixtures(leagueid):
                fixture = league.fixtures.get_fixture_by_id(fixtureid)

                if data.user.club not in (fixture.home.club, fixture.away.club):
                    fixture.home.club.squad.generate_squad()
                    fixture.away.club.squad.generate_squad()

                    club = fixture.home.club
                    fixture.home.team_selection[0] = club.squad.teamselection.team
                    fixture.home.team_selection[1] = club.squad.teamselection.subs

                    club = fixture.away.club
                    fixture.away.team_selection[0] = club.squad.teamselection.team
                    fixture.away.team_selection[1] = club.squad.teamselection.subs

                    structures.match.Score(fixture)
                    league.standings.update_standing(fixture)

                    data.events.process_end_of_match_events(fixture)

        button.set_sensitive(False)
        self.buttonHomeTactics.set_sensitive(False)
        self.buttonAwayTactics.set_sensitive(False)

        data.window.mainscreen.menu.set_sensitive(True)
        data.window.mainscreen.information.set_continue_game_button()
        data.window.mainscreen.information.buttonContinue.set_sensitive(True)
        data.window.mainscreen.information.buttonNews.set_sensitive(True)

        self.statistics.set_visible(True)
        self.notebook.set_show_tabs(True)
        self.notebook.set_current_page(1)

    def run(self):
        self.show_all()

        data.window.mainscreen.menu.set_sensitive(False)
        data.window.mainscreen.information.buttonContinue.set_sensitive(False)
        data.window.mainscreen.information.buttonNews.set_sensitive(False)
        data.window.mainscreen.information.buttonNextMatch.set_label("")
        data.window.mainscreen.information.buttonNextMatch.set_visible(False)

        self.buttonStart.set_sensitive(True)
        self.notebook.set_current_page(0)
        self.notebook.set_show_tabs(False)
        self.notebook.set_show_border(False)
        self.statistics.set_visible(False)

        self.score.eventsHomeTeam.clear_events()
        self.score.eventsAwayTeam.clear_events()


class Score(Gtk.Grid):
    '''
    Class to display and update both teams and scores.
    '''
    def __init__(self):
        Gtk.Grid.__init__(self)
        self.set_column_spacing(5)
        self.set_hexpand(True)
        self.set_column_homogeneous(True)

        self.labelHomeTeam = uigtk.widgets.Label()
        self.labelHomeTeam.set_hexpand(True)
        self.attach(self.labelHomeTeam, 0, 0, 1, 1)

        self.labelResult = uigtk.widgets.Label()
        self.attach(self.labelResult, 1, 0, 1, 1)

        self.labelAwayTeam = uigtk.widgets.Label()
        self.labelAwayTeam.set_hexpand(True)
        self.attach(self.labelAwayTeam, 2, 0, 1, 1)

        self.eventsHomeTeam = Events()
        self.attach(self.eventsHomeTeam, 0, 1, 1, 1)

        self.eventsAwayTeam = Events()
        self.attach(self.eventsAwayTeam, 2, 1, 1, 1)

    def set_teams(self, fixture):
        '''
        Set competing team names and 0-0 scoreline.
        '''
        self.labelHomeTeam.set_markup("<span size='18000'><b>%s</b></span>" % (fixture.home.club.name))
        self.labelAwayTeam.set_markup("<span size='18000'><b>%s</b></span>" % (fixture.away.club.name))
        self.set_result((0, 0))

    def set_result(self, result):
        '''
        Set current result on label.
        '''
        self.labelResult.set_markup("<span size='18000'><b>%i - %i</b></span>" % (result))


class Information(uigtk.widgets.Grid):
    '''
    Information display of match venue and chosen referee.
    '''
    def __init__(self):
        uigtk.widgets.Grid.__init__(self)

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


class Events(uigtk.widgets.ScrolledWindow):
    def __init__(self):
        uigtk.widgets.ScrolledWindow.__init__(self)
        self.set_hexpand(True)

        self.viewport = Gtk.Viewport()
        self.add(self.viewport)

        self.grid = None

    def update_events(self, goalscorers):
        '''
        Add event to list of in-game events.
        '''
        self.grid = Gtk.Grid()
        self.viewport.add(self.grid)

        if goalscorers:
            for count, player in enumerate(goalscorers):
                label = uigtk.widgets.Label(player.get_name(mode=1), leftalign=True)
                self.grid.attach(label, 0, count, 1, 1)

        self.show_all()

    def clear_events(self):
        '''
        Remove and destroy listed events.
        '''
        if self.grid:
            self.grid.destroy()


class Teams(uigtk.widgets.Grid):
    def __init__(self):
        uigtk.widgets.Grid.__init__(self)
        self.set_border_width(5)
        self.set_column_homogeneous(True)

        self.teams = []

        for count in range(0, 2):
            liststore = Gtk.ListStore(int, str, str)
            self.teams.append(liststore)

            scrolledwindow = uigtk.widgets.ScrolledWindow()
            scrolledwindow = Gtk.ScrolledWindow()
            self.attach(scrolledwindow, count, 0, 1, 1)

            self.treeview = uigtk.widgets.TreeView()
            self.treeview.set_vexpand(True)
            self.treeview.set_hexpand(True)
            self.treeview.set_enable_search(False)
            self.treeview.set_search_column(-1)
            self.treeview.set_model(liststore)
            self.treeview.treeselection.set_mode(Gtk.SelectionMode.NONE)
            scrolledwindow.add(self.treeview)

            treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Position",
                                                          column=1)
            self.treeview.append_column(treeviewcolumn)
            treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Player",
                                                          column=2)
            self.treeview.append_column(treeviewcolumn)

    def set_teams_list(self, home, away):
        '''
        Clear list model and set list of players.
        '''
        for count, team in enumerate((home, away)):
            self.teams[count].clear()

            for number, player in enumerate(team.squad.teamselection.get_team_selection()):
                if player:
                    position = team.tactics.get_formation_positions()[number]

                    self.teams[count].append([player.playerid,
                                              position,
                                              player.get_name()])

            for number, player in enumerate(team.squad.teamselection.get_subs_selection(), start=1):
                if player:
                    self.teams[count].append([player.playerid,
                                              "Sub %i" % (number),
                                              player.get_name()])


class Statistics(uigtk.widgets.Grid):
    def __init__(self):
        uigtk.widgets.Grid.__init__(self)
        self.set_border_width(5)

        label = uigtk.widgets.Label("Attendance", leftalign=True)
        self.attach(label, 0, 0, 1, 1)
        self.labelAttendance = uigtk.widgets.Label(leftalign=True)
        self.attach(self.labelAttendance, 1, 0, 1, 1)

        self.statistics = []

        for count, category in enumerate(("Shots On Target",
                                          "Shots Off Target",
                                          "Free Kicks",
                                          "Penalties",
                                          "Corner Kicks",
                                          "Throw-Ins",
                                          "Fouls",
                                          "Yellow Cards",
                                          "Red Cards",
                                          "Possession"),
                                          start=1):
            label = uigtk.widgets.Label(category, leftalign=True)
            self.attach(label, 0, count, 1, 1)

    def set_attendance(self, attendance):
        '''
        Set attendance value at end of match.
        '''
        self.labelAttendance.set_label("%i" % (attendance))


class ProceedToMatch(Gtk.MessageDialog):
    '''
    Message dialog asking to confirm continuance to next match.
    '''
    def __init__(self, opposition):
        Gtk.MessageDialog.__init__(self)
        self.set_transient_for(data.window)
        self.set_modal(True)
        self.set_title("Proceed To Match")
        self.set_markup("<span size='12000'><b>Proceed to match against %s?</b></span>" % (opposition))
        self.format_secondary_text("Once proceeded to the game screen, the match must be played.")
        self.set_property("message-type", Gtk.MessageType.QUESTION)
        self.add_button("_Do Not Proceed", Gtk.ResponseType.CANCEL)
        self.add_button("_Proceed", Gtk.ResponseType.OK)
        self.set_default_response(Gtk.ResponseType.CANCEL)

    def show(self):
        state = self.run() == Gtk.ResponseType.OK
        self.destroy()

        return state


class NotEnoughPlayers(Gtk.MessageDialog):
    '''
    Error dialog displayed when there aren't enough selected players.
    '''
    def __init__(self, count):
        if count == 0:
            message = "No players have been selected for this match."
        else:
            message = "You have selected only %i of the required 11 players." % (count)

        Gtk.MessageDialog.__init__(self)
        self.set_transient_for(data.window)
        self.set_modal(True)
        self.set_title("Not Enough Players")
        self.set_markup(message)
        self.set_property("message-type", Gtk.MessageType.ERROR)
        self.add_button("_Close", Gtk.ResponseType.CLOSE)
        self.add_button("_Go To Squad", Gtk.ResponseType.OK)
        self.set_default_response(Gtk.ResponseType.OK)
        self.connect("response", self.on_response)

        self.show()

    def on_response(self, dialog, response):
        if response == Gtk.ResponseType.OK:
            data.window.screen.change_visible_screen("squad")

        self.destroy()


class NotEnoughSubs(Gtk.MessageDialog):
    '''
    Confirmation dialog on whether to proceed with less than five substitutes.
    '''
    def __init__(self, count):
        if count == 0:
            message = "No substitutes have been selected for this match."
        else:
            message = "You have selected only %i of 5 substitutes." % (count)

        Gtk.MessageDialog.__init__(self)
        self.set_transient_for(data.window)
        self.set_modal(True)
        self.set_title("Not Enough Substitutes")
        self.set_markup("<span size='12000'><b>%s</b></span>" % (message))
        self.format_secondary_text("Do you wish to proceed to the game anyway?")
        self.set_property("message-type", Gtk.MessageType.WARNING)
        self.add_button("_Do Not Proceed", Gtk.ResponseType.CANCEL)
        self.add_button("_Go To Squad", 1)
        self.add_button("_Proceed", Gtk.ResponseType.OK)
        self.set_default_response(1)

    def show(self):
        state = False

        response = self.run()

        if response == Gtk.ResponseType.OK:
            state = True
        elif response == 1:
            data.window.screen.change_visible_screen("squad")

        self.destroy()

        return state


class UnsetResponsibilities(Gtk.MessageDialog):
    def __init__(self):
        Gtk.MessageDialog.__init__(self)
        self.set_transient_for(data.window)
        self.set_modal(True)
        self.set_title("Unset Responsibilities")
        self.set_markup("<span size='12000'><b>There are responsibilities in the team which have no player assigned.</b></span>")
        self.format_secondary_text("Not setting responsibilities for team members can impact team performance.")
        self.add_button("_Do Not Proceed", Gtk.ResponseType.CANCEL)
        self.add_button("_Go To Tactics", 1)
        self.add_button("_Proceed", Gtk.ResponseType.OK)
        self.set_default_response(1)

    def show(self):
        state = False

        response = self.run()

        if response == Gtk.ResponseType.OK:
            state = True
        elif response == 1:
            data.window.screen.change_visible_screen("tactics")

        self.destroy()

        return state
