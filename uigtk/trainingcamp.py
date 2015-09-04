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
import dialogs
import display
import events
import game
import individualtraining
import money
import teamtraining
import trainingcamp
import user
import widgets


class TrainingCamp(Gtk.Grid):
    __name__ = "trainingcamp"

    def __init__(self):
        self.training_camp = trainingcamp.TrainingCamp()
        self.defaults = []

        Gtk.Grid.__init__(self)
        self.set_row_spacing(5)
        self.set_column_spacing(5)

        label = widgets.AlignedLabel("Days")
        self.attach(label, 0, 0, 1, 1)
        comboboxDays = Gtk.ComboBoxText()
        comboboxDays.append("1", "1 Day")
        comboboxDays.append("2", "2 Days")
        comboboxDays.append("3", "3 Days")
        comboboxDays.append("4", "4 Days")
        comboboxDays.append("5", "5 Days")
        comboboxDays.set_active(0)
        comboboxDays.connect("changed", self.update_days)
        self.attach(comboboxDays, 1, 0, 1, 1)

        label = widgets.AlignedLabel("Quality")
        self.attach(label, 0, 1, 1, 1)
        radiobuttonAverage = Gtk.RadioButton("Average")
        radiobuttonAverage.connect("toggled", self.update_quality, 1)
        self.attach(radiobuttonAverage, 1, 1, 1, 1)
        radiobuttonGood = Gtk.RadioButton("Good", group=radiobuttonAverage)
        radiobuttonGood.connect("toggled", self.update_quality, 2)
        self.attach(radiobuttonGood, 2, 1, 1, 1)
        radiobuttonSuperb = Gtk.RadioButton("Superb", group=radiobuttonAverage)
        radiobuttonSuperb.connect("toggled", self.update_quality, 3)
        self.attach(radiobuttonSuperb, 3, 1, 1, 1)

        label = widgets.AlignedLabel("Location")
        self.attach(label, 0, 2, 1, 1)
        radiobuttonHome = Gtk.RadioButton("Home")
        radiobuttonHome.connect("toggled", self.update_location, 0)
        self.attach(radiobuttonHome, 1, 2, 1, 1)
        radiobuttonAbroad = Gtk.RadioButton("Abroad", group=radiobuttonHome)
        radiobuttonAbroad.connect("toggled", self.update_location, 1)
        self.attach(radiobuttonAbroad, 2, 2, 1, 1)

        label = widgets.AlignedLabel("Purpose")
        self.attach(label, 0, 3, 1, 1)
        radiobuttonLeisure = Gtk.RadioButton("Leisure")
        radiobuttonLeisure.connect("toggled", self.update_purpose, 1)
        self.attach(radiobuttonLeisure, 1, 3, 1, 1)
        self.radiobuttonSchedule = Gtk.RadioButton("Schedule", group=radiobuttonLeisure)
        self.radiobuttonSchedule.connect("toggled", self.update_purpose, 2)
        self.attach(self.radiobuttonSchedule, 2, 3, 1, 1)
        radiobuttonIntensive = Gtk.RadioButton("Intensive", group=radiobuttonLeisure)
        radiobuttonIntensive.connect("toggled", self.update_purpose, 3)
        self.attach(radiobuttonIntensive, 3, 3, 1, 1)
        self.buttonScheduleWarning = widgets.Button()
        image = Gtk.Image()
        image.set_from_icon_name("gtk-dialog-warning", Gtk.IconSize.BUTTON)
        self.buttonScheduleWarning.set_image(image)
        self.buttonScheduleWarning.set_relief(Gtk.ReliefStyle.NONE)
        self.buttonScheduleWarning.connect("clicked", lambda q: dialogs.error(12))
        image.show()
        self.attach(self.buttonScheduleWarning, 4, 3, 1, 1)

        label = widgets.AlignedLabel("Squad")
        self.attach(label, 0, 4, 1, 1)
        radiobuttonFirstTeam = Gtk.RadioButton("First Team")
        radiobuttonFirstTeam.connect("toggled", self.update_squad, 0)
        self.attach(radiobuttonFirstTeam, 1, 4, 1, 1)
        radiobuttonReserves = Gtk.RadioButton("Reserves", group=radiobuttonFirstTeam)
        radiobuttonReserves.connect("toggled", self.update_squad, 1)
        self.attach(radiobuttonReserves, 2, 4, 1, 1)
        radiobuttonAll = Gtk.RadioButton("All Players", group=radiobuttonFirstTeam)
        radiobuttonAll.connect("toggled", self.update_squad, 2)
        self.attach(radiobuttonAll, 3, 4, 1, 1)
        self.buttonSquadWarning = widgets.Button()
        image = Gtk.Image()
        image.set_from_icon_name("gtk-dialog-warning", Gtk.IconSize.BUTTON)
        self.buttonSquadWarning.set_image(image)
        self.buttonSquadWarning.set_relief(Gtk.ReliefStyle.NONE)
        self.buttonSquadWarning.connect("clicked", lambda a: dialogs.error(13))
        image.show()
        self.attach(self.buttonSquadWarning, 4, 4, 1, 1)

        separator = Gtk.Separator()
        self.attach(separator, 0, 5, 4, 1)

        label = widgets.AlignedLabel("Cost Per Player")
        self.attach(label, 0, 6, 1, 1)
        self.labelPlayerCost = widgets.AlignedLabel()
        self.attach(self.labelPlayerCost, 1, 6, 1, 1)
        label = widgets.AlignedLabel("Total")
        self.attach(label, 0, 7, 1, 1)
        self.labelTotal = widgets.AlignedLabel()
        self.attach(self.labelTotal, 1, 7, 1, 1)

        buttonbox = Gtk.ButtonBox()
        buttonbox.set_spacing(5)
        buttonbox.set_layout(Gtk.ButtonBoxStyle.END)
        self.attach(buttonbox, 0, 8, 4, 1)
        buttonRevert = widgets.Button("_Revert")
        buttonRevert.connect("clicked", self.revert_training)
        buttonbox.add(buttonRevert)
        buttonConfirm = widgets.Button("_Confirm")
        buttonConfirm.connect("clicked", self.confirm_training)
        buttonbox.add(buttonConfirm)

        self.defaults.append(comboboxDays)
        self.defaults.append(radiobuttonAverage)
        self.defaults.append(radiobuttonHome)
        self.defaults.append(radiobuttonLeisure)
        self.defaults.append(radiobuttonFirstTeam)

    def update_days(self, combobox):
        index = int(combobox.get_active_id())
        self.training_camp.days = index

        self.update_total()

    def update_quality(self, radiobutton, index):
        if radiobutton.get_active():
            self.training_camp.quality = index

            self.update_total()

    def update_location(self, radiobutton, index):
        if radiobutton.get_active():
            self.training_camp.location = index

            self.update_total()

    def update_purpose(self, radiobutton, index):
        if radiobutton.get_active():
            self.training_camp.purpose = index

            self.training_schedule_warning()

            self.update_total()

    def update_squad(self, radiobutton, index):
        if radiobutton.get_active():
            if index == 0:
                self.squad_count_warning()
            elif index == 1:
                players = 0

                for item in game.clubs[game.teamid].squad:
                    if item not in game.clubs[game.teamid].team.values():
                        players += 1

                self.buttonSquadWarning.hide()
            elif index == 2:
                players = len(game.clubs[game.teamid].squad)
                self.buttonSquadWarning.hide()

            self.training_camp.squad = index

            self.update_total()

    def update_total(self):
        player = self.training_camp.get_player_total()
        player = display.currency(player)
        self.labelPlayerCost.set_label("%s" % (player))

        total = self.training_camp.get_total()
        total = display.currency(total)
        self.labelTotal.set_label("<b>%s</b>" % (total))

    def revert_training(self, button=None):
        self.training_camp.revert_options()

        self.defaults[0].set_active(0)

        for item in self.defaults[1:5]:
            item.set_active(True)

        self.update_total()

    def confirm_training(self, button):
        cost = self.training_camp.get_total()

        if dialogs.confirm_training(cost):
            if game.clubs[game.teamid].accounts.request(cost):
                game.clubs[game.teamid].accounts.withdraw(cost, "training")

                self.training_camp.apply_training()

            self.revert_training()

    def squad_count_warning(self):
        '''
        Display warning if number of players in team is less than 16.
        '''
        count = 0

        for item in game.clubs[game.teamid].team.values():
            if item != 0:
                count += 1

        visible = count < 16
        self.buttonSquadWarning.set_visible(visible)

    def training_schedule_warning(self):
        '''
        Display warning if there is no team training schedule assigned.
        '''
        if self.radiobuttonSchedule.get_active():
            if teamtraining.get_schedule_set():
                self.buttonScheduleWarning.show()
            else:
                self.buttonScheduleWarning.hide()
        else:
            self.buttonScheduleWarning.hide()

    def run(self):
        self.update_total()

        self.show_all()

        self.squad_count_warning()
        self.training_schedule_warning()
