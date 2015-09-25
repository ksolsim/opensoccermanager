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

import game
import widgets


class Opposition(Gtk.Dialog):
    def __init__(self):
        Gtk.Dialog.__init__(self)
        self.set_transient_for(game.window)
        self.set_border_width(5)
        self.set_default_size(200, 350)
        self.set_title("View Opposition")
        self.add_button("_Close", Gtk.ResponseType.CLOSE)
        self.connect("response", self.response_handler)

        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)
        self.vbox.add(grid)

        grid2 = Gtk.Grid()
        grid2.set_column_spacing(5)
        grid.attach(grid2, 0, 0, 1, 1)

        self.liststoreClubs = Gtk.ListStore(str, str)
        treemodelsort = Gtk.TreeModelSort(self.liststoreClubs)
        treemodelsort.set_sort_column_id(1, Gtk.SortType.ASCENDING)

        label = widgets.Label("_Opposition")
        grid2.attach(label, 0, 0, 1, 1)
        cellrenderertext = Gtk.CellRendererText()
        self.combobox = Gtk.ComboBox()
        self.combobox.set_model(treemodelsort)
        self.combobox.set_id_column(0)
        self.combobox.connect("changed", self.combobox_changed)
        self.combobox.pack_start(cellrenderertext, True)
        self.combobox.add_attribute(cellrenderertext, "text", 1)
        label.set_mnemonic_widget(self.combobox)
        grid2.attach(self.combobox, 1, 0, 1, 1)

        commonframe = widgets.CommonFrame("Details")
        grid.attach(commonframe, 0, 1, 1, 1)

        grid1 = Gtk.Grid()
        grid1.set_row_spacing(5)
        grid1.set_column_spacing(5)
        commonframe.insert(grid1)

        label = widgets.AlignedLabel("Manager")
        grid1.attach(label, 0, 0, 1, 1)
        self.labelManager = widgets.AlignedLabel()
        grid1.attach(self.labelManager, 1, 0, 1, 1)

        label = widgets.AlignedLabel("Position")
        grid1.attach(label, 0, 1, 1, 1)
        self.labelPosition = widgets.AlignedLabel()
        grid1.attach(self.labelPosition, 1, 1, 1, 1)

        label = widgets.AlignedLabel("Form")
        grid1.attach(label, 0, 2, 1, 1)
        self.labelForm = widgets.AlignedLabel()
        grid1.attach(self.labelForm, 1, 2, 1, 1)

        commonframe = widgets.CommonFrame("Squad")
        grid.attach(commonframe, 1, 1, 2, 2)

        self.notebook = Gtk.Notebook()
        self.notebook.set_show_tabs(False)
        commonframe.insert(self.notebook)

        # Squad Tab
        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_policy(Gtk.PolicyType.NEVER,
                                  Gtk.PolicyType.AUTOMATIC)
        label = widgets.Label("_Squad")
        self.notebook.append_page(scrolledwindow, label)

        self.liststoreSquad = Gtk.ListStore(str)
        treemodelsort = Gtk.TreeModelSort(self.liststoreSquad)
        treemodelsort.set_sort_column_id(0, Gtk.SortType.ASCENDING)

        treeview = Gtk.TreeView()
        treeview.set_vexpand(True)
        treeview.set_hexpand(True)
        treeview.set_headers_visible(False)
        treeview.set_model(treemodelsort)
        treeview.set_enable_search(False)
        treeview.set_search_column(-1)
        treeselection = treeview.get_selection()
        treeselection.set_mode(Gtk.SelectionMode.NONE)
        treeviewcolumn = widgets.TreeViewColumn(column=0)
        treeview.append_column(treeviewcolumn)
        scrolledwindow.add(treeview)

        # Team Selection Tab
        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_policy(Gtk.PolicyType.NEVER,
                                  Gtk.PolicyType.AUTOMATIC)
        label = widgets.Label("_Team")
        self.notebook.append_page(scrolledwindow, label)

        self.liststoreTeam = Gtk.ListStore(str, str)

        treeview = Gtk.TreeView()
        treeview.set_vexpand(True)
        treeview.set_hexpand(True)
        treeview.set_model(self.liststoreTeam)
        treeview.set_enable_search(False)
        treeview.set_search_column(-1)
        treeviewcolumn = widgets.TreeViewColumn(title="Position", column=0)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = widgets.TreeViewColumn(title="Player", column=1)
        treeview.append_column(treeviewcolumn)
        scrolledwindow.add(treeview)

    def display(self, show=None):
        self.liststoreClubs.clear()

        for clubid, club in game.clubs.items():
            if clubid != game.teamid:
                self.liststoreClubs.append([str(clubid), club.name])

        if show:
            self.combobox.set_active_id(show)
        else:
            self.combobox.set_active(0)

        self.show_all()
        self.run()

    def combobox_changed(self, combobox):
        if combobox.get_active_id():
            club = int(combobox.get_active_id())

            self.update_data(club)

    def update_data(self, clubid):
        club = game.clubs[clubid]

        position = game.leagues[club.league].standings.find_position(clubid)
        position = display.format_position(position)

        self.labelManager.set_label(club.manager)
        self.labelPosition.set_label(position)

        if len(club.form) > 0:
            form = "".join(club.form[-6:])
            self.labelForm.set_label(form)
        else:
            self.labelForm.set_label("N/A")

        self.liststoreSquad.clear()

        for playerid in club.squad:
            player = game.players[playerid]
            name = player.get_name()
            self.liststoreSquad.append([name])

        if game.date.eventindex > 0:
            self.notebook.set_show_tabs(True)
            self.liststoreTeam.clear()

            for positionid, playerid in club.team.items():
                formationid = club.tactics[0]

                if positionid < 11:
                    position = constants.formations[formationid][1][positionid]
                else:
                    position = "Sub %i" % (positionid - 10)

                if playerid != 0:
                    player = game.players[playerid]
                    name = player.get_name()
                    self.liststoreTeam.append([position, name])

    def response_handler(self, dialog, response):
        self.destroy()
