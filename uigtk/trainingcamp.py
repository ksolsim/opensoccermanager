#!/usr/bin/env python3

from gi.repository import Gtk

import data
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
        radiobuttonAverage.connect("toggled", self.on_quality_toggled)
        label.set_mnemonic_widget(radiobuttonAverage)
        frame.grid.attach(radiobuttonAverage, 1, 1, 1, 1)
        radiobuttonGood = uigtk.widgets.RadioButton("_Good")
        radiobuttonGood.join_group(radiobuttonAverage)
        radiobuttonGood.connect("toggled", self.on_quality_toggled)
        frame.grid.attach(radiobuttonGood, 2, 1, 1, 1)
        radiobuttonSuperb = uigtk.widgets.RadioButton("_Superb")
        radiobuttonSuperb.join_group(radiobuttonAverage)
        radiobuttonSuperb.connect("toggled", self.on_quality_toggled)
        frame.grid.attach(radiobuttonSuperb, 3, 1, 1, 1)

        label = uigtk.widgets.Label("Location", leftalign=True)
        frame.grid.attach(label, 0, 2, 1, 1)
        radiobuttonHome = uigtk.widgets.RadioButton("_Home")
        radiobuttonHome.connect("toggled", self.on_location_toggled)
        frame.grid.attach(radiobuttonHome, 1, 2, 1, 1)
        radiobuttonAbroad = uigtk.widgets.RadioButton("_Abroad")
        radiobuttonAbroad.join_group(radiobuttonHome)
        radiobuttonAbroad.connect("toggled", self.on_location_toggled)
        frame.grid.attach(radiobuttonAbroad, 2, 2, 1, 1)

        label = uigtk.widgets.Label("Training", leftalign=True)
        frame.grid.attach(label, 0, 3, 1, 1)
        radiobuttonLeisure = uigtk.widgets.RadioButton("_Leisure")
        frame.grid.attach(radiobuttonLeisure, 1, 3, 1, 1)
        radiobuttonSchedule = uigtk.widgets.RadioButton("_Schedule")
        radiobuttonSchedule.join_group(radiobuttonLeisure)
        frame.grid.attach(radiobuttonSchedule, 2, 3, 1, 1)
        radiobuttonIntense = uigtk.widgets.RadioButton("_Intense")
        radiobuttonIntense.join_group(radiobuttonLeisure)
        frame.grid.attach(radiobuttonIntense, 3, 3, 1, 1)

        label = uigtk.widgets.Label("Team", leftalign=True)
        frame.grid.attach(label, 0, 4, 1, 1)
        radiobuttonAllPlayers = uigtk.widgets.RadioButton("_All Players")
        frame.grid.attach(radiobuttonAllPlayers, 1, 4, 1, 1)
        radiobuttonFirstTeam = uigtk.widgets.RadioButton("_First Team Only")
        radiobuttonFirstTeam.join_group(radiobuttonAllPlayers)
        frame.grid.attach(radiobuttonFirstTeam, 2, 4, 1, 1)
        radiobuttonReserves = uigtk.widgets.RadioButton("_Reserves Only")
        radiobuttonReserves.join_group(radiobuttonAllPlayers)
        frame.grid.attach(radiobuttonReserves, 3, 4, 1, 1)

        frame = uigtk.widgets.CommonFrame("Cost")
        self.attach(frame, 0, 1, 1, 1)

        label = uigtk.widgets.Label("Player Cost", leftalign=True)
        frame.grid.attach(label, 0, 0, 1, 1)

        label = uigtk.widgets.Label("Total Cost", leftalign=True)
        frame.grid.attach(label, 0, 1, 1, 1)

        buttonbox = uigtk.widgets.ButtonBox()
        buttonbox.set_layout(Gtk.ButtonBoxStyle.END)
        self.attach(buttonbox, 0, 2, 1, 1)

        buttonReset = uigtk.widgets.Button("_Reset")
        buttonReset.set_tooltip_text("Reset details to default.")
        buttonbox.add(buttonReset)
        buttonArrange = uigtk.widgets.Button("_Arrange")
        buttonArrange.set_tooltip_text("Arrange the training camp with set details.")
        buttonbox.add(buttonArrange)

    def on_days_changed(self, combobox):
        pass

    def on_quality_toggled(self, radiobutton):
        pass

    def on_location_toggled(self, radiobutton):
        pass

    def on_training_toggled(self, radiobutton):
        pass

    def on_team_toggled(self, radiobutton):
        pass

    def on_reset_clicked(self, button):
        '''
        Reset training camp settings to default.
        '''

    def on_arrange_clicked(self, button):
        '''
        Setup training camp with selected details.
        '''

    def run(self):
        self.show_all()


class ConfirmTraining(Gtk.MessageDialog):
    def __init__(self, cost):
        Gtk.MessageDialog.__init__(self)
        self.set_transient_for(data.window)
        self.set_modal(True)
        self.set_title("Confirm Training")
        self.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("C_onfirm", Gtk.ResponseType.OK)
        self.set_default_response(Gtk.ResponseType.CANCEL)
        self.set_property("message-type", Gtk.MessageType.QUESTION)
        self.set_markup("Arrange for trip to training camp at a cost of %s?" % (cost))

        self.show()
