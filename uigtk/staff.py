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

import data
import structures.ability
import structures.morale
import structures.speciality
import uigtk.widgets


class Interface(Gtk.Grid):
    '''
    Shared interface used by both scout and coach pages.
    '''
    def __init__(self):
        Gtk.Grid.__init__(self)
        self.set_vexpand(True)
        self.set_hexpand(True)
        self.set_border_width(5)
        self.set_row_spacing(5)

        commonframe = uigtk.widgets.CommonFrame("Hired")
        self.attach(commonframe, 0, 0, 1, 1)

        scrolledwindow = uigtk.widgets.ScrolledWindow()
        scrolledwindow.set_vexpand(True)
        scrolledwindow.set_hexpand(True)
        commonframe.insert(scrolledwindow)

        self.treeviewHired = uigtk.widgets.TreeView()
        self.treeviewHired.treeselection.connect("changed", self.on_hired_selection_changed)
        scrolledwindow.add(self.treeviewHired)

        commonframe = uigtk.widgets.CommonFrame("Available")
        self.attach(commonframe, 0, 1, 1, 1)

        scrolledwindow = uigtk.widgets.ScrolledWindow()
        scrolledwindow.set_vexpand(True)
        scrolledwindow.set_hexpand(True)
        commonframe.insert(scrolledwindow)

        self.treeviewAvailable = uigtk.widgets.TreeView()
        self.treeviewAvailable.treeselection.connect("changed", self.on_available_selection_changed)
        scrolledwindow.add(self.treeviewAvailable)

        buttonbox = uigtk.widgets.ButtonBox()
        buttonbox.set_hexpand(True)
        buttonbox.set_layout(Gtk.ButtonBoxStyle.END)
        self.attach(buttonbox, 0, 2, 1, 1)

        self.buttonHire = uigtk.widgets.Button("_Hire")
        self.buttonHire.set_tooltip_text("Hire selected staff member.")
        buttonbox.add(self.buttonHire)
        self.buttonFire = uigtk.widgets.Button("_Fire")
        self.buttonFire.set_sensitive(False)
        self.buttonFire.set_tooltip_text("Fire selected staff member.")
        buttonbox.add(self.buttonFire)
        self.buttonRenewContract = uigtk.widgets.Button("_Renew Contract")
        self.buttonRenewContract.set_sensitive(False)
        self.buttonRenewContract.set_tooltip_text("Negotiate contract renewal for selected staff member.")
        buttonbox.add(self.buttonRenewContract)
        self.buttonImproveWage = uigtk.widgets.Button("_Improve Wage")
        self.buttonImproveWage.set_sensitive(False)
        self.buttonImproveWage.set_tooltip_text("Improve wage for selected staff member.")
        buttonbox.add(self.buttonImproveWage)

    def on_available_selection_changed(self, treeselection):
        selected = treeselection.count_selected_rows() > 0

        if selected:
            self.treeviewHired.treeselection.unselect_all()

        self.buttonHire.set_sensitive(selected)

    def on_hired_selection_changed(self, treeselection):
        selected = treeselection.count_selected_rows() > 0

        if selected:
            self.treeviewAvailable.treeselection.unselect_all()

        self.buttonFire.set_sensitive(selected)
        self.buttonRenewContract.set_sensitive(selected)
        self.buttonImproveWage.set_sensitive(selected)

    def run(self):
        self.show_all()


class Staff(Gtk.Grid):
    __name__ = "staff"

    class Coach(Interface):
        def __init__(self):
            Interface.__init__(self)

            self.liststoreAvailable = Gtk.ListStore(int, str, int, str, str, str, str)
            self.treeviewAvailable.set_model(self.liststoreAvailable)

            self.liststoreHired = Gtk.ListStore(int, str, int, str, str, str, str, str, str)
            self.treeviewHired.set_model(self.liststoreHired)

            treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Name",
                                                          column=1)
            self.treeviewHired.append_column(treeviewcolumn)
            treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Age",
                                                          column=2)
            self.treeviewHired.append_column(treeviewcolumn)
            treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Ability",
                                                          column=3)
            self.treeviewHired.append_column(treeviewcolumn)
            treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Speciality",
                                                          column=4)
            self.treeviewHired.append_column(treeviewcolumn)
            treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Wage",
                                                          column=5)
            self.treeviewHired.append_column(treeviewcolumn)
            treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Contract",
                                                          column=6)
            self.treeviewHired.append_column(treeviewcolumn)
            treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Morale",
                                                          column=7)
            self.treeviewHired.append_column(treeviewcolumn)
            treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Training Count",
                                                          column=8)
            self.treeviewHired.append_column(treeviewcolumn)

            treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Name",
                                                          column=1)
            self.treeviewAvailable.append_column(treeviewcolumn)
            treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Age",
                                                          column=2)
            self.treeviewAvailable.append_column(treeviewcolumn)
            treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Ability",
                                                          column=3)
            self.treeviewAvailable.append_column(treeviewcolumn)
            treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Speciality",
                                                          column=4)
            self.treeviewAvailable.append_column(treeviewcolumn)
            treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Wage",
                                                          column=5)
            self.treeviewAvailable.append_column(treeviewcolumn)
            treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Contract",
                                                          column=6)
            self.treeviewAvailable.append_column(treeviewcolumn)

            self.buttonHire.connect("clicked", self.on_hire_clicked)
            self.buttonFire.connect("clicked", self.on_fire_clicked)
            self.buttonRenewContract.connect("clicked", self.renew_contract)
            self.buttonImproveWage.connect("clicked", self.improve_wage)

        def on_hire_clicked(self, *args):
            model, treeiter = self.treeviewAvailable.treeselection.get_selected()

            if treeiter:
                coachid = model[treeiter][0]
                coach = self.club.coaches.available[coachid]

                dialog = HireStaff(name=coach.name, role="Coach")

                if dialog.show():
                    self.club.coaches.hire_staff(coachid)

                    self.populate_data()

        def on_fire_clicked(self, *args):
            model, treeiter = self.treeviewHired.treeselection.get_selected()

            if treeiter:
                coachid = model[treeiter][0]
                coach = self.club.coaches.hired[coachid]

                if coach.count_players_training() > 0:
                    dialog = FireStaffError(coach)
                else:
                    payout = coach.get_payout()
                    dialog = FireStaff(coach.name, payout)

                    if dialog.show():
                        if not self.club.accounts.request(payout):
                            uigtk.accounts.NotEnoughFunds()
                        else:
                            self.club.coaches.fire_staff(coachid)

                            self.populate_data()

        def renew_contract(self, button):
            model, treeiter = self.treeviewHired.treeselection.get_selected()

            if treeiter:
                coachid = model[treeiter][0]
                coach = self.club.coaches.hired[coachid]

                status = coach.get_renew_contract()

                if status != 0:
                    dialog = RenewContractError(coach.name, status)

                    return

                period = coach.get_contract_renewal_period()
                amount = coach.get_contract_renewal_amount()

                dialog = RenewContract(coach.name, period, amount)

                if dialog.show():
                    coach.wage = amount
                    coach.contract = period * 52

                    self.populate_data()

        def improve_wage(self, button):
            model, treeiter = self.treeviewHired.treeselection.get_selected()

            if treeiter:
                coachid = model[treeiter][0]
                coach = self.club.coaches.hired[coachid]

                amount = self.get_improve_wage_amount()

                dialog = ImproveWage(coach.name, amount)

                if dialog.show():
                    coach.wage = amount

                    self.populate_data()

        def populate_data(self):
            self.liststoreAvailable.clear()
            self.liststoreHired.clear()

            abilities = structures.ability.Ability()
            specialities = structures.speciality.Speciality()
            morale = structures.morale.StaffMorale()

            for coachid, coach in self.club.coaches.available.items():
                ability = abilities.get_ability_for_id(coach.ability)
                speciality = specialities.get_speciality_for_id(coach.speciality)
                wage = data.currency.get_currency(coach.wage, integer=True)

                self.liststoreAvailable.append([coachid,
                                                coach.name,
                                                coach.age,
                                                ability,
                                                speciality,
                                                wage,
                                                coach.get_contract_string()])

            for coachid, coach in self.club.coaches.hired.items():
                ability = abilities.get_ability_for_id(coach.ability)
                speciality = specialities.get_speciality_for_id(coach.speciality)
                wage = data.currency.get_currency(coach.wage, integer=True)

                self.liststoreHired.append([coachid,
                                            coach.name,
                                            coach.age,
                                            ability,
                                            speciality,
                                            wage,
                                            coach.get_contract_string(),
                                            morale.get_morale(coach.morale),
                                            "%s Players" % (coach.count_players_training())])

        def run(self):
            self.club = data.user.club
            self.populate_data()

            self.treeviewAvailable.set_cursor(0)

    class Scout(Interface):
        def __init__(self):
            Interface.__init__(self)

            self.liststoreAvailable = Gtk.ListStore(int, str, int, str, str, str)
            self.treeviewAvailable.set_model(self.liststoreAvailable)

            self.liststoreHired = Gtk.ListStore(int, str, int, str, str, str, str)
            self.treeviewHired.set_model(self.liststoreHired)

            treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Name",
                                                          column=1)
            self.treeviewHired.append_column(treeviewcolumn)
            treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Age",
                                                          column=2)
            self.treeviewHired.append_column(treeviewcolumn)
            treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Ability",
                                                          column=3)
            self.treeviewHired.append_column(treeviewcolumn)
            treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Wage",
                                                          column=4)
            self.treeviewHired.append_column(treeviewcolumn)
            treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Contract",
                                                          column=5)
            self.treeviewHired.append_column(treeviewcolumn)
            treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Morale",
                                                          column=6)
            self.treeviewHired.append_column(treeviewcolumn)

            treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Name",
                                                          column=1)
            self.treeviewAvailable.append_column(treeviewcolumn)
            treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Age",
                                                          column=2)
            self.treeviewAvailable.append_column(treeviewcolumn)
            treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Ability",
                                                          column=3)
            self.treeviewAvailable.append_column(treeviewcolumn)
            treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Wage",
                                                          column=4)
            self.treeviewAvailable.append_column(treeviewcolumn)
            treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Contract",
                                                          column=5)
            self.treeviewAvailable.append_column(treeviewcolumn)

            self.buttonHire.connect("clicked", self.on_hire_clicked)
            self.buttonFire.connect("clicked", self.on_fire_clicked)
            self.buttonRenewContract.connect("clicked", self.renew_contract)
            self.buttonImproveWage.connect("clicked", self.improve_wage)

        def on_hire_clicked(self, *args):
            model, treeiter = self.treeviewAvailable.treeselection.get_selected()

            if treeiter:
                scoutid = model[treeiter][0]
                scout = self.club.scouts.available[scoutid]

                dialog = HireStaff(name=scout.name, role="Scout")

                if dialog.show():
                    self.club.scouts.hire_staff(scoutid)

                    self.populate_data()

        def on_fire_clicked(self, *args):
            model, treeiter = self.treeviewHired.treeselection.get_selected()

            if treeiter:
                scoutid = model[treeiter][0]
                scout = self.club.scouts.hired[scoutid]

                dialog = FireStaff(scout.name, scout.get_payout())

                if dialog.show():
                    if not self.club.accounts.request(payout):
                        uigtk.accounts.NotEnoughFunds()
                    else:
                        self.club.scouts.fire_staff(scoutid)

                        self.populate_data()

        def renew_contract(self, button):
            model, treeiter = self.treeviewHired.treeselection.get_selected()

            if treeiter:
                scoutid = model[treeiter][0]
                scout = self.club.scouts.hired[scoutid]

                status = scout.get_renew_contract()

                if status != 0:
                    dialog = RenewContractError(scout.name, status)

                    return

                period = coach.get_contract_renewal_period()
                amount = coach.get_contract_renewal_amount()

                dialog = RenewContract(scout.name, period, amount)

                if dialog.show():
                    scout.contract = period * 52
                    scout.wage = amount

                    self.populate_data()

        def improve_wage(self, button):
            model, treeiter = self.treeviewHired.treeselection.get_selected()

            if treeiter:
                scoutid = model[treeiter][0]
                scout = self.club.scouts.hired[scoutid]

                amount = self.get_improve_wage_amount()

                dialog = ImproveWage(scout.name, amount)

                if dialog.show():
                    scout.wage = amount

                    self.populate_data()

        def populate_data(self):
            self.liststoreAvailable.clear()
            self.liststoreHired.clear()

            abilities = structures.ability.Ability()
            morale = structures.morale.StaffMorale()

            for scoutid, scout in self.club.scouts.available.items():
                ability = abilities.get_ability_for_id(scout.ability)
                wage = data.currency.get_currency(scout.wage, integer=True)

                self.liststoreAvailable.append([scoutid,
                                                scout.name,
                                                scout.age,
                                                ability,
                                                wage,
                                                scout.get_contract_string()])

            for scoutid, scout in self.club.scouts.hired.items():
                ability = abilities.get_ability_for_id(scout.ability)
                wage = data.currency.get_currency(scout.wage, integer=True)

                self.liststoreHired.append([scoutid,
                                            scout.name,
                                            scout.age,
                                            ability,
                                            wage,
                                            scout.get_contract_string(),
                                            morale.get_morale(scout.morale)])

        def run(self):
            self.club = data.user.club
            self.populate_data()

            self.treeviewAvailable.set_cursor(0)

    def __init__(self):
        Gtk.Grid.__init__(self)

        notebook = Gtk.Notebook()
        self.attach(notebook, 0, 0, 1, 1)

        self.coach = self.Coach()
        label = uigtk.widgets.Label("_Coach")
        notebook.append_page(self.coach, label)

        self.scout = self.Scout()
        label = uigtk.widgets.Label("_Scout")
        notebook.append_page(self.scout, label)

    def run(self):
        self.coach.run()
        self.scout.run()

        self.show_all()


class HireStaff(Gtk.MessageDialog):
    '''
    Message dialog displayed to confirm hiring of selected staff.
    '''
    def __init__(self, name, role):
        Gtk.MessageDialog.__init__(self)
        self.set_transient_for(data.window)
        self.set_modal(True)
        self.set_title("Hire Staff")
        self.set_markup("Hire %s for the role of %s?" % (name, role))
        self.set_property("message-type", Gtk.MessageType.QUESTION)
        self.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("_Hire", Gtk.ResponseType.OK)
        self.set_default_response(Gtk.ResponseType.CANCEL)

    def show(self):
        state = self.run() == Gtk.ResponseType.OK
        self.destroy()

        return state


class FireStaff(Gtk.MessageDialog):
    def __init__(self, name, payout):
        Gtk.MessageDialog.__init__(self)
        self.set_transient_for(data.window)
        self.set_modal(True)
        self.set_title("Fire Staff")
        self.set_property("message-type", Gtk.MessageType.QUESTION)
        self.set_markup("<span size='12000'><b>Terminate the contract of %s?</b></span>" % (name))
        self.format_secondary_text("The staff member will be paid %s to end the contract." % (data.currency.get_currency(payout, integer=True)))
        self.add_button("_Do Not Fire", Gtk.ResponseType.CANCEL)
        self.add_button("_Fire", Gtk.ResponseType.OK)
        self.set_default_response(Gtk.ResponseType.CANCEL)

    def show(self):
        state = self.run() == Gtk.ResponseType.OK
        self.destroy()

        return state


class FireStaffError(Gtk.MessageDialog):
    '''
    Message show when staff member can not be fired due to individual training.
    '''
    def __init__(self, coach):
        if coach.count_players_training() > 1:
            message = "%s is currently handling individual training for %i players." % (coach.name, coach.count_players_training())
        else:
            message = "%s is currently handling individual training for %i player." % (coach.name, coach.count_players_training())

        Gtk.MessageDialog.__init__(self)
        self.set_transient_for(data.window)
        self.set_modal(True)
        self.set_title("Fire Staff")
        self.set_markup("<span size='12000'><b>%s</b></span>" % (message))
        self.format_secondary_text("Please remove all players from their individual training roster.")
        self.set_property("message-type", Gtk.MessageType.ERROR)
        self.add_button("_Close", Gtk.ResponseType.CLOSE)
        self.connect("response", self.on_response)

        self.show()

    def on_response(self, *args):
        self.destroy()


class RenewContract(Gtk.MessageDialog):
    def __init__(self, name, period, amount):
        Gtk.MessageDialog.__init__(self)
        self.set_transient_for(data.window)
        self.set_modal(True)
        self.set_title("Hire Staff")
        self.set_property("message-type", Gtk.MessageType.QUESTION)
        self.set_markup("<span size='12000'><b>Do you want to renew the contract of %s?</b></span>" % (name))
        self.format_secondary_text("A demand of a %i year contract for %s per week has been made." % (period, data.currency.get_currency(amount, integer=True)))
        self.add_button("_Reject Contract", Gtk.ResponseType.CANCEL)
        self.add_button("_Accept Contract", Gtk.ResponseType.OK)
        self.set_default_response(Gtk.ResponseType.CANCEL)

    def show(self):
        state = self.run() == Gtk.ResponseType.OK
        self.destroy()

        return state


class RenewContractError(Gtk.MessageDialog):
    '''
    Error displayed when staff does not wish to renew contract.
    '''
    def __init__(self, name, status):
        if status == 1:
            message = "%s is not willing to negotiate a new contract at this time."
        elif status == 2:
            message = "%s is planning to retire at the end of his current contract."

        Gtk.MessageDialog.__init__(self)
        self.set_transient_for(data.window)
        self.set_modal(True)
        self.set_title("Renew Contract")
        self.set_markup(message % (name))
        self.add_button("_Close", Gtk.ResponseType.CLOSE)
        self.connect("response", self.on_response)

    def on_response(self, *args):
        self.destroy()


class ImproveWage(Gtk.MessageDialog):
    def __init__(self, name, amount):
        Gtk.MessageDialog.__init__(self)
        self.set_transient_for(data.window)
        self.set_modal(True)
        self.set_title("Improve Wage")
        self.set_property("message-type", Gtk.MessageType.QUESTION)
        self.set_markup("Offer improved wage of %s per week to %s?" % (data.currency.get_currency(amount, integer=True), name))
        self.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("_Improve Wage", Gtk.ResponseType.OK)
        self.set_default_response(Gtk.ResponseType.CANCEL)

    def show(self):
        state = self.run() == Gtk.ResponseType.OK
        self.destroy()

        return state
