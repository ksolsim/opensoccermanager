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
import structures.trainingcamp
import uigtk.widgets


class TrainingCamp(uigtk.widgets.Grid):
    __name__ = "trainingcamp"

    def __init__(self):
        uigtk.widgets.Grid.__init__(self)

        frame = uigtk.widgets.CommonFrame("Details")
        frame.grid.set_row_homogeneous(True)
        self.attach(frame, 0, 0, 1, 1)

        label = uigtk.widgets.Label("_Days", leftalign=True)
        frame.grid.attach(label, 0, 0, 1, 1)
        comboboxDays = Gtk.ComboBoxText()
        comboboxDays.append("1", "1 Day")
        comboboxDays.append("2", "2 Days")
        comboboxDays.append("3", "3 Days")
        comboboxDays.append("4", "4 Days")
        comboboxDays.append("5", "5 Days")
        comboboxDays.set_active(0)
        comboboxDays.set_tooltip_text("Number of days to run training camp.")
        comboboxDays.connect("changed", self.on_days_changed)
        label.set_mnemonic_widget(comboboxDays)
        frame.grid.attach(comboboxDays, 1, 0, 1, 1)

        label = uigtk.widgets.Label("Quality", leftalign=True)
        frame.grid.attach(label, 0, 1, 1, 1)
        radiobuttonAverage = uigtk.widgets.RadioButton("_Average")
        radiobuttonAverage.quality = 0
        radiobuttonAverage.connect("toggled", self.on_quality_toggled)
        label.set_mnemonic_widget(radiobuttonAverage)
        frame.grid.attach(radiobuttonAverage, 1, 1, 1, 1)
        radiobuttonGood = uigtk.widgets.RadioButton("_Good")
        radiobuttonGood.quality = 1
        radiobuttonGood.join_group(radiobuttonAverage)
        radiobuttonGood.connect("toggled", self.on_quality_toggled)
        frame.grid.attach(radiobuttonGood, 2, 1, 1, 1)
        radiobuttonSuperb = uigtk.widgets.RadioButton("_Superb")
        radiobuttonSuperb.quality = 2
        radiobuttonSuperb.join_group(radiobuttonAverage)
        radiobuttonSuperb.connect("toggled", self.on_quality_toggled)
        frame.grid.attach(radiobuttonSuperb, 3, 1, 1, 1)

        label = uigtk.widgets.Label("Location", leftalign=True)
        frame.grid.attach(label, 0, 2, 1, 1)
        radiobuttonHome = uigtk.widgets.RadioButton("_Home")
        radiobuttonHome.location = 0
        radiobuttonHome.connect("toggled", self.on_location_toggled)
        frame.grid.attach(radiobuttonHome, 1, 2, 1, 1)
        radiobuttonAbroad = uigtk.widgets.RadioButton("_Abroad")
        radiobuttonAbroad.location = 1
        radiobuttonAbroad.join_group(radiobuttonHome)
        radiobuttonAbroad.connect("toggled", self.on_location_toggled)
        frame.grid.attach(radiobuttonAbroad, 2, 2, 1, 1)

        label = uigtk.widgets.Label("Purpose", leftalign=True)
        frame.grid.attach(label, 0, 3, 1, 1)
        radiobuttonLeisure = uigtk.widgets.RadioButton("_Leisure")
        radiobuttonLeisure.purpose = 0
        radiobuttonLeisure.connect("toggled", self.on_purpose_toggled)
        frame.grid.attach(radiobuttonLeisure, 1, 3, 1, 1)
        radiobuttonSchedule = uigtk.widgets.RadioButton("_Schedule")
        radiobuttonSchedule.purpose = 1
        radiobuttonSchedule.join_group(radiobuttonLeisure)
        radiobuttonSchedule.connect("toggled", self.on_purpose_toggled)
        frame.grid.attach(radiobuttonSchedule, 2, 3, 1, 1)
        radiobuttonIntense = uigtk.widgets.RadioButton("_Intense")
        radiobuttonIntense.purpose = 2
        radiobuttonIntense.join_group(radiobuttonLeisure)
        radiobuttonIntense.connect("toggled", self.on_purpose_toggled)
        frame.grid.attach(radiobuttonIntense, 3, 3, 1, 1)

        label = uigtk.widgets.Label("Team", leftalign=True)
        frame.grid.attach(label, 0, 4, 1, 1)
        radiobuttonAllPlayers = uigtk.widgets.RadioButton("_All Players")
        radiobuttonAllPlayers.squad = 0
        radiobuttonAllPlayers.connect("toggled", self.on_team_toggled)
        frame.grid.attach(radiobuttonAllPlayers, 1, 4, 1, 1)
        radiobuttonFirstTeam = uigtk.widgets.RadioButton("_First Team Only")
        radiobuttonFirstTeam.squad = 1
        radiobuttonFirstTeam.join_group(radiobuttonAllPlayers)
        radiobuttonFirstTeam.connect("toggled", self.on_team_toggled)
        frame.grid.attach(radiobuttonFirstTeam, 2, 4, 1, 1)
        radiobuttonReserves = uigtk.widgets.RadioButton("_Reserves Only")
        radiobuttonReserves.squad = 2
        radiobuttonReserves.join_group(radiobuttonAllPlayers)
        radiobuttonReserves.connect("toggled", self.on_team_toggled)
        frame.grid.attach(radiobuttonReserves, 3, 4, 1, 1)

        frame = uigtk.widgets.CommonFrame("Cost")
        self.attach(frame, 0, 1, 1, 1)

        label = uigtk.widgets.Label("Player Cost", leftalign=True)
        frame.grid.attach(label, 0, 0, 1, 1)
        self.labelPlayerCost = uigtk.widgets.Label(leftalign=True)
        frame.grid.attach(self.labelPlayerCost, 1, 0, 1, 1)

        label = uigtk.widgets.Label("Total Cost", leftalign=True)
        frame.grid.attach(label, 0, 1, 1, 1)
        self.labelTotalCost = uigtk.widgets.Label(leftalign=True)
        frame.grid.attach(self.labelTotalCost, 1, 1, 1, 1)

        buttonbox = uigtk.widgets.ButtonBox()
        buttonbox.set_layout(Gtk.ButtonBoxStyle.END)
        self.attach(buttonbox, 0, 2, 1, 1)

        buttonReset = uigtk.widgets.Button("_Reset")
        buttonReset.set_tooltip_text("Reset training camp options to default.")
        buttonbox.add(buttonReset)
        buttonArrange = uigtk.widgets.Button("_Arrange")
        buttonArrange.set_tooltip_text("Arrange training camp with set options.")
        buttonArrange.connect("clicked", self.on_arrange_clicked)
        buttonbox.add(buttonArrange)

    def on_days_changed(self, combobox):
        '''
        Update cost when days value is changed.
        '''
        self.club.training_camp.options.days = int(combobox.get_active_id())
        self.update_cost()

    def on_quality_toggled(self, radiobutton):
        '''
        Update cost when quality of camp is changed.
        '''
        if radiobutton.get_active():
            self.club.training_camp.options.quality = radiobutton.quality
            self.update_cost()

    def on_location_toggled(self, radiobutton):
        '''
        Update cost when location is changed.
        '''
        if radiobutton.get_active():
            self.club.training_camp.options.location = radiobutton.location
            self.update_cost()

    def on_purpose_toggled(self, radiobutton):
        '''
        Update cost when purpose of training is changed.
        '''
        if radiobutton.get_active():
            self.club.training_camp.options.purpose = radiobutton.purpose
            self.update_cost()

    def on_team_toggled(self, radiobutton):
        '''
        Update cost when team members attending is changed.
        '''
        if radiobutton.get_active():
            self.club.training_camp.options.squad = radiobutton.squad
            self.update_cost()

    def update_cost(self):
        '''
        Update costing labels.
        '''
        cost = self.club.training_camp.get_player_cost()
        self.labelPlayerCost.set_label("%i" % (cost))

        cost = self.club.training_camp.get_total_cost()
        self.labelTotalCost.set_label("%i" % (cost))

    def on_reset_clicked(self, *args):
        '''
        Reset training camp settings to default.
        '''

    def on_arrange_clicked(self, *args):
        '''
        Setup training camp with selected details.
        '''
        cost = self.club.training_camp.get_total_cost()
        dialog = ConfirmTraining(cost)

        if dialog.show():
            self.club.training_camp.apply_options()

    def run(self):
        self.club = data.clubs.get_club_by_id(data.user.team)

        self.show_all()


class ConfirmTraining(Gtk.MessageDialog):
    def __init__(self, cost):
        cost = data.currency.get_currency(cost, integer=True)

        Gtk.MessageDialog.__init__(self)
        self.set_transient_for(data.window)
        self.set_modal(True)
        self.set_title("Confirm Training")
        self.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("C_onfirm", Gtk.ResponseType.OK)
        self.set_default_response(Gtk.ResponseType.CANCEL)
        self.set_property("message-type", Gtk.MessageType.QUESTION)
        self.set_markup("Arrange for trip to training camp at a cost of %s?" % (cost))

    def show(self):
        state = self.run() == Gtk.ResponseType.OK
        self.destroy()

        return state

