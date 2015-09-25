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

import constants
import dialogs
import game
import widgets


class Comparison(Gtk.Dialog):
    def __init__(self):
        self.comparison = [None, None]

        Gtk.Dialog.__init__(self)
        self.set_transient_for(game.window)
        self.set_resizable(False)
        self.set_title("Player Comparison")
        self.set_border_width(5)
        self.add_button("_Close", Gtk.ResponseType.CLOSE)

        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        grid.set_column_spacing(10)
        self.vbox.add(grid)

        for count, title in enumerate(("Name",
                                         "Age",
                                         "Position",
                                         "Keeping",
                                         "Tackling",
                                         "Passing",
                                         "Shooting",
                                         "Heading",
                                         "Pace",
                                         "Stamina",
                                         "Ball Control",
                                         "Set Pieces")):
            label = Gtk.Label("<b>%s</b>" % (title))
            label.set_use_markup(True)
            grid.attach(label, count, 0, 1, 1)

        self.labelName1 = widgets.AlignedLabel()
        grid.attach(self.labelName1, 0, 1, 1, 1)
        self.labelName2 = widgets.AlignedLabel()
        grid.attach(self.labelName2, 0, 2, 1, 1)

        self.labelAge1 = widgets.AlignedLabel()
        grid.attach(self.labelAge1, 1, 1, 1, 1)
        self.labelAge2 = widgets.AlignedLabel()
        grid.attach(self.labelAge2, 1, 2, 1, 1)

        self.labelPosition1 = widgets.AlignedLabel()
        grid.attach(self.labelPosition1, 2, 1, 1, 1)
        self.labelPosition2 = widgets.AlignedLabel()
        grid.attach(self.labelPosition2, 2, 2, 1, 1)

        self.labels = []

        for count, item in enumerate(constants.skill):
            label1 = Gtk.Label()
            label1.set_use_markup(True)
            grid.attach(label1, count + 3, 1, 1, 1)

            label2 = Gtk.Label()
            label2.set_use_markup(True)
            grid.attach(label2, count + 3, 2, 1, 1)

            self.labels.append([label1, label2])

    def display(self):
        player1 = game.players[self.comparison[0]]
        player2 = game.players[self.comparison[1]]

        self.labelName1.set_label(player1.get_name(mode=1))
        self.labelName2.set_label(player2.get_name(mode=1))

        self.labelAge1.set_label("%i" % (player1.get_age()))
        self.labelAge2.set_label("%i" % (player2.get_age()))

        self.labelPosition1.set_label(player1.position)
        self.labelPosition2.set_label(player2.position)

        skills1 = player1.get_skills()
        skills2 = player2.get_skills()

        for count in range(0, 9):
            if skills1[count] > skills2[count]:
                self.labels[count][0].set_markup("<b>%i</b>" % skills1[count])
                self.labels[count][1].set_markup("%i" % skills2[count])
            elif skills1[count] < skills2[count]:
                self.labels[count][0].set_markup("%i" % skills1[count])
                self.labels[count][1].set_markup("<b>%i</b>" % skills2[count])
            else:
                self.labels[count][0].set_markup("%i" % skills1[count])
                self.labels[count][1].set_markup("%i" % skills2[count])

        self.show_all()
        self.run()
        self.hide()
