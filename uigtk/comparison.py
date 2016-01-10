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
import structures.comparison
import uigtk.widgets


class ComparisonDialog(Gtk.Dialog):
    def __init__(self, *args):
        Gtk.Dialog.__init__(self)
        self.set_transient_for(data.window)
        self.set_modal(True)
        self.set_resizable(False)
        self.set_title("Player Comparison")
        self.add_button("_Close", Gtk.ResponseType.CLOSE)
        self.connect("response", self.on_response)
        self.vbox.set_border_width(5)
        self.vbox.set_spacing(5)

        grid = uigtk.widgets.Grid()
        self.vbox.add(grid)

        for count, title in enumerate(("Name",
                                       "Age",
                                       "Position",
                                       "KP",
                                       "TK",
                                       "PS",
                                       "SH",
                                       "HD",
                                       "PC",
                                       "ST",
                                       "BC",
                                       "SP")):
            label = uigtk.widgets.Label("<b>%s</b>" % (title))
            grid.attach(label, count, 0, 1, 1)

        playerid1, playerid2 = data.comparison.get_comparison()

        player1 = data.players.get_player_by_id(playerid1)
        player2 = data.players.get_player_by_id(playerid2)

        label = uigtk.widgets.Label("%s" % (player1.get_name(mode=1)), leftalign=True)
        grid.attach(label, 0, 1, 1, 1)
        label = uigtk.widgets.Label("%s" % (player2.get_name(mode=1)), leftalign=True)
        grid.attach(label, 0, 2, 1, 1)

        label = uigtk.widgets.Label("%i" % (player1.get_age()))
        grid.attach(label, 1, 1, 1, 1)
        label = uigtk.widgets.Label("%i" % (player2.get_age()))
        grid.attach(label, 1, 2, 1, 1)

        label = uigtk.widgets.Label("%s" % (player1.position))
        grid.attach(label, 2, 1, 1, 1)
        label = uigtk.widgets.Label("%s" % (player2.position))
        grid.attach(label, 2, 2, 1, 1)

        skills1 = player1.get_skills()
        skills2 = player2.get_skills()

        for count in range(0, 9):
            label1 = uigtk.widgets.Label()
            label2 = uigtk.widgets.Label()

            if skills1[count] > skills2[count]:
                label1.set_markup("<b>%i</b>" % (skills1[count]))
                label2.set_markup("%i" % (skills2[count]))
            elif skills1[count] < skills2[count]:
                label1.set_markup("%i" % (skills1[count]))
                label2.set_markup("<b>%i</b>" % (skills2[count]))
            else:
                label1.set_markup("%i" % (skills1[count]))
                label2.set_markup("%i" % (skills2[count]))

            grid.attach(label1, 3 + count, 1, 1, 1)
            grid.attach(label2, 3 + count, 2, 1, 1)

        self.show_all()

    def on_response(self, dialog, response):
        self.destroy()


class ComparisonError(Gtk.MessageDialog):
    def __init__(self):
        Gtk.MessageDialog.__init__(self)
        self.set_transient_for(data.window)
        self.set_title("Player Comparison")
        self.set_property("message-type", Gtk.MessageType.ERROR)

        if data.comparison.get_comparison_count() == 0:
            message = "There are no players defined for comparison."
        elif data.comparison.get_comparison_count() == 1:
            message = "There is only one player defined for comparison. Please add another."

        self.set_markup("<span size='12000'><b>%s</b></span>" % (message))
        self.format_secondary_text("There must be two players must be added for comparison.")

        self.add_button("_Close", Gtk.ResponseType.CLOSE)
        self.connect("response", self.on_response)

        self.show()

    def on_response(self, *args):
        self.destroy()
