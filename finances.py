#!/usr/bin/env python3

from gi.repository import Gtk
import random

import game
import constants
import display
import dialogs
import widgets
import money
import calculator


class Finances(Gtk.Grid):
    def __init__(self):
        Gtk.Grid.__init__(self)
        self.set_vexpand(True)
        self.set_border_width(5)
        self.set_row_spacing(5)
        self.set_column_spacing(5)
        self.set_column_homogeneous(True)

        notebook = Gtk.Notebook()
        self.attach(notebook, 0, 0, 1, 5)

        # Loan
        grid = Gtk.Grid()
        grid.set_vexpand(True)
        grid.set_hexpand(False)
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)
        grid.set_border_width(5)
        notebook.append_page(grid, Gtk.Label("Loan"))

        label = widgets.AlignedLabel("A loan can be taken out to provide extra funds for a club, in order to purchase players and improve stadia. The interest is charged at a percentage agreed when the loan is taken out.")
        label.set_line_wrap(True)
        grid.attach(label, 0, 1, 3, 1)

        label = widgets.AlignedLabel("Maximum Amount")
        grid.attach(label, 0, 2, 1, 1)
        self.labelLoanMaximum = widgets.AlignedLabel()
        grid.attach(self.labelLoanMaximum, 1, 2, 1, 1)
        label = widgets.AlignedLabel("Interest Rate")
        grid.attach(label, 0, 3, 1, 1)
        self.labelLoanInterest = widgets.AlignedLabel()
        grid.attach(self.labelLoanInterest, 1, 3, 1, 1)

        label = widgets.AlignedLabel("Amount To Borrow")
        grid.attach(label, 0, 4, 1, 1)
        self.spinbuttonAmount = Gtk.SpinButton()
        self.spinbuttonAmount.connect("value-changed", self.update_amount_button)
        grid.attach(self.spinbuttonAmount, 1, 4, 1, 1)
        label = widgets.AlignedLabel("Repayment Period")
        grid.attach(label, 0, 5, 1, 1)
        self.spinbuttonYears = Gtk.SpinButton.new_with_range(1, 5, 1)
        self.spinbuttonYears.connect("value-changed", self.update_amount_button)
        grid.attach(self.spinbuttonYears, 1, 5, 1, 1)
        label = widgets.AlignedLabel("Years")
        grid.attach(label, 2, 5, 1, 1)
        label = widgets.AlignedLabel("Weekly Repayment")
        grid.attach(label, 0, 6, 1, 1)
        self.labelWeekly = widgets.AlignedLabel()
        grid.attach(self.labelWeekly, 1, 6, 1, 1)

        buttonbox = Gtk.ButtonBox()
        buttonbox.set_layout(Gtk.ButtonBoxStyle.END)
        self.buttonApply = widgets.Button("_Borrow")
        self.buttonApply.set_sensitive(False)
        self.buttonApply.connect("clicked", self.apply_loan)
        buttonbox.add(self.buttonApply)
        grid.attach(buttonbox, 0, 7, 3, 1)

        separator = Gtk.Separator()
        grid.attach(separator, 0, 8, 3, 1)

        label = widgets.AlignedLabel("Repay")
        grid.attach(label, 0, 9, 1, 1)
        self.spinbuttonRepay = Gtk.SpinButton.new_with_range(0, 100000000, 10000)
        self.spinbuttonRepay.connect("value-changed", self.update_repay_button)
        grid.attach(self.spinbuttonRepay, 1, 9, 1, 1)
        buttonbox = Gtk.ButtonBox()
        buttonbox.set_layout(Gtk.ButtonBoxStyle.END)
        self.buttonRepay = widgets.Button("_Repay")
        self.buttonRepay.connect("clicked", self.repay_loan)
        buttonbox.add(self.buttonRepay)
        grid.attach(buttonbox, 0, 10, 3, 1)

        # Overdraft
        grid = Gtk.Grid()
        grid.set_vexpand(True)
        grid.set_hexpand(False)
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)
        grid.set_border_width(5)
        notebook.append_page(grid, Gtk.Label("Overdraft"))

        label = widgets.AlignedLabel("An overdraft can be applied for to provide extra cash reserves for the club, up to an amount determined by the assets of the club. A percentage is charged on the amount owed.")
        label.set_line_wrap(Gtk.WrapMode.WORD)
        grid.attach(label, 0, 0, 3, 1)

        label = widgets.AlignedLabel("Maximum Amount")
        grid.attach(label, 0, 1, 1, 1)
        self.labelOverdraftMaximum = widgets.AlignedLabel()
        grid.attach(self.labelOverdraftMaximum, 1, 1, 1, 1)
        label = widgets.AlignedLabel("Interest Rate")
        grid.attach(label, 0, 2, 1, 1)
        self.labelOverdraftInterest = widgets.AlignedLabel()
        grid.attach(self.labelOverdraftInterest, 1, 2, 1, 1)
        label = widgets.AlignedLabel("Amount For Overdraft")
        grid.attach(label, 0, 3, 1, 1)
        self.spinbuttonOverdraft = Gtk.SpinButton()
        self.spinbuttonOverdraft.connect("value-changed", self.update_overdraft_button)
        grid.attach(self.spinbuttonOverdraft, 1, 3, 1, 1)
        label = widgets.AlignedLabel("Overdraft Charge")
        grid.attach(label, 0, 4, 1, 1)
        self.labelOverdraftCharge = widgets.AlignedLabel()
        grid.attach(self.labelOverdraftCharge, 1, 4, 1, 1)

        buttonbox = Gtk.ButtonBox()
        buttonbox.set_layout(Gtk.ButtonBoxStyle.END)
        grid.attach(buttonbox, 0, 5, 3, 1)
        self.buttonApplyOverdraft = widgets.Button("_Apply")
        self.buttonApplyOverdraft.set_sensitive(False)
        self.buttonApplyOverdraft.connect("clicked", self.apply_overdraft)
        buttonbox.add(self.buttonApplyOverdraft)

        # Stadium Improvement
        grid = Gtk.Grid()
        grid.set_vexpand(True)
        grid.set_hexpand(False)
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)
        grid.set_border_width(5)
        notebook.append_page(grid, Gtk.Label("Stadium Improvement"))

        label = widgets.AlignedLabel("Stadium improvement grants are available for clubs to improve features of their stadium, or the shops outside. Certain criteria must be met before a grant can be considered, including current capacity, average attedances, existing club financials, and the club reputation.")
        label.set_line_wrap(Gtk.WrapMode.WORD)
        grid.attach(label, 0, 0, 2, 1)
        self.labelGrantStatus = widgets.AlignedLabel("An improvement grant is not currently available.")
        self.labelGrantStatus.set_line_wrap(Gtk.WrapMode.WORD)
        grid.attach(self.labelGrantStatus, 0, 1, 2, 1)

        label = widgets.AlignedLabel("Amount to request for grant:")
        grid.attach(label, 0, 2, 1, 1)
        self.spinbuttonGrant = Gtk.SpinButton()
        self.spinbuttonGrant.set_increments(1000, 10000)
        grid.attach(self.spinbuttonGrant, 1, 2, 1, 1)

        buttonbox = Gtk.ButtonBox()
        buttonbox.set_layout(Gtk.ButtonBoxStyle.END)
        grid.attach(buttonbox, 0, 3, 2, 1)
        self.buttonGrant = widgets.Button("_Apply")
        self.buttonGrant.set_sensitive(False)
        self.buttonGrant.connect("clicked", self.apply_grant)
        buttonbox.add(self.buttonGrant)

        # Flotation
        grid = Gtk.Grid()
        grid.set_vexpand(True)
        grid.set_hexpand(False)
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)
        grid.set_border_width(5)
        notebook.append_page(grid, Gtk.Label("Flotation"))

        label = widgets.AlignedLabel("A club can be floated on the stock market to generate cash for transfers, stadium improvements, paying off debt, and much more. The club will then be owned by the shareholders who receive dividend payments for the initial investment. Calculation of the amount flotation will generate is made using the clubs current form, assets, and future potential.")
        label.set_line_wrap(Gtk.WrapMode.WORD)
        grid.attach(label, 0, 0, 1, 1)
        label = widgets.AlignedLabel("<b>Once the club has been floated on the stock market, it can not be taken private again.</b>")
        label.set_line_wrap(Gtk.WrapMode.WORD)
        grid.attach(label, 0, 1, 1, 1)
        self.labelFlotationAmount = widgets.AlignedLabel()
        grid.attach(self.labelFlotationAmount, 0, 3, 1, 1)
        buttonbox = Gtk.ButtonBox()
        buttonbox.set_layout(Gtk.ButtonBoxStyle.END)
        grid.attach(buttonbox, 0, 4, 1, 1)
        buttonFloat = widgets.Button("_Float")
        buttonFloat.connect("clicked", self.apply_float)
        buttonbox.add(buttonFloat)

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

    def apply_loan(self, button):
        game.bankloan.amount = self.spinbuttonAmount.get_value_as_int()
        money.deposit(game.bankloan.amount, 7)

        amount = self.spinbuttonAmount.get_value_as_int()
        years = self.spinbuttonYears.get_value_as_int()
        weeks = years * 52

        game.bankloan.repayment = money.calculate_loan_repayment(amount, weeks)

        self.update_finances(0)

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

        if money.request(amount):
            money.withdraw(amount, 16)
            game.bankloan.amount -= amount

        self.spinbuttonRepay.set_range(0, game.bankloan.amount)

        self.update_finances(0)

        if game.bankloan.amount == 0:
            self.spinbuttonRepay.set_sensitive(False)
            self.spinbuttonAmount.set_sensitive(True)
            self.spinbuttonYears.set_sensitive(True)
            button.set_sensitive(False)

    def apply_overdraft(self, button):
        game.overdraft.amount = self.spinbuttonOverdraft.get_value_as_int()

        self.update_finances(1)

    def apply_grant(self, button):
        self.spinbuttonGrant.set_sensitive(False)
        self.buttonGrant.set_sensitive(False)

        game.grant.status = False
        game.grant.timeout = random.randint(8, 10)
        game.grant.amount = self.spinbuttonGrant.get_value_as_int()

        money.process_grant()

    def apply_float(self, button):
        state = dialogs.float_club(game.flotation.amount)

        if state:
            game.flotation.status = 1
            game.flotation.timeout = random.randint(12, 16)

            button.set_sensitive(False)

    def update_finances(self, index):
        if index == 0:
            amount = display.currency(game.bankloan.amount)
            self.labelLoan.set_label("%s" % (amount))
        elif index == 1:
            amount = display.currency(game.overdraft.amount)
            self.labelOverdraft.set_label("%s" % (amount))

    def update_amount_button(self, spinbutton):
        if spinbutton.get_value_as_int() > 0:
            self.buttonApply.set_sensitive(True)
        else:
            self.buttonApply.set_sensitive(False)

        amount = self.spinbuttonAmount.get_value_as_int()
        years = self.spinbuttonYears.get_value_as_int()
        weeks = years * 52

        repayment = money.calculate_loan_repayment(amount, weeks)
        repayment = display.currency(repayment)
        self.labelWeekly.set_label("%s" % (repayment))

    def update_repay_button(self, spinbutton):
        if spinbutton.get_value_as_int() > 0:
            self.buttonRepay.set_sensitive(True)
        else:
            self.buttonRepay.set_sensitive(False)

    def update_overdraft_button(self, spinbutton):
        if spinbutton.get_value_as_int() > 0 or game.overdraft.amount > 0:
            self.buttonApplyOverdraft.set_sensitive(True)
        else:
            self.buttonApplyOverdraft.set_sensitive(False)

        charge = self.spinbuttonOverdraft.get_value_as_int() * 0.01
        charge = display.currency(charge)
        self.labelOverdraftCharge.set_label("%s" % (charge))

    def run(self):
        club = game.clubs[game.teamid]

        # Loan
        amount = display.currency(game.bankloan.maximum)
        self.labelLoanMaximum.set_label("%s" % (amount))

        self.labelLoanInterest.set_label("%i%%" % (game.bankloan.rate))

        self.spinbuttonAmount.set_value(0)
        self.spinbuttonAmount.set_range(0, game.bankloan.maximum)
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

        # Overdraft
        amount = display.currency(game.overdraft.maximum)
        self.labelOverdraftMaximum.set_label("%s" % (amount))

        self.labelOverdraftInterest.set_label("%i%%" % (game.overdraft.rate))

        self.spinbuttonOverdraft.set_value(game.overdraft.amount)
        self.spinbuttonOverdraft.set_range(0, game.overdraft.maximum)
        self.spinbuttonOverdraft.set_increments(10000, 100000)

        amount = display.currency(0)
        self.labelOverdraftCharge.set_label("%s" % (amount))

        # Grant
        if game.grant.status:
            value = display.currency(game.grant.maximum)
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

        # Float
        amount = display.currency(game.flotation.amount)
        self.labelFlotationAmount.set_label("Floating at this time would raise %s." % (amount))

        # Update overview
        amount = display.currency(game.bankloan.amount)
        self.labelLoan.set_label("%s" % (amount))

        amount = display.currency(game.overdraft.amount)
        self.labelOverdraft.set_label("%s" % (amount))

        if game.grant.maximum > 0:
            amount = display.currency(game.grant.maximum)
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

        for x in range(0, 9):
            label = widgets.AlignedLabel()
            self.labels_week.append(label)
            self.attach(label, 1, x + 1, 1, 1)

            label = widgets.AlignedLabel()
            self.labels_season.append(label)
            self.attach(label, 2, x + 1, 1, 1)

        for x in range(9, 19):
            label = widgets.AlignedLabel()
            self.labels_week.append(label)
            self.attach(label, 5, x - 8, 1, 1)

            label = widgets.AlignedLabel()
            self.labels_season.append(label)
            self.attach(label, 6, x - 8, 1, 1)

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
        label = widgets.AlignedLabel("Television Money")
        self.attach(label, 0, 9, 1, 1)

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

        for item in range(0, 9):
            amount = display.currency(club.accounts[item][0])
            self.labels_week[item].set_label("%s" % (amount))

            amount = display.currency(club.accounts[item][1])
            self.labels_season[item].set_label("%s" % (amount))

        for item in range(9, 19):
            amount = display.currency(club.accounts[item][0])
            self.labels_week[item].set_label("%s" % (amount))

            amount = display.currency(club.accounts[item][1])
            self.labels_season[item].set_label("%s" % (amount))

        amount = display.currency(club.income)
        self.labelIncome.set_label("<b>%s</b>" % (amount))
        amount = display.currency(club.expenditure)
        self.labelExpenditure.set_label("<b>%s</b>" % (amount))
        amount = display.currency(club.balance)
        self.labelBalance.set_label("<b>%s</b>" % (amount))

        self.show_all()
