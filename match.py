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
import random

import ai
import constants
import events
import game
import money
import news
import sales
import structures
import widgets


class Match(Gtk.Grid):
    class Score(Gtk.Grid):
        def __init__(self):
            Gtk.Grid.__init__(self)
            self.set_hexpand(True)
            self.set_column_homogeneous(True)

            self.labelTeam1 = widgets.Label()
            self.labelTeam1.set_hexpand(True)
            self.attach(self.labelTeam1, 0, 0, 1, 1)
            self.labelScore = widgets.Label()
            self.labelScore.set_hexpand(True)
            self.attach(self.labelScore, 1, 0, 1, 1)
            self.labelTeam2 = widgets.Label()
            self.labelTeam2.set_hexpand(True)
            self.attach(self.labelTeam2, 2, 0, 1, 1)

        def update_teams(self, *teams):
            self.labelTeam1.set_markup("<span size='16000'><b>%s</b></span>" % (teams[0]))
            self.labelTeam2.set_markup("<span size='16000'><b>%s</b></span>" % (teams[1]))
            self.labelScore.set_markup("<span size='16000'><b>0 - 0</b></span>")

        def update_score(self, score):
            score = "%i - %i" % (score[0], score[1])
            self.labelScore.set_markup("<span size='16000'><b>%s</b></span>" % (score))

    class Events(Gtk.ScrolledWindow):
        def __init__(self):
            Gtk.ScrolledWindow.__init__(self)
            self.set_hexpand(True)

            self.viewport = Gtk.Viewport()
            self.add(self.viewport)

            self.grid = None

            self.show_all()

        def update(self, scorers):
            self.grid = Gtk.Grid()
            self.viewport.add(self.grid)

            for count, playerid in enumerate(scorers):
                player = game.players[playerid]
                name = player.get_name(mode=1)

                label = widgets.AlignedLabel("%s" % (name))
                self.grid.attach(label, 0, count, 1, 1)

            self.show_all()

        def clear(self):
            if self.grid:
                self.grid.destroy()

    class Teams(Gtk.Grid):
        def __init__(self):
            Gtk.Grid.__init__(self)
            self.set_row_spacing(5)
            self.set_column_spacing(5)
            self.set_border_width(5)
            self.set_column_homogeneous(True)

            scrolledwindow = Gtk.ScrolledWindow()
            self.attach(scrolledwindow, 0, 0, 1, 1)

            self.treeviewHome = Gtk.TreeView()
            self.treeviewHome.set_vexpand(True)
            self.treeviewHome.set_hexpand(True)
            self.treeviewHome.set_enable_search(False)
            self.treeviewHome.set_search_column(-1)
            scrolledwindow.add(self.treeviewHome)
            treeselection = self.treeviewHome.get_selection()
            treeselection.set_mode(Gtk.SelectionMode.NONE)

            treeviewcolumn = widgets.TreeViewColumn(title="Position", column=0)
            self.treeviewHome.append_column(treeviewcolumn)
            treeviewcolumn = widgets.TreeViewColumn(title="Player", column=1)
            self.treeviewHome.append_column(treeviewcolumn)

            scrolledwindow = Gtk.ScrolledWindow()
            self.attach(scrolledwindow, 1, 0, 1, 1)

            self.treeviewAway = Gtk.TreeView()
            self.treeviewAway.set_vexpand(True)
            self.treeviewAway.set_hexpand(True)
            self.treeviewAway.set_enable_search(False)
            self.treeviewAway.set_search_column(-1)
            scrolledwindow.add(self.treeviewAway)
            treeselection = self.treeviewAway.get_selection()
            treeselection.set_mode(Gtk.SelectionMode.NONE)

            treeviewcolumn = widgets.TreeViewColumn(title="Position", column=0)
            self.treeviewAway.append_column(treeviewcolumn)
            treeviewcolumn = widgets.TreeViewColumn(title="Player", column=1)
            self.treeviewAway.append_column(treeviewcolumn)

            self.show_all()

    class Information(Gtk.Grid):
        def __init__(self):
            Gtk.Grid.__init__(self)
            self.set_hexpand(True)
            self.set_row_spacing(5)

            self.labelVenue = Gtk.Label()
            self.labelVenue.set_hexpand(True)
            self.attach(self.labelVenue, 0, 0, 1, 1)

            self.labelReferee = Gtk.Label()
            self.labelReferee.set_hexpand(True)
            self.attach(self.labelReferee, 0, 1, 1, 1)

        def set_referee(self, referee):
            '''
            Display the selected referee on the match screen.
            '''
            self.labelReferee.set_label("Referee: %s" % (referee))

        def set_venue(self, venue):
            '''
            Display the venue on the match screen.
            '''
            self.labelVenue.set_label("Venue: %s" % (venue))

    class Statistics(Gtk.Grid):
        def __init__(self):
            Gtk.Grid.__init__(self)
            self.set_hexpand(True)
            self.set_border_width(5)
            self.set_row_spacing(5)
            self.set_column_spacing(5)

            label = widgets.AlignedLabel("Attendance")
            self.attach(label, 0, 0, 1, 1)
            self.labelAttendance = widgets.AlignedLabel()
            self.attach(self.labelAttendance, 1, 0, 1, 1)

            label = widgets.AlignedLabel("Shots On Target")
            self.attach(label, 0, 1, 1, 1)
            self.labelShotsOn1 = widgets.AlignedLabel()
            self.attach(self.labelShotsOn1, 1, 1, 1, 1)
            self.labelShotsOn2 = widgets.AlignedLabel()
            self.attach(self.labelShotsOn2, 2, 1, 1, 1)

            label = widgets.AlignedLabel("Shots Off Target")
            self.attach(label, 0, 2, 1, 1)
            self.labelShotsOff1 = widgets.AlignedLabel()
            self.attach(self.labelShotsOff1, 1, 2, 1, 1)
            self.labelShotsOff2 = widgets.AlignedLabel()
            self.attach(self.labelShotsOff2, 2, 2, 1, 1)

            label = widgets.AlignedLabel("Free Kicks")
            self.attach(label, 0, 3, 1, 1)
            self.labelFreeKicks1 = widgets.AlignedLabel()
            self.attach(self.labelFreeKicks1, 1, 3, 1, 1)
            self.labelFreeKicks2 = widgets.AlignedLabel()
            self.attach(self.labelFreeKicks2, 2, 3, 1, 1)

            label = widgets.AlignedLabel("Corner Kicks")
            self.attach(label, 0, 4, 1, 1)
            self.labelCornerKicks1 = widgets.AlignedLabel()
            self.attach(self.labelCornerKicks1, 1, 4, 1, 1)
            self.labelCornerKicks2 = widgets.AlignedLabel()
            self.attach(self.labelCornerKicks2, 2, 4, 1, 1)

            label = widgets.AlignedLabel("Throw-Ins")
            self.attach(label, 0, 5, 1, 1)
            self.labelThrowIns1 = widgets.AlignedLabel()
            self.attach(self.labelThrowIns1, 1, 5, 1, 1)
            self.labelThrowIns2 = widgets.AlignedLabel()
            self.attach(self.labelThrowIns2, 2, 5, 1, 1)

            label = widgets.AlignedLabel("Fouls")
            self.attach(label, 0, 6, 1, 1)
            self.labelFouls1 = widgets.AlignedLabel()
            self.attach(self.labelFouls1, 1, 6, 1, 1)
            self.labelFouls2 = widgets.AlignedLabel()
            self.attach(self.labelFouls2, 2, 6, 1, 1)

            label = widgets.AlignedLabel("Yellow Cards")
            self.attach(label, 0, 7, 1, 1)
            self.labelYellowCards1 = widgets.AlignedLabel()
            self.attach(self.labelYellowCards1, 1, 7, 1, 1)
            self.labelYellowCards2 = widgets.AlignedLabel()
            self.attach(self.labelYellowCards2, 2, 7, 1, 1)

            label = widgets.AlignedLabel("Red Cards")
            self.attach(label, 0, 8, 1, 1)
            self.labelRedCards1 = widgets.AlignedLabel()
            self.attach(self.labelRedCards1, 1, 8, 1, 1)
            self.labelRedCards2 = widgets.AlignedLabel()
            self.attach(self.labelRedCards2, 2, 8, 1, 1)

            label = widgets.AlignedLabel("Possession")
            self.attach(label, 0, 9, 1, 1)
            self.labelPossession1 = widgets.AlignedLabel()
            self.attach(self.labelPossession1, 1, 9, 1, 1)
            self.labelPossession2 = widgets.AlignedLabel()
            self.attach(self.labelPossession2, 2, 9, 1, 1)

    def __init__(self):
        Gtk.Grid.__init__(self)
        self.set_row_spacing(5)
        self.set_column_spacing(5)
        self.set_border_width(5)
        self.set_vexpand(True)
        self.set_hexpand(True)

        buttonbox = Gtk.ButtonBox()
        buttonbox.set_orientation(Gtk.Orientation.VERTICAL)
        buttonbox.set_layout(Gtk.ButtonBoxStyle.START)
        self.attach(buttonbox, 0, 0, 1, 1)
        self.buttonStart = widgets.Button("_Start Match")
        self.buttonStart.connect("clicked", self.start_button_clicked)
        buttonbox.add(self.buttonStart)

        grid = Gtk.Grid()
        grid.set_hexpand(True)
        grid.set_column_homogeneous(True)
        self.attach(grid, 1, 0, 1, 1)

        # Score
        self.score = self.Score()
        grid.attach(self.score, 0, 0, 3, 1)

        # Events
        self.team1events = self.Events()
        grid.attach(self.team1events, 0, 1, 1, 3)

        self.team2events = self.Events()
        grid.attach(self.team2events, 2, 1, 1, 3)

        # Information
        self.information = self.Information()
        grid.attach(self.information, 1, 1, 1, 3)

        # Notebook
        self.notebook = Gtk.Notebook()
        self.notebook.set_hexpand(True)
        self.notebook.set_vexpand(True)
        self.attach(self.notebook, 1, 1, 1, 1)

        self.teams = self.Teams()
        label = widgets.Label("_Teams")
        self.notebook.append_page(self.teams, label)

        self.liststoreHome = Gtk.ListStore(str, str)
        self.teams.treeviewHome.set_model(self.liststoreHome)

        self.liststoreAway = Gtk.ListStore(str, str)
        self.teams.treeviewAway.set_model(self.liststoreAway)

        self.stats = self.Statistics()
        label = widgets.Label("_Statistics")
        self.notebook.append_page(self.stats, label)

    def run(self):
        self.buttonStart.set_sensitive(True)
        self.notebook.set_show_tabs(False)
        self.notebook.set_show_border(False)
        self.notebook.set_current_page(0)

        leagueid = game.clubs[game.teamid].league
        fixtures = game.leagues[leagueid].fixtures

        for count, fixture in enumerate(fixtures.fixtures[game.fixturesindex]):
            if game.teamid in fixture:
                match = fixture

        self.team1 = structures.Team()
        self.team1.teamid = match[0]
        self.team1.name = game.clubs[self.team1.teamid].name
        self.team2 = structures.Team()
        self.team2.teamid = match[1]
        self.team2.name = game.clubs[self.team2.teamid].name

        if self.team1.teamid != game.teamid:
            ai.generate_team(self.team1.teamid)
        else:
            ai.generate_team(self.team2.teamid)

        # Populate team lists
        self.liststoreHome.clear()
        self.liststoreAway.clear()

        model = 0

        for team in (self.team1.teamid, self.team2.teamid):
            count = 0

            for key, playerid in game.clubs[team].team.items():
                if playerid:
                    player = game.players[playerid]
                    name = player.get_name(mode=1)

                    if count < 11:
                        # First Team
                        formationid = game.clubs[team].tactics[0]
                        position = constants.formations[formationid][1][count]
                    elif count >= 11:
                        # Substitutes
                        position = "Sub %i" % (count - 10)

                    (self.liststoreHome, self.liststoreAway)[model].append([position, name])

                    count += 1

            model = 1

        self.score.update_teams(self.team1.name, self.team2.name)

        # Determine venue and referee
        club = game.clubs[self.team1.teamid]
        venue = game.stadiums[club.stadium].name
        self.information.set_venue(venue)

        self.referees = list(game.leagues[leagueid].referees.values())
        random.shuffle(self.referees)
        self.referee = self.referees[0]
        self.information.set_referee(self.referee.name)

        game.menu.set_sensitive(False)
        widgets.continuegame.set_sensitive(False)
        widgets.news.set_sensitive(False)

        # Remove previous events grid and labels
        self.team1events.clear()
        self.team2events.clear()

        # Append empty list to all leagues and payout television money
        for league in game.leagues.values():
            league.results.append([])

            televised = league.televised[game.fixturesindex]
            clubid = league.fixtures.fixtures[game.fixturesindex][televised][0]

            if clubid == game.teamid:
                amount = game.clubs[game.teamid].reputation * 3 * random.randint(950, 1050)
                game.clubs[game.teamid].accounts.deposit(amount=amount,
                                                         category="television")

        self.show_all()

    def start_button_clicked(self, button):
        # Generate player match result and display
        airesult = ai.Result(self.team1.teamid, self.team2.teamid)

        self.score.update_score(airesult.final_score)

        result = (self.team1.teamid,
                  airesult.final_score[0],
                  airesult.final_score[1],
                  self.team2.teamid)

        # Standings
        leagueid = game.clubs[game.teamid].league
        self.leagueid = leagueid
        standings = game.leagues[leagueid].standings

        standings.update_item(result)

        game.leagues[leagueid].add_result(result)

        self.referee.increment_appearance(airesult.yellows, airesult.reds)

        # Man of the match selection
        game.players[airesult.man_of_the_match_id].man_of_the_match += 1

        # Team Events
        self.team1events.update(airesult.scorers[0])
        self.team2events.update(airesult.scorers[1])

        # Update player morale
        if result[1] > result[2]:
            events.update_morale(result[0], 5)
            events.update_morale(result[3], -5)
        elif result[1] < result[2]:
            events.update_morale(result[3], 5)
            events.update_morale(result[0], -5)
        else:
            events.update_morale(result[0], 1)
            events.update_morale(result[3], 1)

        # Communication from chairman about result
        if result[0] == game.teamid:
            if result[1] - result[2] > 3:
                club = game.clubs[result[3]].name
                score = "%i - %i" % (result[1], result[2])
                game.news.publish("RE01", result=score, team=club)
            elif result[1] - result[2] < -3:
                club = game.clubs[result[3]].name
                score = "%i - %i" % (result[1], result[2])
                game.news.publish("RE02", result=score, team=club)
        elif result[3] == game.teamid:
            if result[2] - result[1] > 3:
                club = game.clubs[result[0]].name
                score = "%i - %i" % (result[1], result[2])
                game.news.publish("RE01", result=score, team=club)
            elif result[2] - result[1] < -3:
                club = game.clubs[result[0]].name
                score = "%i - %i" % (result[1], result[2])
                game.news.publish("RE02", result=score, team=club)

        # Pay player win bonus
        if result[0] == game.teamid:
            if result[1] > result[2]:
                money.pay_bonus()
                money.pay_win_bonus()
        elif result[3] == game.teamid:
            if result[2] > result[1]:
                money.pay_bonus()
                money.pay_win_bonus()

        # Declare attendance
        attendance = airesult.attendance(self.team1, self.team2)
        self.stats.labelAttendance.set_label("%s" % (attendance))

        if self.team1.teamid == game.teamid:
            game.clubs[game.teamid].attendances.append(attendance)

        events.increment_goalscorers(airesult.scorers[0], airesult.scorers[1])
        events.increment_assists(airesult.assists[0], airesult.assists[1])

        # Decrement matches player is suspended for
        for player in game.players.values():
            if player.suspension_period > 0:
                player.suspension_period -= 1

                if player.suspension_period == 0:
                    player.suspension_type = 0

        # Matchday ticket sales
        if self.team1.teamid == game.teamid:
            sales.matchday_tickets(attendance)
            sales.merchandise(attendance)
            sales.catering(attendance)

        # Process remaining matches
        self.process_remaining_league()
        self.process_remaining()

        events.update_statistics(airesult)

        widgets.continuegame.set_sensitive(True)
        self.buttonStart.set_sensitive(False)
        self.notebook.set_show_tabs(True)
        self.notebook.set_show_border(True)
        self.notebook.set_current_page(1)

        game.fixturesindex += 1

    def process_remaining_league(self):
        for count, fixture in enumerate(game.leagues[self.leagueid].fixtures.fixtures[game.fixturesindex], start=1):
            team1 = structures.Team()
            team2 = structures.Team()

            team1.teamid = fixture[0]
            team2.teamid = fixture[1]

            club1 = game.clubs[team1.teamid]
            club2 = game.clubs[team2.teamid]

            league = game.leagues[self.leagueid]

            if game.teamid not in fixture:
                ai.generate_team(team1.teamid)
                ai.generate_team(team2.teamid)

                airesult = ai.Result(team1.teamid, team2.teamid)

                score = (team1.teamid,
                         airesult.final_score[0],
                         airesult.final_score[1],
                         team2.teamid)

                game.leagues[self.leagueid].standings.update_item(score)

                league.add_result(score)

                # Events
                self.referee = self.referees[count]
                self.referee.increment_appearance(airesult.yellows, airesult.reds)

                events.increment_goalscorers(airesult.scorers[0], airesult.scorers[1])
                events.increment_assists(airesult.assists[0], airesult.assists[1])

    def process_remaining(self):
        '''
        Produce results for all remaining fixtures.
        '''
        for leagueid, league in game.leagues.items():
            if leagueid != self.leagueid:
                self.referees = list(game.leagues[leagueid].referees.values())
                random.shuffle(self.referees)

                for count, fixture in enumerate(league.fixtures.fixtures[game.fixturesindex], start=0):
                    team1 = structures.Team()
                    team2 = structures.Team()

                    team1.teamid = fixture[0]
                    team2.teamid = fixture[1]

                    club1 = game.clubs[team1.teamid]
                    club2 = game.clubs[team2.teamid]

                    ai.generate_team(team1.teamid)
                    ai.generate_team(team2.teamid)

                    airesult = ai.Result(team1.teamid, team2.teamid)

                    score = (team1.teamid,
                             airesult.final_score[0],
                             airesult.final_score[1],
                             team2.teamid)

                    game.leagues[leagueid].standings.update_item(score)

                    league.add_result(score)

                    # Events
                    self.referee = self.referees[count]
                    self.referee.increment_appearance(airesult.yellows, airesult.reds)

                    events.increment_goalscorers(airesult.scorers[0], airesult.scorers[1])
                    events.increment_assists(airesult.assists[0], airesult.assists[1])
