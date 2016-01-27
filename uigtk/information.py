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
import uigtk.infotip


class Information(Gtk.Grid):
    '''
    Display information statusbar with current date, unread news widget, next
    match, and button to continue on with the game.
    '''
    def __init__(self):
        Gtk.Grid.__init__(self)
        self.set_hexpand(True)
        self.set_column_spacing(5)

        self.labelDate = Gtk.Label()
        self.labelDate.set_has_tooltip(True)
        self.labelDate.connect("query-tooltip", self.on_tooltip_queried)
        self.attach(self.labelDate, 0, 0, 1, 1)

        self.buttonNews = uigtk.widgets.Button("_News Items Available")
        self.buttonNews.set_relief(Gtk.ReliefStyle.NONE)
        self.buttonNews.connect("clicked", self.on_news_clicked)
        self.attach(self.buttonNews, 1, 0, 1, 1)

        label = Gtk.Label()
        label.set_hexpand(True)
        self.attach(label, 2, 0, 1, 1)

        self.buttonNextMatch = Gtk.Button()
        self.buttonNextMatch.set_relief(Gtk.ReliefStyle.NONE)
        self.buttonNextMatch.connect("clicked", self.on_match_clicked)
        self.attach(self.buttonNextMatch, 3, 0, 1, 1)

        self.buttonContinue = uigtk.widgets.Button("_Continue Game")
        self.buttonContinue.connect("clicked", self.on_continue_clicked)
        self.attach(self.buttonContinue, 4, 0, 1, 1)

        self.infotip = uigtk.infotip.InfoTip()

        self.leagueid = None
        self.fixtureid = None

    def on_tooltip_queried(self, widget, x, y, mode, tooltip):
        '''
        Display latest overview information in tooltip.
        '''
        tooltip.set_custom(self.infotip)
        self.infotip.show()

        return True

    def on_news_clicked(self, *args):
        '''
        Change to news screen when button is clicked.
        '''
        data.window.screen.change_visible_screen("news")

    def on_match_clicked(self, *args):
        '''
        Display result screen for next match
        '''
        data.window.screen.change_visible_screen("result")
        data.window.screen.active.set_visible_result(self.leagueid, self.fixtureid)

    def on_continue_clicked(self, *args):
        '''
        Continue to next date in game, or the next scheduled match.
        '''
        data.continuegame.on_continue_game()

    def set_continue_to_match(self, *args):
        '''
        Update continue button for proceeding to match.
        '''
        self.buttonContinue.set_label("_Continue To Match")

    def set_continue_game_button(self, *args):
        '''
        Update continue button for continuing game.
        '''
        self.buttonContinue.set_label("_Continue Game")

    def set_show_next_match(self, *teams):
        '''
        Display next match button and show fixture.
        '''
        self.buttonNextMatch.set_label("%s - %s" % teams)
        self.buttonNextMatch.set_visible(True)

    def set_hide_next_match(self):
        '''
        Remove next match from view.
        '''
        self.buttonNextMatch.set_label("")
        self.buttonNextMatch.set_visible(False)

    def update_news_visible(self):
        '''
        Update whether unread news item is visible.
        '''
        club = data.clubs.get_club_by_id(data.user.team)

        visible = club.news.get_unread_count() > 0
        self.buttonNews.set_visible(visible)

    def update_date(self):
        '''
        Update date displayed to the user.
        '''
        self.labelDate.set_text(data.date.get_date_as_string())
