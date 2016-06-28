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
import uigtk.widgets


class Advertising(uigtk.widgets.Grid):
    __name__ = "advertising"

    class AdvertType(uigtk.widgets.Grid):
        def __init__(self, label, advert, typeid):
            self.advert = advert
            self.typeid = typeid

            uigtk.widgets.Grid.__init__(self)
            self.set_hexpand(True)
            self.set_column_homogeneous(True)

            label = uigtk.widgets.Label("<b>%s</b>" % (label), leftalign=True)
            self.attach(label, 0, 0, 1, 1)

            self.labelCount = uigtk.widgets.Label(rightalign=True)
            self.attach(self.labelCount, 1, 0, 1, 1)

            scrolledwindow = uigtk.widgets.ScrolledWindow()
            self.attach(scrolledwindow, 0, 1, 1, 1)

            targets = [("MY_TREE_MODEL_ROW", Gtk.TargetFlags.SAME_APP, 0),
                       ("TEXT", 0, 1)]

            self.liststoreAvailable = Gtk.ListStore(int, str, int, str, str)

            self.treeviewAvailable = uigtk.widgets.TreeView()
            self.treeviewAvailable.set_vexpand(True)
            self.treeviewAvailable.set_model(self.liststoreAvailable)
            self.treeviewAvailable.enable_model_drag_source(Gdk.ModifierType.BUTTON1_MASK, targets, Gdk.DragAction.MOVE)
            self.treeviewAvailable.connect("row-activated", self.on_row_activated)
            self.treeviewAvailable.connect("drag-data-get", self.on_drag_data_get)
            scrolledwindow.add(self.treeviewAvailable)

            treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Company",
                                                          column=1)
            treeviewcolumn.set_expand(True)
            self.treeviewAvailable.append_column(treeviewcolumn)
            treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Quantity",
                                                          column=2)
            self.treeviewAvailable.append_column(treeviewcolumn)
            treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Period",
                                                          column=3)
            self.treeviewAvailable.append_column(treeviewcolumn)
            treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Amount",
                                                          column=4)
            self.treeviewAvailable.append_column(treeviewcolumn)

            scrolledwindow = uigtk.widgets.ScrolledWindow()
            self.attach(scrolledwindow, 1, 1, 1, 1)

            self.liststoreCurrent = Gtk.ListStore(int, str, int, str)

            self.treeviewCurrent = uigtk.widgets.TreeView()
            self.treeviewCurrent.set_vexpand(True)
            self.treeviewCurrent.set_model(self.liststoreCurrent)
            self.treeviewCurrent.enable_model_drag_dest(targets, Gdk.DragAction.MOVE)
            self.treeviewCurrent.treeselection.set_mode(Gtk.SelectionMode.NONE)
            self.treeviewCurrent.connect("drag-data-received", self.on_drag_data_received)
            scrolledwindow.add(self.treeviewCurrent)

            treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Company",
                                                          column=1)
            treeviewcolumn.set_expand(True)
            self.treeviewCurrent.append_column(treeviewcolumn)
            treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Quantity",
                                                          column=2)
            self.treeviewCurrent.append_column(treeviewcolumn)
            treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Period",
                                                          column=3)
            self.treeviewCurrent.append_column(treeviewcolumn)

        def add_advertising(self):
            '''
            Get advert for advertising update.
            '''
            model, treeiter = self.treeviewAvailable.treeselection.get_selected()

            if treeiter:
                advertid = model[treeiter][0]
                self.advert.move(advertid)

                self.update_advert_count()

        def on_drag_data_get(self, treeview, context, selection, info, time):
            '''
            Grab data for drag-and-drop and prepare for move.
            '''
            model, treeiter = treeview.treeselection.get_selected()

            advertid = "%i/%s" % (self.typeid, model[treeiter][0])
            selectiondata = bytes(advertid, "utf-8")

            selection.set(selection.get_target(), 8, selectiondata)

        def on_drag_data_received(self, treeview, context, x, y, selection, info, time):
            '''
            Process dropped item and move within the supplied advert type.
            '''
            selectiondata = selection.get_data()
            selectiondata = selectiondata.decode("utf-8")
            typeid, advertid = selectiondata.split("/")

            if int(typeid) == self.typeid:
                advertid = int(advertid)
                self.advert.move(advertid)

                context.finish(True, True, time)

                self.populate_data()

        def on_row_activated(self, treeview, treepath, treeviewcolumn):
            '''
            Move selected advert to current listing.
            '''
            self.add_advertising()

        def update_advert_count(self):
            '''
            Set the current number of adverts running.
            '''
            count = self.advert.get_advert_count()
            self.labelCount.set_label("%i out of %i spaces used" % (count, self.advert.maximum))

        def populate_data(self):
            self.liststoreAvailable.clear()
            self.liststoreCurrent.clear()

            for advertid, advert in self.advert.available.items():
                amount = data.currency.get_currency(advert.amount, integer=True)

                self.liststoreAvailable.append([advertid,
                                                advert.name,
                                                advert.quantity,
                                                advert.get_period(),
                                                amount])

            for advertid, advert in self.advert.current.items():
                self.liststoreCurrent.append([advertid,
                                              advert.name,
                                              advert.quantity,
                                              advert.get_period()])

            self.update_advert_count()

    def __init__(self):
        uigtk.widgets.Grid.__init__(self)

        grid = uigtk.widgets.Grid()
        self.attach(grid, 0, 0, 1, 1)

        self.hoardings = self.AdvertType(label="Hoardings",
                                         advert=data.user.club.hoardings,
                                         typeid=0)
        grid.attach(self.hoardings, 0, 0, 1, 1)

        self.programmes = self.AdvertType(label="Programmes",
                                          advert=data.user.club.programmes,
                                          typeid=1)
        grid.attach(self.programmes, 0, 1, 1, 1)

        buttonbox = Gtk.ButtonBox()
        buttonbox.set_layout(Gtk.ButtonBoxStyle.END)
        self.attach(buttonbox, 0, 1, 1, 1)

        self.buttonAssistant = uigtk.widgets.ToggleButton("_Assistant")
        self.buttonAssistant.set_tooltip_text("Set assistant manager to handle advertising.")
        self.buttonAssistant.connect("toggled", self.on_assistant_toggled)
        buttonbox.add(self.buttonAssistant)

    def on_assistant_toggled(self, togglebutton):
        '''
        Toggle assistant manager to handle advertising.
        '''
        data.user.club.assistant.set_handle_advertising(togglebutton.get_active())

    def run(self):
        self.hoardings.populate_data()
        self.programmes.populate_data()

        self.buttonAssistant.set_active(data.user.club.assistant.get_handle_advertising())

        self.show_all()
