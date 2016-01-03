#!/usr/bin/env python3

from gi.repository import Gtk

import data
import structures.training
import uigtk.widgets


class TeamTraining(Gtk.Grid):
    def __init__(self):
        Gtk.Grid.__init__(self)
        self.set_row_spacing(5)

        grid = uigtk.widgets.Grid()
        grid.set_hexpand(True)
        self.attach(grid, 0, 0, 1, 1)

        hours = ("09:00-10:00", "10:00-11:00", "11:00-12:00", "12:00-13:00", "13:00-14:00", "14:00-15:00")

        for count, hour in enumerate(hours, start=1):
            label = uigtk.widgets.Label("%s" % (hour))
            grid.attach(label, count, 0, 1, 1)

        days = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")

        for count, day in enumerate(days, start=1):
            label = uigtk.widgets.Label("%s" % (day), leftalign=True)
            grid.attach(label, 0, count, 1, 1)

        self.comboboxes = []
        count = 0

        training = structures.training.Training()

        for day in range(0, 7):
            for hour in range(0, 6):
                combobox = Gtk.ComboBoxText()
                combobox.set_hexpand(True)

                combobox.append("0", "No Training")
                combobox.append("1", "Individual")

                for categoryid, category in enumerate(training.get_training(),
                                                      start=2):
                    combobox.append(str(categoryid), category)

                combobox.value = count
                combobox.connect("changed", self.on_combobox_changed)

                grid.attach(combobox, hour + 1, day + 1, 1, 1)
                self.comboboxes.append(combobox)

                count += 1

        buttonbox = uigtk.widgets.ButtonBox()
        buttonbox.set_layout(Gtk.ButtonBoxStyle.START)
        self.attach(buttonbox, 0, 1, 1, 1)

        buttonAssistant = uigtk.widgets.Button("Assistant")
        buttonAssistant.set_tooltip_text("Have assistant manager generate a training schedule.")
        buttonAssistant.connect("clicked", self.on_assistant_clicked)
        buttonbox.add(buttonAssistant)

    def on_combobox_changed(self, combobox):
        '''
        Update schedule with selected categories.
        '''
        self.club.team_training[combobox.value] = int(combobox.get_active_id())

    def on_assistant_clicked(self, *args):
        '''
        Generate random training session and display.
        '''
        self.club.team_training.get_random_schedule()

        self.populate_data()

    def populate_data(self):
        for count, trainingid in enumerate(self.club.team_training):
            self.comboboxes[count].set_active(trainingid)

    def run(self):
        self.club = data.clubs.get_club_by_id(data.user.team)

        self.populate_data()
        self.show_all()
