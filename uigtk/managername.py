#!/usr/bin/env python3

from gi.repository import Gtk

import data
import uigtk.widgets


class ManagerName(Gtk.Dialog):
    def __init__(self, *args):
        Gtk.Dialog.__init__(self)
        self.set_transient_for(data.window)
        self.set_title("Manager Name")
        self.set_resizable(False)
        self.add_button("C_lose", Gtk.ResponseType.CLOSE)
        self.add_button("_Change", Gtk.ResponseType.OK)
        self.set_default_response(Gtk.ResponseType.OK)
        self.connect("response", self.on_response)
        self.vbox.set_border_width(5)
        self.vbox.set_spacing(5)

        grid = uigtk.widgets.Grid()
        self.vbox.add(grid)

        label = uigtk.widgets.Label("_Enter New Manager Name", leftalign=True)
        grid.attach(label, 0, 0, 1, 1)

        self.comboboxName = Gtk.ComboBoxText.new_with_entry()
        self.entryName = self.comboboxName.get_child()
        self.entryName.set_activates_default(True)
        label.set_mnemonic_widget(self.comboboxName)
        grid.attach(self.comboboxName, 1, 0, 1, 1)

        self.populate_names()

        club = data.clubs.get_club_by_id(data.user.team)
        self.entryName.set_text(club.manager)

        self.show_all()

    def populate_names(self):
        '''
        Load list of previously used player names.
        '''
        self.comboboxName.remove_all()

        for name in data.names.get_names():
            self.comboboxName.append_text(name)

    def on_response(self, dialog, response):
        if response == Gtk.ResponseType.OK:
            name = self.entryName.get_text()
            data.names.set_name(name)

        self.destroy()
