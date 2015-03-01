#!/usr/bin/env python3

from gi.repository import Gtk
from gi.repository import Gdk
import random
import re
import statistics

import game
import constants
import widgets
import display
import chart
import evaluation


class News(Gtk.Grid):
    def __init__(self):
        Gtk.Grid.__init__(self)
        self.set_border_width(5)
        self.set_row_spacing(5)

        self.liststoreNews = Gtk.ListStore(str, str, str, int, str, bool, int)
        self.treefilter = self.liststoreNews.filter_new()
        self.treefilter.set_visible_func(self.filter_visible, game.clubs)

        grid = Gtk.Grid()
        grid.set_column_spacing(5)
        self.attach(grid, 0, 0, 1, 1)

        entrySearch = Gtk.SearchEntry()
        entrySearch.set_placeholder_text("Search")
        entrySearch.connect("activate", self.search_activated)
        entrySearch.connect("icon-press", self.icon_press)
        entrySearch.connect("changed", self.search_changed)
        entrySearch.add_accelerator("grab-focus",
                                    game.accelgroup,
                                    102,
                                    Gdk.ModifierType.CONTROL_MASK,
                                    Gtk.AccelFlags.VISIBLE)
        grid.attach(entrySearch, 0, 0, 1, 1)

        label = Gtk.Label("_Filter")
        label.set_hexpand(True)
        label.set_alignment(1, 0.5)
        label.set_use_underline(True)
        grid.attach(label, 1, 0, 1, 1)
        self.comboboxFilter = Gtk.ComboBoxText()
        self.comboboxFilter.append("0", "All")
        for categoryid, category in constants.category.items():
            self.comboboxFilter.append(str(categoryid), category)
        self.comboboxFilter.set_active(0)
        self.comboboxFilter.connect("changed", self.filter_changed)
        label.set_mnemonic_widget(self.comboboxFilter)
        grid.attach(self.comboboxFilter, 2, 0, 1, 1)

        paned = Gtk.Paned()
        paned.set_position(150)
        paned.set_orientation(Gtk.Orientation.VERTICAL)
        self.attach(paned, 0, 1, 1, 1)

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_vexpand(True)
        scrolledwindow.set_hexpand(True)
        paned.add1(scrolledwindow)

        treeviewNews = Gtk.TreeView()
        treeviewNews.set_model(self.treefilter)
        treeviewNews.set_activate_on_single_click(True)
        treeviewNews.set_enable_search(False)
        treeviewNews.set_search_column(-1)
        treeviewNews.connect("row-activated", self.item_selected)
        scrolledwindow.add(treeviewNews)

        cellrenderertext = Gtk.CellRendererText()
        treeviewcolumn = Gtk.TreeViewColumn("Date",
                                            cellrenderertext,
                                            text=0)
        treeviewNews.append_column(treeviewcolumn)

        treeviewcolumn = Gtk.TreeViewColumn("Title")
        treeviewcolumn.set_expand(True)
        treeviewNews.append_column(treeviewcolumn)
        cellrendererTitle = Gtk.CellRendererText()
        treeviewcolumn.pack_start(cellrendererTitle, True)
        treeviewcolumn.add_attribute(cellrendererTitle, "text", 1)
        treeviewcolumn.add_attribute(cellrendererTitle, "weight-set", 5)
        treeviewcolumn.add_attribute(cellrendererTitle, "weight", 6)

        treeviewcolumn = Gtk.TreeViewColumn("Category",
                                            cellrenderertext,
                                            text=4)
        treeviewNews.append_column(treeviewcolumn)

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_policy(Gtk.PolicyType.NEVER,
                                  Gtk.PolicyType.ALWAYS)
        paned.add2(scrolledwindow)

        self.textviewNews = Gtk.TextView()
        self.textviewNews.set_editable(False)
        self.textviewNews.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        self.textviewNews.set_left_margin(5)
        self.textviewNews.set_right_margin(5)
        self.textviewNews.set_vexpand(True)
        self.textviewNews.set_hexpand(True)
        scrolledwindow.add(self.textviewNews)

    def search_changed(self, entry):
        if entry.get_text_length() == 0:
            self.populate_data(game.news)

    def search_activated(self, entry):
        criteria = entry.get_text()

        if len(criteria) > 0:
            data = []

            for item in game.news:
                title = item[1]
                message = item[2]

                for search in (title, message):
                    if re.findall(criteria, search, re.IGNORECASE):
                        data.append(item[0:])

                        break

            self.populate_data(data)

    def icon_press(self, entry, position, event):
        if position == Gtk.EntryIconPosition.SECONDARY:
            self.populate_data(game.news)

    def item_selected(self, treeview, path, column):
        model = treeview.get_model()

        text = model[path][2]

        textbuffer = self.textviewNews.get_buffer()
        textbuffer.set_text(text)

        model[path][5] = False

        # Update news list with read/unread status
        game.news = []

        for item in model:
            news = item[0:4]
            news.append(item[5])
            game.news.append(news)

        unread_count = 0

        for item in model:
            if item[5]:
                unread_count += 1

        # Check how many unread items there are
        if unread_count == 0:
            widgets.news.hide()
            game.unreadnews = False

    def filter_changed(self, combobox):
        self.treefilter.refilter()

    def filter_visible(self, model, treeiter, data):
        filterid = int(self.comboboxFilter.get_active_id())
        show = True

        if filterid != 0:
            if model[treeiter][3] != filterid:
                show = False

        return show

    def populate_data(self, data):
        self.liststoreNews.clear()

        for item in data:
            category = constants.category[item[3]]

            # Weight of 700 required to make font bold when item unread
            if item[4]:
                weight = 700
            else:
                weight = 400

            self.liststoreNews.append([item[0],
                                       item[1],
                                       item[2],
                                       item[3],
                                       category,
                                       item[4],
                                       weight])

    def run(self):
        self.populate_data(game.news)

        self.show_all()


class Fixtures(Gtk.Grid):
    def __init__(self):
        Gtk.Grid.__init__(self)
        self.set_border_width(5)
        self.set_row_spacing(5)
        self.set_column_spacing(5)

        self.liststoreClubFixtures = Gtk.ListStore(str)        # Club fixtures
        self.liststoreFixtures = Gtk.ListStore(str, str, str)  # All fixtures

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_policy(Gtk.PolicyType.NEVER,
                                  Gtk.PolicyType.AUTOMATIC)
        self.attach(scrolledwindow, 0, 1, 1, 1)

        # Fixtures for players club
        label = widgets.AlignedLabel("Your Fixtures")
        self.attach(label, 0, 0, 1, 1)

        self.treeviewClubFixtures = Gtk.TreeView()
        self.treeviewClubFixtures.set_headers_visible(False)
        self.treeviewClubFixtures.set_model(self.liststoreClubFixtures)
        self.treeviewClubFixtures.set_vexpand(True)
        self.treeviewClubFixtures.set_enable_search(False)
        self.treeviewClubFixtures.set_search_column(-1)
        scrolledwindow.add(self.treeviewClubFixtures)

        cellrenderertext = Gtk.CellRendererText()
        treeviewcolumn = Gtk.TreeViewColumn(None,
                                            cellrenderertext,
                                            text=0)
        self.treeviewClubFixtures.append_column(treeviewcolumn)

        # Fixtures for all clubs
        self.labelFixturesView = widgets.AlignedLabel("Round 1")
        self.attach(self.labelFixturesView, 1, 0, 1, 1)

        buttonbox = Gtk.ButtonBox()
        buttonbox.set_spacing(5)
        buttonbox.set_layout(Gtk.ButtonBoxStyle.END)
        self.buttonPrevious = widgets.Button("_Previous")
        self.buttonPrevious.set_sensitive(False)
        self.buttonPrevious.connect("clicked", self.change_fixtures, -1)
        buttonbox.add(self.buttonPrevious)
        self.buttonNext = widgets.Button("_Next")
        self.buttonNext.connect("clicked", self.change_fixtures, 1)
        buttonbox.add(self.buttonNext)
        self.attach(buttonbox, 2, 0, 1, 1)

        treeviewFixtures = Gtk.TreeView()
        treeviewFixtures.set_model(self.liststoreFixtures)
        treeviewFixtures.set_enable_search(False)
        treeviewFixtures.set_search_column(-1)
        treeviewFixtures.set_vexpand(True)
        treeviewFixtures.set_hexpand(True)
        treeselection = treeviewFixtures.get_selection()
        treeselection.set_mode(Gtk.SelectionMode.NONE)
        self.attach(treeviewFixtures, 1, 1, 2, 1)

        cellrenderertext = Gtk.CellRendererText()
        treeviewcolumn = Gtk.TreeViewColumn("Home",
                                            cellrenderertext,
                                            text=0)
        treeviewcolumn.set_expand(True)
        treeviewFixtures.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Away",
                                            cellrenderertext,
                                            text=1)
        treeviewcolumn.set_expand(True)
        treeviewFixtures.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Venue",
                                            cellrenderertext,
                                            text=2)
        treeviewcolumn.set_expand(True)
        treeviewFixtures.append_column(treeviewcolumn)

    def run(self):
        self.populate_data()

        if game.fixturespage > 0:
            self.buttonPrevious.set_sensitive(True)

        self.show_all()

    def change_fixtures(self, button, direction):
        game.fixturespage += direction

        if game.fixturespage > 0:
            self.buttonPrevious.set_sensitive(True)
        else:
            self.buttonPrevious.set_sensitive(False)

        if game.fixturespage < len(game.fixtures) - 1:
            self.buttonNext.set_sensitive(True)
        else:
            self.buttonNext.set_sensitive(False)

        self.populate_data()

    def populate_data(self):
        self.liststoreClubFixtures.clear()
        self.liststoreFixtures.clear()

        self.labelFixturesView.set_label("Round %i" % (game.fixturespage + 1))

        for week in game.fixtures:
            for match in week:
                if game.teamid in (match[0], match[1]):
                    match = "%s - %s" % (game.clubs[match[0]].name, game.clubs[match[1]].name)
                    self.liststoreClubFixtures.append([match])

        for match in game.fixtures[game.fixturespage]:
            team1 = game.clubs[match[0]].name
            team2 = game.clubs[match[1]].name

            clubid = match[0]
            stadiumid = game.clubs[clubid].stadium
            stadium = game.stadiums[stadiumid].name

            self.liststoreFixtures.append([team1, team2, stadium])

        self.treeviewClubFixtures.set_cursor(game.fixturespage)


class Results(Gtk.Grid):
    page = 0

    def __init__(self):
        Gtk.Grid.__init__(self)
        self.set_border_width(5)
        self.set_row_spacing(5)

        scrolledwindow = Gtk.ScrolledWindow()
        self.attach(scrolledwindow, 0, 1, 1, 1)

        self.overlay = Gtk.Overlay()
        scrolledwindow.add(self.overlay)
        self.labelNoResults = Gtk.Label("No fixtures have yet been played.")
        self.overlay.add_overlay(self.labelNoResults)

        buttonbox = Gtk.ButtonBox()
        buttonbox.set_spacing(5)
        buttonbox.set_layout(Gtk.ButtonBoxStyle.END)
        self.attach(buttonbox, 0, 0, 1, 1)

        self.buttonPrevious = widgets.Button("_Previous")
        self.buttonPrevious.set_sensitive(False)
        self.buttonPrevious.connect("clicked", self.change_page, 0)
        buttonbox.add(self.buttonPrevious)
        self.buttonNext = widgets.Button("_Next")
        self.buttonNext.set_sensitive(False)
        self.buttonNext.connect("clicked", self.change_page, 1)
        buttonbox.add(self.buttonNext)

        self.liststoreResults = Gtk.ListStore(str, int, int, str)

        self.treeviewResults = Gtk.TreeView()
        self.treeviewResults.set_model(self.liststoreResults)
        self.treeviewResults.set_hexpand(True)
        self.treeviewResults.set_vexpand(True)
        treeselection = self.treeviewResults.get_selection()
        treeselection.set_mode(Gtk.SelectionMode.NONE)
        self.overlay.add(self.treeviewResults)

        cellrenderertext = Gtk.CellRendererText()
        treeviewcolumn = Gtk.TreeViewColumn("Home",
                                            cellrenderertext,
                                            text=0)
        treeviewcolumn.set_expand(True)
        self.treeviewResults.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn(None,
                                            cellrenderertext,
                                            text=1)
        self.treeviewResults.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn(None,
                                            cellrenderertext,
                                            text=2)
        self.treeviewResults.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Away",
                                            cellrenderertext,
                                            text=3)
        treeviewcolumn.set_expand(True)
        self.treeviewResults.append_column(treeviewcolumn)

    def run(self):
        self.show_all()
        self.liststoreResults.clear()

        self.treeviewResults.set_sensitive(False)

        if len(game.results) > 0:
            for result in game.results[self.page]:
                team1 = game.clubs[result[0]].name
                team2 = game.clubs[result[3]].name

                self.liststoreResults.append([team1, result[1], result[2], team2])

            self.labelNoResults.hide()
            self.treeviewResults.set_sensitive(True)

        if len(game.results) > 1:
            self.buttonNext.set_sensitive(True)
            self.buttonPrevious.set_sensitive(True)

            if self.page == 0:
                self.buttonPrevious.set_sensitive(False)
            elif self.page == len(game.results) - 1:
                self.buttonNext.set_sensitive(False)
        else:
            self.buttonNext.set_sensitive(False)
            self.buttonPrevious.set_sensitive(False)

    def change_page(self, button, mode):
        if mode == 0:
            if self.page > 0:
                self.page -= 1
        elif mode == 1:
            if self.page < len(game.results) - 1:
                self.page += 1

        self.liststoreResults.clear()

        for result in game.results[self.page]:
            team1 = game.clubs[result[0]].name
            team2 = game.clubs[result[3]].name

            self.liststoreResults.append([team1, result[1], result[2], team2])

        if mode == 0:
            if self.page > 0:
                self.buttonNext.set_sensitive(True)
                self.buttonPrevious.set_sensitive(True)
            else:
                self.buttonNext.set_sensitive(True)
                self.buttonPrevious.set_sensitive(False)
        elif mode == 1:
            if self.page < len(game.results) - 1:
                self.buttonPrevious.set_sensitive(True)
                self.buttonNext.set_sensitive(True)
            else:
                self.buttonPrevious.set_sensitive(True)
                self.buttonNext.set_sensitive(False)


class Standings(Gtk.Grid):
    def __init__(self):
        Gtk.Grid.__init__(self)
        self.set_border_width(5)

        scrolledwindow = Gtk.ScrolledWindow()
        self.attach(scrolledwindow, 0, 0, 1, 1)

        self.liststoreStandings = Gtk.ListStore(str, int, int, int, int, int, int, int, int, str)
        self.treemodelsort = Gtk.TreeModelSort(self.liststoreStandings)
        self.treemodelsort.set_sort_column_id(0, Gtk.SortType.ASCENDING)
        self.treemodelsort.set_sort_func(0, self.standings_sort)

        treeviewStandings = Gtk.TreeView()
        treeviewStandings.set_model(self.treemodelsort)
        treeviewStandings.set_enable_search(False)
        treeviewStandings.set_search_column(-1)
        treeviewStandings.set_vexpand(True)
        treeviewStandings.set_hexpand(True)
        treeselection = treeviewStandings.get_selection()
        treeselection.set_mode(Gtk.SelectionMode.NONE)
        scrolledwindow.add(treeviewStandings)

        cellrenderertext = Gtk.CellRendererText()
        treeviewcolumn = Gtk.TreeViewColumn("Team",
                                            cellrenderertext,
                                            text=0)
        treeviewcolumn.set_expand(True)
        treeviewStandings.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Played",
                                            cellrenderertext,
                                            text=1)
        treeviewcolumn.set_fixed_width(48)
        treeviewStandings.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Won",
                                            cellrenderertext,
                                            text=2)
        treeviewcolumn.set_fixed_width(48)
        treeviewStandings.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Drawn",
                                            cellrenderertext,
                                            text=3)
        treeviewcolumn.set_fixed_width(48)
        treeviewStandings.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Lost",
                                            cellrenderertext,
                                            text=4)
        treeviewcolumn.set_fixed_width(48)
        treeviewStandings.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn(None,
                                            cellrenderertext,
                                            text=5)
        label = Gtk.Label("GF")
        label.set_tooltip_text("Goals For")
        label.show()
        treeviewcolumn.set_widget(label)
        treeviewcolumn.set_fixed_width(48)
        treeviewStandings.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn(None,
                                            cellrenderertext,
                                            text=6)
        label = Gtk.Label("GA")
        label.set_tooltip_text("Goals Against")
        label.show()
        treeviewcolumn.set_widget(label)
        treeviewcolumn.set_fixed_width(48)
        treeviewStandings.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn(None,
                                            cellrenderertext,
                                            text=7)
        label = Gtk.Label("GD")
        label.set_tooltip_text("Goal Difference")
        label.show()
        treeviewcolumn.set_widget(label)
        treeviewcolumn.set_fixed_width(48)
        treeviewStandings.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Points",
                                            cellrenderertext,
                                            text=8)
        treeviewcolumn.set_fixed_width(48)
        treeviewStandings.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Form",
                                            cellrenderertext,
                                            text=9)
        treeviewcolumn.set_fixed_width(96)
        treeviewStandings.append_column(treeviewcolumn)

    def standings_sort(self, treesortable, treeiter1, treeiter2, data):
        if game.eventindex == 0:
            # Sort by club name if zero games played
            team2 = treesortable[treeiter1][0]
            team1 = treesortable[treeiter2][0]
        else:
            # Sort by points, goal difference, goals for, goals against
            team1 = (treesortable[treeiter1][8],
                     treesortable[treeiter1][7],
                     treesortable[treeiter1][5],
                     treesortable[treeiter1][6])
            team2 = (treesortable[treeiter2][8],
                     treesortable[treeiter2][7],
                     treesortable[treeiter2][5],
                     treesortable[treeiter2][6])

        if team1 < team2:
            return 1
        elif team1 == team2:
            return 0
        else:
            return -1

    def run(self):
        self.liststoreStandings.clear()

        for clubid, details in game.standings.items():
            club = game.clubs[clubid]

            form = "".join(club.form[-6:])

            self.liststoreStandings.append([club.name,
                                            details.played,
                                            details.wins,
                                            details.draws,
                                            details.losses,
                                            details.goals_for,
                                            details.goals_against,
                                            details.goal_difference,
                                            details.points,
                                            form])

        self.show_all()


class Charts(Gtk.Grid):
    views = {0: chart.GoalScorers(),
             1: chart.Assists(),
             2: chart.Cards(),
             3: chart.Transfers(),
             4: chart.Referees(),
            }

    def __init__(self):
        self.charts = self.views[0]

        Gtk.Grid.__init__(self)
        self.set_border_width(5)
        self.set_row_spacing(5)
        self.set_vexpand(True)
        self.set_hexpand(True)

        buttonbox = Gtk.ButtonBox()
        buttonbox.set_spacing(5)
        buttonbox.set_layout(Gtk.ButtonBoxStyle.END)
        self.attach(buttonbox, 1, 0, 1, 1)

        label = Gtk.Label("View")
        label.set_alignment(1, 0.5)
        buttonbox.add(label)

        comboboxChart = Gtk.ComboBoxText()
        comboboxChart.append("0", "Goalscorers")
        comboboxChart.append("1", "Assists")
        comboboxChart.append("2", "Cards")
        comboboxChart.append("3", "Transfers")
        comboboxChart.append("4", "Referees")
        comboboxChart.set_active(0)
        comboboxChart.connect("changed", self.view_changed)
        buttonbox.add(comboboxChart)

        self.grid = Gtk.Grid()
        self.grid.set_vexpand(True)
        self.grid.set_hexpand(True)
        self.grid.set_row_spacing(5)
        self.grid.set_column_spacing(5)
        self.attach(self.grid, 0, 2, 2, 1)

        self.charts.set_vexpand(True)
        self.charts.set_hexpand(True)
        self.grid.add(self.charts)

    def view_changed(self, combobox):
        viewid = int(combobox.get_active_id())

        if self.charts:
            self.grid.remove(self.charts)

        self.charts = self.views[viewid]
        self.charts.set_vexpand(True)
        self.charts.set_hexpand(True)

        self.grid.add(self.charts)
        self.charts.run()

    def run(self):
        self.charts.run()
        self.show_all()


class Evaluation(Gtk.Grid):
    def __init__(self):
        Gtk.Grid.__init__(self)
        self.set_vexpand(True)
        self.set_hexpand(True)
        self.set_border_width(5)
        self.set_row_spacing(5)
        self.set_column_spacing(5)

        for count, text in enumerate(("Chairman", "Fans", "Finances", "Players", "Staff", "Overall")):
            label = widgets.AlignedLabel("<b>%s</b>" % (text))
            self.attach(label, 0, count * 2, 1, 1)

        label = Gtk.Label()
        self.attach(label, 0, 1, 1, 1)

        self.labelChairman = Gtk.Label()
        self.labelChairman.set_hexpand(True)
        self.labelChairman.set_alignment(0, 0.5)
        self.attach(self.labelChairman, 1, 1, 1, 1)
        self.labelChairmanPercent = Gtk.Label()
        self.attach(self.labelChairmanPercent, 2, 1, 1, 1)

        self.labelFans = Gtk.Label()
        self.labelFans.set_hexpand(True)
        self.labelFans.set_alignment(0, 0.5)
        self.attach(self.labelFans, 1, 3, 1, 1)
        self.labelFansPercent = Gtk.Label()
        self.attach(self.labelFansPercent, 2, 3, 1, 1)

        self.labelFinances = Gtk.Label()
        self.labelFinances.set_hexpand(True)
        self.labelFinances.set_alignment(0, 0.5)
        self.attach(self.labelFinances, 1, 5, 1, 1)
        self.labelFinancesPercent = Gtk.Label()
        self.attach(self.labelFinancesPercent, 2, 5, 1, 1)

        self.labelPlayers = Gtk.Label()
        self.labelPlayers.set_hexpand(True)
        self.labelPlayers.set_alignment(0, 0.5)
        self.attach(self.labelPlayers, 1, 7, 1, 1)
        self.labelPlayersPercent = Gtk.Label()
        self.attach(self.labelPlayersPercent, 2, 7, 1, 1)

        self.labelStaff = Gtk.Label()
        self.labelStaff.set_hexpand(True)
        self.labelStaff.set_alignment(0, 0.5)
        self.attach(self.labelStaff, 1, 9, 1, 1)
        self.labelStaffPercent = Gtk.Label()
        self.attach(self.labelStaffPercent, 2, 9, 1, 1)

        self.labelOverallPercent = Gtk.Label()
        self.attach(self.labelOverallPercent, 2, 11, 1, 1)

    def run(self):
        evaluation.update()

        club = game.clubs[game.teamid]

        # Chairman
        value = evaluation.indexer(club.evaluation[0])
        self.labelChairman.set_label('"%s"' % (random.choice(constants.evaluation[0][value])))
        self.labelChairmanPercent.set_markup("<b>%i%%</b>" % (club.evaluation[0]))

        # Fans
        value = evaluation.indexer(club.evaluation[1])
        self.labelFans.set_label('"%s"' % (random.choice(constants.evaluation[1][value])))
        self.labelFansPercent.set_markup("<b>%i%%</b>" % (club.evaluation[1]))

        # Finances
        value = evaluation.indexer(club.evaluation[2])
        self.labelFinances.set_label('"%s"' % (random.choice(constants.evaluation[2][value])))
        self.labelFinancesPercent.set_markup("<b>%i%%</b>" % (club.evaluation[2]))

        # Players
        value = evaluation.indexer(club.evaluation[3])
        self.labelPlayers.set_label('"%s"' % (random.choice(constants.evaluation[3][value])))
        self.labelPlayersPercent.set_markup("<b>%i%%</b>" % (club.evaluation[3]))

        # Staff
        if len(club.scouts_hired) + len(club.coaches_hired) > 0:
            value = evaluation.indexer(club.evaluation[4])
            self.labelStaff.set_label('"%s"' % (random.choice(constants.evaluation[4][value])))
            self.labelStaffPercent.set_markup("<b>%i%%</b>" % (club.evaluation[4]))
        else:
            self.labelStaff.set_label('"There are no scouts or coaches on staff."')
            self.labelStaffPercent.set_label("")

        overall = evaluation.calculate_overall()
        self.labelOverallPercent.set_markup("<b>%i%%</b>" % (overall))

        self.show_all()


class Statistics(Gtk.Grid):
    class TreeView(Gtk.TreeView):
        def __init__(self):
            Gtk.TreeView.__init__(self)
            self.set_hexpand(True)
            self.set_fixed_height_mode(True)
            self.set_enable_search(False)
            self.set_search_column(-1)

            cellrenderertext = Gtk.CellRendererText()
            treeviewcolumn = Gtk.TreeViewColumn("Season", cellrenderertext, text=0)
            treeviewcolumn.set_fixed_width(75)
            treeviewcolumn.set_sizing(Gtk.TreeViewColumnSizing.FIXED)
            self.append_column(treeviewcolumn)
            treeviewcolumn = Gtk.TreeViewColumn("Played", cellrenderertext, text=1)
            treeviewcolumn.set_fixed_width(50)
            treeviewcolumn.set_sizing(Gtk.TreeViewColumnSizing.FIXED)
            self.append_column(treeviewcolumn)
            treeviewcolumn = Gtk.TreeViewColumn("Won", cellrenderertext, text=2)
            treeviewcolumn.set_fixed_width(50)
            treeviewcolumn.set_sizing(Gtk.TreeViewColumnSizing.FIXED)
            self.append_column(treeviewcolumn)
            treeviewcolumn = Gtk.TreeViewColumn("Drawn", cellrenderertext, text=3)
            treeviewcolumn.set_fixed_width(50)
            treeviewcolumn.set_sizing(Gtk.TreeViewColumnSizing.FIXED)
            self.append_column(treeviewcolumn)
            treeviewcolumn = Gtk.TreeViewColumn("Lost", cellrenderertext, text=4)
            treeviewcolumn.set_fixed_width(50)
            treeviewcolumn.set_sizing(Gtk.TreeViewColumnSizing.FIXED)
            self.append_column(treeviewcolumn)
            treeviewcolumn = Gtk.TreeViewColumn("Goals For", cellrenderertext, text=5)
            treeviewcolumn.set_fixed_width(100)
            treeviewcolumn.set_sizing(Gtk.TreeViewColumnSizing.FIXED)
            self.append_column(treeviewcolumn)
            treeviewcolumn = Gtk.TreeViewColumn("Goals Against", cellrenderertext, text=6)
            treeviewcolumn.set_fixed_width(100)
            treeviewcolumn.set_sizing(Gtk.TreeViewColumnSizing.FIXED)
            self.append_column(treeviewcolumn)
            treeviewcolumn = Gtk.TreeViewColumn("Goal Difference", cellrenderertext, text=7)
            treeviewcolumn.set_fixed_width(100)
            treeviewcolumn.set_sizing(Gtk.TreeViewColumnSizing.FIXED)
            self.append_column(treeviewcolumn)
            treeviewcolumn = Gtk.TreeViewColumn("Points", cellrenderertext, text=8)
            treeviewcolumn.set_fixed_width(50)
            treeviewcolumn.set_sizing(Gtk.TreeViewColumnSizing.FIXED)
            self.append_column(treeviewcolumn)
            treeviewcolumn = Gtk.TreeViewColumn("Position", cellrenderertext, text=9)
            treeviewcolumn.set_sizing(Gtk.TreeViewColumnSizing.FIXED)
            self.append_column(treeviewcolumn)

    def __init__(self):
        Gtk.Grid.__init__(self)
        self.set_vexpand(True)
        self.set_hexpand(True)
        self.set_border_width(5)
        self.set_row_spacing(5)
        self.set_column_spacing(5)

        commonframe = widgets.CommonFrame("Games")
        self.attach(commonframe, 0, 0, 1, 1)

        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)
        commonframe.insert(grid)

        label = widgets.AlignedLabel("Largest Win")
        grid.attach(label, 0, 0, 1, 1)
        self.labelWin = widgets.AlignedLabel("Not Applicable")
        grid.attach(self.labelWin, 1, 0, 1, 1)
        label = widgets.AlignedLabel("Largest Loss")
        grid.attach(label, 0, 1, 1, 1)
        self.labelLoss = widgets.AlignedLabel("Not Applicable")
        grid.attach(self.labelLoss, 1, 1, 1, 1)

        commonframe = widgets.CommonFrame("Goals")
        self.attach(commonframe, 0, 1, 1, 1)

        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)
        commonframe.insert(grid)

        label = widgets.AlignedLabel("Leading Goalscorer")
        grid.attach(label, 0, 0, 1, 1)
        self.labelGoalscorer = widgets.AlignedLabel()
        grid.attach(self.labelGoalscorer, 1, 0, 1, 1)
        label = widgets.AlignedLabel("Leading Assister")
        grid.attach(label, 0, 1, 1, 1)
        self.labelAssister = widgets.AlignedLabel()
        grid.attach(self.labelAssister, 1, 1, 1, 1)

        commonframe = widgets.CommonFrame("Cards")
        self.attach(commonframe, 1, 0, 1, 1)

        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)
        commonframe.insert(grid)

        label = widgets.AlignedLabel("Yellow Cards")
        grid.attach(label, 0, 0, 1, 1)
        label = widgets.AlignedLabel("Red Cards")
        grid.attach(label, 0, 1, 1, 1)

        commonframe = widgets.CommonFrame("Stadium")
        self.attach(commonframe, 1, 1, 1, 1)

        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)
        commonframe.insert(grid)

        label = widgets.AlignedLabel("Highest Attendance")
        grid.attach(label, 0, 0, 1, 1)
        labelHighAttendance = widgets.AlignedLabel()
        grid.attach(labelHighAttendance, 1, 0, 1, 1)
        label = widgets.AlignedLabel("Lowest Attendance")
        grid.attach(label, 0, 1, 1, 1)
        labelLowAttendance = widgets.AlignedLabel()
        grid.attach(labelLowAttendance, 1, 1, 1, 1)
        label = widgets.AlignedLabel("Average Attendance")
        grid.attach(label, 0, 2, 1, 1)
        labelAverageAttendance = widgets.AlignedLabel()
        grid.attach(labelAverageAttendance, 1, 2, 1, 1)

        commonframe = widgets.CommonFrame("Salary")
        self.attach(commonframe, 2, 0, 1, 1)

        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)
        commonframe.insert(grid)

        label = widgets.AlignedLabel("Highest Salary")
        grid.attach(label, 0, 0, 1, 1)
        self.labelHighSalary = widgets.AlignedLabel()
        grid.attach(self.labelHighSalary, 1, 0, 1, 1)
        label = widgets.AlignedLabel("Lowest Salary")
        grid.attach(label, 0, 1, 1, 1)
        self.labelLowSalary = widgets.AlignedLabel()
        grid.attach(self.labelLowSalary, 1, 1, 1, 1)
        label = widgets.AlignedLabel("Average Salary")
        grid.attach(label, 0, 2, 1, 1)
        self.labelAvgSalary = widgets.AlignedLabel()
        grid.attach(self.labelAvgSalary, 1, 2, 1, 1)

        commonframe = widgets.CommonFrame("Value")
        self.attach(commonframe, 2, 1, 1, 1)

        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)
        commonframe.insert(grid)

        label = widgets.AlignedLabel("Highest Value")
        grid.attach(label, 0, 0, 1, 1)
        self.labelHighValue = widgets.AlignedLabel()
        grid.attach(self.labelHighValue, 1, 0, 1, 1)
        label = widgets.AlignedLabel("Lowest Value")
        grid.attach(label, 0, 1, 1, 1)
        self.labelLowValue = widgets.AlignedLabel()
        grid.attach(self.labelLowValue, 1, 1, 1, 1)
        label = widgets.AlignedLabel("Average Value")
        grid.attach(label, 0, 2, 1, 1)
        self.labelAvgValue = widgets.AlignedLabel()
        grid.attach(self.labelAvgValue, 1, 2, 1, 1)

        self.liststoreRecordCurrent = Gtk.ListStore(str, int, int, int, int, int, int, int, int, str)
        self.liststoreRecordPrevious = Gtk.ListStore(str, int, int, int, int, int, int, int, int, str)

        commonframe = widgets.CommonFrame("Current League Record")
        self.attach(commonframe, 0, 2, 3, 1)

        treeview = self.TreeView()
        treeview.set_model(self.liststoreRecordCurrent)
        treeselection = treeview.get_selection()
        treeselection.set_mode(Gtk.SelectionMode.NONE)
        commonframe.insert(treeview)

        commonframe = widgets.CommonFrame("Previous League Record")
        self.attach(commonframe, 0, 3, 3, 1)

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)
        commonframe.insert(scrolledwindow)

        treeview = self.TreeView()
        treeview.set_model(self.liststoreRecordPrevious)
        treeselection = treeview.get_selection()
        treeselection.set_mode(Gtk.SelectionMode.NONE)
        scrolledwindow.add(treeview)

    def run(self):
        self.show_all()

        self.liststoreRecordPrevious.clear()
        [self.liststoreRecordPrevious.append(item) for item in game.record[1]]

        self.liststoreRecordCurrent.clear()
        self.liststoreRecordCurrent.insert(0, game.record[0])

        # Highest win / loss
        if game.statistics[0][0]:
            clubid = game.statistics[0][0]
            opposition = game.clubs[clubid].name
            self.labelWin.set_label("%i - %i (against %s)" % (game.statistics[0][1][0],
                                                              game.statistics[0][1][1],
                                                              opposition)
                                   )

        if game.statistics[1][0]:
            clubid = game.statistics[1][0]
            opposition = game.clubs[clubid].name
            self.labelLoss.set_label("%i - %i (against %s)" % (game.statistics[1][1][0],
                                                               game.statistics[1][1][1],
                                                               opposition)
                                    )

        # Top goalscorer
        top = [0, 0]

        for playerid in game.clubs[game.teamid].squad:
            player = game.players[playerid]

            if player.goals > top[1]:
                top[0] = playerid
                top[1] = player.goals

        if top[0] != 0:
            player = game.players[top[0]]
            name = display.name(player, mode=1)
            self.labelGoalscorer.set_label("%s (%i goals)" % (name, top[1]))
        else:
            self.labelGoalscorer.set_label("Not applicable")

        # Top assister
        top = [0, 0]

        for playerid in game.clubs[game.teamid].squad:
            player = game.players[playerid]

            if player.assists > top[1]:
                top[0] = playerid
                top[1] = player.assists

        if top[0] != 0:
            player = game.players[top[0]]
            name = display.name(player, mode=1)
            self.labelAssister.set_label("%s (%i assists)" % (name, top[1]))
        else:
            self.labelAssister.set_label("Not applicable")

        # Highest wage / player value
        wage = [game.players[key].wage for key in game.clubs[game.teamid].squad]
        value = [game.players[key].value for key in game.clubs[game.teamid].squad]

        maximum = display.currency(max(wage))
        self.labelHighSalary.set_label("%s" % (maximum))
        minimum = display.currency(min(wage))
        self.labelLowSalary.set_label("%s" % (minimum))
        average = display.currency(statistics.mean(wage))
        self.labelAvgSalary.set_label("%s" % (average))

        maximum = display.currency(max(value))
        self.labelHighValue.set_label("%s" % (maximum))
        minimum = display.currency(min(value))
        self.labelLowValue.set_label("%s" % (minimum))
        average = display.currency(statistics.mean(value))
        self.labelAvgValue.set_label("%s" % (average))
