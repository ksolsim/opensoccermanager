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
import random

import constants
import user
import widgets


class TeamTraining(Gtk.Grid):
    __name__ = "teamtraining"

    def __init__(self):
        Gtk.Grid.__init__(self)
        self.set_row_spacing(5)
        self.set_column_spacing(5)

        label = Gtk.Label("09:00 - 10:00")
        label.set_hexpand(True)
        self.attach(label, 1, 0, 1, 1)
        label = Gtk.Label("10:00 - 11:00")
        label.set_hexpand(True)
        self.attach(label, 2, 0, 1, 1)
        label = Gtk.Label("11:00 - 12:00")
        label.set_hexpand(True)
        self.attach(label, 3, 0, 1, 1)
        label = Gtk.Label("12:00 - 13:00")
        label.set_hexpand(True)
        self.attach(label, 4, 0, 1, 1)
        label = Gtk.Label("13:00 - 14:00")
        label.set_hexpand(True)
        self.attach(label, 5, 0, 1, 1)
        label = Gtk.Label("14:00 - 15:00")
        label.set_hexpand(True)
        self.attach(label, 6, 0, 1, 1)

        label = widgets.AlignedLabel("Monday")
        self.attach(label, 0, 1, 1, 1)
        label = widgets.AlignedLabel("Tuesday")
        self.attach(label, 0, 2, 1, 1)
        label = widgets.AlignedLabel("Wednesday")
        self.attach(label, 0, 3, 1, 1)
        label = widgets.AlignedLabel("Thursday")
        self.attach(label, 0, 4, 1, 1)
        label = widgets.AlignedLabel("Friday")
        self.attach(label, 0, 5, 1, 1)
        label = widgets.AlignedLabel("Saturday")
        self.attach(label, 0, 6, 1, 1)
        label = widgets.AlignedLabel("Sunday")
        self.attach(label, 0, 7, 1, 1)

        liststoreTraining = Gtk.ListStore(str)
        liststoreTraining.append([constants.team_training[0]])
        liststoreTraining.append([constants.team_training[1]])

        for item in sorted(constants.team_training[2]):
            liststoreTraining.append([item])

        self.comboboxes = []
        count = 0

        for row in range(1, 8):
            for column in range(1, 7):
                combobox = Gtk.ComboBoxText()
                combobox.set_model(liststoreTraining)
                combobox.connect("changed", self.training_changed, count)
                self.attach(combobox, column, row, 1, 1)
                self.comboboxes.append(combobox)

                count += 1

        buttonbox = Gtk.ButtonBox()
        buttonbox.set_layout(Gtk.ButtonBoxStyle.START)
        buttonbox.set_spacing(5)
        self.attach(buttonbox, 0, 8, 7, 1)

        buttonAssistant = widgets.Button("_Assistant Generated")
        buttonAssistant.set_tooltip_text("Assistant Manager will generate a training schedule.")
        buttonAssistant.connect("clicked", self.assistant_generated)
        buttonbox.add(buttonAssistant)

    def assistant_generated(self, button):
        '''
        Clear existing session and randomly generate new schedule.
        '''
        for item in self.comboboxes:
            item.set_active(0)

        club = user.get_user_club()
        club.team_training.generate_schedule()

        self.populate_data()

    def training_changed(self, combobox, index):
        club = user.get_user_club()

        club.team_training.training[index] = combobox.get_active()
        club.team_training.timeout = random.randint(16, 24)

    def populate_data(self):
        count = 0

        for row in range(1, 8):
            for column in range(1, 7):
                club = user.get_user_club()

                value = club.team_training.training[count]
                self.comboboxes[count].set_active(value)

                count += 1

    def run(self):
        self.populate_data()

        self.show_all()
