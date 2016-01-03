#!/usr/bin/env python3

from gi.repository import Gtk

import data
import uigtk.widgets


class InfoTip(Gtk.Grid):
    def __init__(self):
        Gtk.Grid.__init__(self)
        self.set_row_spacing(5)
        self.set_column_spacing(5)

        label = uigtk.widgets.Label("Manager", leftalign=True)
        self.attach(label, 0, 0, 1, 1)
        self.labelManager = uigtk.widgets.Label(leftalign=True)
        self.attach(self.labelManager, 1, 0, 1, 1)
        label = uigtk.widgets.Label("Chairman", leftalign=True)
        self.attach(label, 0, 1, 1, 1)
        self.labelChairman = uigtk.widgets.Label(leftalign=True)
        self.attach(self.labelChairman, 1, 1, 1, 1)

        separator = Gtk.Separator()
        self.attach(separator, 0, 2, 2, 1)

        label = uigtk.widgets.Label("Balance", leftalign=True)
        self.attach(label, 0, 3, 1, 1)
        self.labelBalance = uigtk.widgets.Label(leftalign=True)
        self.attach(self.labelBalance, 1, 3, 1, 1)

    def show(self):
        club = data.clubs.get_club_by_id(data.user.team)

        self.labelManager.set_label("%s" % (club.manager))
        self.labelChairman.set_label("%s" % (club.chairman))
        self.labelBalance.set_label("%s" % (data.currency.get_currency(club.accounts.balance, integer=True)))

        self.show_all()
