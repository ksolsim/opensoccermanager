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
        self.comboboxDays = Gtk.ComboBoxText()
        self.comboboxDays.append("1", "1 Day")
        self.comboboxDays.append("2", "2 Days")
        self.comboboxDays.append("3", "3 Days")
        self.comboboxDays.append("4", "4 Days")
        self.comboboxDays.append("5", "5 Days")
        self.comboboxDays.set_active(0)
        self.comboboxDays.set_tooltip_text("Number of days to run training camp.")
        self.comboboxDays.connect("changed", self.on_days_changed)
        label.set_mnemonic_widget(self.comboboxDays)
        frame.grid.attach(self.comboboxDays, 1, 0, 1, 1)

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
        self.radiobuttonSchedule = uigtk.widgets.RadioButton("_Schedule")
        self.radiobuttonSchedule.purpose = 1
        self.radiobuttonSchedule.join_group(radiobuttonLeisure)
        self.radiobuttonSchedule.connect("toggled", self.on_purpose_toggled)
        frame.grid.attach(self.radiobuttonSchedule, 2, 3, 1, 1)
        radiobuttonIntense = uigtk.widgets.RadioButton("_Intense")
        radiobuttonIntense.purpose = 2
        radiobuttonIntense.join_group(radiobuttonLeisure)
        radiobuttonIntense.connect("toggled", self.on_purpose_toggled)
        frame.grid.attach(radiobuttonIntense, 3, 3, 1, 1)

        image = Gtk.Image()
        image.set_from_icon_name("gtk-dialog-warning", Gtk.IconSize.BUTTON)
        self.buttonScheduleWarning = Gtk.Button()
        self.buttonScheduleWarning.set_visible(False)
        self.buttonScheduleWarning.set_image(image)
        self.buttonScheduleWarning.set_relief(Gtk.ReliefStyle.NONE)
        self.buttonScheduleWarning.connect("clicked", self.on_schedule_warning_clicked)
        frame.grid.attach(self.buttonScheduleWarning, 4, 3, 1, 1)

        label = uigtk.widgets.Label("Team", leftalign=True)
        frame.grid.attach(label, 0, 4, 1, 1)
        radiobuttonAllPlayers = uigtk.widgets.RadioButton("_All Players")
        radiobuttonAllPlayers.squad = 0
        radiobuttonAllPlayers.connect("toggled", self.on_team_toggled)
        frame.grid.attach(radiobuttonAllPlayers, 1, 4, 1, 1)
        self.radiobuttonFirstTeam = uigtk.widgets.RadioButton("_First Team Only")
        self.radiobuttonFirstTeam.squad = 1
        self.radiobuttonFirstTeam.join_group(radiobuttonAllPlayers)
        self.radiobuttonFirstTeam.connect("toggled", self.on_team_toggled)
        frame.grid.attach(self.radiobuttonFirstTeam, 2, 4, 1, 1)
        radiobuttonReserves = uigtk.widgets.RadioButton("_Reserves Only")
        radiobuttonReserves.squad = 2
        radiobuttonReserves.join_group(radiobuttonAllPlayers)
        radiobuttonReserves.connect("toggled", self.on_team_toggled)
        frame.grid.attach(radiobuttonReserves, 3, 4, 1, 1)

        image = Gtk.Image()
        image.set_from_icon_name("gtk-dialog-warning", Gtk.IconSize.BUTTON)
        self.buttonSquadWarning = Gtk.Button()
        self.buttonSquadWarning.set_visible(False)
        self.buttonSquadWarning.set_image(image)
        self.buttonSquadWarning.set_relief(Gtk.ReliefStyle.NONE)
        self.buttonSquadWarning.connect("clicked", self.on_squad_warning_clicked)
        frame.grid.attach(self.buttonSquadWarning, 4, 4, 1, 1)

        frame = uigtk.widgets.CommonFrame("Cost")
        self.attach(frame, 0, 1, 1, 1)

        label = uigtk.widgets.Label("Single Player Cost", leftalign=True)
        frame.grid.attach(label, 0, 0, 1, 1)
        self.labelPlayerCost = uigtk.widgets.Label(leftalign=True)
        frame.grid.attach(self.labelPlayerCost, 1, 0, 1, 1)

        label = uigtk.widgets.Label("First Team Cost", leftalign=True)
        frame.grid.attach(label, 0, 1, 1, 1)
        self.labelFirstTeamCost = uigtk.widgets.Label(leftalign=True)
        frame.grid.attach(self.labelFirstTeamCost, 1, 1, 1, 1)

        label = uigtk.widgets.Label("Reserve Team Cost", leftalign=True)
        frame.grid.attach(label, 0, 2, 1, 1)
        self.labelReserveTeamCost = uigtk.widgets.Label(leftalign=True)
        frame.grid.attach(self.labelReserveTeamCost, 1, 2, 1, 1)

        label = uigtk.widgets.Label("Total Cost", leftalign=True)
        frame.grid.attach(label, 0, 3, 1, 1)
        self.labelTotalCost = uigtk.widgets.Label(leftalign=True)
        frame.grid.attach(self.labelTotalCost, 1, 3, 1, 1)

        buttonbox = uigtk.widgets.ButtonBox()
        buttonbox.set_layout(Gtk.ButtonBoxStyle.END)
        self.attach(buttonbox, 0, 5, 1, 1)

        buttonReset = uigtk.widgets.Button("_Reset")
        buttonReset.set_tooltip_text("Reset training camp options to default.")
        buttonReset.connect("clicked", self.on_reset_clicked)
        buttonbox.add(buttonReset)
        buttonArrange = uigtk.widgets.Button("_Arrange")
        buttonArrange.set_tooltip_text("Arrange training camp with set options.")
        buttonArrange.connect("clicked", self.on_arrange_clicked)
        buttonbox.add(buttonArrange)

    def on_days_changed(self, combobox):
        '''
        Update cost when days value is changed.
        '''
        data.user.club.training_camp.options.days = int(combobox.get_active_id())
        self.update_cost()

    def on_quality_toggled(self, radiobutton):
        '''
        Update cost when quality of camp is changed.
        '''
        if radiobutton.get_active():
            data.user.club.training_camp.options.quality = radiobutton.quality
            self.update_cost()

    def on_location_toggled(self, radiobutton):
        '''
        Update cost when location is changed.
        '''
        if radiobutton.get_active():
            data.user.club.training_camp.options.location = radiobutton.location
            self.update_cost()

    def on_purpose_toggled(self, radiobutton):
        '''
        Update cost when purpose of training is changed.
        '''
        if radiobutton.get_active():
            data.user.club.training_camp.options.purpose = radiobutton.purpose
            self.update_cost()

        self.update_warning_status()

    def on_team_toggled(self, radiobutton):
        '''
        Update cost when team members attending is changed.
        '''
        if radiobutton.get_active():
            data.user.club.training_camp.options.squad = radiobutton.squad
            self.update_cost()

        self.update_warning_status()

    def update_cost(self):
        '''
        Update costing labels.
        '''
        cost = data.user.club.training_camp.get_player_cost()
        self.labelPlayerCost.set_label("%s" % (data.currency.get_currency(cost, integer=True)))

        cost = data.user.club.training_camp.get_first_team_cost()
        self.labelFirstTeamCost.set_label("%s" % (data.currency.get_currency(cost, integer=True)))

        cost = data.user.club.training_camp.get_reserve_team_cost()
        self.labelReserveTeamCost.set_label("%s" % (data.currency.get_currency(cost, integer=True)))

        cost = data.user.club.training_camp.get_total_cost()
        self.labelTotalCost.set_label("%s" % (data.currency.get_currency(cost, integer=True)))

    def on_reset_clicked(self, *args):
        '''
        Reset training camp settings to default.
        '''
        self.comboboxDays.set_active(0)

    def on_arrange_clicked(self, *args):
        '''
        Setup training camp with selected details.
        '''
        cost = data.user.club.training_camp.get_total_cost()
        dialog = ConfirmTraining(data.currency.get_currency(cost, integer=True))

        if dialog.show():
            data.user.club.training_camp.apply_options()

    def on_squad_warning_clicked(self, *args):
        '''
        Display warning that not enough squad members have been selected.
        '''
        SquadWarning()

    def on_schedule_warning_clicked(self, *args):
        '''
        Display warning that no team training schedule has been devised.
        '''
        ScheduleWarning()

    def update_warning_status(self):
        '''
        Toggle whether warning icons are displayed.
        '''
        self.buttonScheduleWarning.set_visible(False)

        if self.radiobuttonSchedule.get_active():
            if not data.user.club.team_training.get_schedule_set():
                self.buttonScheduleWarning.set_visible(True)
        else:
            self.buttonScheduleWarning.set_visible(False)

        if self.radiobuttonFirstTeam.get_active():
            if data.user.club.squad.teamselection.get_team_count() + data.user.club.squad.teamselection.get_subs_count() < 16:
                self.buttonSquadWarning.set_visible(True)
        else:
            self.buttonSquadWarning.set_visible(False)

    def run(self):
        self.show_all()

        self.update_warning_status()
        self.update_cost()


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


class SquadWarning(Gtk.MessageDialog):
    def __init__(self):
        Gtk.MessageDialog.__init__(self)
        self.set_transient_for(data.window)
        self.set_modal(True)
        self.set_title("Squad Selection Warning")
        self.set_property("message-type", Gtk.MessageType.WARNING)
        self.set_markup("There is not a full selection of first team and substitute players selected. The training camp can still be booked for the listed players at the cost of all sixteen.")
        self.add_button("_Close", Gtk.ResponseType.CLOSE)
        self.connect("response", self.on_response)

        self.show()

    def on_response(self, *args):
        self.destroy()


class ScheduleWarning(Gtk.MessageDialog):
    def __init__(self):
        Gtk.MessageDialog.__init__(self)
        self.set_transient_for(data.window)
        self.set_modal(True)
        self.set_title("Training Schedule Warning")
        self.set_property("message-type", Gtk.MessageType.WARNING)
        self.set_markup("There is currently no training schedule setup. The training camp can still be booked, however the players will not achieve the most out of the session.")
        self.add_button("_Close", Gtk.ResponseType.CLOSE)
        self.connect("response", self.on_response)

        self.show()

    def on_response(self, *args):
        self.destroy()
