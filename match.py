#!/usr/bin/env python3

from gi.repository import Gtk
import random

import actions
import ai
import constants
import display
import events
import game
import league
import money
import news
import sales
import structures
import widgets


class Referee:
    def __init__(self):
        self.referees = []

    def generate(self):
        self.referees = [refereeid for refereeid in game.referees.keys()]
        random.shuffle(self.referees)

    def select(self, count):
        selected = self.referees[count]

        return selected

    def increment(self, refereeid, yellows, reds):
        events.increment_referee(refereeid, yellows, reds)


class Match(Gtk.Grid):
    class Score(Gtk.Grid):
        def __init__(self):
            Gtk.Grid.__init__(self)
            self.set_hexpand(True)

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
                name = display.name(player, mode=1)

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

            cellrenderertext = Gtk.CellRendererText()

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

            treeviewcolumn = Gtk.TreeViewColumn("Position",
                                                cellrenderertext,
                                                text=0)
            self.treeviewHome.append_column(treeviewcolumn)
            treeviewcolumn = Gtk.TreeViewColumn("Player",
                                                cellrenderertext,
                                                text=1)
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

            treeviewcolumn = Gtk.TreeViewColumn("Position",
                                                cellrenderertext,
                                                text=0)
            self.treeviewAway.append_column(treeviewcolumn)
            treeviewcolumn = Gtk.TreeViewColumn("Player",
                                                cellrenderertext,
                                                text=1)
            self.treeviewAway.append_column(treeviewcolumn)

            self.show_all()

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
        gridInfo = Gtk.Grid()
        grid.set_row_spacing(5)
        grid.attach(gridInfo, 1, 1, 1, 2)

        self.labelStadium = Gtk.Label()
        self.labelStadium.set_hexpand(True)
        self.labelStadium.set_alignment(0.5, 0)
        gridInfo.attach(self.labelStadium, 0, 0, 1, 1)
        self.labelReferee = Gtk.Label()
        self.labelReferee.set_hexpand(True)
        self.labelReferee.set_alignment(0.5, 0)
        gridInfo.attach(self.labelReferee, 0, 1, 1, 1)

        # Notebook
        self.notebook = Gtk.Notebook()
        self.notebook.set_hexpand(True)
        self.notebook.set_vexpand(True)
        grid.attach(self.notebook, 0, 4, 4, 1)

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

        self.player_match = 0

    def run(self):
        self.buttonStart.set_sensitive(True)
        self.notebook.set_show_tabs(False)
        self.notebook.set_show_border(False)
        self.notebook.set_current_page(0)

        for count, item in enumerate(game.fixtures[game.fixturesindex]):
            if game.teamid in (item[0], item[1]):
                match = item
                self.player_match = count

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
                if playerid != 0:
                    player = game.players[playerid]
                    name = display.name(player, mode=1)

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

        # Determine referee
        self.referee = Referee()
        self.referee.generate()

        stadiumid = game.clubs[self.team1.teamid].stadium
        venue = game.stadiums[stadiumid].name
        self.labelStadium.set_label("Venue: %s" % (venue))

        self.refereeid = self.referee.select(0)
        referee = game.referees[self.refereeid].name
        self.labelReferee.set_label("Referee: %s" % (referee))

        game.menu.set_sensitive(False)
        widgets.continuegame.set_sensitive(False)
        widgets.news.set_sensitive(False)

        # Remove previous events grid and labels
        self.team1events.clear()
        self.team2events.clear()

        game.results.append([])

        self.show_all()

    def start_button_clicked(self, button):
        # Generate player match result and display
        airesult = ai.Result(self.team1.teamid, self.team2.teamid)

        self.score.update_score(airesult.final_score)

        result = self.team1.teamid, airesult.final_score[0], airesult.final_score[1], self.team2.teamid

        # Standings
        league.update(result)
        game.results[game.fixturesindex].append(result)

        events.increment_referee(self.refereeid, airesult.yellows, airesult.reds)

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
                news.publish("RE01", result=score, team=club)
            elif result[1] - result[2] < -3:
                club = game.clubs[result[3]].name
                score = "%i - %i" % (result[1], result[2])
                news.publish("RE02", result=score, team=club)
        elif result[3] == game.teamid:
            if result[2] - result[1] > 3:
                club = game.clubs[result[0]].name
                score = "%i - %i" % (result[1], result[2])
                news.publish("RE01", result=score, team=club)
            elif result[2] - result[1] < -3:
                club = game.clubs[result[0]].name
                score = "%i - %i" % (result[1], result[2])
                news.publish("RE02", result=score, team=club)

        # Pay player bonus
        if result[0] == game.teamid:
            if result[1] > result[2]:
                money.pay_bonus()
        elif result[3] == game.teamid:
            if result[2] > result[1]:
                money.pay_bonus()

        # Declare attendance
        attendance = actions.attendance(self.team1, self.team2)
        self.stats.labelAttendance.set_label("%s" % (attendance))

        if self.team1.teamid == game.teamid:
            game.clubs[game.teamid].attendances.append(attendance)

        events.increment_goalscorers(airesult.scorers[0], airesult.scorers[1])
        events.increment_assists(airesult.assists[0], airesult.assists[1])

        events.update_statistics(airesult)
        events.update_records()

        # Decrement matches player is suspended for
        for playerid, player in game.players.items():
            if player.suspension_period > 0:
                player.suspension_period -= 1

                if player.suspension_period == 0:
                    player.suspension_type = 0

        # Televised games
        if game.televised[game.fixturesindex] == game.teamid:
            reputation = game.clubs[game.teamid].reputation
            amount = reputation * 3 * random.randint(950, 1050)
            money.deposit(amount, 8)

        # Matchday ticket sales
        if self.team1 == game.teamid:
            sales.matchday_tickets(attendance)
            sales.merchandise(attendance)
            sales.catering(attendance)

        # Process remaining matches
        self.process_remaining()

        widgets.continuegame.set_sensitive(True)
        self.buttonStart.set_sensitive(False)
        self.notebook.set_show_tabs(True)
        self.notebook.set_show_border(True)
        self.notebook.set_current_page(1)

        game.fixturesindex += 1
        game.fixturespage = game.fixturesindex

    def process_remaining(self):
        # Update league table for all other matches
        for index, item in enumerate(game.fixtures[game.fixturesindex]):
            if index != self.player_match:
                club1 = structures.Team()
                club1.teamid = item[0]
                club2 = structures.Team()
                club2.teamid = item[1]

                ai.generate_team(club1.teamid)
                ai.generate_team(club2.teamid)

                airesult = ai.Result(club1.teamid, club2.teamid)

                score = club1.teamid, airesult.final_score[0], airesult.final_score[1], club2.teamid

                league.update(score)
                game.results[game.fixturesindex].append(score)

                selection1, selection2 = events.increment_appearances(club1, club2)

                # Events
                refereeid = self.referee.select(index + 1)
                self.referee.increment(refereeid, airesult.yellows, airesult.reds)

                events.increment_goalscorers(airesult.scorers[0], airesult.scorers[1])
                events.increment_assists(airesult.assists[0], airesult.assists[1])
