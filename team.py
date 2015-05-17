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
import display
import game
import widgets


class Tactics(Gtk.Grid):
    __name__ = "tactics"

    def __init__(self):
        self.style = []
        self.passing = []
        self.tackling = []

        Gtk.Grid.__init__(self)

        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)
        grid.set_row_homogeneous(True)
        self.attach(grid, 0, 0, 1, 1)

        self.liststoreFormation = Gtk.ListStore(int, str)
        self.liststoreCaptain = Gtk.ListStore(str, str)
        self.liststorePenaltyTaker = Gtk.ListStore(str, str)
        self.liststoreFreeKickTaker = Gtk.ListStore(str, str)
        self.liststoreCornerTaker = Gtk.ListStore(str, str)

        cellrenderertext = Gtk.CellRendererText()

        label = widgets.AlignedLabel("_Formation")
        grid.attach(label, 0, 0, 1, 1)
        self.comboboxFormation = Gtk.ComboBox()
        self.comboboxFormation.set_model(self.liststoreFormation)
        self.comboboxFormation.connect("changed", self.formation_changed)
        self.comboboxFormation.pack_start(cellrenderertext, True)
        self.comboboxFormation.add_attribute(cellrenderertext, "text", 1)
        label.set_mnemonic_widget(self.comboboxFormation)
        grid.attach(self.comboboxFormation, 1, 0, 1, 1)

        label = widgets.AlignedLabel("_Captain")
        grid.attach(label, 0, 1, 1, 1)
        self.comboboxCaptain = Gtk.ComboBox()
        self.comboboxCaptain.set_model(self.liststoreCaptain)
        self.comboboxCaptain.set_id_column(0)
        self.comboboxCaptain.set_sensitive(False)
        self.comboboxCaptain.pack_start(cellrenderertext, True)
        self.comboboxCaptain.add_attribute(cellrenderertext, "text", 1)
        self.comboboxCaptain.connect("changed", self.role_changed, 1)
        label.set_mnemonic_widget(self.comboboxCaptain)
        grid.attach(self.comboboxCaptain, 1, 1, 2, 1)

        label = widgets.AlignedLabel("_Penalty Taker")
        grid.attach(label, 0, 2, 1, 1)
        self.comboboxPenaltyTaker = Gtk.ComboBox()
        self.comboboxPenaltyTaker.set_model(self.liststorePenaltyTaker)
        self.comboboxPenaltyTaker.set_id_column(0)
        self.comboboxPenaltyTaker.set_sensitive(False)
        self.comboboxPenaltyTaker.pack_start(cellrenderertext, True)
        self.comboboxPenaltyTaker.add_attribute(cellrenderertext, "text", 1)
        self.comboboxPenaltyTaker.connect("changed", self.role_changed, 2)
        label.set_mnemonic_widget(self.comboboxPenaltyTaker)
        grid.attach(self.comboboxPenaltyTaker, 1, 2, 2, 1)

        label = widgets.AlignedLabel("Free _Kick Taker")
        grid.attach(label, 0, 3, 1, 1)
        self.comboboxFreeKickTaker = Gtk.ComboBox()
        self.comboboxFreeKickTaker.set_model(self.liststoreFreeKickTaker)
        self.comboboxFreeKickTaker.set_id_column(0)
        self.comboboxFreeKickTaker.set_sensitive(False)
        self.comboboxFreeKickTaker.pack_start(cellrenderertext, True)
        self.comboboxFreeKickTaker.add_attribute(cellrenderertext, "text", 1)
        self.comboboxFreeKickTaker.connect("changed", self.role_changed, 3)
        label.set_mnemonic_widget(self.comboboxFreeKickTaker)
        grid.attach(self.comboboxFreeKickTaker, 1, 3, 2, 1)

        label = widgets.AlignedLabel("_Corner Taker")
        grid.attach(label, 0, 4, 1, 1)
        self.comboboxCornerTaker = Gtk.ComboBox()
        self.comboboxCornerTaker.set_model(self.liststoreCornerTaker)
        self.comboboxCornerTaker.set_id_column(0)
        self.comboboxCornerTaker.set_sensitive(False)
        self.comboboxCornerTaker.pack_start(cellrenderertext, True)
        self.comboboxCornerTaker.add_attribute(cellrenderertext, "text", 1)
        self.comboboxCornerTaker.connect("changed", self.role_changed, 4)
        label.set_mnemonic_widget(self.comboboxCornerTaker)
        grid.attach(self.comboboxCornerTaker, 1, 4, 2, 1)

        label = widgets.AlignedLabel("P_laying Style")
        grid.attach(label, 0, 5, 1, 1)
        radiobuttonStyleDefensive = Gtk.RadioButton("Defensive")
        radiobuttonStyleDefensive.connect("toggled", self.style_changed, 0)
        label.set_mnemonic_widget(radiobuttonStyleDefensive)
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

        label = widgets.AlignedLabel("_Tackling Style")
        grid.attach(label, 0, 6, 1, 1)
        radiobuttonTacklingSoft = Gtk.RadioButton("Soft")
        radiobuttonTacklingSoft.connect("toggled", self.tackling_changed, 0)
        label.set_mnemonic_widget(radiobuttonTacklingSoft)
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

        label = widgets.AlignedLabel("_Passing Style")
        grid.attach(label, 0, 7, 1, 1)
        radiobuttonPassingDirect = Gtk.RadioButton("Direct")
        radiobuttonPassingDirect.connect("toggled", self.passing_changed, 0)
        label.set_mnemonic_widget(radiobuttonPassingDirect)
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

        label = widgets.AlignedLabel("Win _Bonus")
        grid.attach(label, 0, 8, 1, 1)
        self.comboboxWinBonus = Gtk.ComboBoxText()
        self.comboboxWinBonus.append("0", "No Bonus")
        self.comboboxWinBonus.append("1", "10%")
        self.comboboxWinBonus.append("3", "30%")
        self.comboboxWinBonus.append("5", "50%")
        self.comboboxWinBonus.connect("changed", self.bonus_changed)
        label.set_mnemonic_widget(self.comboboxWinBonus)
        grid.attach(self.comboboxWinBonus, 1, 8, 1, 1)

    def formation_changed(self, combobox):
        treeiter = combobox.get_active_iter()

        if treeiter:
            model = combobox.get_model()
            game.clubs[game.teamid].tactics[0] = model[treeiter][0]

    def role_changed(self, combobox, index):
        '''
        Store player ID for selected role (e.g. captain, penalty taker).
        '''
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

        game.clubs[game.teamid].tactics[8] = int(bonusid)

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

        for playerid in game.clubs[game.teamid].team.values():
            if playerid != 0:
                player = game.players[playerid]
                name = player.get_name()
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


class Interface(Gtk.Grid):
    def __init__(self):
        Gtk.Grid.__init__(self)
        self.set_vexpand(True)
        self.set_hexpand(True)
        self.set_border_width(5)
        self.set_row_spacing(5)

        commonframe = widgets.CommonFrame("Current")
        self.attach(commonframe, 0, 0, 1, 1)

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_vexpand(True)
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_policy(Gtk.PolicyType.NEVER,
                                  Gtk.PolicyType.AUTOMATIC)
        commonframe.insert(scrolledwindow)

        self.treeviewCurrent = Gtk.TreeView()
        self.treeviewCurrent.set_enable_search(False)
        self.treeviewCurrent.set_search_column(-1)
        scrolledwindow.add(self.treeviewCurrent)

        self.treeselectionCurrent = self.treeviewCurrent.get_selection()
        self.treeselectionCurrent.connect("changed", self.selection_changed, 1)

        commonframe = widgets.CommonFrame("Available")
        self.attach(commonframe, 0, 1, 1, 1)

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_vexpand(True)
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_policy(Gtk.PolicyType.NEVER,
                                  Gtk.PolicyType.AUTOMATIC)
        commonframe.insert(scrolledwindow)

        self.treeviewAvailable = Gtk.TreeView()
        self.treeviewAvailable.set_enable_search(False)
        self.treeviewAvailable.set_search_column(-1)
        scrolledwindow.add(self.treeviewAvailable)

        self.treeselectionAvailable = self.treeviewAvailable.get_selection()
        self.treeselectionAvailable.connect("changed", self.selection_changed, 0)

        buttonbox = Gtk.ButtonBox()
        buttonbox.set_hexpand(True)
        buttonbox.set_spacing(5)
        buttonbox.set_layout(Gtk.ButtonBoxStyle.END)
        self.attach(buttonbox, 0, 2, 1, 1)

        self.buttonHire = widgets.Button("_Hire")
        buttonbox.add(self.buttonHire)
        self.buttonFire = widgets.Button("_Fire")
        self.buttonFire.set_sensitive(False)
        buttonbox.add(self.buttonFire)
        self.buttonRenewContract = widgets.Button("_Renew Contract")
        self.buttonRenewContract.set_sensitive(False)
        buttonbox.add(self.buttonRenewContract)
        self.buttonImproveWage = widgets.Button("_Improve Wage")
        self.buttonImproveWage.set_sensitive(False)
        buttonbox.add(self.buttonImproveWage)

    def selection_changed(self, treeselection, index):
        selected = treeselection.count_selected_rows() > 0

        if index == 0:
            if selected:
                self.treeselectionCurrent.unselect_all()
                self.buttonHire.set_sensitive(True)
            else:
                self.buttonHire.set_sensitive(False)
        elif index == 1:
            if selected:
                self.treeselectionAvailable.unselect_all()
                self.buttonFire.set_sensitive(True)
                self.buttonRenewContract.set_sensitive(True)
                self.buttonImproveWage.set_sensitive(True)
            else:
                self.buttonFire.set_sensitive(False)
                self.buttonRenewContract.set_sensitive(False)
                self.buttonImproveWage.set_sensitive(False)

    def run(self):
        self.show_all()


class Staff(Gtk.Grid):
    __name__ = "staff"

    class Coach(Interface):
        def __init__(self):
            Interface.__init__(self)

            self.liststoreAvailable = Gtk.ListStore(int, str, int, str, str, str, str)
            self.treeviewAvailable.set_model(self.liststoreAvailable)

            self.liststoreCurrent = Gtk.ListStore(int, str, int, str, str, str, str, str)
            self.treeviewCurrent.set_model(self.liststoreCurrent)

            treeviewcolumn = widgets.TreeViewColumn(title="Name", column=1)
            self.treeviewCurrent.append_column(treeviewcolumn)
            treeviewcolumn = widgets.TreeViewColumn(title="Age", column=2)
            self.treeviewCurrent.append_column(treeviewcolumn)
            treeviewcolumn = widgets.TreeViewColumn(title="Rating", column=3)
            self.treeviewCurrent.append_column(treeviewcolumn)
            treeviewcolumn = widgets.TreeViewColumn(title="Speciality", column=4)
            self.treeviewCurrent.append_column(treeviewcolumn)
            treeviewcolumn = widgets.TreeViewColumn(title="Wage", column=5)
            self.treeviewCurrent.append_column(treeviewcolumn)
            treeviewcolumn = widgets.TreeViewColumn(title="Contract", column=6)
            self.treeviewCurrent.append_column(treeviewcolumn)
            treeviewcolumn = widgets.TreeViewColumn(title="Morale", column=7)
            self.treeviewCurrent.append_column(treeviewcolumn)

            treeviewcolumn = widgets.TreeViewColumn(title="Name", column=1)
            self.treeviewAvailable.append_column(treeviewcolumn)
            treeviewcolumn = widgets.TreeViewColumn(title="Age", column=2)
            self.treeviewAvailable.append_column(treeviewcolumn)
            treeviewcolumn = widgets.TreeViewColumn(title="Rating", column=3)
            self.treeviewAvailable.append_column(treeviewcolumn)
            treeviewcolumn = widgets.TreeViewColumn(title="Speciality", column=4)
            self.treeviewAvailable.append_column(treeviewcolumn)
            treeviewcolumn = widgets.TreeViewColumn(title="Wage", column=5)
            self.treeviewAvailable.append_column(treeviewcolumn)
            treeviewcolumn = widgets.TreeViewColumn(title="Contract", column=6)
            self.treeviewAvailable.append_column(treeviewcolumn)

            self.buttonHire.connect("clicked", self.staff_hire)
            self.buttonFire.connect("clicked", self.staff_fire)
            self.buttonRenewContract.connect("clicked", self.renew_contract)
            self.buttonImproveWage.connect("clicked", self.improve_wage)

        def staff_hire(self, button):
            model, treeiter = self.treeselectionAvailable.get_selected()

            if treeiter:
                coachid = model[treeiter][0]
                club = game.clubs[game.teamid]
                coach = club.coaches_available[coachid]

                if coach.hire():
                    club.coaches_hired[coachid] = club.coaches_available[coachid]
                    del club.coaches_available[coachid]

                    self.populate_data()

        def staff_fire(self, button):
            model, treeiter = self.treeselectionCurrent.get_selected()

            if treeiter:
                staffid = model[treeiter][0]
                coach = game.clubs[game.teamid].coaches_hired[staffid]

                if coach.fire():
                    del game.clubs[game.teamid].coaches_hired[staffid]

                    self.populate_data()

        def renew_contract(self, button):
            model, treeiter = self.treeselectionCurrent.get_selected()

            if treeiter:
                staffid = model[treeiter][0]
                coach = game.clubs[game.teamid].coaches_hired[staffid]

                if coach.renew_contract():
                    self.populate_data()

        def improve_wage(self, button):
            model, treeiter = self.treeselectionCurrent.get_selected()

            if treeiter:
                staffid = model[treeiter][0]
                coach = game.clubs[game.teamid].coaches_hired[staffid]

                if coach.improve_wage():
                    self.populate_data()

        def populate_data(self):
            self.liststoreAvailable.clear()
            self.liststoreCurrent.clear()

            for coachid, coach in game.clubs[game.teamid].coaches_available.items():
                ability = constants.ability[coach.ability]
                speciality = constants.speciality[coach.speciality]
                wage = "%s" % (display.currency(coach.wage))
                contract = coach.get_contract()

                self.liststoreAvailable.append([coachid,
                                                coach.name,
                                                coach.age,
                                                ability,
                                                speciality,
                                                wage,
                                                contract])

            for coachid, coach in game.clubs[game.teamid].coaches_hired.items():
                ability = constants.ability[coach.ability]
                speciality = constants.speciality[coach.speciality]
                wage = "%s" % (display.currency(coach.wage))
                contract = coach.get_contract()
                morale = coach.get_morale()

                self.liststoreCurrent.append([coachid,
                                              coach.name,
                                              coach.age,
                                              ability,
                                              speciality,
                                              wage,
                                              contract,
                                              morale])

        def run(self):
            self.populate_data()

            self.treeviewAvailable.set_cursor(0)

    class Scout(Interface):
        def __init__(self):
            Interface.__init__(self)

            self.liststoreAvailable = Gtk.ListStore(int, str, int, str, str, str)
            self.treeviewAvailable.set_model(self.liststoreAvailable)

            self.liststoreCurrent = Gtk.ListStore(int, str, int, str, str, str, str)
            self.treeviewCurrent.set_model(self.liststoreCurrent)

            treeviewcolumn = widgets.TreeViewColumn(title="Name", column=1)
            self.treeviewCurrent.append_column(treeviewcolumn)
            treeviewcolumn = widgets.TreeViewColumn(title="Age", column=2)
            self.treeviewCurrent.append_column(treeviewcolumn)
            treeviewcolumn = widgets.TreeViewColumn(title="Rating", column=3)
            self.treeviewCurrent.append_column(treeviewcolumn)
            treeviewcolumn = widgets.TreeViewColumn(title="Wage", column=4)
            self.treeviewCurrent.append_column(treeviewcolumn)
            treeviewcolumn = widgets.TreeViewColumn(title="Contract", column=5)
            self.treeviewCurrent.append_column(treeviewcolumn)
            treeviewcolumn = widgets.TreeViewColumn(title="Morale", column=6)
            self.treeviewCurrent.append_column(treeviewcolumn)

            treeviewcolumn = widgets.TreeViewColumn(title="Name", column=1)
            self.treeviewAvailable.append_column(treeviewcolumn)
            treeviewcolumn = widgets.TreeViewColumn(title="Age", column=2)
            self.treeviewAvailable.append_column(treeviewcolumn)
            treeviewcolumn = widgets.TreeViewColumn(title="Rating", column=3)
            self.treeviewAvailable.append_column(treeviewcolumn)
            treeviewcolumn = widgets.TreeViewColumn(title="Wage", column=4)
            self.treeviewAvailable.append_column(treeviewcolumn)
            treeviewcolumn = widgets.TreeViewColumn(title="Contract", column=5)
            self.treeviewAvailable.append_column(treeviewcolumn)

            self.buttonHire.connect("clicked", self.staff_hire)
            self.buttonFire.connect("clicked", self.staff_fire)
            self.buttonRenewContract.connect("clicked", self.renew_contract)
            self.buttonImproveWage.connect("clicked", self.improve_wage)

        def staff_hire(self, button):
            model, treeiter = self.treeselectionAvailable.get_selected()

            if treeiter:
                scoutid = model[treeiter][0]
                club = game.clubs[game.teamid]
                scout = club.scouts_available[scoutid]

                if scout.hire():
                    club.scouts_hired[scoutid] = club.scouts_available[scoutid]
                    del club.scouts_available[scoutid]

                    self.populate_data()

        def staff_fire(self, button):
            model, treeiter = self.treeselectionCurrent.get_selected()

            if treeiter:
                staffid = model[treeiter][0]
                scout = game.clubs[game.teamid].scouts_hired[staffid]

                if scout.fire():
                    del game.clubs[game.teamid].scouts_hired[staffid]

                    self.populate_data()

        def renew_contract(self, button):
            model, treeiter = self.treeselectionCurrent.get_selected()

            if treeiter:
                staffid = model[treeiter][0]
                scout = game.clubs[game.teamid].scouts_hired[staffid]

                if scout.renew_contract():
                    self.populate_data()

        def improve_wage(self, button):
            model, treeiter = self.treeselectionCurrent.get_selected()

            if treeiter:
                staffid = model[treeiter][0]
                scout = game.clubs[game.teamid].scouts_hired[staffid]

                if scout.improve_wage():
                    self.populate_data()

        def populate_data(self):
            self.liststoreAvailable.clear()
            self.liststoreCurrent.clear()

            for scoutid, scout in game.clubs[game.teamid].scouts_available.items():
                ability = constants.ability[scout.ability]
                wage = "%s" % (display.currency(scout.wage))
                contract = scout.get_contract()

                self.liststoreAvailable.append([scoutid,
                                                scout.name,
                                                scout.age,
                                                ability,
                                                wage,
                                                contract])

            for scoutid, scout in game.clubs[game.teamid].scouts_hired.items():
                ability = constants.ability[scout.ability]
                wage = "%s" % (display.currency(scout.wage))
                contract = scout.get_contract()
                morale = scout.get_morale()

                self.liststoreCurrent.append([scoutid,
                                              scout.name,
                                              scout.age,
                                              ability,
                                              wage,
                                              contract,
                                              morale])

        def run(self):
            self.populate_data()

            self.treeviewAvailable.set_cursor(0)

    def __init__(self):
        Gtk.Grid.__init__(self)

        notebook = Gtk.Notebook()
        self.attach(notebook, 0, 0, 1, 1)

        self.coach = self.Coach()
        label = widgets.Label("_Coach")
        notebook.append_page(self.coach, label)

        self.scout = self.Scout()
        label = widgets.Label("_Scout")
        notebook.append_page(self.scout, label)

    def run(self):
        self.coach.run()
        self.scout.run()

        self.show_all()
