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
import os

import data
import uigtk.widgets


class DeleteDialog(Gtk.Dialog):
    '''
    Deletion dialog for removing saved game files.
    '''
    def __init__(self, *args):
        Gtk.Dialog.__init__(self)
        self.set_transient_for(data.window)
        self.set_modal(True)
        self.set_default_size(225, 350)
        self.set_title("Delete Game")
        self.add_button("_Close", Gtk.ResponseType.CLOSE)
        self.connect("response", self.on_response)
        self.vbox.set_border_width(5)
        self.vbox.set_spacing(5)

        filepath = os.path.join(data.preferences.data_path, "saves")

        self.filechooserbutton = Gtk.FileChooserButton()
        self.filechooserbutton.set_action(Gtk.FileChooserAction.SELECT_FOLDER)
        self.filechooserbutton.set_tooltip_text("Change the visible directory.")
        self.filechooserbutton.set_current_folder(filepath)
        self.filechooserbutton.connect("file-set", self.on_file_set)
        self.filechooserbutton.connect("file-activated", self.on_file_set)
        self.vbox.add(self.filechooserbutton)

        scrolledwindow = Gtk.ScrolledWindow()
        self.vbox.add(scrolledwindow)

        self.liststore = Gtk.ListStore(str)
        treemodelsort = Gtk.TreeModelSort(self.liststore)
        treemodelsort.set_sort_column_id(0, Gtk.SortType.ASCENDING)

        self.treeview = uigtk.widgets.TreeView()
        self.treeview.set_vexpand(True)
        self.treeview.set_model(treemodelsort)
        self.treeview.set_headers_visible(False)
        self.treeview.set_rubber_banding(True)
        self.treeview.treeselection.set_mode(Gtk.SelectionMode.MULTIPLE)
        self.treeview.treeselection.connect("changed", self.on_selection_changed)
        scrolledwindow.add(self.treeview)

        treeviewcolumn = uigtk.widgets.TreeViewColumn(column=0)
        self.treeview.append_column(treeviewcolumn)

        buttonbox = uigtk.widgets.ButtonBox()
        buttonbox.set_layout(Gtk.ButtonBoxStyle.END)
        self.vbox.add(buttonbox)

        self.buttonDelete = uigtk.widgets.Button("_Delete")
        self.buttonDelete.set_sensitive(False)
        self.buttonDelete.set_tooltip_text("Delete selected files from the file system.")
        self.buttonDelete.connect("clicked", self.on_delete_clicked)
        buttonbox.add(self.buttonDelete)

        self.populate_data(filepath)
        self.show_all()

    def on_selection_changed(self, *args):
        '''
        Update delete button sensitivity on selection change.
        '''
        model, treepaths = self.treeview.treeselection.get_selected_rows()

        if treepaths:
            self.buttonDelete.set_sensitive(True)
        else:
            self.buttonDelete.set_sensitive(False)

    def on_delete_clicked(self, *args):
        '''
        Take selected file and delete from disk.
        '''
        filepath = self.filechooserbutton.get_filename()

        model, treepaths = self.treeview.treeselection.get_selected_rows()

        for treepath in treepaths:
            os.remove(os.path.join(filepath, model[treepath][0]))

        self.populate_data(filepath)

    def on_file_set(self, filechooserbutton):
        '''
        Update view when file chooser button is changed.
        '''
        filepath = filechooserbutton.get_filename()

        self.populate_data(filepath)

    def populate_data(self, filepath):
        '''
        Populate list of files in selected directory.
        '''
        self.liststore.clear()

        for filename in os.listdir(filepath):
            self.liststore.append([filename])

    def on_response(self, *args):
        self.destroy()
