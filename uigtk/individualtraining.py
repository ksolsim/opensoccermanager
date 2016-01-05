#!/usr/bin/env python3

from gi.repository import Gtk

import data
import structures.intensity
import structures.skills
import uigtk.widgets


class IndividualTraining(Gtk.Grid):
    class AddTraining(Gtk.Dialog):
        def __init__(self, playerid=None):
            self.playerid = playerid
            self.club = data.clubs.get_club_by_id(data.user.team)

            Gtk.Dialog.__init__(self)
            self.set_transient_for(data.window)
            self.set_modal(True)
            self.set_resizable(False)
            self.set_title("Individual Training")
            self.vbox.set_border_width(5)
            self.add_button("_Cancel", Gtk.ResponseType.CANCEL)

            if not playerid:
                self.add_button("_Add", Gtk.ResponseType.OK)
            else:
                self.add_button("_Edit", Gtk.ResponseType.OK)

            self.set_default_response(Gtk.ResponseType.OK)

            grid = uigtk.widgets.Grid()
            self.vbox.add(grid)

            if not playerid:
                label = uigtk.widgets.Label("_Player", leftalign=True)
                grid.attach(label, 0, 0, 1, 1)

                liststore = Gtk.ListStore(int, str)
                treemodelsort = Gtk.TreeModelSort(liststore)
                treemodelsort.set_sort_column_id(1, Gtk.SortType.ASCENDING)

                for playerid in self.club.squad.get_squad():
                    if not self.club.individual_training.get_player_in_training(playerid):
                        player = data.players.get_player_by_id(playerid)
                        liststore.append([playerid, player.get_name(mode=1)])

                self.comboboxPlayer = uigtk.widgets.ComboBox(column=1)
                self.comboboxPlayer.set_active(0)
                self.comboboxPlayer.set_model(treemodelsort)
                self.comboboxPlayer.set_tooltip_text("Player to add to individual training list.")
                label.set_mnemonic_widget(self.comboboxPlayer)
                grid.attach(self.comboboxPlayer, 1, 0, 1, 1)

            label = uigtk.widgets.Label("_Coach", leftalign=True)
            grid.attach(label, 0, 1, 1, 1)

            self.comboboxCoach = Gtk.ComboBoxText()
            self.comboboxCoach.connect("changed", self.on_coach_changed)
            label.set_mnemonic_widget(self.comboboxCoach)
            grid.attach(self.comboboxCoach, 1, 1, 1, 1)

            self.categories = structures.speciality.Categories()

            self.labelCategory = uigtk.widgets.Label(leftalign=True)
            grid.attach(self.labelCategory, 2, 1, 1, 1)

            for coachid, coach in self.club.coaches.hired.items():
                self.comboboxCoach.append(str(coachid), coach.name)

            self.comboboxCoach.set_active(0)

            label = uigtk.widgets.Label("_Skill", leftalign=True)
            grid.attach(label, 0, 2, 1, 1)

            self.comboboxSkill = Gtk.ComboBoxText()
            label.set_mnemonic_widget(self.comboboxSkill)
            grid.attach(self.comboboxSkill, 1, 2, 1, 1)

            skills = structures.skills.Skills()

            for count, skill in enumerate(skills.get_names()):
                self.comboboxSkill.append(str(count), skill)

            self.comboboxSkill.append("9", "Fitness")
            self.comboboxSkill.set_active(0)
            self.comboboxSkill.set_tooltip_text("Skill selected player will train.")

            label = uigtk.widgets.Label("Intensity", leftalign=True)
            grid.attach(label, 0, 3, 1, 1)

            box = uigtk.widgets.Box()
            box.set_tooltip_text("Intensity at which the skill will be trained.")
            grid.attach(box, 1, 3, 1, 1)

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

        def on_coach_changed(self, combobox):
            '''
            Update recommended training categories when coach is changed.
            '''
            coachid = int(combobox.get_active_id())
            coach = self.club.coaches.get_coach_by_id(coachid)

            label = self.categories.get_category_label(coach.speciality)
            self.labelCategory.set_label(label)

        def show(self):
            self.show_all()

            if self.run() == Gtk.ResponseType.OK:
                if not self.playerid:
                    model = self.comboboxPlayer.get_model()
                    treeiter = self.comboboxPlayer.get_active_iter()

                    self.playerid = model[treeiter][0]

                coachid = int(self.comboboxCoach.get_active_id())
                skill = int(self.comboboxSkill.get_active_id())

                for radiobutton in self.intensity:
                    if radiobutton.get_active():
                        intensity = radiobutton.intensity

                training = (self.playerid, coachid, skill, intensity)

                self.club.individual_training.add_to_training(training)

            self.destroy()

    class RemoveTraining(Gtk.MessageDialog):
        def __init__(self, playerid):
            player = data.players.get_player_by_id(playerid)

            Gtk.MessageDialog.__init__(self)
            self.set_transient_for(data.window)
            self.set_modal(True)
            self.set_title("Individual Training")
            self.set_property("message-type", Gtk.MessageType.QUESTION)
            self.set_markup("Do you want to remove %s from individual training?" % (player.get_name(mode=1)))
            self.add_button("_Do Not Remove", Gtk.ResponseType.CANCEL)
            self.add_button("_Remove", Gtk.ResponseType.OK)
            self.set_default_response(Gtk.ResponseType.CANCEL)

        def show(self):
            state = self.run() == Gtk.ResponseType.OK
            self.destroy()

            return state

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

        self.liststore = Gtk.ListStore(int, str, str, str, str, int, int, str)
        treemodelsort = Gtk.TreeModelSort(self.liststore)
        treemodelsort.set_sort_column_id(1, Gtk.SortType.ASCENDING)

        self.treeview = uigtk.widgets.TreeView()
        self.treeview.set_hexpand(True)
        self.treeview.set_vexpand(True)
        self.treeview.set_sensitive(False)
        self.treeview.set_model(treemodelsort)
        self.treeview.treeselection.connect("changed", self.on_selection_changed)
        self.overlay.add(self.treeview)

        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Name", column=1)
        treeviewcolumn.set_expand(True)
        self.treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Coach", column=2)
        self.treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Skill", column=3)
        self.treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Intensity", column=4)
        self.treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Start Value", column=5)
        self.treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Current Value", column=6)
        self.treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Status", column=7)
        self.treeview.append_column(treeviewcolumn)

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

    def on_add_clicked(self, *args):
        '''
        Launch dialog for adding player to individual training.
        '''
        dialog = self.AddTraining()
        dialog.show()

        self.populate_data()

    def on_edit_clicked(self, *args):
        '''
        Display dialog to edit selected individual player training.
        '''
        model, treeiter = self.treeview.treeselection.get_selected()

        if treeiter:
            playerid = model[treeiter][0]

            dialog = self.AddTraining(playerid)
            dialog.show()

            self.populate_data()

    def on_remove_clicked(self, *args):
        '''
        Confirm from user to remove selected player from individual training.
        '''
        model, treeiter = self.treeview.treeselection.get_selected()
        playerid = model[treeiter][0]

        dialog = self.RemoveTraining(playerid)

        if dialog.show():
            self.club.individual_training.remove_from_training(playerid)

            self.populate_data()

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
        skills = structures.skills.Skills()
        intensity = structures.intensity.Intensity()
        status = Status()

        self.liststore.clear()

        for playerid, training in self.club.individual_training.get_individual_training():
            player = data.players.get_player_by_id(playerid)
            coach = self.club.coaches.get_coach_by_id(training.coachid)

            self.liststore.append([playerid,
                                   player.get_name(),
                                   coach.name,
                                   skills.get_skill_name(training.skill),
                                   intensity.get_intensity_by_index(training.intensity),
                                   training.start_value,
                                   player.get_skill_by_index(training.skill),
                                   status.get_status(training.status)])

    def run(self):
        self.club = data.clubs.get_club_by_id(data.user.team)

        self.populate_data()
        self.show_all()

        if self.club.team_training.get_individual_set():
            self.infobar.hide()

        state = self.club.coaches.get_staff_count() > 0
        self.buttonAddTraining.set_sensitive(state)
        self.treeview.set_sensitive(state)
        self.labelNoStaff.set_visible(not state)


class Status:
    def __init__(self):
        self.status = {0: "Just started training.",
                       1: "Improving slowly.",
                       2: "Making good progress.",
                       3: "Quickly developing.",
                       4: "No longer progressing."}

    def get_status(self, index):
        '''
        Get status string for given index.
        '''
        return self.status[index]
