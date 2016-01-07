#!/usr/bin/env python3

from gi.repository import Gtk
from gi.repository import Gdk

import data
import uigtk.widgets


targets = [("MY_TREE_MODEL_ROW", Gtk.TargetFlags.SAME_APP, 0),
           ("text/plain", 0, 1),
           ("TEXT", 0, 2),
           ("STRING", 0, 3)]
target = Gtk.TargetEntry.new("MY_TREE_MODEL_ROW", Gtk.TargetFlags.SAME_APP, 0)


class Advertising(uigtk.widgets.Grid):
    __name__ = "advertising"

    class AdvertType(uigtk.widgets.Grid):
        def __init__(self, label):
            uigtk.widgets.Grid.__init__(self)
            self.set_hexpand(True)
            self.set_column_homogeneous(True)

            label = uigtk.widgets.Label("<b>%s</b>" % (label), leftalign=True)
            self.attach(label, 0, 0, 1, 1)

            self.labelCount = uigtk.widgets.Label(rightalign=True)
            self.attach(self.labelCount, 1, 0, 1, 1)

            scrolledwindow = uigtk.widgets.ScrolledWindow()
            self.attach(scrolledwindow, 0, 1, 1, 1)

            self.liststoreAvailable = Gtk.ListStore(int, str, int, str, str)

            self.treeviewAvailable = uigtk.widgets.TreeView()
            self.treeviewAvailable.set_vexpand(True)
            self.treeviewAvailable.set_model(self.liststoreAvailable)
            self.treeviewAvailable.enable_model_drag_source(Gdk.ModifierType.BUTTON1_MASK, targets, Gdk.DragAction.MOVE)
            self.treeviewAvailable.drag_source_set(Gdk.ModifierType.BUTTON1_MASK, [(target)], Gdk.DragAction.MOVE)
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

        def add_advertising(self, data):
            '''
            Get advert for advertising update.
            '''
            model, treeiter = self.treeviewAvailable.treeselection.get_selected()

            if treeiter:
                advertid = model[treeiter][0]
                data.move(advertid)

                self.update_advert_count(data)

        def on_drag_data_get(self, treeview, context, selection, info, time, index):
            '''
            Grab data for drag and drop and prepare for move.
            '''
            model, treeiter = treeview.treeselection.get_selected()

            advertid = "%i/%s" % (index, str(model[treeiter][0]))
            selectiondata = bytes(advertid, "utf-8")

            selection.set(selection.get_target(), 8, selectiondata)

        def on_drag_data_received(self, treeview, context, x, y, selection, info, time, index):
            '''
            Process dropped item and move within the supplied advert type.
            '''
            selectiondata = selection.get_data().decode("utf-8")
            selectiondata = selectiondata.split("/")

            advertid = int(selectiondata[1])

            if int(selectiondata[0]) == index:
                club = data.clubs.get_club_by_id(data.user.team)

                if index == 0:
                    club.hoardings.move(advertid)
                elif index == 1:
                    club.programmes.move(advertid)

                context.finish(True, True, time)

            return

        def update_advert_count(self, advert):
            '''
            Set the current number of adverts running.
            '''
            club = data.clubs.get_club_by_id(data.user.team)
            count = advert.get_advert_count()
            self.labelCount.set_label("%i out of %i spaces used" % (count, advert.maximum))

    def __init__(self):
        uigtk.widgets.Grid.__init__(self)

        grid = uigtk.widgets.Grid()
        self.attach(grid, 0, 0, 1, 1)

        self.hoardings = self.AdvertType(label="Hoardings")
        self.hoardings.treeviewAvailable.connect("row-activated", self.on_row_activated, self.hoardings)
        self.hoardings.treeviewAvailable.connect("drag-data-get", self.hoardings.on_drag_data_get, 0)
        self.hoardings.treeviewCurrent.connect("drag-data-received", self.on_advert_drag_and_drop, 0)
        grid.attach(self.hoardings, 0, 0, 1, 1)

        self.programmes = self.AdvertType(label="Programmes")
        self.programmes.treeviewAvailable.connect("row-activated", self.on_row_activated, self.programmes)
        self.programmes.treeviewAvailable.connect("drag-data-get", self.programmes.on_drag_data_get, 1)
        self.programmes.treeviewCurrent.connect("drag-data-received", self.on_advert_drag_and_drop, 1)
        grid.attach(self.programmes, 0, 1, 1, 1)

        buttonbox = Gtk.ButtonBox()
        buttonbox.set_layout(Gtk.ButtonBoxStyle.END)
        self.attach(buttonbox, 0, 1, 1, 1)
        self.buttonAssistant = uigtk.widgets.ToggleButton("_Assistant")
        self.buttonAssistant.set_tooltip_text("Set assistant manager to handle advertising.")
        self.buttonAssistant.connect("toggled", self.on_assistant_toggled)
        buttonbox.add(self.buttonAssistant)

    def on_row_activated(self, treeview, treepath, treeviewcolumn, advert):
        '''
        Move selected advert to current listing.
        '''
        if advert is self.hoardings:
            advert.add_advertising(self.club.hoardings)
            self.populate_hoardings()
        else:
            advert.add_advertising(self.club.programmes)
            self.populate_programmes()

    def on_advert_drag_and_drop(self, treeview, context, x, y, selection, info, time, index):
        '''
        Handle drag and drop event, adding advert to current listing.
        '''
        if index == 0:
            self.hoardings.on_drag_data_received(treeview, context, x, y, selection, info, time, index)
            self.populate_hoardings()
        elif index == 1:
            self.programmes.on_drag_data_received(treeview, context, x, y, selection, info, time, index)
            self.populate_programmes()

    def on_assistant_toggled(self, togglebutton):
        '''
        Toggle assistant manager to handle advertising.
        '''
        self.club.assistant.set_handle_advertising(togglebutton.get_active())

    def populate_hoardings(self):
        self.hoardings.liststoreAvailable.clear()
        self.hoardings.liststoreCurrent.clear()

        for advertid, advert in self.club.hoardings.available.items():
            amount = data.currency.get_currency(advert.amount, integer=True)

            self.hoardings.liststoreAvailable.append([advertid,
                                                      advert.name,
                                                      advert.quantity,
                                                      advert.get_period(),
                                                      amount])

        for advertid, advert in self.club.hoardings.current.items():
            amount = data.currency.get_currency(advert.amount, integer=True)

            self.hoardings.liststoreCurrent.append([advertid,
                                                    advert.name,
                                                    advert.quantity,
                                                    advert.get_period()])

        self.hoardings.update_advert_count(self.club.hoardings)

    def populate_programmes(self):
        self.programmes.liststoreAvailable.clear()
        self.programmes.liststoreCurrent.clear()

        for advertid, advert in self.club.programmes.available.items():
            amount = data.currency.get_currency(advert.amount, integer=True)

            self.programmes.liststoreAvailable.append([advertid,
                                                       advert.name,
                                                       advert.quantity,
                                                       advert.get_period(),
                                                       amount])

        for advertid, advert in self.club.programmes.current.items():
            amount = data.currency.get_currency(advert.amount, integer=True)

            self.programmes.liststoreCurrent.append([advertid,
                                                     advert.name,
                                                     advert.quantity,
                                                     advert.get_period()])

        self.programmes.update_advert_count(self.club.programmes)

    def run(self):
        self.club = data.clubs.get_club_by_id(data.user.team)

        self.populate_hoardings()
        self.populate_programmes()

        self.buttonAssistant.set_active(self.club.assistant.get_handle_advertising())

        self.show_all()
