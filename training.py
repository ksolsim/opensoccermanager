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
import money
import structures
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

        for item in constants.team_training[2]:
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
        buttonAssistant.set_tooltip_text("Assistant Manager will generate a training schedule")
        buttonAssistant.connect("clicked", self.assistant_generated)
        buttonbox.add(buttonAssistant)

    def assistant_generated(self, button):
        '''
        Clear existing session and randomly generate new schedule.
        '''
        values = [count for count in range(2, 18)]
        random.shuffle(values)

        # Reset comboboxes to zero
        for item in self.comboboxes:
            item.set_active(0)

        self.comboboxes[0].set_active(values[0])
        self.comboboxes[1].set_active(values[1])
        self.comboboxes[2].set_active(1)
        self.comboboxes[6].set_active(values[2])
        self.comboboxes[7].set_active(values[3])
        self.comboboxes[8].set_active(1)
        self.comboboxes[12].set_active(values[4])
        self.comboboxes[13].set_active(values[5])
        self.comboboxes[14].set_active(1)
        self.comboboxes[18].set_active(values[6])
        self.comboboxes[19].set_active(values[7])
        self.comboboxes[20].set_active(1)
        self.comboboxes[24].set_active(values[8])
        self.comboboxes[25].set_active(values[9])
        self.comboboxes[26].set_active(1)
        self.comboboxes[30].set_active(values[10])
        self.comboboxes[31].set_active(values[11])
        self.comboboxes[32].set_active(1)

    def training_changed(self, combobox, index):
        game.clubs[game.teamid].team_training[index] = combobox.get_active()

        game.team_training_timeout = random.randint(16, 24)

    def run(self):
        count = 0

        for row in range(1, 8):
            for column in range(1, 7):
                value = game.clubs[game.teamid].team_training[count]
                self.comboboxes[count].set_active(value)

                count += 1

        self.show_all()


class IndividualTraining(Gtk.Grid):
    __name__ = "indtraining"

    def __init__(self):
        Gtk.Grid.__init__(self)
        self.set_row_spacing(5)

        self.infobar = Gtk.InfoBar()
        self.infobar.set_message_type(Gtk.MessageType.WARNING)
        label = Gtk.Label("There is no individual training assigned in the team training schedule. Individual training must be allocated for if players are to improve.")
        child = self.infobar.get_content_area()
        child.add(label)
        self.attach(self.infobar, 0, 0, 1, 1)

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_vexpand(True)
        scrolledwindow.set_hexpand(True)
        self.attach(scrolledwindow, 0, 1, 1, 1)

        self.overlay = Gtk.Overlay()
        scrolledwindow.add(self.overlay)
        self.labelNoStaff = Gtk.Label("There are no coaches on staff. To assign players to individual training, at least one coach must be hired.")
        self.overlay.add_overlay(self.labelNoStaff)

        self.liststore = Gtk.ListStore(int, str, str, str, str, int, int)

        self.treeview = Gtk.TreeView()
        self.treeview.set_model(self.liststore)
        self.treeview.set_enable_search(False)
        self.treeview.set_search_column(-1)
        self.treeselection = self.treeview.get_selection()
        self.treeselection.connect("changed", self.selection_changed)
        self.overlay.add(self.treeview)

        cellrenderertext = Gtk.CellRendererText()
        treeviewcolumn = Gtk.TreeViewColumn("Name",
                                            cellrenderertext,
                                            text=1)
        self.treeview.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Coach",
                                            cellrenderertext,
                                            text=2)
        self.treeview.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Skill",
                                            cellrenderertext,
                                            text=3)
        self.treeview.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Intensity",
                                            cellrenderertext,
                                            text=4)
        self.treeview.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Start Value",
                                            cellrenderertext,
                                            text=5)
        self.treeview.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Current Value",
                                            cellrenderertext,
                                            text=6)
        self.treeview.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Notes")
        self.treeview.append_column(treeviewcolumn)

        buttonbox = Gtk.ButtonBox()
        buttonbox.set_layout(Gtk.ButtonBoxStyle.END)
        buttonbox.set_spacing(5)
        self.attach(buttonbox, 0, 2, 1, 1)

        self.buttonAdd = widgets.Button("_Add To Training")
        self.buttonAdd.connect("clicked", self.dialog_add)
        buttonbox.add(self.buttonAdd)
        self.buttonEdit = widgets.Button("_Edit Training")
        self.buttonEdit.set_sensitive(False)
        self.buttonEdit.connect("clicked", self.dialog_add, 1)
        buttonbox.add(self.buttonEdit)
        self.buttonRemove = widgets.Button("_Remove From Training")
        self.buttonRemove.set_sensitive(False)
        self.buttonRemove.connect("clicked", self.dialog_remove)
        buttonbox.add(self.buttonRemove)

    def selection_changed(self, treeselection):
        model, treeiter = treeselection.get_selected()

        if treeiter:
            self.buttonEdit.set_sensitive(True)
            self.buttonRemove.set_sensitive(True)
        else:
            self.buttonEdit.set_sensitive(False)
            self.buttonRemove.set_sensitive(False)

    def dialog_add(self, button, mode=0):
        if mode == 0:
            training = dialogs.add_individual_training()
        elif mode == 1:
            model, treeiter = self.treeselection.get_selected()
            playerid = model[treeiter][0]
            training = dialogs.add_individual_training(playerid)

        if training:
            playerid = training[0]
            player = game.players[playerid]
            coachid = training[1]

            if training[2] != 9:
                skill = training[2]

                skills = player.skills()
                start_value = skills[skill]
            else:
                skill = 9
                start_value = player.fitness

            intensity = training[3]

            club = game.clubs[game.teamid]

            individual_training = structures.IndividualTraining()
            individual_training.playerid = playerid
            individual_training.coachid = coachid
            individual_training.skill = skill
            individual_training.intensity = intensity
            individual_training.start_value = start_value
            club.individual_training[playerid] = individual_training

            self.populate_data()

    def dialog_remove(self, button):
        model, treeiter = self.treeselection.get_selected()
        playerid = model[treeiter][0]

        if dialogs.remove_individual_training(playerid):
            self.populate_data()

    def populate_data(self):
        self.liststore.clear()

        training = game.clubs[game.teamid].individual_training

        for playerid, item in training.items():
            player = game.players[playerid]

            skills = player.skills()

            name = display.name(player)
            coachid = int(item.coachid)
            coach = game.clubs[game.teamid].coaches_hired[coachid].name

            if item.skill == 9:
                skill = "Fitness"
                current = player.fitness
            else:
                skill = constants.skill[item.skill]
                current = skills[item.skill]

            intensity = constants.intensity[item.intensity]

            self.liststore.append([playerid,
                                   name,
                                   coach,
                                   skill,
                                   intensity,
                                   item.start_value,
                                   current])

    def run(self):
        self.populate_data()

        self.show_all()

        if 1 in game.clubs[game.teamid].team_training:
            self.infobar.hide()

        sensitive = len(game.clubs[game.teamid].coaches_hired) > 0
        self.treeview.set_sensitive(sensitive)
        self.buttonAdd.set_sensitive(sensitive)

        if sensitive:
            self.labelNoStaff.hide()


class TrainingCamp(Gtk.Grid):
    __name__ = "trainingcamp"

    def __init__(self):
        self.subtotals = [1, 0, 0, 0, 0]
        self.options = [0, 0, 0, 0, 0]
        self.cost_per_player = 0
        self.cost = 0
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
        radiobuttonAverage.connect("toggled", self.update_quality, 0)
        self.attach(radiobuttonAverage, 1, 1, 1, 1)
        radiobuttonGood = Gtk.RadioButton("Good", group=radiobuttonAverage)
        radiobuttonGood.connect("toggled", self.update_quality, 1)
        self.attach(radiobuttonGood, 2, 1, 1, 1)
        radiobuttonSuperb = Gtk.RadioButton("Superb", group=radiobuttonAverage)
        radiobuttonSuperb.connect("toggled", self.update_quality, 2)
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
        radiobuttonLeisure.connect("toggled", self.update_purpose, 0)
        self.attach(radiobuttonLeisure, 1, 3, 1, 1)
        self.radiobuttonSchedule = Gtk.RadioButton("Schedule", group=radiobuttonLeisure)
        self.radiobuttonSchedule.connect("toggled", self.update_purpose, 1)
        self.attach(self.radiobuttonSchedule, 2, 3, 1, 1)
        radiobuttonIntensive = Gtk.RadioButton("Intensive", group=radiobuttonLeisure)
        radiobuttonIntensive.connect("toggled", self.update_purpose, 2)
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
        self.subtotals[0] = index
        self.options[0] = index

        self.update_total()

    def update_quality(self, radiobutton, index):
        if radiobutton.get_active():
            self.subtotals[1] = (index * 300) + (index * 2300)
            self.options[1] = index

            self.update_total()

    def update_location(self, radiobutton, index):
        if radiobutton.get_active():
            self.subtotals[2] = (index * 800) + (index * 3700)
            self.options[2] = index

            self.update_total()

    def update_purpose(self, radiobutton, index):
        if radiobutton.get_active():
            self.subtotals[3] = (index * 1000) + (index * 1200) * index
            self.options[3] = index

            schedule = False

            for item in game.clubs[game.teamid].team_training:
                if item != 0:
                    schedule = True

                    break

            if index == 1:
                if not schedule:
                    self.buttonScheduleWarning.show()
            else:
                self.buttonScheduleWarning.hide()

            self.update_total()

    def update_squad(self, radiobutton, index):
        if radiobutton.get_active():
            if index == 0:
                players = 0

                for item in game.clubs[game.teamid].team.values():
                    if item != 0:
                        players += 1

                if players < 16:
                    self.buttonSquadWarning.show()
                else:
                    self.buttonSquadWarning.hide()
            elif index == 1:
                players = 0

                for item in game.clubs[game.teamid].squad:
                    if item not in game.clubs[game.teamid].team.values():
                        players += 1

                self.buttonSquadWarning.hide()
            elif index == 2:
                players = len(game.clubs[game.teamid].squad)
                self.buttonSquadWarning.hide()

            self.subtotals[4] = index
            self.options[4] = index

            self.update_total()

    def update_total(self):
        squad_index = self.subtotals[4]

        if squad_index == 0:
            squad_count = 16
        elif squad_index == 1:
            count = 0

            for item in game.clubs[game.teamid].squad:
                if item not in game.clubs[game.teamid].team.values():
                    count += 1

            squad_count = count
        elif squad_index == 2:
            squad_count = len(game.clubs[game.teamid].squad)

        self.cost_per_player = (self.subtotals[0] * 500) + sum(self.subtotals[1:4])
        self.cost = self.cost_per_player * squad_count

        cost = display.currency(self.cost_per_player)
        self.labelPlayerCost.set_label("%s" % (cost))

        cost = display.currency(self.cost)
        self.labelTotal.set_label("<b>%s</b>" % (cost))

    def revert_training(self, button=None):
        self.subtotals = [1, 0, 0, 0, 0]
        self.cost = 0

        self.defaults[0].set_active(0)

        for item in self.defaults[1:5]:
            item.set_active(True)

    def confirm_training(self, button):
        state = dialogs.confirm_training(self.cost)

        if state:
            if money.request(self.cost):
                money.withdraw(self.cost, 18)

                events.training_camp(self.options)

            self.revert_training()

    def run(self):
        self.update_total()

        self.show_all()

        count = 0

        for item in game.clubs[game.teamid].team.values():
            if item != 0:
                count += 1

        if count < 16:
            self.buttonSquadWarning.show()
        else:
            self.buttonSquadWarning.hide()

        schedule = False

        for item in game.clubs[game.teamid].team_training:
            if item != 0:
                schedule = True

                break

        if self.radiobuttonSchedule.get_active():
            if not schedule:
                self.buttonScheduleWarning.show()
        else:
            self.buttonScheduleWarning.hide()
