#!/usr/bin/env python3

from gi.repository import Gtk
import random

import ai
import constants
import display
import evaluation
import events
import fixtures
import game
import league
import money
import news
import sales
import widgets


class Match(Gtk.Grid):
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
        self.labelTeam1 = Gtk.Label()
        self.labelTeam1.set_size_request(180, -1)
        self.labelTeam1.set_hexpand(True)
        self.labelTeam1.set_use_markup(True)
        grid.attach(self.labelTeam1, 0, 0, 1, 1)
        self.labelScore = Gtk.Label()
        self.labelScore.set_hexpand(True)
        self.labelScore.set_use_markup(True)
        grid.attach(self.labelScore, 1, 0, 1, 1)
        self.labelTeam2 = Gtk.Label()
        self.labelTeam2.set_size_request(180, -1)
        self.labelTeam2.set_hexpand(True)
        self.labelTeam2.set_use_markup(True)
        grid.attach(self.labelTeam2, 2, 0, 1, 1)

        # Events
        scrolledwindow = Gtk.ScrolledWindow()
        grid.attach(scrolledwindow, 0, 1, 1, 3)
        self.viewportEvents1 = Gtk.Viewport()
        scrolledwindow.add(self.viewportEvents1)

        scrolledwindow = Gtk.ScrolledWindow()
        grid.attach(scrolledwindow, 2, 1, 1, 3)
        self.viewportEvents2 = Gtk.Viewport()
        scrolledwindow.add(self.viewportEvents2)

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
        self.notebook.set_show_tabs(False)
        grid.attach(self.notebook, 0, 4, 4, 1)

        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)
        grid.set_border_width(5)
        grid.set_column_homogeneous(True)
        self.notebook.append_page(grid, Gtk.Label("Teams"))

        cellrenderertext = Gtk.CellRendererText()
        self.liststoreHome = Gtk.ListStore(str, str)
        self.liststoreAway = Gtk.ListStore(str, str)

        for count, model in enumerate((self.liststoreHome, self.liststoreAway)):
            scrolledwindow = Gtk.ScrolledWindow()
            grid.attach(scrolledwindow, count, 0, 1, 1)

            treeview = Gtk.TreeView()
            treeview.set_vexpand(True)
            treeview.set_hexpand(True)
            treeview.set_model(model)
            scrolledwindow.add(treeview)
            treeselection = treeview.get_selection()
            treeselection.set_mode(Gtk.SelectionMode.NONE)

            treeviewcolumn = Gtk.TreeViewColumn("Position", cellrenderertext, text=0)
            treeview.append_column(treeviewcolumn)
            treeviewcolumn = Gtk.TreeViewColumn("Player", cellrenderertext, text=1)
            treeview.append_column(treeviewcolumn)

        grid = Gtk.Grid()
        grid.set_hexpand(True)
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)
        grid.set_border_width(5)
        self.notebook.append_page(grid, Gtk.Label("Statistics"))

        label = widgets.AlignedLabel("Attendance")
        grid.attach(label, 0, 0, 1, 1)
        self.labelAttendance = widgets.AlignedLabel()
        grid.attach(self.labelAttendance, 1, 0, 1, 1)
        label = widgets.AlignedLabel("Shots On Target")
        grid.attach(label, 0, 1, 1, 1)
        label = widgets.AlignedLabel("Shots Off Target")
        grid.attach(label, 0, 2, 1, 1)
        label = widgets.AlignedLabel("Free Kicks")
        grid.attach(label, 0, 3, 1, 1)
        label = widgets.AlignedLabel("Corner Kicks")
        grid.attach(label, 0, 4, 1, 1)
        label = widgets.AlignedLabel("Throw-Ins")
        grid.attach(label, 0, 5, 1, 1)
        label = widgets.AlignedLabel("Fouls")
        grid.attach(label, 0, 6, 1, 1)
        label = widgets.AlignedLabel("Yellow Cards")
        grid.attach(label, 0, 7, 1, 1)
        label = widgets.AlignedLabel("Red Cards")
        grid.attach(label, 0, 8, 1, 1)
        label = widgets.AlignedLabel("Possession")
        grid.attach(label, 0, 9, 1, 1)

        self.player_match = 0

    def run(self):
        self.buttonStart.set_sensitive(True)
        self.notebook.set_show_tabs(False)
        self.notebook.set_current_page(0)

        for count, item in enumerate(game.fixtures[game.fixturesindex]):
            if game.teamid in (item[0], item[1]):
                match = item
                self.player_match = count

        self.team1 = match[0]
        self.team2 = match[1]

        if self.team1 != game.teamid:
            ai.generate_team(self.team1)
        else:
            ai.generate_team(self.team2)

        # Populate team lists
        self.liststoreHome.clear()
        self.liststoreAway.clear()

        model = 0

        for team in (self.team1, self.team2):
            count = 0

            for key, playerid in game.clubs[team].team.items():
                # First team
                if playerid != 0:
                    player = game.players[playerid]
                    name = display.name(player, mode=1)

                    if count < 11:
                        formationid = game.clubs[team].tactics[0]
                        position = constants.formations[formationid][1][count]

                        (self.liststoreHome, self.liststoreAway)[model].append([position, name])

                    # Substitutes
                    if count >= 11:
                        position = "Sub %i" % (count - 10)

                        (self.liststoreHome, self.liststoreAway)[model].append([position, name])

                    count += 1

            model = 1

        self.labelTeam1.set_markup('<span size="16000"><b>%s</b></span>' % (game.clubs[match[0]].name))
        self.labelTeam2.set_markup('<span size="16000"><b>%s</b></span>' % (game.clubs[match[1]].name))
        self.labelScore.set_markup('<span size="16000"><b>0 - 0</b></span>')

        # Determine referee
        self.referee = []

        for refereeid, referee in game.referees.items():
            self.referee.append([refereeid, referee[0]])

        random.shuffle(self.referee)

        stadiumid = game.clubs[self.team1].stadium
        venue = game.stadiums[stadiumid].name
        self.labelStadium.set_label("Venue: %s" % (venue))
        self.labelReferee.set_label("Referee: %s" % (self.referee[0][1]))

        game.menu.set_sensitive(False)
        widgets.continuegame.set_sensitive(False)
        widgets.news.set_sensitive(False)

        # Remove previous events grid and labels
        child = self.viewportEvents1.get_child()

        if child is not None:
            self.viewportEvents1.remove(child)
            child.destroy()

        child = self.viewportEvents2.get_child()

        if child is not None:
            self.viewportEvents2.remove(child)
            child.destroy()

        game.results.append([])

        self.show_all()

    def start_button_clicked(self, button):
        # Generate player match result and display
        result = ai.generate_result(self.team1, self.team2)
        self.labelScore.set_markup('<span size="16000"><b>%i - %i</b></span>' % (result[1], result[2]))

        # Decrement matches player is suspended for
        for playerid, player in game.players.items():
            if player.suspension_period > 0:
                player.suspension_period -= 1

                if player.suspension_period == 0:
                    player.suspension_type = 0

        # Standings
        game.standings = league.league_update(result, game.standings)
        game.results[game.fixturesindex].append(result)

        selection1, selection2 = events.increment_appearances(self.team1, self.team2)

        # Events
        scorers = events.goalscorers(result, selection1, selection2)
        assists = events.assists(result, selection1, selection2, scorers)
        yellows, reds = events.cards(self.team1, self.team2)
        events.match_injury(self.team1, self.team2)

        refereeid = self.referee[0][0]
        match = game.referees[refereeid][0]
        game.referees[refereeid][1] += 1
        game.referees[refereeid][3] += yellows
        game.referees[refereeid][4] += reds

        # Player match ratings
        ratings = [{}, {}]
        ratings[0] = events.rating(selection1)
        ratings[1] = events.rating(selection2)

        ratings = dict(ratings[0].items() | ratings[1].items())

        # Man of the match selection
        motm = []
        value = 0

        for playerid, rating in ratings.items():
            if rating > value:
                motm.append(playerid)
                value = rating

        playerid = random.choice(motm)
        game.players[playerid].man_of_the_match += 1

        # Team 1
        grid = Gtk.Grid()
        self.viewportEvents1.add(grid)

        for count, playerid in enumerate(scorers[0]):
            player = game.players[playerid]
            name = display.name(player, mode=1)

            label = widgets.AlignedLabel("%s" % (name))
            grid.attach(label, 0, count, 1, 1)

        grid.show_all()

        # Team 2
        grid = Gtk.Grid()
        self.viewportEvents2.add(grid)

        for count, playerid in enumerate(scorers[1]):
            player = game.players[playerid]
            name = display.name(player, mode=1)

            label = widgets.AlignedLabel("%s" % (name))
            grid.attach(label, 2, count, 1, 1)

        grid.show_all()

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

        # Update chairman evaluation
        if result[1] > result[2]:
            diff = result[1] - result[2]
        elif result[2] > result[1]:
            diff = result[2] - result[1]

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

        events.increment_goalscorers(scorers[0], scorers[1])
        events.increment_assists(assists[0], assists[1])
        events.update_statistics(result)
        events.update_records()

        # Televised games
        if game.televised[game.fixturesindex] == game.teamid:
            reputation = game.clubs[game.teamid].reputation
            amount = reputation * 3 * random.randint(950, 1050)
            money.deposit(amount, 8)

        # Declare attendance
        attendance = events.attendance(self.team1, self.team2)
        self.labelAttendance.set_text("%s" % (attendance))

        # Matchday ticket sales
        if game.teamid == self.team1:
            club = game.clubs[self.team1]

            available = 100 - club.season_tickets
            total = available / 100

            stadium = game.stadiums[club.stadium]
            capacity = stadium.capacity

            amount = club.tickets[10] * (capacity * total)
            money.deposit(amount, 5)

            sales.merchandise(attendance)
            sales.catering(attendance)

        # Update league table for all other matches
        for index, item in enumerate(game.fixtures[game.fixturesindex]):
            if index != self.player_match:
                ai.generate_team(item[0])
                ai.generate_team(item[1])
                result = ai.generate_result(item[0], item[1])
                game.standings = league.league_update(result, game.standings)
                game.results[game.fixturesindex].append(result)

                selection1, selection2 = events.increment_appearances(item[0], item[1])

                # Events
                scorers = events.goalscorers(result, selection1, selection2)
                assists = events.assists(result, selection1, selection2, scorers)
                yellows, reds = events.cards(item[0], item[1])
                events.match_injury(item[0], item[1])

                refereeid = self.referee[index + 1][0]
                match = game.referees[refereeid][0]
                game.referees[refereeid][1] += 1
                game.referees[refereeid][3] += yellows
                game.referees[refereeid][4] += reds

                events.increment_goalscorers(scorers[0], scorers[1])
                events.increment_assists(assists[0], assists[1])
                events.update_statistics(result)
                events.update_records()

        widgets.continuegame.set_sensitive(True)
        self.buttonStart.set_sensitive(False)
        self.notebook.set_show_tabs(True)
        self.notebook.set_current_page(1)

        game.fixturesindex += 1
        game.fixturespage = game.fixturesindex
