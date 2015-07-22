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

import display
import game
import user
import widgets


class Accounts(Gtk.Grid):
    def __init__(self):
        Gtk.Grid.__init__(self)
        self.set_border_width(5)
        self.set_row_spacing(5)
        self.set_column_spacing(10)
        self.set_vexpand(True)
        self.set_hexpand(True)

        self.labels_week = []
        self.labels_season = []

        for count in range(0, 10):
            label = widgets.AlignedLabel()
            self.labels_week.append(label)
            self.attach(label, 1, count + 1, 1, 1)

            label = widgets.AlignedLabel()
            self.labels_season.append(label)
            self.attach(label, 2, count + 1, 1, 1)

        for count in range(10, 20):
            label = widgets.AlignedLabel()
            self.labels_week.append(label)
            self.attach(label, 5, count - 9, 1, 1)

            label = widgets.AlignedLabel()
            self.labels_season.append(label)
            self.attach(label, 6, count - 9, 1, 1)

        label = Gtk.Label("<b>Income</b>")
        label.set_use_markup(True)
        self.attach(label, 0, 0, 1, 1)
        label = Gtk.Label("This Week")
        label.set_hexpand(True)
        self.attach(label, 1, 0, 1, 1)
        label = Gtk.Label("This Season")
        label.set_hexpand(True)
        self.attach(label, 2, 0, 1, 1)

        label = widgets.AlignedLabel("Prize Money")
        self.attach(label, 0, 1, 1, 1)
        label = widgets.AlignedLabel("Sponsorship")
        self.attach(label, 0, 2, 1, 1)
        label = widgets.AlignedLabel("Advertising")
        self.attach(label, 0, 3, 1, 1)
        label = widgets.AlignedLabel("Merchandise")
        self.attach(label, 0, 4, 1, 1)
        label = widgets.AlignedLabel("Catering")
        self.attach(label, 0, 5, 1, 1)
        label = widgets.AlignedLabel("Ticket Sales")
        self.attach(label, 0, 6, 1, 1)
        label = widgets.AlignedLabel("Transfer Fees")
        self.attach(label, 0, 7, 1, 1)
        label = widgets.AlignedLabel("Loan")
        self.attach(label, 0, 8, 1, 1)
        label = widgets.AlignedLabel("Grant")
        self.attach(label, 0, 9, 1, 1)
        label = widgets.AlignedLabel("Television Money")
        self.attach(label, 0, 10, 1, 1)

        separator = Gtk.Separator()
        separator.set_orientation(Gtk.Orientation.VERTICAL)
        self.attach(separator, 3, 0, 1, 12)

        label = Gtk.Label("<b>Expenditure</b>")
        label.set_use_markup(True)
        self.attach(label, 4, 0, 1, 1)
        label = Gtk.Label("This Week")
        label.set_hexpand(True)
        self.attach(label, 5, 0, 1, 1)
        label = Gtk.Label("This Season")
        label.set_hexpand(True)
        self.attach(label, 6, 0, 1, 1)

        label = widgets.AlignedLabel("Fines")
        self.attach(label, 4, 1, 1, 1)
        label = widgets.AlignedLabel("Stadium")
        self.attach(label, 4, 2, 1, 1)
        label = widgets.AlignedLabel("Staff Wages")
        self.attach(label, 4, 3, 1, 1)
        label = widgets.AlignedLabel("Player Wages")
        self.attach(label, 4, 4, 1, 1)
        label = widgets.AlignedLabel("Transfer Fees")
        self.attach(label, 4, 5, 1, 1)
        label = widgets.AlignedLabel("Merchandise")
        self.attach(label, 4, 6, 1, 1)
        label = widgets.AlignedLabel("Catering")
        self.attach(label, 4, 7, 1, 1)
        label = widgets.AlignedLabel("Loan Repayment")
        self.attach(label, 4, 8, 1, 1)
        label = widgets.AlignedLabel("Overdraft Repayment")
        self.attach(label, 4, 9, 1, 1)
        label = widgets.AlignedLabel("Training")
        self.attach(label, 4, 10, 1, 1)

        separator = Gtk.Separator()
        separator.set_orientation(Gtk.Orientation.HORIZONTAL)
        self.attach(separator, 0, 20, 7, 1)

        label = widgets.AlignedLabel("Total Income")
        self.attach(label, 0, 21, 1, 1)
        self.labelIncome = widgets.AlignedLabel()
        self.attach(self.labelIncome, 1, 21, 1, 1)
        label = widgets.AlignedLabel("Total Expenditure")
        self.attach(label, 0, 22, 1, 1)
        self.labelExpenditure = widgets.AlignedLabel()
        self.attach(self.labelExpenditure, 1, 22, 1, 1)

        separator = Gtk.Separator()
        separator.set_orientation(Gtk.Orientation.HORIZONTAL)
        self.attach(separator, 0, 23, 2, 1)

        label = widgets.AlignedLabel("Current Bank Balance")
        self.attach(label, 0, 24, 1, 1)
        self.labelBalance = widgets.AlignedLabel()
        self.attach(self.labelBalance, 1, 24, 1, 1)

    def run(self):
        club = user.get_user_club()

        for count, (key, item) in enumerate(club.accounts.incomes.items()):
            amount = display.currency(item.week)
            self.labels_week[count].set_label("%s" % (amount))

            amount = display.currency(item.season)
            self.labels_season[count].set_label("%s" % (amount))

        for count, (key, item) in enumerate(club.accounts.expenditures.items(), start=10):
            amount = display.currency(item.week)
            self.labels_week[count].set_label("%s" % (amount))

            amount = display.currency(item.season)
            self.labels_season[count].set_label("%s" % (amount))

        amount = display.currency(club.accounts.income)
        self.labelIncome.set_label("<b>%s</b>" % (amount))
        amount = display.currency(club.accounts.expenditure)
        self.labelExpenditure.set_label("<b>%s</b>" % (amount))
        amount = display.currency(club.accounts.balance)
        self.labelBalance.set_label("<b>%s</b>" % (amount))

        self.show_all()
