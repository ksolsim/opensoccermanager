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

import constants
import game
import user
import widgets


class Advertising(Gtk.Grid):
    __name__ = "advertising"

    class Display(Gtk.Grid):
        def __init__(self, category):
            self.liststoreAvailable = Gtk.ListStore(int, str, int, int, int, str)
            self.liststoreCurrent = Gtk.ListStore(int, str, int, int, int, str)

            Gtk.Grid.__init__(self)
            self.set_column_homogeneous(True)
            self.set_row_spacing(5)
            self.set_column_spacing(5)

            label = widgets.AlignedLabel("<b>%s</b>" % (category))
            label.set_use_markup(True)
            self.attach(label, 0, 0, 1, 1)

            self.labelCount = Gtk.Label()
            self.labelCount.set_alignment(1, 0.5)
            self.attach(self.labelCount, 1, 0, 1, 1)

            target = Gtk.TargetEntry.new("MY_TREE_MODEL_ROW", Gtk.TargetFlags.SAME_APP, 0)

            targets = [("MY_TREE_MODEL_ROW", Gtk.TargetFlags.SAME_APP, 0),
                       ("text/plain", 0, 1),
                       ("TEXT", 0, 2),
                       ("STRING", 0, 3),
                      ]

            cellrenderertext = Gtk.CellRendererText()

            scrolledwindow = Gtk.ScrolledWindow()
            scrolledwindow.set_vexpand(True)
            scrolledwindow.set_hexpand(True)
            self.attach(scrolledwindow, 0, 1, 1, 1)

            self.treeviewAvailable = Gtk.TreeView()
            self.treeviewAvailable.set_model(self.liststoreAvailable)
            self.treeviewAvailable.set_enable_search(False)
            self.treeviewAvailable.set_search_column(-1)
            self.treeviewAvailable.enable_model_drag_source(Gdk.ModifierType.BUTTON1_MASK, targets, Gdk.DragAction.MOVE)
            self.treeviewAvailable.drag_source_set(Gdk.ModifierType.BUTTON1_MASK, [(target)], Gdk.DragAction.MOVE)
            self.treeselection = self.treeviewAvailable.get_selection()
            scrolledwindow.add(self.treeviewAvailable)
            treeviewcolumn = widgets.TreeViewColumn(title="Name", column=1)
            treeviewcolumn.set_expand(True)
            self.treeviewAvailable.append_column(treeviewcolumn)
            treeviewcolumn = widgets.TreeViewColumn(title="Quantity", column=2)
            self.treeviewAvailable.append_column(treeviewcolumn)
            treeviewcolumn = widgets.TreeViewColumn(title="Period", column=3)
            self.treeviewAvailable.append_column(treeviewcolumn)
            treeviewcolumn = widgets.TreeViewColumn(title="Cost", column=5)
            self.treeviewAvailable.append_column(treeviewcolumn)

            scrolledwindow = Gtk.ScrolledWindow()
            scrolledwindow.set_vexpand(True)
            scrolledwindow.set_hexpand(True)
            self.attach(scrolledwindow, 1, 1, 1, 1)

            self.treeviewCurrent = Gtk.TreeView()
            self.treeviewCurrent.set_model(self.liststoreCurrent)
            self.treeviewCurrent.set_enable_search(False)
            self.treeviewCurrent.set_search_column(-1)
            self.treeviewCurrent.enable_model_drag_dest(targets, Gdk.DragAction.MOVE)
            scrolledwindow.add(self.treeviewCurrent)
            treeselection = self.treeviewCurrent.get_selection()
            treeselection.set_mode(Gtk.SelectionMode.NONE)
            treeviewcolumn = widgets.TreeViewColumn(title="Name", column=1)
            treeviewcolumn.set_expand(True)
            self.treeviewCurrent.append_column(treeviewcolumn)
            treeviewcolumn = widgets.TreeViewColumn(title="Quantity", column=2)
            self.treeviewCurrent.append_column(treeviewcolumn)
            treeviewcolumn = widgets.TreeViewColumn(title="Period", column=3)
            self.treeviewCurrent.append_column(treeviewcolumn)

        def advertising_add(self, index):
            model, treeiter = self.treeselection.get_selected()

            advertid = model[treeiter][0]
            club = user.get_user_club()

            if index == 0:
                club.hoardings.move(advertid)
            elif index == 1:
                club.programmes.move(advertid)

        def on_drag_data_get(self, treeview, context, selection, info, time, index):
            model, treeiter = self.treeselection.get_selected()

            advertid = "%i/%s" % (index, str(model[treeiter][0]))
            data = bytes(advertid, "utf-8")

            selection.set(selection.get_target(), 8, data)

        def on_drag_data_received(self, treeview, context, x, y, selection, info, time, index):
            data = selection.get_data().decode("utf-8")
            data = data.split("/")

            drop_info = treeview.get_dest_row_at_pos(x, y)

            advertid = int(data[1])

            if int(data[0]) == index:
                club = user.get_user_club()

                if index == 0:
                    club.hoardings.move(advertid)
                elif index == 1:
                    club.programmes.move(advertid)

                if context.get_actions() == Gdk.DragAction.MOVE:
                    context.finish(True, True, time)

            return

    def __init__(self):
        Gtk.Grid.__init__(self)
        self.set_row_spacing(5)

        self.hoardings = self.Display("Hoardings")
        self.hoardings.treeviewAvailable.connect("row-activated", self.advertising_add, 0)
        self.hoardings.treeviewAvailable.connect("drag-data-get", self.hoardings.on_drag_data_get, 0)
        self.hoardings.treeviewCurrent.connect("drag-data-received", self.advertising_dnd, 0)
        self.attach(self.hoardings, 0, 0, 2, 1)

        self.programmes = self.Display("Programmes")
        self.programmes.treeviewAvailable.connect("row-activated", self.advertising_add, 1)
        self.programmes.treeviewAvailable.connect("drag-data-get", self.programmes.on_drag_data_get, 1)
        self.programmes.treeviewCurrent.connect("drag-data-received", self.advertising_dnd, 1)
        self.attach(self.programmes, 0, 1, 2, 1)

        buttonbox = Gtk.ButtonBox()
        buttonbox.set_layout(Gtk.ButtonBoxStyle.END)
        self.attach(buttonbox, 0, 2, 2, 1)

        buttonAuto = Gtk.ToggleButton("_Assistant")
        buttonAuto.set_use_underline(True)
        buttonAuto.set_tooltip_text("Advertising handled by assistant manager.")
        buttonAuto.connect("toggled", self.assistant_handler)
        buttonbox.add(buttonAuto)

    def assistant_handler(self, togglebutton):
        game.advertising_assistant = togglebutton.get_active()

    def advertising_add(self, treeview, treepath, treeviewcolumn, index):
        if index == 0:
            self.hoardings.advertising_add(index)
        elif index == 1:
            self.programmes.advertising_add(index)

        self.populate_data()

    def advertising_dnd(self, treeview, context, x, y, selection, info, time, index):
        if index == 0:
            self.hoardings.on_drag_data_received(treeview, context, x, y, selection, info, time, index)
        elif index == 1:
            self.programmes.on_drag_data_received(treeview, context, x, y, selection, info, time, index)

        self.populate_data()

    def update_totals(self):
        club = user.get_user_club()

        quantity = club.hoardings.get_advert_count()
        self.hoardings.labelCount.set_label("Used %i of %i hoarding spaces" % (quantity, club.hoardings.maximum))

        quantity = club.programmes.get_advert_count()
        self.programmes.labelCount.set_label("Used %i of %i programme spaces" % (quantity, club.programmes.maximum))

    def populate_data(self):
        self.hoardings.liststoreAvailable.clear()
        self.programmes.liststoreAvailable.clear()
        self.hoardings.liststoreCurrent.clear()
        self.programmes.liststoreCurrent.clear()

        club = user.get_user_club()

        for advertid, advert in club.hoardings.available.items():
            item = advert.get_details()
            item.insert(0, advertid)
            self.hoardings.liststoreAvailable.append(item)

        for advertid, advert in club.programmes.available.items():
            item = advert.get_details()
            item.insert(0, advertid)
            self.programmes.liststoreAvailable.append(item)

        for advert in club.hoardings.current.values():
            item = advert.get_details()
            item.insert(0, advertid)
            self.hoardings.liststoreCurrent.append(item)

        for advert in club.programmes.current.values():
            item = advert.get_details()
            item.insert(0, advertid)
            self.programmes.liststoreCurrent.append(item)

        self.update_totals()

    def run(self):
        self.populate_data()

        self.show_all()
