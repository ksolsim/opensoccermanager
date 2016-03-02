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
import uigtk.widgets


class EndOfSeason(Gtk.MessageDialog):
    '''
    Message dialog to indicate end of current season.
    '''
    def __init__(self):
        Gtk.MessageDialog.__init__(self)
        self.set_transient_for(data.window)
        self.set_modal(True)
        self.set_title("End of Season")
        self.set_property("message-type", Gtk.MessageType.INFO)
        self.set_markup("The end of the season has now been reached, and the players will be on leave for three weeks, before returning to team and individual training in July. Any ongoing stadium construction work and player recovery from injury will continue. The game will now continue from the 1st August, which will signify the start of the new season.")
        self.add_button("_Continue", Gtk.ResponseType.CLOSE)

        self.run()
        self.destroy()


class Awards(Gtk.Dialog):
    '''
    Awards dialog shown at end of season displaying champions, top scorers, etc.
    '''
    class Information(uigtk.widgets.Grid):
        def __init__(self):
            uigtk.widgets.Grid.__init__(self)

            label = uigtk.widgets.Label("League Champions", leftalign=True)
            self.attach(label, 0, 0, 1, 1)
            self.labelLeagueChampion = uigtk.widgets.Label(leftalign=True)
            self.attach(self.labelLeagueChampion, 1, 0, 1, 1)

            label = uigtk.widgets.Label("Top Scorer", leftalign=True)
            self.attach(label, 0, 1, 1, 1)
            self.labelTopScorer = uigtk.widgets.Label(leftalign=True)
            self.attach(self.labelTopScorer, 1, 1, 1, 1)

            label = uigtk.widgets.Label("Top Assister", leftalign=True)
            self.attach(label, 0, 0, 1, 1)
            self.labelTopAssister = uigtk.widgets.Label(leftalign=True)
            self.attach(self.labelTopAssister, 1, 0, 1, 1)

    def __init__(self):
        Gtk.Dialog.__init__(self)
        self.set_transient_for(data.window)
        self.set_modal(True)
        self.set_default_size(400, 300)
        self.set_title("Awards")
        self.add_button("_Continue", Gtk.ResponseType.CLOSE)
        self.vbox.set_border_width(5)

        self.stack = Gtk.Stack()
        self.vbox.add(self.stack)

        stacksidebar = Gtk.StackSidebar()
        stacksidebar.set_stack(self.stack)

    def show(self):
        for leagueid, league in data.leagues.get_leagues():
            information = self.Information()
            self.stack.add_titled(information, str(league.leagueid), league.name)

        self.show_all()
        self.run()
        self.destroy()
