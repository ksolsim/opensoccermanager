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
import random

import dialogs
import display
import game
import loan
import money
import widgets


class Finances(Gtk.Grid):
    class Loan(Gtk.Grid):
        def __init__(self, labelLoan):
            self.labelLoan = labelLoan

            Gtk.Grid.__init__(self)
            self.set_vexpand(True)
            self.set_hexpand(False)
            self.set_row_spacing(5)
            self.set_column_spacing(5)
            self.set_border_width(5)

            label = widgets.AlignedLabel("A loan can be taken out to provide extra funds for a club, in order to purchase players and improve stadia. The interest is charged at a percentage agreed when the loan is taken out.")
            label.set_line_wrap(True)
            self.attach(label, 0, 1, 3, 1)

            label = widgets.AlignedLabel("Maximum Amount")
            self.attach(label, 0, 2, 1, 1)
            self.labelLoanMaximum = widgets.AlignedLabel()
            self.attach(self.labelLoanMaximum, 1, 2, 1, 1)
            label = widgets.AlignedLabel("Interest Rate")
            self.attach(label, 0, 3, 1, 1)
            self.labelLoanInterest = widgets.AlignedLabel()
            self.attach(self.labelLoanInterest, 1, 3, 1, 1)

            label = widgets.AlignedLabel("_Amount To Borrow")
            self.attach(label, 0, 4, 1, 1)
            self.spinbuttonAmount = Gtk.SpinButton()
            self.spinbuttonAmount.connect("value-changed", self.update_amount_button)
            label.set_mnemonic_widget(self.spinbuttonAmount)
            self.attach(self.spinbuttonAmount, 1, 4, 1, 1)
            label = widgets.AlignedLabel("_Repayment Period")
            self.attach(label, 0, 5, 1, 1)
            self.spinbuttonYears = Gtk.SpinButton.new_with_range(1, 5, 1)
            self.spinbuttonYears.connect("value-changed", self.update_amount_button)
            label.set_mnemonic_widget(self.spinbuttonYears)
            self.attach(self.spinbuttonYears, 1, 5, 1, 1)
            label = widgets.AlignedLabel("Years")
            self.attach(label, 2, 5, 1, 1)
            label = widgets.AlignedLabel("Weekly Repayment")
            self.attach(label, 0, 6, 1, 1)
            self.labelWeekly = widgets.AlignedLabel()
            self.attach(self.labelWeekly, 1, 6, 1, 1)

            buttonbox = Gtk.ButtonBox()
            buttonbox.set_layout(Gtk.ButtonBoxStyle.END)
            self.buttonApply = widgets.Button("_Borrow")
            self.buttonApply.set_sensitive(False)
            self.buttonApply.connect("clicked", self.apply_loan)
            buttonbox.add(self.buttonApply)
            self.attach(buttonbox, 0, 7, 3, 1)

            separator = Gtk.Separator()
            self.attach(separator, 0, 8, 3, 1)

            label = widgets.AlignedLabel("_Repay")
            self.attach(label, 0, 9, 1, 1)
            self.spinbuttonRepay = Gtk.SpinButton.new_with_range(0, 100000000, 10000)
            self.spinbuttonRepay.connect("value-changed", self.update_repay_button)
            label.set_mnemonic_widget(self.spinbuttonRepay)
            self.attach(self.spinbuttonRepay, 1, 9, 1, 1)
            buttonbox = Gtk.ButtonBox()
            buttonbox.set_layout(Gtk.ButtonBoxStyle.END)
            self.buttonRepay = widgets.Button("_Repay")
            self.buttonRepay.connect("clicked", self.repay_loan)
            buttonbox.add(self.buttonRepay)
            self.attach(buttonbox, 0, 10, 3, 1)

        def update_amount_button(self, spinbutton):
            sensitive = spinbutton.get_value_as_int() > 0
            self.buttonApply.set_sensitive(sensitive)

            amount = self.spinbuttonAmount.get_value_as_int()
            years = self.spinbuttonYears.get_value_as_int()
            weeks = years * 52

            repayment = game.bankloan.get_repayment(amount, weeks)
            repayment = display.currency(repayment)
            self.labelWeekly.set_label("%s" % (repayment))

        def update_repay_button(self, spinbutton):
            sensitive = spinbutton.get_value_as_int() > 0
            self.buttonRepay.set_sensitive(sensitive)

        def apply_loan(self, button):
            game.bankloan.amount = self.spinbuttonAmount.get_value_as_int()
            game.clubs[game.teamid].accounts.deposit(amount=game.bankloan.amount, category="loan")

            amount = self.spinbuttonAmount.get_value_as_int()
            years = self.spinbuttonYears.get_value_as_int()
            weeks = years * 52

            self.update_finances()

            button.set_sensitive(False)
            self.spinbuttonAmount.set_sensitive(False)
            self.spinbuttonYears.set_sensitive(False)
            self.spinbuttonRepay.set_sensitive(True)
            self.spinbuttonRepay.set_range(0, game.bankloan.amount)

        def repay_loan(self, button):
            '''
            Manual repayment of loan by user.
            '''
            amount = self.spinbuttonRepay.get_value_as_int()

            if game.clubs[game.teamid].accounts.request(amount):
                game.clubs[game.teamid].accounts.withdraw(amount, "loan")
                game.bankloan.amount -= amount

            self.spinbuttonRepay.set_range(0, game.bankloan.amount)

            self.update_finances()

            if game.bankloan.amount == 0:
                self.spinbuttonRepay.set_sensitive(False)
                self.spinbuttonAmount.set_sensitive(True)
                self.spinbuttonYears.set_sensitive(True)
                button.set_sensitive(False)

        def update_finances(self):
            amount = display.currency(game.bankloan.amount)
            self.labelLoan.set_label("%s" % (amount))

        def run(self):
            maximum = game.bankloan.get_maximum()
            amount = display.currency(maximum)
            self.labelLoanMaximum.set_label("%s" % (amount))

            self.labelLoanInterest.set_label("%i%%" % (game.bankloan.rate))

            self.spinbuttonAmount.set_value(0)
            self.spinbuttonAmount.set_range(0, maximum)
            self.spinbuttonAmount.set_increments(10000, 100000)
            self.spinbuttonRepay.set_range(0, game.bankloan.amount)
            self.spinbuttonRepay.set_value(game.bankloan.amount)

            amount = display.currency(0)
            self.labelWeekly.set_label("%s" % (amount))

            # Setup buttons for loan status
            if game.bankloan.amount > 0:
                self.spinbuttonAmount.set_sensitive(False)
                self.spinbuttonYears.set_sensitive(False)
                self.spinbuttonRepay.set_sensitive(True)
                self.buttonRepay.set_sensitive(True)
            else:
                self.spinbuttonRepay.set_sensitive(False)
                self.buttonRepay.set_sensitive(False)

    class Overdraft(Gtk.Grid):
        def __init__(self, labelOverdraft):
            self.labelOverdraft = labelOverdraft

            Gtk.Grid.__init__(self)
            self.set_vexpand(True)
            self.set_hexpand(False)
            self.set_row_spacing(5)
            self.set_column_spacing(5)
            self.set_border_width(5)

            label = widgets.AlignedLabel("An overdraft can be applied for to provide extra cash reserves for the club, up to an amount determined by the assets of the club. A percentage is charged on the amount owed.")
            label.set_line_wrap(Gtk.WrapMode.WORD)
            self.attach(label, 0, 0, 3, 1)

            label = widgets.AlignedLabel("Maximum Amount")
            self.attach(label, 0, 1, 1, 1)
            self.labelOverdraftMaximum = widgets.AlignedLabel()
            self.attach(self.labelOverdraftMaximum, 1, 1, 1, 1)
            label = widgets.AlignedLabel("Interest Rate")
            self.attach(label, 0, 2, 1, 1)
            self.labelOverdraftInterest = widgets.AlignedLabel()
            self.attach(self.labelOverdraftInterest, 1, 2, 1, 1)
            label = widgets.AlignedLabel("_Amount For Overdraft")
            self.attach(label, 0, 3, 1, 1)
            self.spinbuttonOverdraft = Gtk.SpinButton()
            self.spinbuttonOverdraft.connect("value-changed", self.update_overdraft_button)
            label.set_mnemonic_widget(self.spinbuttonOverdraft)
            self.attach(self.spinbuttonOverdraft, 1, 3, 1, 1)
            label = widgets.AlignedLabel("Overdraft Charge")
            self.attach(label, 0, 4, 1, 1)
            self.labelOverdraftCharge = widgets.AlignedLabel()
            self.attach(self.labelOverdraftCharge, 1, 4, 1, 1)

            buttonbox = Gtk.ButtonBox()
            buttonbox.set_layout(Gtk.ButtonBoxStyle.END)
            self.attach(buttonbox, 0, 5, 3, 1)
            self.buttonApplyOverdraft = widgets.Button("_Apply")
            self.buttonApplyOverdraft.set_sensitive(False)
            self.buttonApplyOverdraft.connect("clicked", self.apply_overdraft)
            buttonbox.add(self.buttonApplyOverdraft)

        def apply_overdraft(self, button):
            game.overdraft.amount = self.spinbuttonOverdraft.get_value_as_int()

            self.update_finances()

        def update_overdraft_button(self, spinbutton):
            if spinbutton.get_value_as_int() > 0 or game.overdraft.amount > 0:
                self.buttonApplyOverdraft.set_sensitive(True)
            else:
                self.buttonApplyOverdraft.set_sensitive(False)

            charge = self.spinbuttonOverdraft.get_value_as_int() * 0.01
            charge = display.currency(charge)
            self.labelOverdraftCharge.set_label("%s" % (charge))

        def update_finances(self):
            amount = display.currency(game.overdraft.amount)
            self.labelOverdraft.set_label("%s" % (amount))

        def run(self):
            maximum = game.overdraft.get_maximum()
            amount = display.currency(maximum)
            self.labelOverdraftMaximum.set_label("%s" % (amount))

            self.labelOverdraftInterest.set_label("%i%%" % (game.overdraft.rate))

            self.spinbuttonOverdraft.set_value(game.overdraft.amount)
            self.spinbuttonOverdraft.set_range(0, maximum)
            self.spinbuttonOverdraft.set_increments(10000, 100000)

            amount = display.currency(0)
            self.labelOverdraftCharge.set_label("%s" % (amount))

    class Grant(Gtk.Grid):
        def __init__(self, labelGrant):
            self.labelGrant = labelGrant

            Gtk.Grid.__init__(self)
            self.set_vexpand(True)
            self.set_hexpand(False)
            self.set_row_spacing(5)
            self.set_column_spacing(5)
            self.set_border_width(5)

            label = widgets.AlignedLabel("Stadium improvement grants are available for clubs to improve features of their stadium, or the shops outside. Certain criteria must be met before a grant can be considered, including current capacity, average attedances, existing club financials, and the club reputation.")
            label.set_line_wrap(Gtk.WrapMode.WORD)
            self.attach(label, 0, 0, 2, 1)
            self.labelGrantStatus = widgets.AlignedLabel("An improvement grant is not currently available.")
            self.labelGrantStatus.set_line_wrap(Gtk.WrapMode.WORD)
            self.attach(self.labelGrantStatus, 0, 1, 2, 1)

            label = widgets.AlignedLabel("_Grant Amount To Request:")
            self.attach(label, 0, 2, 1, 1)
            self.spinbuttonGrant = Gtk.SpinButton()
            self.spinbuttonGrant.set_increments(1000, 10000)
            label.set_mnemonic_widget(self.spinbuttonGrant)
            self.attach(self.spinbuttonGrant, 1, 2, 1, 1)

            buttonbox = Gtk.ButtonBox()
            buttonbox.set_layout(Gtk.ButtonBoxStyle.END)
            self.attach(buttonbox, 0, 3, 2, 1)
            self.buttonGrant = widgets.Button("_Apply")
            self.buttonGrant.set_sensitive(False)
            self.buttonGrant.connect("clicked", self.apply_grant)
            buttonbox.add(self.buttonGrant)

        def apply_grant(self, button):
            self.spinbuttonGrant.set_sensitive(False)
            self.buttonGrant.set_sensitive(False)

            game.grant.amount = self.spinbuttonGrant.get_value_as_int()

        def run(self):
            if game.grant.get_grant_allowed():
                maximum = game.grant.get_grant_maximum()
                value = display.currency(maximum)
                self.labelGrantStatus.set_label("A maximum grant amount of %s is available." % (value))

                self.buttonGrant.set_sensitive(True)
                self.spinbuttonGrant.set_sensitive(True)
                self.spinbuttonGrant.set_value(0)
                self.spinbuttonGrant.set_range(0, game.grant.maximum)
                self.spinbuttonGrant.set_increments(10000, 100000)
            else:
                self.labelGrantStatus.set_label("An improvement grant is not currently available.")

                self.buttonGrant.set_sensitive(False)
                self.spinbuttonGrant.set_sensitive(False)

    class Flotation(Gtk.Grid):
        def __init__(self, labelFlotation):
            self.labelFlotation = labelFlotation

            Gtk.Grid.__init__(self)
            self.set_vexpand(True)
            self.set_hexpand(False)
            self.set_row_spacing(5)
            self.set_column_spacing(5)
            self.set_border_width(5)

            label = widgets.AlignedLabel("A club can be floated on the stock market to generate cash for transfers, stadium improvements, paying off debt, and much more. The club will then be owned by the shareholders who receive dividend payments for the initial investment. Calculation of the amount flotation will generate is made using the clubs current form, assets, and future potential.")
            label.set_line_wrap(Gtk.WrapMode.WORD)
            self.attach(label, 0, 0, 1, 1)
            label = widgets.AlignedLabel("<b>Once the club has been floated on the stock market, it can not be taken private again.</b>")
            label.set_line_wrap(Gtk.WrapMode.WORD)
            self.attach(label, 0, 1, 1, 1)
            self.labelFlotationAmount = widgets.AlignedLabel()
            self.attach(self.labelFlotationAmount, 0, 3, 1, 1)
            buttonbox = Gtk.ButtonBox()
            buttonbox.set_layout(Gtk.ButtonBoxStyle.END)
            self.attach(buttonbox, 0, 4, 1, 1)
            buttonFloat = widgets.Button("_Float")
            buttonFloat.connect("clicked", self.apply_float)
            buttonbox.add(buttonFloat)

        def apply_float(self, button):
            if dialogs.float_club(game.flotation.amount):
                game.flotation.status = 1
                game.flotation.timeout = random.randint(12, 16)

                button.set_sensitive(False)

        def run(self):
            amount = display.currency(game.flotation.amount)
            self.labelFlotationAmount.set_label("Floating at this time would raise %s." % (amount))

    def __init__(self):
        Gtk.Grid.__init__(self)
        self.set_vexpand(True)
        self.set_border_width(5)
        self.set_row_spacing(5)
        self.set_column_spacing(5)
        self.set_column_homogeneous(True)

        notebook = Gtk.Notebook()
        self.attach(notebook, 0, 0, 1, 5)

        # Overview
        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)
        self.attach(grid, 1, 0, 1, 1)

        label = widgets.AlignedLabel("<b>Finances Overview</b>")
        grid.attach(label, 0, 0, 1, 1)

        label = widgets.AlignedLabel("Current Loan")
        grid.attach(label, 0, 1, 1, 1)
        self.labelLoan = widgets.AlignedLabel()
        grid.attach(self.labelLoan, 1, 1, 1, 1)
        label = widgets.AlignedLabel("Current Overdraft")
        grid.attach(label, 0, 2, 1, 1)
        self.labelOverdraft = widgets.AlignedLabel()
        grid.attach(self.labelOverdraft, 1, 2, 1, 1)
        label = widgets.AlignedLabel("Stadium Improvement Status")
        grid.attach(label, 0, 3, 1, 1)
        self.labelGrant = widgets.AlignedLabel()
        grid.attach(self.labelGrant, 1, 3, 1, 1)
        label = widgets.AlignedLabel("Public Flotation Estimate")
        grid.attach(label, 0, 4, 1, 1)
        self.labelFlotation = widgets.AlignedLabel()
        grid.attach(self.labelFlotation, 1, 4, 1, 1)

        # Loan
        label = Gtk.Label("_Loan")
        label.set_use_underline(True)

        self.loan = self.Loan(self.labelLoan)
        notebook.append_page(self.loan, label)

        # Overdraft
        label = Gtk.Label("_Overdraft")
        label.set_use_underline(True)

        self.overdraft = self.Overdraft(self.labelOverdraft)
        notebook.append_page(self.overdraft, label)

        # Stadium Improvement
        label = Gtk.Label("_Stadium Improvement")
        label.set_use_underline(True)

        self.grant = self.Grant(self.labelGrant)
        notebook.append_page(self.grant, label)

        # Flotation
        label = Gtk.Label("_Flotation")
        label.set_use_underline(True)

        self.flotation = self.Flotation(self.labelFlotation)
        notebook.append_page(self.flotation, label)

    def run(self):
        self.loan.run()
        self.overdraft.run()
        self.grant.run()
        self.flotation.run()

        # Update overview
        amount = display.currency(game.bankloan.amount)
        self.labelLoan.set_label("%s" % (amount))

        amount = display.currency(game.overdraft.amount)
        self.labelOverdraft.set_label("%s" % (amount))

        if game.grant.get_grant_allowed():
            amount = display.currency(game.grant.get_grant_maximum())
        else:
            amount = "Not Available"

        self.labelGrant.set_label("%s" % (amount))

        amount = display.currency(game.flotation.amount)
        self.labelFlotation.set_label("%s" % (amount))

        self.show_all()


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
        club = game.clubs[game.teamid]

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
