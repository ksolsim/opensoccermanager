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
    Deletion dialog for removing saved game files in the selected directory.
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

        saves = os.path.join(data.preferences.data_path, "saves")

        filechooser = Gtk.FileChooserButton()
        filechooser.set_action(Gtk.FileChooserAction.SELECT_FOLDER)
        filechooser.set_tooltip_text("Change the visible directory.")
        filechooser.set_current_folder(saves)
        self.vbox.add(filechooser)

        scrolledwindow = uigtk.widgets.ScrolledWindow()
        self.vbox.add(scrolledwindow)

        self.liststore = Gtk.ListStore(str, str)

        treemodelsort = Gtk.TreeModelSort(self.liststore)
        treemodelsort.set_sort_column_id(1, Gtk.SortType.ASCENDING)

        treeview = uigtk.widgets.TreeView()
        treeview.set_vexpand(True)
        treeview.set_model(treemodelsort)
        treeview.set_headers_visible(False)
        treeview.set_rubber_banding(True)
        treeview.treeselection.set_mode(Gtk.SelectionMode.MULTIPLE)
        scrolledwindow.add(treeview)

        treeviewcolumn = uigtk.widgets.TreeViewColumn(column=1)
        treeview.append_column(treeviewcolumn)

        buttonbox = uigtk.widgets.ButtonBox()
        buttonbox.set_layout(Gtk.ButtonBoxStyle.END)
        self.vbox.add(buttonbox)

        self.buttonDelete = uigtk.widgets.Button("_Delete")
        self.buttonDelete.set_sensitive(False)
        self.buttonDelete.set_tooltip_text("Delete selected files from the file system.")
        buttonbox.add(self.buttonDelete)

        self.show_all()

    def on_response(self, *args):
        self.destroy()
