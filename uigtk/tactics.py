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
import structures.formations
import uigtk.widgets


class Tactics(uigtk.widgets.Grid):
    __name__ = "tactics"

    club = None

    def __init__(self):
        uigtk.widgets.Grid.__init__(self)

        self.formations = Formations()
        self.attach(self.formations, 0, 0, 1, 1)

        self.styles = Styles()
        self.attach(self.styles, 0, 1, 1, 1)

        self.responsibilities = Responsibilities()
        self.attach(self.responsibilities, 0, 2, 1, 1)

        self.bonuses = Bonuses()
        self.attach(self.bonuses, 0, 3, 1, 1)

    def populate_data(self):
        self.formations.set_formation()
        self.responsibilities.set_responsibilities()
        self.styles.set_styles()
        self.bonuses.set_bonus()

    def run(self):
        Tactics.club = data.clubs.get_club_by_id(data.user.team)

        self.responsibilities.update_players_list()
        self.populate_data()

        self.show_all()


class Formations(uigtk.widgets.CommonFrame):
    def __init__(self):
        uigtk.widgets.CommonFrame.__init__(self, "Formation")

        label = uigtk.widgets.Label("_Team Formation")
        self.grid.attach(label, 0, 0, 1, 1)

        self.comboboxFormation = Gtk.ComboBoxText()
        self.comboboxFormation.set_tooltip_text("Set formation that the team will play.")
        self.comboboxFormation.connect("changed", self.on_formation_changed)
        label.set_mnemonic_widget(self.comboboxFormation)
        self.grid.attach(self.comboboxFormation, 1, 0, 1, 1)

        formations = structures.formations.Formations()

        for count, formation in enumerate(formations.get_formation_names()):
            self.comboboxFormation.append(str(count), formation)

    def on_formation_changed(self, combobox):
        '''
        Update formation for team when combobox is changed.
        '''
        Tactics.club.tactics.formationid = int(self.comboboxFormation.get_active_id())

    def set_formation(self):
        self.comboboxFormation.set_active(Tactics.club.tactics.formationid)


class Styles(uigtk.widgets.CommonFrame):
    def __init__(self):
        uigtk.widgets.CommonFrame.__init__(self, "Style")

        self.checkbuttonOffsideTrap = uigtk.widgets.CheckButton("Play _Offside Trap")
        self.checkbuttonOffsideTrap.set_tooltip_text("Attempt to subdue attacks by playing opposition offside.")
        self.checkbuttonOffsideTrap.connect("toggled", self.on_offside_trap_changed)
        self.grid.attach(self.checkbuttonOffsideTrap, 0, 0, 2, 1)

        label = uigtk.widgets.Label("_Tackling Style", leftalign=True)
        self.grid.attach(label, 0, 1, 1, 1)

        radiobuttonSoftTackling = uigtk.widgets.RadioButton("Soft Tackling")
        radiobuttonSoftTackling.style = 0
        radiobuttonSoftTackling.set_tooltip_text("Utilise soft tackling to reduce fouls.")
        radiobuttonSoftTackling.connect("toggled", self.on_tackling_style_changed)
        label.set_mnemonic_widget(radiobuttonSoftTackling)
        self.grid.attach(radiobuttonSoftTackling, 1, 1, 1, 1)
        radiobuttonNormalTackling = uigtk.widgets.RadioButton("Normal Tackling")
        radiobuttonNormalTackling.join_group(radiobuttonSoftTackling)
        radiobuttonNormalTackling.set_active(True)
        radiobuttonNormalTackling.style = 1
        radiobuttonNormalTackling.set_tooltip_text("Utilise normal tackling to balance successful tackles with fouls.")
        radiobuttonNormalTackling.connect("toggled", self.on_tackling_style_changed)
        self.grid.attach(radiobuttonNormalTackling, 2, 1, 1, 1)
        radiobuttonHardTackling = uigtk.widgets.RadioButton("Hard Tackling")
        radiobuttonHardTackling.join_group(radiobuttonSoftTackling)
        radiobuttonHardTackling.style = 2
        radiobuttonHardTackling.set_tooltip_text("Utilise hard tackling to increase number of successful tackles.")
        radiobuttonHardTackling.connect("toggled", self.on_tackling_style_changed)
        self.grid.attach(radiobuttonHardTackling, 3, 1, 1, 1)

        self.tackling = (radiobuttonSoftTackling,
                         radiobuttonNormalTackling,
                         radiobuttonHardTackling)

        label = uigtk.widgets.Label("Pa_ssing Style", leftalign=True)
        self.grid.attach(label, 0, 2, 1, 1)

        radiobuttonDirectPassing = uigtk.widgets.RadioButton("Direct Passing")
        radiobuttonDirectPassing.style = 0
        radiobuttonDirectPassing.set_tooltip_text("Aim to pass balls forward at an early opportunity.")
        radiobuttonDirectPassing.connect("toggled", self.on_passing_style_changed)
        label.set_mnemonic_widget(radiobuttonDirectPassing)
        self.grid.attach(radiobuttonDirectPassing, 1, 2, 1, 1)
        radiobuttonLongBallPassing = uigtk.widgets.RadioButton("Long Ball Passing")
        radiobuttonLongBallPassing.join_group(radiobuttonDirectPassing)
        radiobuttonLongBallPassing.style = 1
        radiobuttonLongBallPassing.set_tooltip_text("Aim to loft balls high up the field.")
        radiobuttonLongBallPassing.connect("toggled", self.on_passing_style_changed)
        self.grid.attach(radiobuttonLongBallPassing, 2, 2, 1, 1)
        radiobuttonShortPassing = uigtk.widgets.RadioButton("Short Passing")
        radiobuttonShortPassing.join_group(radiobuttonDirectPassing)
        radiobuttonShortPassing.style = 2
        radiobuttonShortPassing.set_tooltip_text("Aim to play short passes to nearby team-mates.")
        radiobuttonShortPassing.connect("toggled", self.on_passing_style_changed)
        self.grid.attach(radiobuttonShortPassing, 3, 2, 1, 1)

        self.passing = (radiobuttonDirectPassing,
                        radiobuttonLongBallPassing,
                        radiobuttonShortPassing)

        label = uigtk.widgets.Label("_Playing Style", leftalign=True)
        self.grid.attach(label, 0, 3, 1, 1)

        radiobuttonDefensivePlay = uigtk.widgets.RadioButton("Defensive")
        radiobuttonDefensivePlay.style = 0
        radiobuttonDefensivePlay.set_tooltip_text("Sit back defensively allowing opposition team to bring ball forward.")
        radiobuttonDefensivePlay.connect("toggled", self.on_playing_style_changed)
        label.set_mnemonic_widget(radiobuttonDefensivePlay)
        self.grid.attach(radiobuttonDefensivePlay, 1, 3, 1, 1)
        radiobuttonNormalPlay = uigtk.widgets.RadioButton("Normal")
        radiobuttonNormalPlay.join_group(radiobuttonDefensivePlay)
        radiobuttonNormalPlay.set_active(True)
        radiobuttonNormalPlay.style = 1
        radiobuttonNormalPlay.set_tooltip_text("Try to find balance between defensive and attacking play.")
        radiobuttonNormalPlay.connect("toggled", self.on_playing_style_changed)
        self.grid.attach(radiobuttonNormalPlay, 2, 3, 1, 1)
        radiobuttonAttackingPlay = uigtk.widgets.RadioButton("Attacking")
        radiobuttonAttackingPlay.join_group(radiobuttonDefensivePlay)
        radiobuttonAttackingPlay.style = 2
        radiobuttonAttackingPlay.set_tooltip_text("Attack opposition team at every opportunity.")
        radiobuttonAttackingPlay.connect("toggled", self.on_playing_style_changed)
        self.grid.attach(radiobuttonAttackingPlay, 3, 3, 1, 1)

        self.playing = (radiobuttonDefensivePlay,
                        radiobuttonNormalPlay,
                        radiobuttonAttackingPlay)

    def on_offside_trap_changed(self, checkbutton):
        '''
        Update option to play offside trap.
        '''
        Tactics.club.tactics.offside_trap = checkbutton.get_active()

    def on_tackling_style_changed(self, radiobutton):
        '''
        Update tackling style used by team.
        '''
        if radiobutton.get_active():
            Tactics.club.tactics.tackling_style = radiobutton.style

    def on_passing_style_changed(self, radiobutton):
        '''
        Update passing style used by team.
        '''
        if radiobutton.get_active():
            Tactics.club.tactics.passing_style = radiobutton.style

    def on_playing_style_changed(self, radiobutton):
        '''
        Update playing style used by team.
        '''
        if radiobutton.get_active():
            Tactics.club.tactics.playing_style = radiobutton.style

    def set_styles(self):
        self.checkbuttonOffsideTrap.set_active(Tactics.club.tactics.offside_trap)

        self.tackling[Tactics.club.tactics.tackling_style].set_active(True)
        self.passing[Tactics.club.tactics.passing_style].set_active(True)
        self.playing[Tactics.club.tactics.playing_style].set_active(True)


class Responsibilities(uigtk.widgets.CommonFrame):
    def __init__(self):
        uigtk.widgets.CommonFrame.__init__(self, "Responsibilities")

        self.selectors = []

        label = uigtk.widgets.Label("_Captain", leftalign=True)
        self.grid.attach(label, 0, 0, 1, 1)
        self.comboboxCaptain = Selector()
        self.comboboxCaptain.set_active(0)
        self.comboboxCaptain.set_tooltip_text("Define the captain of the team.")
        self.comboboxCaptain.connect("changed", self.on_captain_changed)
        label.set_mnemonic_widget(self.comboboxCaptain)
        self.grid.attach(self.comboboxCaptain, 1, 0, 1, 1)
        self.selectors.append(self.comboboxCaptain)

        label = uigtk.widgets.Label("_Penalty Taker", leftalign=True)
        self.grid.attach(label, 0, 1, 1, 1)
        self.comboboxPenaltyTaker = Selector()
        self.comboboxPenaltyTaker.set_active(0)
        self.comboboxPenaltyTaker.set_tooltip_text("Define main taker of penalties.")
        label.set_mnemonic_widget(self.comboboxPenaltyTaker)
        self.grid.attach(self.comboboxPenaltyTaker, 1, 1, 1, 1)
        self.selectors.append(self.comboboxPenaltyTaker)

        label = uigtk.widgets.Label("_Free Kick Taker", leftalign=True)
        self.grid.attach(label, 0, 2, 1, 1)
        self.comboboxFreeKickTaker = Selector()
        self.comboboxFreeKickTaker.set_active(0)
        self.comboboxFreeKickTaker.set_tooltip_text("Define main taker of free kicks.")
        label.set_mnemonic_widget(self.comboboxFreeKickTaker)
        self.grid.attach(self.comboboxFreeKickTaker, 1, 2, 1, 1)
        self.selectors.append(self.comboboxFreeKickTaker)

        label = uigtk.widgets.Label("_Corner Taker", leftalign=True)
        self.grid.attach(label, 0, 3, 1, 1)
        self.comboboxCornerTaker = Selector()
        self.comboboxCornerTaker.set_active(0)
        self.comboboxCornerTaker.set_tooltip_text("Define main taker of corner kicks.")
        label.set_mnemonic_widget(self.comboboxCornerTaker)
        self.grid.attach(self.comboboxCornerTaker, 1, 3, 1, 1)
        self.selectors.append(self.comboboxCornerTaker)

    def update_players_list(self):
        '''
        Update list of players that are selectable.
        '''
        for selector in self.selectors:
            selector.populate_items()

    def on_captain_changed(self, combobox):
        '''
        Update selected team captain.
        '''
        if combobox.get_active_id():
            Tactics.club.tactics.captain = int(combobox.get_active_id())

    def on_penalty_taker_changed(self, combobox):
        '''
        Update selected penalty taker.
        '''
        if combobox.get_active_id():
            Tactics.club.tactics.penalty_taker = int(combobox.get_active_id())

    def on_free_kick_taker_changed(self, combobox):
        '''
        Update selected free kick taker.
        '''
        if combobox.get_active_id():
            Tactics.club.tactics.free_kick_taker = int(combobox.get_active_id())

    def on_corner_taker_changed(self, combobox):
        '''
        Update selected corner kick taker.
        '''
        if combobox.get_active_id():
            Tactics.club.tactics.corner_taker = int(combobox.get_active_id())

    def set_responsibilities(self):
        if not self.comboboxCaptain.set_active_id(str(Tactics.club.tactics.captain)):
            self.comboboxCaptain.set_active(0)
            Tactics.club.tactics.captain = None

        if not self.comboboxPenaltyTaker.set_active_id(str(Tactics.club.tactics.penalty_taker)):
            self.comboboxPenaltyTaker.set_active(0)
            Tactics.club.tactics.penalty_taker = None

        if not self.comboboxFreeKickTaker.set_active_id(str(Tactics.club.tactics.free_kick_taker)):
            self.comboboxFreeKickTaker.set_active(0)
            Tactics.club.tactics.free_kick_taker = None

        if not self.comboboxCornerTaker.set_active_id(str(Tactics.club.tactics.corner_taker)):
            self.comboboxCornerTaker.set_active(0)
            Tactics.club.tactics.corner_taker = None


class Bonuses(uigtk.widgets.CommonFrame):
    def __init__(self):
        uigtk.widgets.CommonFrame.__init__(self, "Bonuses")

        label = uigtk.widgets.Label("_Win Bonus", leftalign=True)
        self.grid.attach(label, 0, 0, 1, 1)
        self.comboboxBonus = Gtk.ComboBoxText()
        self.comboboxBonus.append("0", "None")
        self.comboboxBonus.append("1", "10%")
        self.comboboxBonus.append("2", "30%")
        self.comboboxBonus.append("3", "50%")
        self.comboboxBonus.connect("changed", self.on_bonus_changed)
        self.grid.attach(self.comboboxBonus, 1, 0, 1, 1)

    def on_bonus_changed(self, combobox):
        '''
        Update bonus to be paid on win in next match.
        '''
        club = data.clubs.get_club_by_id(data.user.team)

        if combobox.get_active_id() != "0":
            club.tactics.bonus = int(combobox.get_active_id())
        else:
            club.tactics.bonus = None

    def set_bonus(self):
        '''
        Set win bonus for next match.
        '''
        club = data.clubs.get_club_by_id(data.user.team)

        if club.tactics.bonus:
            self.comboboxBonus.set_active_id(str(club.tactics.bonus))
        else:
            self.comboboxBonus.set_active_id("0")


class Selector(uigtk.widgets.ComboBox):
    def __init__(self):
        self.liststore = Gtk.ListStore(str, str)

        uigtk.widgets.ComboBox.__init__(self, column=1)
        self.set_model(self.liststore)
        self.set_id_column(0)

    def populate_items(self):
        club = data.clubs.get_club_by_id(data.user.team)

        self.liststore.clear()

        self.liststore.insert(0, [None, "Not Selected"])

        for playerid in club.squad.teamselection.get_team_ids():
            player = data.players.get_player_by_id(playerid)
            self.liststore.append([str(playerid), player.get_name()])
