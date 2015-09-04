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
import individualtraining
import money
import teamtraining
import trainingcamp
import user
import widgets


class IndividualTraining(Gtk.Grid):
    __name__ = "indtraining"

    def __init__(self):
        Gtk.Grid.__init__(self)
        self.set_row_spacing(5)

        self.infobar = Gtk.InfoBar()
        self.infobar.set_message_type(Gtk.MessageType.WARNING)
        label = Gtk.Label("There is no individual training assigned in the team training schedule. Individual training time must be allocated for players to improve.")
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

        self.liststore = Gtk.ListStore(int, str, str, str, str, int, int, str)
        treemodelsort = Gtk.TreeModelSort(self.liststore)
        treemodelsort.set_sort_column_id(1, Gtk.SortType.ASCENDING)

        self.treeview = Gtk.TreeView()
        self.treeview.set_model(treemodelsort)
        self.treeview.set_enable_search(False)
        self.treeview.set_search_column(-1)
        self.treeselection = self.treeview.get_selection()
        self.treeselection.connect("changed", self.selection_changed)
        self.overlay.add(self.treeview)

        treeviewcolumn = widgets.TreeViewColumn(title="Name", column=1)
        self.treeview.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Coach", column=2)
        self.treeview.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Skill", column=3)
        self.treeview.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Intensity", column=4)
        self.treeview.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Start Value", column=5)
        self.treeview.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Current Value", column=6)
        self.treeview.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Notes", column=7)
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

                skills = player.get_skills()
                start_value = skills[skill]
            else:
                skill = 9
                start_value = player.fitness

            intensity = training[3]

            club = game.clubs[game.teamid]

            individual_training = individualtraining.IndividualTraining()
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

        club = user.get_user_club()

        for playerid, item in club.individual_training.individual_training.items():
            player = game.players[playerid]

            skills = player.get_skills()

            name = player.get_name()
            coachid = int(item.coachid)
            coach = club.coaches_hired[coachid].name

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
                                   current,
                                   ""])

    def run(self):
        self.populate_data()

        self.show_all()

        club = user.get_user_club()

        if 1 in club.team_training.training:
            self.infobar.hide()

        sensitive = club.coaches.get_number_of_coaches() > 0
        self.treeview.set_sensitive(sensitive)
        self.buttonAdd.set_sensitive(sensitive)

        if sensitive:
            self.labelNoStaff.hide()
