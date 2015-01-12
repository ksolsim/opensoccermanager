#!/usr/bin/env python3

from gi.repository import Gtk
import random

import game
import constants
import money
import dialogs
import display
import widgets


class Tactics(Gtk.Grid):
    def __init__(self):
        self.style = []
        self.passing = []
        self.tackling = []

        Gtk.Grid.__init__(self)
        self.set_border_width(5)
        self.set_vexpand(True)
        self.set_hexpand(True)

        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)
        grid.set_row_homogeneous(True)
        self.attach(grid, 0, 0, 1, 1)

        label = widgets.AlignedLabel("Formation")
        grid.attach(label, 0, 0, 1, 1)

        self.liststoreFormation = Gtk.ListStore(int, str)
        self.liststoreCaptain = Gtk.ListStore(str, str)
        self.liststorePenaltyTaker = Gtk.ListStore(str, str)
        self.liststoreFreeKickTaker = Gtk.ListStore(str, str)
        self.liststoreCornerTaker = Gtk.ListStore(str, str)

        cellrenderertext = Gtk.CellRendererText()

        self.comboboxFormation = Gtk.ComboBox()
        self.comboboxFormation.set_model(self.liststoreFormation)
        self.comboboxFormation.connect("changed", self.formation_changed)
        self.comboboxFormation.pack_start(cellrenderertext, True)
        self.comboboxFormation.add_attribute(cellrenderertext, "text", 1)
        grid.attach(self.comboboxFormation, 1, 0, 1, 1)

        label = widgets.AlignedLabel("Captain")
        grid.attach(label, 0, 1, 1, 1)
        self.comboboxCaptain = Gtk.ComboBox()
        self.comboboxCaptain.set_model(self.liststoreCaptain)
        self.comboboxCaptain.set_sensitive(False)
        self.comboboxCaptain.set_id_column(0)
        self.comboboxCaptain.pack_start(cellrenderertext, True)
        self.comboboxCaptain.add_attribute(cellrenderertext, "text", 1)
        self.comboboxCaptain.connect("changed", self.role_changed, 1)
        grid.attach(self.comboboxCaptain, 1, 1, 2, 1)

        label = widgets.AlignedLabel("Penalty Taker")
        grid.attach(label, 0, 2, 1, 1)
        self.comboboxPenaltyTaker = Gtk.ComboBox()
        self.comboboxPenaltyTaker.set_model(self.liststorePenaltyTaker)
        self.comboboxPenaltyTaker.set_sensitive(False)
        self.comboboxPenaltyTaker.set_id_column(0)
        self.comboboxPenaltyTaker.pack_start(cellrenderertext, True)
        self.comboboxPenaltyTaker.add_attribute(cellrenderertext, "text", 1)
        self.comboboxPenaltyTaker.connect("changed", self.role_changed, 2)
        grid.attach(self.comboboxPenaltyTaker, 1, 2, 2, 1)

        label = widgets.AlignedLabel("Free Kick Taker")
        grid.attach(label, 0, 3, 1, 1)
        self.comboboxFreeKickTaker = Gtk.ComboBox()
        self.comboboxFreeKickTaker.set_model(self.liststoreFreeKickTaker)
        self.comboboxFreeKickTaker.set_sensitive(False)
        self.comboboxFreeKickTaker.set_id_column(0)
        self.comboboxFreeKickTaker.pack_start(cellrenderertext, True)
        self.comboboxFreeKickTaker.add_attribute(cellrenderertext, "text", 1)
        self.comboboxFreeKickTaker.connect("changed", self.role_changed, 3)
        grid.attach(self.comboboxFreeKickTaker, 1, 3, 2, 1)

        label = widgets.AlignedLabel("Corner Taker")
        grid.attach(label, 0, 4, 1, 1)
        self.comboboxCornerTaker = Gtk.ComboBox()
        self.comboboxCornerTaker.set_model(self.liststoreCornerTaker)
        self.comboboxCornerTaker.set_sensitive(False)
        self.comboboxCornerTaker.set_id_column(0)
        self.comboboxCornerTaker.pack_start(cellrenderertext, True)
        self.comboboxCornerTaker.add_attribute(cellrenderertext, "text", 1)
        self.comboboxCornerTaker.connect("changed", self.role_changed, 4)
        grid.attach(self.comboboxCornerTaker, 1, 4, 2, 1)

        label = widgets.AlignedLabel("Playing Style")
        grid.attach(label, 0, 5, 1, 1)
        radiobuttonStyleDefensive = Gtk.RadioButton("Defensive")
        radiobuttonStyleDefensive.connect("toggled", self.style_changed, 0)
        self.style.append(radiobuttonStyleDefensive)
        grid.attach(radiobuttonStyleDefensive, 1, 5, 1, 1)
        radiobuttonStyleNormal = Gtk.RadioButton("Normal", group=radiobuttonStyleDefensive)
        radiobuttonStyleNormal.connect("toggled", self.style_changed, 1)
        self.style.append(radiobuttonStyleNormal)
        grid.attach(radiobuttonStyleNormal, 2, 5, 1, 1)
        radiobuttonStyleAttacking = Gtk.RadioButton("Attacking", group=radiobuttonStyleDefensive)
        radiobuttonStyleAttacking.connect("toggled", self.style_changed, 2)
        self.style.append(radiobuttonStyleAttacking)
        grid.attach(radiobuttonStyleAttacking, 3, 5, 1, 1)

        label = widgets.AlignedLabel("Tackling Style")
        grid.attach(label, 0, 6, 1, 1)
        radiobuttonTacklingSoft = Gtk.RadioButton("Soft")
        radiobuttonTacklingSoft.connect("toggled", self.tackling_changed, 0)
        self.tackling.append(radiobuttonTacklingSoft)
        grid.attach(radiobuttonTacklingSoft, 1, 6, 1, 1)
        radiobuttonTacklingNormal = Gtk.RadioButton("Normal", group=radiobuttonTacklingSoft)
        radiobuttonTacklingNormal.connect("toggled", self.tackling_changed, 1)
        self.tackling.append(radiobuttonTacklingNormal)
        grid.attach(radiobuttonTacklingNormal, 2, 6, 1, 1)
        radiobuttonTacklingHard = Gtk.RadioButton("Hard", group=radiobuttonTacklingSoft)
        radiobuttonTacklingHard.connect("toggled", self.tackling_changed, 2)
        self.tackling.append(radiobuttonTacklingHard)
        grid.attach(radiobuttonTacklingHard, 3, 6, 1, 1)

        label = widgets.AlignedLabel("Passing Style")
        grid.attach(label, 0, 7, 1, 1)
        radiobuttonPassingDirect = Gtk.RadioButton("Direct")
        radiobuttonPassingDirect.connect("toggled", self.passing_changed, 0)
        self.passing.append(radiobuttonPassingDirect)
        grid.attach(radiobuttonPassingDirect, 1, 7, 1, 1)
        radiobuttonPassingLong = Gtk.RadioButton("Long Ball", group=radiobuttonPassingDirect)
        radiobuttonPassingLong.connect("toggled", self.passing_changed, 1)
        self.passing.append(radiobuttonPassingLong)
        grid.attach(radiobuttonPassingLong, 2, 7, 1, 1)
        radiobuttonPassingShort = Gtk.RadioButton("Short", group=radiobuttonPassingDirect)
        radiobuttonPassingShort.connect("toggled", self.passing_changed, 2)
        self.passing.append(radiobuttonPassingShort)
        grid.attach(radiobuttonPassingShort, 3, 7, 1, 1)

        label = widgets.AlignedLabel("Win Bonus")
        grid.attach(label, 0, 8, 1, 1)
        self.comboboxWinBonus = Gtk.ComboBoxText()
        self.comboboxWinBonus.append("0", "No Bonus")
        self.comboboxWinBonus.append("1", "10%")
        self.comboboxWinBonus.append("2", "30%")
        self.comboboxWinBonus.append("3", "50%")
        self.comboboxWinBonus.connect("changed", self.bonus_changed)
        grid.attach(self.comboboxWinBonus, 1, 8, 1, 1)

    def formation_changed(self, combobox):
        treeiter = combobox.get_active_iter()

        if treeiter:
            model = combobox.get_model()
            game.clubs[game.teamid].tactics[0] = model[treeiter][0]

    def role_changed(self, combobox, index):
        # Used to set the captain, corner taker, free kick taker, penalty taker
        # Stores ID number of player in tactics list
        treeiter = combobox.get_active_iter()

        if treeiter:
            model = combobox.get_model()
            game.clubs[game.teamid].tactics[index] = model[treeiter][0]

    def style_changed(self, radiobutton, index):
        if radiobutton.get_active():
            game.clubs[game.teamid].tactics[5] = index

    def tackling_changed(self, radiobutton, index):
        if radiobutton.get_active():
            game.clubs[game.teamid].tactics[6] = index

    def passing_changed(self, radiobutton, index):
        if radiobutton.get_active():
            game.clubs[game.teamid].tactics[7] = index

    def bonus_changed(self, combobox):
        bonusid = combobox.get_active_id()
        bonusid = int(bonusid)

        game.clubs[game.teamid].tactics[8] = bonusid

    def run(self):
        self.liststoreFormation.clear()

        for index, item in enumerate(constants.formations):
            self.liststoreFormation.append([index, item[0]])

        self.liststoreCaptain.clear()
        self.liststorePenaltyTaker.clear()
        self.liststoreFreeKickTaker.clear()
        self.liststoreCornerTaker.clear()

        self.liststoreCaptain.append(["0", "Not Selected"])
        self.liststorePenaltyTaker.append(["0", "Not Selected"])
        self.liststoreFreeKickTaker.append(["0", "Not Selected"])
        self.liststoreCornerTaker.append(["0", "Not Selected"])

        self.comboboxCaptain.set_sensitive(False)
        self.comboboxPenaltyTaker.set_sensitive(False)
        self.comboboxFreeKickTaker.set_sensitive(False)
        self.comboboxCornerTaker.set_sensitive(False)

        for key, playerid in game.clubs[game.teamid].team.items():
            if playerid != 0:
                name = display.name(game.players[playerid])
                playerid = str(playerid)

                self.liststoreCaptain.append([playerid, name])
                self.liststorePenaltyTaker.append([playerid, name])
                self.liststoreFreeKickTaker.append([playerid, name])
                self.liststoreCornerTaker.append([playerid, name])

                self.comboboxCaptain.set_sensitive(True)
                self.comboboxPenaltyTaker.set_sensitive(True)
                self.comboboxFreeKickTaker.set_sensitive(True)
                self.comboboxCornerTaker.set_sensitive(True)

        self.comboboxFormation.set_active(game.clubs[game.teamid].tactics[0])

        captain = str(game.clubs[game.teamid].tactics[1])
        if not self.comboboxCaptain.set_active_id(captain):
            self.comboboxCaptain.set_active(0)

        penaltytaker = str(game.clubs[game.teamid].tactics[2])
        if not self.comboboxPenaltyTaker.set_active_id(penaltytaker):
            self.comboboxPenaltyTaker.set_active(0)

        freekicktaker = str(game.clubs[game.teamid].tactics[3])
        if not self.comboboxFreeKickTaker.set_active_id(freekicktaker):
            self.comboboxFreeKickTaker.set_active(0)

        cornertaker = str(game.clubs[game.teamid].tactics[4])
        if not self.comboboxCornerTaker.set_active_id(cornertaker):
            self.comboboxCornerTaker.set_active(0)

        self.style[game.clubs[game.teamid].tactics[5]].set_active(True)
        self.tackling[game.clubs[game.teamid].tactics[6]].set_active(True)
        self.passing[game.clubs[game.teamid].tactics[7]].set_active(True)
        self.comboboxWinBonus.set_active(game.clubs[game.teamid].tactics[8])

        self.show_all()


class Staff(Gtk.Grid):
    class Coach(Gtk.Grid):
        def __init__(self):
            def selection_changed(treeselection, index):
                model, treeiter = treeselection.get_selected()

                if treeiter:
                    if index == 0:
                        self.treeselectionCurrent.unselect_all()
                        buttonHire.set_sensitive(True)
                    else:
                        buttonHire.set_sensitive(False)

                    if index == 1:
                        treeselectionAvailable.unselect_all()
                        buttonFire.set_sensitive(True)
                        buttonRenewContract.set_sensitive(True)
                        buttonImproveWage.set_sensitive(True)
                    else:
                        buttonFire.set_sensitive(False)
                        buttonRenewContract.set_sensitive(False)
                        buttonImproveWage.set_sensitive(False)

            Gtk.Grid.__init__(self)
            self.set_vexpand(True)
            self.set_hexpand(True)
            self.set_border_width(5)
            self.set_row_spacing(5)

            self.liststoreAvailable = Gtk.ListStore(int, str, int, str, str, str, str)
            self.liststoreCurrent = Gtk.ListStore(int, str, int, str, str, str, str, str)

            label = widgets.AlignedLabel("<b>Current</b>")
            self.attach(label, 0, 0, 1, 1)

            scrolledwindow = Gtk.ScrolledWindow()
            scrolledwindow.set_vexpand(True)
            self.attach(scrolledwindow, 0, 1, 1, 1)

            treeviewCurrent = Gtk.TreeView()
            treeviewCurrent.set_model(self.liststoreCurrent)
            scrolledwindow.add(treeviewCurrent)
            self.treeselectionCurrent = treeviewCurrent.get_selection()
            self.treeselectionCurrent.connect("changed", selection_changed, 1)

            cellrenderertext = Gtk.CellRendererText()
            treeviewcolumn = Gtk.TreeViewColumn("Name", cellrenderertext, text=1)
            treeviewCurrent.append_column(treeviewcolumn)
            treeviewcolumn = Gtk.TreeViewColumn("Age", cellrenderertext, text=2)
            treeviewCurrent.append_column(treeviewcolumn)
            treeviewcolumn = Gtk.TreeViewColumn("Rating", cellrenderertext, text=3)
            treeviewCurrent.append_column(treeviewcolumn)
            treeviewcolumn = Gtk.TreeViewColumn("Speciality", cellrenderertext, text=4)
            treeviewCurrent.append_column(treeviewcolumn)
            treeviewcolumn = Gtk.TreeViewColumn("Wage", cellrenderertext, text=5)
            treeviewCurrent.append_column(treeviewcolumn)
            treeviewcolumn = Gtk.TreeViewColumn("Contract", cellrenderertext, text=6)
            treeviewCurrent.append_column(treeviewcolumn)
            treeviewcolumn = Gtk.TreeViewColumn("Morale", cellrenderertext, text=7)
            treeviewCurrent.append_column(treeviewcolumn)

            label = widgets.AlignedLabel("<b>Available</b>")
            self.attach(label, 0, 2, 1, 1)

            scrolledwindow = Gtk.ScrolledWindow()
            scrolledwindow.set_vexpand(True)
            self.attach(scrolledwindow, 0, 3, 1, 1)

            self.treeviewAvailable = Gtk.TreeView()
            self.treeviewAvailable.set_model(self.liststoreAvailable)
            self.treeviewAvailable.set_cursor(0)
            self.treeviewAvailable.connect("row-activated", self.staff_hire)
            scrolledwindow.add(self.treeviewAvailable)
            treeselectionAvailable = self.treeviewAvailable.get_selection()
            treeselectionAvailable.connect("changed", selection_changed, 0)

            treeviewcolumn = Gtk.TreeViewColumn("Name", cellrenderertext, text=1)
            self.treeviewAvailable.append_column(treeviewcolumn)
            treeviewcolumn = Gtk.TreeViewColumn("Age", cellrenderertext, text=2)
            self.treeviewAvailable.append_column(treeviewcolumn)
            treeviewcolumn = Gtk.TreeViewColumn("Rating", cellrenderertext, text=3)
            self.treeviewAvailable.append_column(treeviewcolumn)
            treeviewcolumn = Gtk.TreeViewColumn("Speciality", cellrenderertext, text=4)
            self.treeviewAvailable.append_column(treeviewcolumn)
            treeviewcolumn = Gtk.TreeViewColumn("Wage", cellrenderertext, text=5)
            self.treeviewAvailable.append_column(treeviewcolumn)
            treeviewcolumn = Gtk.TreeViewColumn("Contract", cellrenderertext, text=6)
            self.treeviewAvailable.append_column(treeviewcolumn)

            buttonbox = Gtk.ButtonBox()
            buttonbox.set_hexpand(True)
            buttonbox.set_spacing(5)
            buttonbox.set_layout(Gtk.ButtonBoxStyle.END)
            self.attach(buttonbox, 0, 4, 1, 1)

            buttonHire = Gtk.Button("_Hire")
            buttonHire.set_use_underline(True)
            buttonHire.connect("clicked", self.staff_hire)
            buttonbox.add(buttonHire)
            buttonFire = Gtk.Button("_Fire")
            buttonFire.set_use_underline(True)
            buttonFire.connect("clicked", self.staff_fire)
            buttonFire.set_sensitive(False)
            buttonbox.add(buttonFire)
            buttonRenewContract = Gtk.Button("_Renew Contract")
            buttonRenewContract.set_use_underline(True)
            buttonRenewContract.set_sensitive(False)
            buttonRenewContract.connect("clicked", self.renew_contract)
            buttonbox.add(buttonRenewContract)
            buttonImproveWage = Gtk.Button("_Improve Wage")
            buttonImproveWage.set_use_underline(True)
            buttonImproveWage.set_sensitive(False)
            buttonImproveWage.connect("clicked", self.improve_wage)
            buttonbox.add(buttonImproveWage)

        def staff_hire(self, widget, path=None, column=None):
            selection = self.treeviewAvailable.get_selection()
            model, treeiter = selection.get_selected()

            if treeiter:
                coachid = model[treeiter][0]
                coach = game.clubs[game.teamid].coaches_available[coachid]

                state = dialogs.hire_staff(0, coach.name)

                if state:
                    # Set coach morale to "delighted"
                    coach.morale = 9

                    game.clubs[game.teamid].coaches_hired[coachid] = game.clubs[game.teamid].coaches_available[coachid]
                    del game.clubs[game.teamid].coaches_available[coachid]

                    self.populate_data()

        def staff_fire(self, button):
            model, treeiter = self.treeselectionCurrent.get_selected()

            count = 0

            for key, item in game.clubs[game.teamid].individual_training.items():
                if item[0] == model[treeiter][0]:
                    count += 1

            staffid = model[treeiter][0]

            if count > 0:
                coach = game.clubs[game.teamid].coaches_hired[staffid]
                dialogs.fire_staff_error(coach.name, count)
            else:
                if treeiter:
                    coach = game.clubs[game.teamid].coaches_hired[staffid]
                    payout = coach.wage * coach.contract

                    state = dialogs.fire_staff(0, coach.name, payout)

                    if state:
                        del game.clubs[game.teamid].coaches_hired[staffid]
                        money.withdraw(payout, 10)

                        self.populate_data()

        def renew_contract(self, button):
            model, treeiter = self.treeselectionCurrent.get_selected()

            if treeiter:
                staffid = model[treeiter][0]
                coach = game.clubs[game.teamid].coaches_hired[staffid]
                year = random.randint(2, 4)
                amount = coach.wage * 0.055 + coach.wage

                state = dialogs.renew_staff_contract(coach.name, year, amount)

                if state:
                    coach.wage = amount
                    coach.contract = year * 52

                    self.populate_data()

        def improve_wage(self, button):
            model, treeiter = self.treeselectionCurrent.get_selected()

            if treeiter:
                staffid = model[treeiter][0]
                coach = game.clubs[game.teamid].coaches_hired[staffid]
                amount = coach.wage * 0.025 + coach.wage

                state = dialogs.improve_wage(coach.name, amount)

                if state:
                    coach.wage = amount

                    self.populate_data()

        def populate_data(self):
            self.liststoreAvailable.clear()
            self.liststoreCurrent.clear()

            for key, coach in game.clubs[game.teamid].coaches_available.items():
                name = coach.name
                age = coach.age
                skill = coach.skill
                speciality = coach.speciality
                wage = "%s" % (display.currency(coach.wage))
                contract = "%i Weeks" % (coach.contract)

                self.liststoreAvailable.append([key, name, age, skill, speciality, wage, contract])

            for key, coach in game.clubs[game.teamid].coaches_hired.items():
                name = coach.name
                age = coach.age
                skill = coach.skill
                speciality = coach.speciality
                wage = "%s" % (display.currency(coach.wage))
                contract = "%i Weeks" % (coach.contract)
                morale = display.staff_morale(coach.morale)

                self.liststoreCurrent.append([key, name, age, skill, speciality, wage, contract, morale])

        def run(self):
            self.populate_data()

            self.show_all()

    class Scout(Gtk.Grid):
        def __init__(self):
            def selection_changed(treeselection, index):
                model, treeiter = treeselection.get_selected()

                if treeiter:
                    if index == 0:
                        self.treeselectionCurrent.unselect_all()
                        buttonHire.set_sensitive(True)
                    else:
                        buttonHire.set_sensitive(False)

                    if index == 1:
                        treeselectionAvailable.unselect_all()
                        buttonFire.set_sensitive(True)
                        buttonRenewContract.set_sensitive(True)
                        buttonImproveWage.set_sensitive(True)
                    else:
                        buttonFire.set_sensitive(False)
                        buttonRenewContract.set_sensitive(False)
                        buttonImproveWage.set_sensitive(False)

            Gtk.Grid.__init__(self)
            self.set_vexpand(True)
            self.set_hexpand(True)
            self.set_border_width(5)
            self.set_row_spacing(5)

            self.liststoreAvailable = Gtk.ListStore(int, str, int, str, str, str)
            self.liststoreCurrent = Gtk.ListStore(int, str, int, str, str, str, str)

            label = widgets.AlignedLabel("<b>Current</b>")
            label.set_use_markup(True)
            self.attach(label, 0, 0, 1, 1)

            scrolledwindow = Gtk.ScrolledWindow()
            scrolledwindow.set_vexpand(True)
            self.attach(scrolledwindow, 0, 1, 1, 1)

            treeviewCurrent = Gtk.TreeView()
            treeviewCurrent.set_model(self.liststoreCurrent)
            self.treeselectionCurrent = treeviewCurrent.get_selection()
            self.treeselectionCurrent.connect("changed", selection_changed, 1)
            cellrenderertext = Gtk.CellRendererText()
            treeviewcolumn = Gtk.TreeViewColumn("Name", cellrenderertext, text=1)
            treeviewCurrent.append_column(treeviewcolumn)
            treeviewcolumn = Gtk.TreeViewColumn("Age", cellrenderertext, text=2)
            treeviewCurrent.append_column(treeviewcolumn)
            treeviewcolumn = Gtk.TreeViewColumn("Rating", cellrenderertext, text=3)
            treeviewCurrent.append_column(treeviewcolumn)
            treeviewcolumn = Gtk.TreeViewColumn("Wage", cellrenderertext, text=4)
            treeviewCurrent.append_column(treeviewcolumn)
            treeviewcolumn = Gtk.TreeViewColumn("Contract", cellrenderertext, text=5)
            treeviewCurrent.append_column(treeviewcolumn)
            treeviewcolumn = Gtk.TreeViewColumn("Morale", cellrenderertext, text=6)
            treeviewCurrent.append_column(treeviewcolumn)
            scrolledwindow.add(treeviewCurrent)

            label = widgets.AlignedLabel("<b>Available</b>")
            label.set_use_markup(True)
            self.attach(label, 0, 2, 1, 1)

            scrolledwindow = Gtk.ScrolledWindow()
            scrolledwindow.set_vexpand(True)
            self.attach(scrolledwindow, 0, 3, 1, 1)

            self.treeviewAvailable = Gtk.TreeView()
            self.treeviewAvailable.set_model(self.liststoreAvailable)
            self.treeviewAvailable.set_cursor(0)
            scrolledwindow.add(self.treeviewAvailable)
            treeselectionAvailable = self.treeviewAvailable.get_selection()
            treeselectionAvailable.connect("changed", selection_changed, 0)

            treeviewcolumn = Gtk.TreeViewColumn("Name", cellrenderertext, text=1)
            self.treeviewAvailable.append_column(treeviewcolumn)
            treeviewcolumn = Gtk.TreeViewColumn("Age", cellrenderertext, text=2)
            self.treeviewAvailable.append_column(treeviewcolumn)
            treeviewcolumn = Gtk.TreeViewColumn("Rating", cellrenderertext, text=3)
            self.treeviewAvailable.append_column(treeviewcolumn)
            treeviewcolumn = Gtk.TreeViewColumn("Wage", cellrenderertext, text=4)
            self.treeviewAvailable.append_column(treeviewcolumn)
            treeviewcolumn = Gtk.TreeViewColumn("Contract", cellrenderertext, text=5)
            self.treeviewAvailable.append_column(treeviewcolumn)

            buttonbox = Gtk.ButtonBox()
            buttonbox.set_hexpand(True)
            buttonbox.set_spacing(5)
            buttonbox.set_layout(Gtk.ButtonBoxStyle.END)
            self.attach(buttonbox, 0, 4, 1, 1)

            buttonHire = Gtk.Button("_Hire")
            buttonHire.set_use_underline(True)
            buttonHire.connect("clicked", self.staff_hire)
            buttonbox.add(buttonHire)
            buttonFire = Gtk.Button("_Fire")
            buttonFire.set_use_underline(True)
            buttonFire.set_sensitive(False)
            buttonFire.connect("clicked", self.staff_fire)
            buttonbox.add(buttonFire)
            buttonRenewContract = Gtk.Button("_Renew Contract")
            buttonRenewContract.set_use_underline(True)
            buttonRenewContract.set_sensitive(False)
            buttonRenewContract.connect("clicked", self.renew_contract)
            buttonbox.add(buttonRenewContract)
            buttonImproveWage = Gtk.Button("_Improve Wage")
            buttonImproveWage.set_use_underline(True)
            buttonImproveWage.set_sensitive(False)
            buttonImproveWage.connect("clicked", self.improve_wage)
            buttonbox.add(buttonImproveWage)

        def staff_hire(self, widget, path=None, column=None):
            selection = self.treeviewAvailable.get_selection()
            model, treeiter = selection.get_selected()

            if treeiter:
                staffid = model[treeiter][0]
                scout = game.clubs[game.teamid].scouts_available[staffid]

                state = dialogs.hire_staff(1, scout.name)

                if state:
                    scoutid = model[treeiter][0]

                    scout.morale = 9

                    game.clubs[game.teamid].scouts_hired[scoutid] = game.clubs[game.teamid].scouts_available[scoutid]
                    del game.clubs[game.teamid].scouts_available[scoutid]

                    self.populate_data()

        def staff_fire(self, widget):
            model, treeiter = self.treeselectionCurrent.get_selected()

            if treeiter:
                staffid = model[treeiter][0]
                scout = game.clubs[game.teamid].scouts_hired[staffid]
                payout = scout.wage * scout.contract

                state = dialogs.fire_staff(0, scout.name, payout)

                if state:
                    del game.clubs[game.teamid].scouts_hired[staffid]
                    money.withdraw(payout, 10)

                    self.populate_data()

        def renew_contract(self, button):
            model, treeiter = self.treeselectionCurrent.get_selected()

            if treeiter:
                staffid = model[treeiter][0]
                scout = game.clubs[game.teamid].scouts_hired[staffid]
                year = random.randint(2, 4)
                amount = scout.wage * 0.055 + scout.wage

                state = dialogs.renew_staff_contract(scout.name, year, amount)

                if state:
                    scout.wage = amount
                    scout.contract = year * 52

                    self.populate_data()

        def improve_wage(self, button):
            model, treeiter = self.treeselectionCurrent.get_selected()

            if treeiter:
                staffid = model[treeiter][0]
                scout = game.clubs[game.teamid].scouts_hired[staffid]
                amount = scout.wage * 0.025 + scout.wage

                state = dialogs.improve_wage(scout.name, amount)

                if state:
                    scout.wage = amount

                    self.populate_data()

        def populate_data(self):
            self.liststoreAvailable.clear()

            for key, scout in game.clubs[game.teamid].scouts_available.items():
                name = scout.name
                age = scout.age
                skill = scout.skill
                wage = "%s" % (display.currency(scout.wage))
                contract = "%i Weeks" % (scout.contract)

                self.liststoreAvailable.append([key, name, age, skill, wage, contract])

            self.liststoreCurrent.clear()

            for key, scout in game.clubs[game.teamid].scouts_hired.items():
                name = scout.name
                age = scout.age
                skill = scout.skill
                wage = "%s" % (display.currency(scout.wage))
                contract = "%i Weeks" % (scout.wage)
                morale = display.staff_morale(scout.morale)

                self.liststoreCurrent.append([key, name, age, skill, wage, contract, morale])

        def run(self):
            self.populate_data()

            self.show_all()

    def __init__(self):
        Gtk.Grid.__init__(self)
        self.set_vexpand(True)
        self.set_hexpand(True)
        self.set_border_width(5)

        notebook = Gtk.Notebook()
        self.attach(notebook, 0, 0, 1, 1)

        self.coach = self.Coach()
        label = Gtk.Label("Coach")
        notebook.append_page(self.coach, label)
        self.scout = self.Scout()
        label = Gtk.Label("Scout")
        notebook.append_page(self.scout, label)

    def run(self):
        self.coach.run()
        self.scout.run()

        self.show_all()
