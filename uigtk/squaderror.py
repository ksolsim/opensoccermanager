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
import uigtk.widgets

import data


class SquadError(Gtk.Dialog):
    def __init__(self):
        Gtk.Dialog.__init__(self)
        self.set_transient_for(data.window)
        self.set_border_width(5)
        self.set_title("Squad Errors")
        self.add_button("_Close", Gtk.ResponseType.CLOSE)
        self.vbox.set_spacing(5)

        label = uigtk.widgets.Label("The players listed below are unavailable to play in the next match.")
        self.vbox.add(label)

        self.frameInjuries = uigtk.widgets.CommonFrame("Injuries")
        self.vbox.add(self.frameInjuries)

        label = uigtk.widgets.Label("<b>Player</b>")
        self.frameInjuries.grid.attach(label, 0, 0, 1, 1)
        label = uigtk.widgets.Label("<b>Injury</b>")
        self.frameInjuries.grid.attach(label, 1, 0, 1, 1)
        label = uigtk.widgets.Label("<b>Period</b>")
        self.frameInjuries.grid.attach(label, 2, 0, 1, 1)

        self.frameSuspensions = uigtk.widgets.CommonFrame("Suspensions")
        self.vbox.add(self.frameSuspensions)

        label = uigtk.widgets.Label("<b>Player</b>")
        self.frameSuspensions.grid.attach(label, 0, 0, 1, 1)
        label = uigtk.widgets.Label("<b>Suspension</b>")
        self.frameSuspensions.grid.attach(label, 1, 0, 1, 1)

    def show(self):
        self.show_all()

        if len(data.user.club.squad.get_injured_players()) > 0:
            for count, player in enumerate(data.user.club.squad.teamselection.get_injured_players(), start=1):
                label = uigtk.widgets.Label(player.get_name(mode=1), leftalign=True)
                self.frameInjuries.grid.attach(label, 0, count, 1, 1)

                label = uigtk.widgets.Label(player.injury.get_injury_name())
                self.frameInjuries.grid.attach(label, 1, count, 1, 1)

                label = uigtk.widgets.Label(player.injury.get_injury_period())
                self.frameInjuries.grid.attach(label, 2, count, 1, 1)

            self.frameInjuries.show_all()
        else:
            self.frameInjuries.hide()

        if len(data.user.club.squad.get_suspended_players()) > 0:
            for count, player in enumerate(data.user.club.squad.teamselection.get_suspended_players(), start=1):
                label = uigtk.widgets.Label(player.get_name(mode=1), leftalign=True)
                self.frameSuspensions.grid.attach(label, 0, count, 1, 1)

                label = uigtk.widgets.Label(player.injury.get_suspension_name())
                self.frameSuspensions.grid.attach(label, 1, count, 1, 1)

            self.frameSuspensions.show_all()
        else:
            self.frameSuspensions.hide()

        self.run()
        self.destroy()
