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

            clubobj = user.get_user_club()

            for coachid, coach in clubobj.coaches.available.items():
                ability = constants.ability[coach.ability]
                speciality = constants.speciality[coach.speciality]
                wage = "%s" % (display.currency(coach.wage))

                self.liststoreAvailable.append([coachid,
                                                coach.name,
                                                coach.age,
                                                ability,
                                                speciality,
                                                wage,
                                                coach.get_contract_string()])

            for coachid, coach in clubobj.coaches.hired.items():
                ability = constants.ability[coach.ability]
                speciality = constants.speciality[coach.speciality]
                wage = "%s" % (display.currency(coach.wage))

                self.liststoreCurrent.append([coachid,
                                              coach.name,
                                              coach.age,
                                              ability,
                                              speciality,
                                              wage,
                                              coach.get_contract_string(),
                                              coach.get_morale_string()])

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

            clubobj = user.get_user_club()

            for scoutid, scout in clubobj.scouts.available.items():
                wage = "%s" % (display.currency(scout.wage))

                self.liststoreAvailable.append([scoutid,
                                                scout.name,
                                                scout.age,
                                                scout.get_ability_string(),
                                                wage,
                                                scout.get_contract_string()])

            for scoutid, scout in clubobj.scouts.hired.items():
                wage = "%s" % (display.currency(scout.wage))

                self.liststoreAvailable.append([scoutid,
                                                scout.name,
                                                scout.age,
                                                scout.get_ability_string(),
                                                wage,
                                                scout.get_contract_string(),
                                                scout.get_morale_string()])

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
