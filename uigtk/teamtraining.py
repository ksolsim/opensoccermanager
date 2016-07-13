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
import structures.training
import uigtk.widgets


class TeamTraining(uigtk.widgets.Grid):
    __name__ = "teamtraining"

    def __init__(self):
        uigtk.widgets.Grid.__init__(self)

        frame = uigtk.widgets.CommonFrame("Training Schedule")
        self.attach(frame, 0, 0, 1, 1)

        grid = uigtk.widgets.Grid()
        grid.set_hexpand(True)
        frame.grid.attach(grid, 0, 0, 1, 1)

        hours = ("09:00-10:00", "10:00-11:00", "11:00-12:00", "12:00-13:00", "13:00-14:00", "14:00-15:00")

        for count, hour in enumerate(hours, start=1):
            label = uigtk.widgets.Label("%s" % (hour))
            grid.attach(label, count, 0, 1, 1)

        self.comboboxes = []
        count = 0

        days = data.calendar.get_days()
        training = structures.training.Training()

        for day in range(0, 7):
            label = uigtk.widgets.Label("_%s" % (days[day]), leftalign=True)
            grid.attach(label, 0, day + 1, 1, 1)

            mnemonic = True

            for hour in range(0, 6):
                combobox = Gtk.ComboBoxText()

                if mnemonic:
                    label.set_mnemonic_widget(combobox)
                    mnemonic = False

                combobox.append("0", "No Training")
                combobox.append("1", "Individual")

                for categoryid, category in enumerate(training.get_training(),
                                                      start=2):
                    combobox.append(str(categoryid), category)

                combobox.set_hexpand(True)
                combobox.value = count
                connectid = combobox.connect("changed", self.on_combobox_changed)
                combobox.connectid = connectid

                grid.attach(combobox, hour + 1, day + 1, 1, 1)
                self.comboboxes.append(combobox)

                count += 1

        grid = uigtk.widgets.Grid()
        frame.grid.attach(grid, 0, 1, 1, 1)

        buttonbox = uigtk.widgets.ButtonBox()
        buttonbox.set_layout(Gtk.ButtonBoxStyle.START)
        grid.attach(buttonbox, 0, 0, 1, 1)

        buttonAssistant = uigtk.widgets.Button("_Assistant")
        buttonAssistant.set_tooltip_text("Have assistant manager generate a training schedule.")
        buttonAssistant.connect("clicked", self.on_assistant_clicked)
        buttonbox.add(buttonAssistant)

        self.boxAccept = Gtk.Box()
        self.boxAccept.set_spacing(5)
        grid.attach(self.boxAccept, 1, 0, 1, 1)

        label = uigtk.widgets.Label("Do you wish to apply the generated schedule?", leftalign=True)
        self.boxAccept.add(label)

        buttonbox = uigtk.widgets.ButtonBox()
        self.boxAccept.add(buttonbox)

        self.buttonAccept = uigtk.widgets.Button("_Accept")
        self.buttonAccept.connect("clicked", self.on_accept_schedule)
        buttonbox.add(self.buttonAccept)
        self.buttonReject = uigtk.widgets.Button("_Reject")
        self.buttonReject.connect("clicked", self.on_reject_schedule)
        buttonbox.add(self.buttonReject)

        percentages = Percentages()
        self.attach(percentages, 0, 1, 1, 1)

    def on_combobox_changed(self, combobox):
        '''
        Update schedule with selected categories.
        '''
        data.user.club.team_training.set_training(combobox.value, int(combobox.get_active_id()))

    def on_assistant_clicked(self, *args):
        '''
        Generate random training session and display.
        '''
        self.boxAccept.show_all()

        self.populate_generated()

    def on_accept_schedule(self, *args):
        '''
        Accept randomly generated schedule and save.
        '''
        self.boxAccept.hide()

        data.user.club.team_training.set_random_schedule()

        self.populate_data()

    def on_reject_schedule(self, *args):
        '''
        Reject randomly generated schedule and revert to previous.
        '''
        self.boxAccept.hide()

        self.populate_data()

    def populate_data(self):
        '''
        Populate team training schedule in use.
        '''
        for count, trainingid in enumerate(data.user.club.team_training.get_training()):
            self.comboboxes[count].set_active(trainingid)

    def populate_generated(self):
        '''
        Populate generated team training schedule.
        '''
        for count, trainingid in enumerate(data.user.club.team_training.get_random_schedule()):
            self.comboboxes[count].handler_block(self.comboboxes[count].connectid)
            self.comboboxes[count].set_active(trainingid)
            self.comboboxes[count].handler_unblock(self.comboboxes[count].connectid)

    def run(self):
        self.populate_data()
        self.show_all()
        self.boxAccept.hide()


class Percentages(uigtk.widgets.CommonFrame):
    def __init__(self):
        uigtk.widgets.CommonFrame.__init__(self, "Training Percentages")
