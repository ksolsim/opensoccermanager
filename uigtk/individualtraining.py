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

import data
import structures.individualtraining
import structures.intensity
import structures.skills
import uigtk.widgets


class IndividualTraining(Gtk.Grid):
    __name__ = "individualtraining"

    def __init__(self):
        Gtk.Grid.__init__(self)
        self.set_row_spacing(5)

        self.infobar = Gtk.InfoBar()
        self.infobar.set_message_type(Gtk.MessageType.WARNING)
        label = Gtk.Label("There is no individual training time assigned in the team training schedule. Individual training time must be allocated for players to improve.")
        self.infobar.get_content_area().add(label)
        self.attach(self.infobar, 0, 0, 1, 1)

        scrolledwindow = uigtk.widgets.ScrolledWindow()
        self.attach(scrolledwindow, 0, 1, 1, 1)

        self.overlay = Gtk.Overlay()
        scrolledwindow.add(self.overlay)

        self.labelNoStaff = Gtk.Label("There are no coaches on staff. To assign players to individual training, at least one coach must be hired.")
        self.overlay.add_overlay(self.labelNoStaff)

        IndividualTraining.liststore = IndividualTrainingList()
        treemodelsort = Gtk.TreeModelSort(IndividualTraining.liststore)
        treemodelsort.set_sort_column_id(1, Gtk.SortType.ASCENDING)

        IndividualTraining.treeview = uigtk.widgets.TreeView()
        IndividualTraining.treeview.set_hexpand(True)
        IndividualTraining.treeview.set_vexpand(True)
        IndividualTraining.treeview.set_sensitive(False)
        IndividualTraining.treeview.set_model(treemodelsort)
        IndividualTraining.treeview.connect("row-activated", self.on_row_activated)
        IndividualTraining.treeview.connect("button-release-event", self.on_button_release_event)
        IndividualTraining.treeview.connect("key-press-event", self.on_key_press_event)
        IndividualTraining.treeview.treeselection.connect("changed", self.on_selection_changed)
        self.overlay.add(IndividualTraining.treeview)

        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Name", column=1)
        treeviewcolumn.set_expand(True)
        IndividualTraining.treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Coach", column=2)
        IndividualTraining.treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Skill", column=3)
        IndividualTraining.treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Intensity", column=4)
        IndividualTraining.treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Start Value", column=5)
        IndividualTraining.treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Current Value", column=6)
        IndividualTraining.treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Status", column=7)
        IndividualTraining.treeview.append_column(treeviewcolumn)

        buttonbox = uigtk.widgets.ButtonBox()
        buttonbox.set_layout(Gtk.ButtonBoxStyle.END)
        self.attach(buttonbox, 0, 2, 1, 1)

        self.buttonAddTraining = uigtk.widgets.Button("_Add Player")
        self.buttonAddTraining.set_sensitive(False)
        self.buttonAddTraining.set_tooltip_text("Add player to individual training.")
        self.buttonAddTraining.connect("clicked", self.on_add_clicked)
        buttonbox.add(self.buttonAddTraining)
        self.buttonEditTraining = uigtk.widgets.Button("_Edit Player")
        self.buttonEditTraining.set_sensitive(False)
        self.buttonEditTraining.set_tooltip_text("Edit individual training for selected player.")
        self.buttonEditTraining.connect("clicked", self.on_edit_clicked)
        buttonbox.add(self.buttonEditTraining)
        self.buttonRemoveTraining = uigtk.widgets.Button("_Remove Player")
        self.buttonRemoveTraining.set_sensitive(False)
        self.buttonRemoveTraining.set_tooltip_text("Remove selected player from individual training.")
        self.buttonRemoveTraining.connect("clicked", self.on_remove_clicked)
        buttonbox.add(self.buttonRemoveTraining)

        self.contextmenu = ContextMenu()

    def on_add_clicked(self, *args):
        '''
        Launch dialog for adding player to individual training.
        '''
        dialog = AddTraining()
        dialog.show()

        self.populate_data()

    def on_edit_clicked(self, *args):
        '''
        Display dialog to edit selected individual player training.
        '''
        model, treeiter = IndividualTraining.treeview.treeselection.get_selected()

        if treeiter:
            playerid = model[treeiter][0]

            training = data.user.club.individual_training.get_individual_training_by_playerid(playerid)

            dialog = EditTraining(training)
            dialog.show()

            self.populate_data()

    def on_remove_clicked(self, *args):
        '''
        Confirm from user to remove selected player from individual training.
        '''
        model, treeiter = IndividualTraining.treeview.treeselection.get_selected()
        playerid = model[treeiter][0]

        dialog = RemoveTraining(playerid)

        if dialog.show():
            data.user.club.individual_training.remove_from_training(playerid)

            self.populate_data()

    def on_row_activated(self, *args):
        '''
        Handle double-click on row in treeview.
        '''
        self.on_edit_clicked()

    def on_button_release_event(self, treeview, event):
        '''
        Handle right-clicking on the treeview.
        '''
        if event.button == 3:
            self.on_context_menu_event(event)

    def on_key_press_event(self, treeview, event):
        '''
        Handle button clicks on the treeview.
        '''
        if Gdk.keyval_name(event.keyval) == "Menu":
            event.button = 3
            self.on_context_menu_event(event)
        elif Gdk.keyval_name(event.keyval) == "Delete":
            self.on_remove_clicked()

    def on_context_menu_event(self, event):
        '''
        Display context menu for selected player id.
        '''
        model, treeiter = IndividualTraining.treeview.treeselection.get_selected()

        if treeiter:
            playerid = model[treeiter][0]

            player = data.players.get_player_by_id(playerid)

            self.contextmenu.show(player)
            self.contextmenu.popup(None,
                                   None,
                                   None,
                                   None,
                                   event.button,
                                   event.time)

    def on_selection_changed(self, treeselection):
        '''
        Update button sensitivity on row change.
        '''
        model, treeiter = treeselection.get_selected()

        if treeiter:
            self.buttonEditTraining.set_sensitive(True)
            self.buttonRemoveTraining.set_sensitive(True)
        else:
            self.buttonEditTraining.set_sensitive(False)
            self.buttonRemoveTraining.set_sensitive(False)

    def populate_data(self):
        IndividualTraining.liststore.update()

    def run(self):
        self.populate_data()
        self.show_all()

        individual = data.user.club.team_training.get_individual_set()
        self.infobar.set_visible(not individual)

        state = data.user.club.coaches.get_staff_count() > 0
        self.buttonAddTraining.set_sensitive(state)
        IndividualTraining.treeview.set_sensitive(state)
        self.labelNoStaff.set_visible(not state)


class IndividualTrainingList(Gtk.ListStore):
    '''
    ListStore holding list of players in individual training.
    '''
    def __init__(self):
        Gtk.ListStore.__init__(self)
        self.set_column_types([int, str, str, str, str, int, int, str])

    def update(self):
        skills = structures.skills.Skills()
        intensity = structures.intensity.Intensity()
        status = structures.individualtraining.Status()

        self.clear()

        for playerid, training in data.user.club.individual_training.get_individual_training():
            player = data.players.get_player_by_id(playerid)

            self.append([playerid,
                         player.get_name(),
                         training.coach.name,
                         skills.get_skill_name(training.skill),
                         intensity.get_intensity_by_index(training.intensity),
                         training.start_value,
                         player.get_skill_by_index(training.skill),
                         status.get_status(training.status)])


class Training(Gtk.Dialog):
    def __init__(self):
        Gtk.Dialog.__init__(self)
        self.set_transient_for(data.window)
        self.set_modal(True)
        self.set_resizable(False)
        self.vbox.set_border_width(5)
        self.add_button("_Cancel", Gtk.ResponseType.CANCEL)

        self.grid = uigtk.widgets.Grid()
        self.vbox.add(self.grid)

        self.categories = structures.speciality.Categories()

        label = uigtk.widgets.Label("_Coach", leftalign=True)
        self.grid.attach(label, 0, 1, 1, 1)

        scrolledwindow = uigtk.widgets.ScrolledWindow()
        scrolledwindow.set_size_request(-1, 100)
        self.grid.attach(scrolledwindow, 1, 1, 2, 1)

        self.liststoreCoach = Gtk.ListStore(int, str, str)

        for coachid, coach in data.user.club.coaches.hired.items():
            speciality = self.categories.get_category_label(coach.speciality)
            self.liststoreCoach.append([coachid, coach.name, speciality])

        IndividualTraining.treeviewCoach = uigtk.widgets.TreeView()
        IndividualTraining.treeviewCoach.set_model(self.liststoreCoach)
        label.set_mnemonic_widget(IndividualTraining.treeviewCoach)
        IndividualTraining.treeviewCoach.treeselection.set_mode(Gtk.SelectionMode.BROWSE)
        scrolledwindow.add(IndividualTraining.treeviewCoach)

        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Coach", column=1)
        IndividualTraining.treeviewCoach.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Speciality", column=2)
        IndividualTraining.treeviewCoach.append_column(treeviewcolumn)

        label = uigtk.widgets.Label("_Skill", leftalign=True)
        self.grid.attach(label, 0, 2, 1, 1)

        self.comboboxSkill = Gtk.ComboBoxText()
        label.set_mnemonic_widget(self.comboboxSkill)
        self.grid.attach(self.comboboxSkill, 1, 2, 1, 1)

        skills = structures.skills.Skills()

        for count, skill in enumerate(skills.get_names()):
            self.comboboxSkill.append(str(count), skill)

        self.comboboxSkill.append("9", "Fitness")
        self.comboboxSkill.set_active(0)
        self.comboboxSkill.set_tooltip_text("Skill selected player will train.")

        label = uigtk.widgets.Label("Intensity", leftalign=True)
        self.grid.attach(label, 0, 3, 1, 1)

        box = uigtk.widgets.Box()
        box.set_tooltip_text("Intensity at which the skill will be trained.")
        self.grid.attach(box, 1, 3, 1, 1)

        self.intensity = []

        radiobuttonIntensityLow = uigtk.widgets.RadioButton("_Low")
        radiobuttonIntensityLow.intensity = 0
        self.intensity.append(radiobuttonIntensityLow)
        box.add(radiobuttonIntensityLow)
        radiobuttonIntensityMedium = uigtk.widgets.RadioButton("_Medium")
        radiobuttonIntensityMedium.join_group(radiobuttonIntensityLow)
        radiobuttonIntensityMedium.set_active(True)
        radiobuttonIntensityMedium.intensity = 1
        self.intensity.append(radiobuttonIntensityMedium)
        box.add(radiobuttonIntensityMedium)
        radiobuttonIntensityHigh = uigtk.widgets.RadioButton("_High")
        radiobuttonIntensityHigh.join_group(radiobuttonIntensityLow)
        radiobuttonIntensityHigh.intensity = 2
        self.intensity.append(radiobuttonIntensityHigh)
        box.add(radiobuttonIntensityHigh)


class AddTraining(Training):
    def __init__(self):
        Training.__init__(self)

        self.set_title("Add Individual Training")
        self.add_button("_Add", Gtk.ResponseType.OK)
        self.set_default_response(Gtk.ResponseType.OK)

        label = uigtk.widgets.Label("_Player", leftalign=True)
        self.grid.attach(label, 0, 0, 1, 1)

        liststore = Gtk.ListStore(int, str)
        treemodelsort = Gtk.TreeModelSort(liststore)
        treemodelsort.set_sort_column_id(1, Gtk.SortType.ASCENDING)

        for playerid, player in data.user.club.squad.get_squad():
            if not data.user.club.individual_training.get_player_in_training(playerid):
                liststore.append([playerid, player.get_name(mode=1)])

        self.comboboxPlayer = uigtk.widgets.ComboBox(column=1)
        self.comboboxPlayer.set_active(0)
        self.comboboxPlayer.set_model(treemodelsort)
        self.comboboxPlayer.set_tooltip_text("Player to add to individual training list.")
        label.set_mnemonic_widget(self.comboboxPlayer)
        self.grid.attach(self.comboboxPlayer, 1, 0, 1, 1)

    def show(self):
        self.show_all()

        IndividualTraining.treeviewCoach.scroll_to_cell(0)
        IndividualTraining.treeviewCoach.treeselection.select_path(0)

        if self.run() == Gtk.ResponseType.OK:
            model = self.comboboxPlayer.get_model()
            treeiter = self.comboboxPlayer.get_active_iter()

            playerid = model[treeiter][0]
            player = data.players.get_player_by_id(playerid)

            model, treeiter = IndividualTraining.treeviewCoach.treeselection.get_selected()

            coachid = int(model[treeiter][0])
            coach = data.user.club.coaches.get_coach_by_id(coachid)

            skill = int(self.comboboxSkill.get_active_id())

            for radiobutton in self.intensity:
                if radiobutton.get_active():
                    intensity = radiobutton.intensity

            training = (player, coach, skill, intensity)

            data.user.club.individual_training.add_to_training(training)

        self.destroy()


class EditTraining(Training):
    def __init__(self, training):
        Training.__init__(self)
        self.training = training

        self.set_title("Edit Individual Training")
        self.add_button("_Edit", Gtk.ResponseType.OK)
        self.set_default_response(Gtk.ResponseType.OK)

        label = uigtk.widgets.Label("Editing individual training for %s." % (training.player.get_name(mode=1)), leftalign=True)
        self.grid.attach(label, 0, 0, 2, 1)

        # Set values
        model = IndividualTraining.treeviewCoach.get_model()

        for item in model:
            if item[0] == training.coach.coachid:
                IndividualTraining.treeviewCoach.treeselection.select_iter(item.iter)

        self.comboboxSkill.set_active_id(str(training.skill))
        self.intensity[training.intensity].set_active(True)

    def show(self):
        self.show_all()

        if self.run() == Gtk.ResponseType.OK:
            model, treeiter = IndividualTraining.treeviewCoach.treeselection.get_selected()

            coachid = model[treeiter][0]
            self.training.coach = data.user.club.coaches.get_coach_by_id(coachid)

            self.training.skill = int(self.comboboxSkill.get_active_id())
            self.training.start_value = self.training.player.get_skill_by_index(self.training.skill)

            for radiobutton in self.intensity:
                if radiobutton.get_active():
                    self.training.intensity = radiobutton.intensity

        self.destroy()


class RemoveTraining(Gtk.MessageDialog):
    '''
    Message dialog for confirmation of individual training removal.
    '''
    def __init__(self, playerid):
        player = data.players.get_player_by_id(playerid)

        Gtk.MessageDialog.__init__(self)
        self.set_transient_for(data.window)
        self.set_modal(True)
        self.set_title("Remove Individual Training")
        self.set_property("message-type", Gtk.MessageType.QUESTION)
        self.set_markup("Do you want to remove %s from individual training?" % (player.get_name(mode=1)))
        self.add_button("_Do Not Remove", Gtk.ResponseType.CANCEL)
        self.add_button("_Remove", Gtk.ResponseType.OK)
        self.set_default_response(Gtk.ResponseType.CANCEL)

    def show(self):
        state = self.run() == Gtk.ResponseType.OK
        self.destroy()

        return state


class ContextMenu(Gtk.Menu):
    def __init__(self):
        Gtk.Menu.__init__(self)

        menuitem = uigtk.widgets.MenuItem("_Edit Player")
        menuitem.connect("activate", self.on_edit_clicked)
        self.append(menuitem)
        menuitem = uigtk.widgets.MenuItem("_Remove Player")
        menuitem.connect("activate", self.on_remove_clicked)
        self.append(menuitem)

    def on_edit_clicked(self, *args):
        '''
        Edit individual training values for selected player.
        '''
        training = data.user.club.individual_training.get_individual_training_by_playerid(self.player.playerid)

        dialog = EditTraining(training)
        dialog.show()

        IndividualTraining.liststore.update()

    def on_remove_clicked(self, *args):
        '''
        Remove player from individual training.
        '''
        dialog = RemoveTraining(self.player.playerid)

        if dialog.show():
            data.user.club.individual_training.remove_from_training(self.player.playerid)

            IndividualTraining.liststore.update()

    def show(self, player):
        self.player = player
        self.show_all()
