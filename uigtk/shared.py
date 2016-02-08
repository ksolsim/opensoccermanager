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
import uigtk.widgets


class FilterButtons(uigtk.widgets.ButtonBox):
    '''
    Shared combination of filter and reset buttons for list screens.
    '''
    def __init__(self):
        uigtk.widgets.ButtonBox.__init__(self)
        self.set_layout(Gtk.ButtonBoxStyle.END)

        self.buttonFilter = uigtk.widgets.Button("_Filter")
        self.buttonFilter.set_tooltip_text("Filter visible players according to criteria.")
        self.add(self.buttonFilter)

        self.buttonReset = uigtk.widgets.Button("_Reset")
        self.buttonReset.set_sensitive(False)
        self.buttonReset.set_tooltip_text("Reset any applied filters.")
        self.add(self.buttonReset)


class ColumnViews(uigtk.widgets.Grid):
    '''
    Selector for changing visible columns in list screens.
    '''
    def __init__(self):
        uigtk.widgets.Grid.__init__(self)

        label = uigtk.widgets.Label("_View")
        self.attach(label, 2, 0, 1, 1)
        self.comboboxView = Gtk.ComboBoxText()
        self.comboboxView.append("0", "Personal")
        self.comboboxView.append("1", "Skill")
        self.comboboxView.append("2", "Form")
        self.comboboxView.set_active(1)
        self.comboboxView.set_tooltip_text("Change visible columns of information.")
        label.set_mnemonic_widget(self.comboboxView)
        self.attach(self.comboboxView, 3, 0, 1, 1)


class TransferEnquiry(Gtk.MessageDialog):
    '''
    Message dialog base class confirming whether to approach for a player.
    '''
    def __init__(self):
        Gtk.MessageDialog.__init__(self)
        self.set_transient_for(data.window)
        self.set_modal(True)
        self.set_title("Transfer Offer")
        self.set_property("message-type", Gtk.MessageType.QUESTION)
        self.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("_Approach", Gtk.ResponseType.OK)
        self.set_default_response(Gtk.ResponseType.CANCEL)


class ContractNegotiation(Gtk.Dialog):
    '''
    Dialog to negotiate contract with provided player.
    '''
    def __init__(self):
        Gtk.Dialog.__init__(self)
        self.set_transient_for(data.window)
        self.set_modal(True)
        self.set_resizable(False)
        self.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        self.set_default_response(Gtk.ResponseType.CANCEL)
        self.vbox.set_border_width(5)
        self.vbox.set_spacing(5)

        self.labelContract = uigtk.widgets.Label(leftalign=True)
        self.vbox.add(self.labelContract)

        frame = uigtk.widgets.CommonFrame("Details")
        self.vbox.add(frame)

        label = uigtk.widgets.Label("_Weekly Wage", leftalign=True)
        frame.grid.attach(label, 0, 0, 1, 1)
        spinbuttonWage = uigtk.widgets.SpinButton(maximum=100000)
        label.set_mnemonic_widget(spinbuttonWage)
        #spinbuttonWage.set_value(wage)
        frame.grid.attach(spinbuttonWage, 1, 0, 1, 1)
        label = uigtk.widgets.Label("League _Champions Bonus", leftalign=True)
        frame.grid.attach(label, 0, 1, 1, 1)
        spinbuttonLeagueChampions = uigtk.widgets.SpinButton(maximum=200000)
        label.set_mnemonic_widget(spinbuttonLeagueChampions)
        #spinbuttonLeagueChampions.set_value(leaguewin)
        frame.grid.attach(spinbuttonLeagueChampions, 1, 1, 1, 1)
        label = uigtk.widgets.Label("League _Runner Up Bonus", leftalign=True)
        frame.grid.attach(label, 0, 2, 1, 1)
        spinbuttonLeagueRunnerUp = uigtk.widgets.SpinButton(maximum=200000)
        label.set_mnemonic_widget(spinbuttonLeagueRunnerUp)
        #spinbuttonLeagueRunnerUp.set_value(leaguerunnerup)
        frame.grid.attach(spinbuttonLeagueRunnerUp, 1, 2, 1, 1)
        label = uigtk.widgets.Label("_Win Bonus", leftalign=True)
        frame.grid.attach(label, 0, 3, 1, 1)
        spinbuttonWinBonus = uigtk.widgets.SpinButton(maximum=10000)
        label.set_mnemonic_widget(spinbuttonWinBonus)
        #spinbuttonWinBonus.set_value(winbonus)
        frame.grid.attach(spinbuttonWinBonus, 1, 3, 1, 1)
        label = uigtk.widgets.Label("_Goal Bonus", leftalign=True)
        frame.grid.attach(label, 0, 4, 1, 1)
        spinbuttonGoalBonus = uigtk.widgets.SpinButton(maximum=10000)
        label.set_mnemonic_widget(spinbuttonGoalBonus)
        #spinbuttonGoalBonus.set_value(goalbonus)
        frame.grid.attach(spinbuttonGoalBonus, 1, 4, 1, 1)
        label = uigtk.widgets.Label("_Contract Length", leftalign=True)
        frame.grid.attach(label, 0, 5, 1, 1)
        spinbuttonContract = Gtk.SpinButton.new_with_range(1, 5, 1)
        label.set_mnemonic_widget(spinbuttonContract)
        #spinbuttonContract.set_value(contract)
        frame.grid.attach(spinbuttonContract, 1, 5, 1, 1)

    def show(self, *args):
        self.show_all()

        state = self.run() == Gtk.ResponseType.OK
        self.destroy()

        return state
