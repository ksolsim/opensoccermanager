#!/usr/bin/env python3

from gi.repository import Gtk

import data
import uigtk.widgets


class Result(uigtk.widgets.Grid):
    '''
    Screen displaying match results, statistics, and data.
    '''
    __name__ = "result"

    def __init__(self):
        uigtk.widgets.Grid.__init__(self)

        grid = uigtk.widgets.Grid()
        grid.set_hexpand(True)
        grid.set_column_homogeneous(True)
        self.attach(grid, 0, 0, 1, 1)

        self.labelHome = uigtk.widgets.Label()
        self.labelHome.connect("activate-link", self.on_label_activated)
        grid.attach(self.labelHome, 0, 0, 1, 1)
        self.labelResult = uigtk.widgets.Label()
        grid.attach(self.labelResult, 1, 0, 1, 1)
        self.labelAway = uigtk.widgets.Label()
        self.labelAway.connect("activate-link", self.on_label_activated)
        grid.attach(self.labelAway, 2, 0, 1, 1)

    def set_visible_result(self, leagueid, fixtureid):
        '''
        Display result information for given fixture id in passed league.
        '''
        league = data.leagues.get_league_by_id(leagueid)
        fixture = league.fixtures.get_fixture_for_id(fixtureid)

        home = data.clubs.get_club_by_id(fixture.home)
        away = data.clubs.get_club_by_id(fixture.away)

        self.labelHome.set_markup("<a href='club'><span size='24000'><b>%s</b></span></a>" % (home.name))
        self.labelAway.set_markup("<a href='club'><span size='24000'><b>%s</b></span></a>" % (away.name))
        #self.labelResult.set_markup("%i - %i" % (result))

    def on_label_activated(self, *args):
        return True

    def run(self):
        self.show_all()
