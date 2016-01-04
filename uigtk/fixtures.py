#!/usr/bin/env python3

from gi.repository import Gtk

import data
import uigtk.widgets


class Fixtures(uigtk.widgets.Grid):
    def __init__(self):
        uigtk.widgets.Grid.__init__(self)

        grid = uigtk.widgets.Grid()
        self.attach(grid, 0, 0, 1, 1)

        label = uigtk.widgets.Label("_League")
        grid.attach(label, 0, 0, 1, 1)
        self.comboboxLeagues = Gtk.ComboBoxText()
        self.comboboxLeagues.set_tooltip_text("Select league to show visible fixtures.")
        self.comboboxLeagues.connect("changed", self.on_league_changed)
        label.set_mnemonic_widget(self.comboboxLeagues)
        grid.attach(self.comboboxLeagues, 1, 0, 1, 1)

        label = uigtk.widgets.Label("Display", leftalign=True)
        grid.attach(label, 2, 0, 1, 1)

        self.radiobuttonAllFixtures = uigtk.widgets.RadioButton("_All Fixtures")
        self.radiobuttonAllFixtures.view = 0
        self.radiobuttonAllFixtures.set_tooltip_text("Display fixtures for all clubs.")
        self.radiobuttonAllFixtures.connect("toggled", self.on_view_toggled)
        grid.attach(self.radiobuttonAllFixtures, 3, 0, 1, 1)
        self.radiobuttonClubFixtures = uigtk.widgets.RadioButton()
        self.radiobuttonClubFixtures.join_group(self.radiobuttonAllFixtures)
        self.radiobuttonClubFixtures.view = 1
        self.radiobuttonClubFixtures.set_tooltip_text("Display only fixtures for your club.")
        self.radiobuttonClubFixtures.connect("toggled", self.on_view_toggled)
        grid.attach(self.radiobuttonClubFixtures, 4, 0, 1, 1)

        label = Gtk.Label()
        label.set_hexpand(True)
        grid.attach(label, 5, 0, 1, 1)

        buttonFriendly = uigtk.widgets.Button("Arrange _Friendly")
        buttonFriendly.set_tooltip_text("Arrange a pre-season friendly with another club.")
        buttonFriendly.connect("clicked", self.on_friendly_clicked)
        grid.attach(buttonFriendly, 6, 0, 1, 1)

        scrolledwindow = uigtk.widgets.ScrolledWindow()
        self.attach(scrolledwindow, 0, 1, 1, 1)

        self.treestore = Gtk.TreeStore(int, str, str, str, str, int)

        self.treeview = uigtk.widgets.TreeView()
        self.treeview.set_vexpand(True)
        self.treeview.set_hexpand(True)
        self.treeview.set_model(self.treestore)
        self.treeview.connect("row-activated", self.on_fixture_clicked)
        scrolledwindow.add(self.treeview)

        cellrenderertext = Gtk.CellRendererText()

        treeviewcolumn = Gtk.TreeViewColumn("Home")
        treeviewcolumn.set_expand(True)
        treeviewcolumn.pack_start(cellrenderertext, True)
        treeviewcolumn.add_attribute(cellrenderertext, "text", 1)
        treeviewcolumn.add_attribute(cellrenderertext, "weight", 5)
        self.treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Result", column=2)
        treeviewcolumn.set_fixed_width(60)
        self.treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Away", column=3)
        treeviewcolumn.set_expand(True)
        self.treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Stadium", column=4)
        treeviewcolumn.set_expand(True)
        self.treeview.append_column(treeviewcolumn)

    def on_view_toggled(self, radiobutton):
        if radiobutton.view == 0:
            self.comboboxLeagues.set_sensitive(True)
            self.treeview.set_show_expanders(True)
            self.populate_all_data()
        else:
            self.comboboxLeagues.set_sensitive(False)
            self.treeview.set_show_expanders(False)
            self.populate_club_data()

    def on_fixture_clicked(self, treeview, treepath, treeviewcolumn):
        '''
        Load result view screen for selected fixture.
        '''
        model = treeview.get_model()
        treeiter = model.get_iter(treepath)

        if not model.iter_has_child(treeiter):
            fixtureid = model[treeiter][0]
            leagueid = int(self.comboboxLeagues.get_active_id())

            data.window.screen.change_visible_screen("result")
            data.window.screen.active.set_visible_result(leagueid, fixtureid)

    def on_friendly_clicked(self, *args):
        '''
        Launch dialog to arrange a pre-season friendly.
        '''
        dialog = FriendlyDialog()

    def on_league_changed(self, *args):
        '''
        Change selection of visible league.
        '''
        self.populate_all_data()

    def populate_leagues(self):
        self.comboboxLeagues.remove_all()

        for leagueid, league in data.leagues.get_leagues():
            self.comboboxLeagues.append(str(leagueid), league.name)

        self.comboboxLeagues.set_active(0)

    def populate_all_data(self):
        if self.comboboxLeagues.get_active_id():
            self.treestore.clear()

            leagueid = int(self.comboboxLeagues.get_active_id())
            league = data.leagues.get_league_by_id(leagueid)

            round_count = league.fixtures.get_number_of_rounds()

            for week in range(0, round_count):
                title = "Round %i" % (week + 1)
                parent = self.treestore.append(None, [None, title, "", "", "", 700])

                fixtures = league.fixtures.get_fixtures_for_week(week)

                for fixtureid, fixture in fixtures.items():
                    home = data.clubs.get_club_by_id(fixture.home)
                    away = data.clubs.get_club_by_id(fixture.away)
                    stadium = data.stadiums.get_stadium_by_id(home.stadium)

                    self.treestore.append(parent, [fixtureid, home.name, "", away.name, stadium.name, 400])

        self.treeview.expand_all()

    def populate_club_data(self):
        self.treestore.clear()

        club = data.clubs.get_club_by_id(data.user.team)
        league = data.leagues.get_league_by_id(club.league)

        round_count = league.fixtures.get_number_of_rounds()

        for week in range(0, round_count):
            fixtures = league.fixtures.get_fixtures_for_week(week)

            for fixtureid, fixture in fixtures.items():
                if data.user.team in (fixture.home, fixture.away):
                    home = data.clubs.get_club_by_id(fixture.home)
                    away = data.clubs.get_club_by_id(fixture.away)
                    stadium = data.stadiums.get_stadium_by_id(home.stadium)

                    self.treestore.append(None, [fixtureid, home.name, "", away.name, stadium.name, 400])

    def run(self):
        self.populate_leagues()
        self.populate_all_data()

        self.radiobuttonAllFixtures.set_active(True)

        club = data.clubs.get_club_by_id(data.user.team)
        self.radiobuttonClubFixtures.set_label("%s _Fixtures" % (club.name))

        self.show_all()


class FriendlyDialog(Gtk.Dialog):
    '''
    Dialog displayed when arranging a friendly match.
    '''
    def __init__(self):
        Gtk.Dialog.__init__(self)
        self.set_transient_for(data.window)
        self.set_title("Arrange Friendly")
        self.set_resizable(False)
        self.set_modal(True)
        self.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("_Arrange", Gtk.ResponseType.OK)
        self.set_default_response(Gtk.ResponseType.CANCEL)
        self.connect("response", self.on_response)
        self.vbox.set_border_width(5)

        grid = uigtk.widgets.Grid()
        self.vbox.add(grid)

        self.liststoreLeagues = Gtk.ListStore(str, str)
        self.treemodelsort = Gtk.TreeModelSort(self.liststoreLeagues)
        self.treemodelsort.set_sort_column_id(1, Gtk.SortType.ASCENDING)

        label = uigtk.widgets.Label("_League", leftalign=True)
        grid.attach(label, 0, 0, 1, 1)
        self.comboboxLeague = uigtk.widgets.ComboBox(column=1)
        self.comboboxLeague.set_model(self.treemodelsort)
        self.comboboxLeague.set_id_column(0)
        self.comboboxLeague.set_tooltip_text("Choose league of opposition team for friendly.")
        self.comboboxLeague.connect("changed", self.on_league_changed)
        label.set_mnemonic_widget(self.comboboxLeague)
        grid.attach(self.comboboxLeague, 1, 0, 1, 1)

        self.liststoreClubs = Gtk.ListStore(str, str)
        self.treemodelsort = Gtk.TreeModelSort(self.liststoreClubs)
        self.treemodelsort.set_sort_column_id(1, Gtk.SortType.ASCENDING)

        label = uigtk.widgets.Label("_Opposition", leftalign=True)
        grid.attach(label, 0, 1, 1, 1)
        self.comboboxOpposition = uigtk.widgets.ComboBox(column=1)
        self.comboboxOpposition.set_model(self.treemodelsort)
        self.comboboxOpposition.set_id_column(0)
        self.comboboxOpposition.set_tooltip_text("Choose opposition to compete in friendly match.")
        label.set_mnemonic_widget(self.comboboxOpposition)
        grid.attach(self.comboboxOpposition, 1, 1, 1, 1)

        self.populate_leagues()

        self.show_all()

        self.comboboxLeague.set_active(0)

    def on_league_changed(self, combobox):
        '''
        Repopulate clubs list when league selection is changed.
        '''
        if combobox.get_active_id():
            self.populate_clubs()

    def populate_leagues(self):
        self.liststoreLeagues.clear()

        for leagueid, league in data.leagues.get_leagues():
            self.liststoreLeagues.append([str(leagueid), league.name])

    def populate_clubs(self):
        self.liststoreClubs.clear()

        for leagueid, league in data.leagues.get_leagues():
            for clubid in league.get_clubs():
                if leagueid == int(self.comboboxLeague.get_active_id()):
                    if clubid != data.user.team:
                        club = data.clubs.get_club_by_id(clubid)
                        self.liststoreClubs.append([str(clubid), club.name])

        self.comboboxOpposition.set_active(0)

    def on_response(self, dialog, response):
        self.destroy()
