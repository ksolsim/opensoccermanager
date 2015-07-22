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

import club
import constants
import display
import game
import user
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
        self.comboboxCaptain.connect("changed", self.captain_changed)
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
        self.comboboxPenaltyTaker.connect("changed", self.penalty_taker_changed)
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
        self.comboboxFreeKickTaker.connect("changed", self.free_kick_taker_changed)
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
        self.comboboxCornerTaker.connect("changed", self.corner_taker_changed)
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
            game.clubs[game.teamid].tactics.formation = model[treeiter][0]

    def captain_changed(self, combobox):
        treeiter = combobox.get_active_iter()

        if treeiter:
            model = combobox.get_model()
            game.clubs[game.teamid].tactics.captain = model[treeiter][0]

    def penalty_taker_changed(self, combobox):
        treeiter = combobox.get_active_iter()

        if treeiter:
            model = combobox.get_model()
            game.clubs[game.teamid].tactics.penalty_taker = model[treeiter][0]

    def free_kick_taker_changed(self, combobox):
        treeiter = combobox.get_active_iter()

        if treeiter:
            model = combobox.get_model()
            game.clubs[game.teamid].tactics.free_kick_taker = model[treeiter][0]

    def corner_taker_changed(self, combobox):
        treeiter = combobox.get_active_iter()

        if treeiter:
            model = combobox.get_model()
            game.clubs[game.teamid].tactics.corner_taker = model[treeiter][0]

    def style_changed(self, radiobutton, index):
        if radiobutton.get_active():
            game.clubs[game.teamid].tactics.style = index

    def tackling_changed(self, radiobutton, index):
        if radiobutton.get_active():
            game.clubs[game.teamid].tactics.tackling = index

    def passing_changed(self, radiobutton, index):
        if radiobutton.get_active():
            game.clubs[game.teamid].tactics.passing = index

    def bonus_changed(self, combobox):
        bonusid = combobox.get_active_id()

        game.clubs[game.teamid].tactics.win_bonus = int(bonusid)

    def run(self):
        self.liststoreFormation.clear()

        for index, item in enumerate(constants.formations):
            self.liststoreFormation.append([index, item[0]])

        self.liststoreCaptain.clear()
        self.liststorePenaltyTaker.clear()
        self.liststoreFreeKickTaker.clear()
        self.liststoreCornerTaker.clear()

        self.liststoreCaptain.append([None, "Not Selected"])
        self.liststorePenaltyTaker.append([None, "Not Selected"])
        self.liststoreFreeKickTaker.append([None, "Not Selected"])
        self.liststoreCornerTaker.append([None, "Not Selected"])

        self.comboboxCaptain.set_sensitive(False)
        self.comboboxPenaltyTaker.set_sensitive(False)
        self.comboboxFreeKickTaker.set_sensitive(False)
        self.comboboxCornerTaker.set_sensitive(False)

        club = user.get_user_club()

        for playerid in club.team.values():
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

        self.comboboxFormation.set_active(club.tactics.formation)

        captain = str(club.tactics.captain)

        if not self.comboboxCaptain.set_active_id(captain):
            self.comboboxCaptain.set_active(0)

        penaltytaker = str(club.tactics.penalty_taker)

        if not self.comboboxPenaltyTaker.set_active_id(penaltytaker):
            self.comboboxPenaltyTaker.set_active(0)

        freekicktaker = str(club.tactics.free_kick_taker)

        if not self.comboboxFreeKickTaker.set_active_id(freekicktaker):
            self.comboboxFreeKickTaker.set_active(0)

        cornertaker = str(club.tactics.corner_taker)

        if not self.comboboxCornerTaker.set_active_id(cornertaker):
            self.comboboxCornerTaker.set_active(0)

        self.style[club.tactics.style].set_active(True)
        self.tackling[club.tactics.tackling].set_active(True)
        self.passing[club.tactics.passing].set_active(True)

        self.comboboxWinBonus.set_active(club.tactics.win_bonus)

        self.show_all()
