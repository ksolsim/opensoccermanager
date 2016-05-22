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
from gi.repository import Gdk
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
        self.treeviewHired.connect("button-release-event", self.on_button_release_event)
        self.treeviewHired.connect("key-press-event", self.on_key_press_event)
        self.treeviewHired.treeselection.connect("changed", self.on_hired_selection_changed)
        scrolledwindow.add(self.treeviewHired)

        commonframe = uigtk.widgets.CommonFrame("Available")
        self.attach(commonframe, 0, 1, 1, 1)

        scrolledwindow = uigtk.widgets.ScrolledWindow()
        scrolledwindow.set_vexpand(True)
        scrolledwindow.set_hexpand(True)
        commonframe.insert(scrolledwindow)

        self.treeviewAvailable = uigtk.widgets.TreeView()
        self.treeviewAvailable.connect("row-activated", self.on_row_activated)
        self.treeviewAvailable.connect("button-release-event", self.on_button_release_event)
        self.treeviewAvailable.connect("key-press-event", self.on_key_press_event)
        self.treeviewAvailable.treeselection.connect("changed", self.on_available_selection_changed)
        scrolledwindow.add(self.treeviewAvailable)

        buttonbox = uigtk.widgets.ButtonBox()
        buttonbox.set_hexpand(True)
        buttonbox.set_layout(Gtk.ButtonBoxStyle.END)
        self.attach(buttonbox, 0, 2, 1, 1)

        self.buttonHire = uigtk.widgets.Button("_Hire")
        self.buttonHire.set_tooltip_text("Hire selected staff member.")
        self.buttonHire.connect("clicked", self.on_hire_clicked)
        buttonbox.add(self.buttonHire)
        self.buttonFire = uigtk.widgets.Button("_Fire")
        self.buttonFire.set_sensitive(False)
        self.buttonFire.set_tooltip_text("Fire selected staff member.")
        self.buttonFire.connect("clicked", self.on_fire_clicked)
        buttonbox.add(self.buttonFire)
        self.buttonRenewContract = uigtk.widgets.Button("_Renew Contract")
        self.buttonRenewContract.set_sensitive(False)
        self.buttonRenewContract.set_tooltip_text("Negotiate contract renewal for selected staff member.")
        self.buttonRenewContract.connect("clicked", self.on_renew_contract_clicked)
        buttonbox.add(self.buttonRenewContract)
        self.buttonImproveWage = uigtk.widgets.Button("_Improve Wage")
        self.buttonImproveWage.set_sensitive(False)
        self.buttonImproveWage.set_tooltip_text("Improve wage for selected staff member.")
        self.buttonImproveWage.connect("clicked", self.on_improve_wage_clicked)
        buttonbox.add(self.buttonImproveWage)

        self.contextmenu1 = ContextMenu1()
        self.contextmenu1.menuitemHire.connect("activate", self.on_hire_clicked)

        self.contextmenu2 = ContextMenu2()
        self.contextmenu2.menuitemFire.connect("activate", self.on_fire_clicked)
        self.contextmenu2.menuitemRenewContract.connect("activate", self.on_renew_contract_clicked)
        self.contextmenu2.menuitemImproveWage.connect("activate", self.on_improve_wage_clicked)

    def on_available_selection_changed(self, treeselection):
        '''
        Update button status for selected available staff.
        '''
        selected = treeselection.count_selected_rows() > 0

        if selected:
            self.treeviewHired.treeselection.unselect_all()

        self.buttonHire.set_sensitive(selected)

    def on_hired_selection_changed(self, treeselection):
        '''
        Update button statuses for selected hired staff.
        '''
        selected = treeselection.count_selected_rows() > 0

        if selected:
            self.treeviewAvailable.treeselection.unselect_all()

        self.buttonFire.set_sensitive(selected)
        self.buttonRenewContract.set_sensitive(selected)
        self.buttonImproveWage.set_sensitive(selected)
    
    def on_row_activated(self, *args):
        '''
        Handle row activation on staff member.
        '''
        self.on_hire_clicked()
    
    def on_hire_clicked(self, *args):
        '''
        Handle hiring of selected staff member.
        '''
        model, treeiter = self.treeviewAvailable.treeselection.get_selected()

        if treeiter:
            staffid = model[treeiter][0]
            staff = self.staff.available[staffid]

            dialog = HireStaff(name=staff.name, role=self.role)

            if dialog.show():
                self.staff.hire_staff(staffid)

                self.populate_data()
    
    def on_fire_clicked(self, *args):
        '''
        Handle firing of selected staff member.
        '''
        model, treeiter = self.treeviewHired.treeselection.get_selected()

        if treeiter:
            staffid = model[treeiter][0]
            staff = self.staff.hired[staffid]

            payout = staff.get_payout()
            dialog = FireStaff(staff.name, payout)

            if dialog.show():
                if not data.user.club.accounts.request(payout):
                    uigtk.accounts.NotEnoughFunds()
                else:
                    self.staff.fire_staff(staffid)

                    self.populate_data()

    def on_renew_contract_clicked(self, *args):
        '''
        Handle contract renewal of selected staff member.
        '''
        model, treeiter = self.treeviewHired.treeselection.get_selected()

        if treeiter:
            staffid = model[treeiter][0]
            staff = self.staff.hired[staffid]

            status = staff.get_renew_contract()

            if status != 0:
                dialog = RenewContractError(staff.name, status)

                return

            period = staff.get_contract_renewal_period()
            amount = staff.get_contract_renewal_amount()

            dialog = RenewContract(staff.name, period, amount)

            if dialog.show():
                staff.wage = amount
                staff.contract = period * 52

                self.populate_data()

    def on_improve_wage_clicked(self, *args):
        '''
        Handle wage improvement of selected staff member.
        '''
        model, treeiter = self.treeviewHired.treeselection.get_selected()

        if treeiter:
            staffid = model[treeiter][0]
            staff = self.staff.hired[staffid]

            amount = staff.get_improve_wage_amount()

            dialog = ImproveWage(staff.name, amount)

            if dialog.show():
                staff.wage = amount

                self.populate_data()
    
    def on_key_press_event(self, treeview, event):
        '''
        Handle button clicks on the treeview.
        '''
        if Gdk.keyval_name(event.keyval) == "Menu":
            event.button = 3
            self.on_context_menu_event(treeview, event)

    def on_button_release_event(self, treeview, event):
        '''
        Handle right-clicking on the treeview.
        '''
        if event.button == 3:
            self.on_context_menu_event(treeview, event)

    def on_context_menu_event(self, treeview, event):
        '''
        Display context menu for selected coach id.
        '''
        model, treeiter = treeview.treeselection.get_selected()

        if treeiter:
            staffid = model[treeiter][0]
                        
            if treeview is self.treeviewAvailable:
                staff = self.staff.available[staffid]
                contextmenu = self.contextmenu1
            else:
                staff = self.staff.hired[staffid]
                contextmenu = self.contextmenu2
            
            contextmenu.show(staff)
            contextmenu.popup(None,
                              None,
                              None,
                              None,
                              event.button,
                              event.time)

    def run(self):
        self.populate_data()

        self.treeviewAvailable.set_cursor(0)


class Staff(Gtk.Grid):
    __name__ = "staff"

    class Coach(Interface):
        class Columns:
            def __init__(self):
                self.columns = []

                treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Name",
                                                              column=1)
                self.columns.append(treeviewcolumn)
                treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Age",
                                                              column=2)
                self.columns.append(treeviewcolumn)
                treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Ability",
                                                              column=3)
                self.columns.append(treeviewcolumn)
                treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Speciality",
                                                              column=4)
                self.columns.append(treeviewcolumn)
                treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Wage",
                                                              column=5)
                self.columns.append(treeviewcolumn)
                treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Contract",
                                                              column=6)
                self.columns.append(treeviewcolumn)

        def __init__(self):
            Interface.__init__(self)

            self.liststoreAvailable = Gtk.ListStore(int, str, int, str, str, str, str)
            self.treeviewAvailable.set_model(self.liststoreAvailable)

            self.liststoreHired = Gtk.ListStore(int, str, int, str, str, str, str, str, str)
            self.treeviewHired.set_model(self.liststoreHired)

            columns = self.Columns()

            for column in columns.columns:
                self.treeviewHired.append_column(column)

            treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Morale",
                                                          column=7)
            self.treeviewHired.append_column(treeviewcolumn)
            treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Training Count",
                                                          column=8)
            self.treeviewHired.append_column(treeviewcolumn)

            columns = self.Columns()

            for column in columns.columns:
                self.treeviewAvailable.append_column(column)
        
        def on_fire_clicked(self, *args):
            '''
            Handle firing of selected staff member.
            '''
            model, treeiter = self.treeviewHired.treeselection.get_selected()

            if treeiter:
                staffid = model[treeiter][0]
                staff = self.staff.hired[staffid]

                if staff.count_players_training() > 0:
                    dialog = FireStaffError(staff)
                else:
                    payout = staff.get_payout()
                    dialog = FireStaff(staff.name, payout)

                    if dialog.show():
                        if not data.user.club.accounts.request(payout):
                            uigtk.accounts.NotEnoughFunds()
                        else:
                            self.staff.fire_staff(staffid)

                            self.populate_data()

        def populate_data(self):
            self.liststoreAvailable.clear()
            self.liststoreHired.clear()

            abilities = structures.ability.Ability()
            specialities = structures.speciality.Speciality()
            morale = structures.morale.StaffMorale()

            for coachid, coach in data.user.club.coaches.available.items():
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

            for coachid, coach in data.user.club.coaches.hired.items():
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

    class Scout(Interface):
        class Columns:
            def __init__(self):
                self.columns = []

                treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Name",
                                                              column=1)
                self.columns.append(treeviewcolumn)
                treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Age",
                                                              column=2)
                self.columns.append(treeviewcolumn)
                treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Ability",
                                                              column=3)
                self.columns.append(treeviewcolumn)
                treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Wage",
                                                              column=4)
                self.columns.append(treeviewcolumn)
                treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Contract",
                                                              column=5)
                self.columns.append(treeviewcolumn)

        def __init__(self):
            Interface.__init__(self)

            self.liststoreAvailable = Gtk.ListStore(int, str, int, str, str, str)
            self.treeviewAvailable.set_model(self.liststoreAvailable)

            self.liststoreHired = Gtk.ListStore(int, str, int, str, str, str, str)
            self.treeviewHired.set_model(self.liststoreHired)

            columns = self.Columns()

            for column in columns.columns:
                self.treeviewHired.append_column(column)

            treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Morale",
                                                          column=6)
            self.treeviewHired.append_column(treeviewcolumn)

            columns = self.Columns()

            for column in columns.columns:
                self.treeviewAvailable.append_column(column)

        def populate_data(self):
            self.liststoreAvailable.clear()
            self.liststoreHired.clear()

            abilities = structures.ability.Ability()
            morale = structures.morale.StaffMorale()

            for scoutid, scout in data.user.club.scouts.available.items():
                ability = abilities.get_ability_for_id(scout.ability)
                wage = data.currency.get_currency(scout.wage, integer=True)

                self.liststoreAvailable.append([scoutid,
                                                scout.name,
                                                scout.age,
                                                ability,
                                                wage,
                                                scout.get_contract_string()])

            for scoutid, scout in data.user.club.scouts.hired.items():
                ability = abilities.get_ability_for_id(scout.ability)
                wage = data.currency.get_currency(scout.wage, integer=True)

                self.liststoreHired.append([scoutid,
                                            scout.name,
                                            scout.age,
                                            ability,
                                            wage,
                                            scout.get_contract_string(),
                                            morale.get_morale(scout.morale)])

    def __init__(self):
        Gtk.Grid.__init__(self)

        notebook = Gtk.Notebook()
        self.attach(notebook, 0, 0, 1, 1)

        self.coach = self.Coach()
        self.coach.staff = data.user.club.coaches
        self.coach.role = "Coach"
        label = uigtk.widgets.Label("_Coach")
        notebook.append_page(self.coach, label)

        self.scout = self.Scout()
        self.scout.staff = data.user.club.scouts
        self.scout.role = "Scout"
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
    '''
    Message to confirm firing of staff member from club.
    '''
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
    '''
    Display contract renewal details for user.
    '''
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
    '''
    Message dialog for required wage improvement to be accepted.
    '''
    def __init__(self, name, amount):
        Gtk.MessageDialog.__init__(self)
        self.set_transient_for(data.window)
        self.set_modal(True)
        self.set_title("Improve Wage")
        self.set_property("message-type", Gtk.MessageType.QUESTION)
        self.set_markup("%s is requesting a wage of %s per week?" % (name, data.currency.get_currency(amount, integer=True)))
        self.add_button("_Reject Amount", Gtk.ResponseType.CANCEL)
        self.add_button("_Accept Amount", Gtk.ResponseType.OK)
        self.set_default_response(Gtk.ResponseType.CANCEL)

    def show(self):
        state = self.run() == Gtk.ResponseType.OK
        self.destroy()

        return state


class ContextMenu1(Gtk.Menu):
    '''
    Available staff listing context menu.
    '''
    def __init__(self):
        Gtk.Menu.__init__(self)

        self.menuitemHire = uigtk.widgets.MenuItem("_Hire Staff")
        self.append(self.menuitemHire)

    def show(self, staff):
        self.staff = staff

        self.show_all()


class ContextMenu2(Gtk.Menu):
    '''
    Hired staff listing context menu.
    '''
    def __init__(self):
        Gtk.Menu.__init__(self)

        self.menuitemFire = uigtk.widgets.MenuItem("_Fire Staff")
        self.append(self.menuitemFire)
        self.menuitemRenewContract = uigtk.widgets.MenuItem("_Renew Contract")
        self.append(self.menuitemRenewContract)
        self.menuitemImproveWage = uigtk.widgets.MenuItem("_Improve Wage")
        self.append(self.menuitemImproveWage)

    def show(self, staff):
        self.staff = staff

        self.show_all()
