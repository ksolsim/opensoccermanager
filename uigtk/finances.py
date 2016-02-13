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

import data
import uigtk.widgets


class Finances(uigtk.widgets.Grid):
    __name__ = "finances"

    def __init__(self):
        uigtk.widgets.Grid.__init__(self)
        self.set_column_homogeneous(True)

        self.loan = Loan()
        self.attach(self.loan, 0, 0, 1, 1)
        self.grant = Grant()
        self.attach(self.grant, 0, 1, 1, 1)
        self.overdraft = Overdraft()
        self.attach(self.overdraft, 1, 0, 1, 1)
        self.flotation = Flotation()
        self.attach(self.flotation, 1, 1, 1, 1)

    def run(self):
        self.show_all()
        self.loan.run()
        self.overdraft.run()
        self.grant.run()
        self.flotation.run()


class Loan(uigtk.widgets.CommonFrame):
    class LoanApplication(uigtk.widgets.Grid):
        class LoanDialog(Gtk.MessageDialog):
            def __init__(self, amount, interest, period):
                Gtk.MessageDialog.__init__(self)
                self.set_transient_for(data.window)
                self.set_modal(True)
                self.set_title("Confirm Loan")
                self.set_property("message-type", Gtk.MessageType.QUESTION)
                self.set_markup("Apply for a %i year loan of %s at %i%% interest?" % (period, amount, interest))
                self.add_button("_Cancel", Gtk.ResponseType.CANCEL)
                self.add_button("C_onfirm", Gtk.ResponseType.OK)
                self.set_default_response(Gtk.ResponseType.CANCEL)

            def show(self):
                state = self.run() == Gtk.ResponseType.OK
                self.destroy()

                return state

        def __init__(self):
            uigtk.widgets.Grid.__init__(self)

            grid = uigtk.widgets.Grid()
            self.attach(grid, 0, 1, 1, 1)

            label = uigtk.widgets.Label("Loan _Amount", leftalign=True)
            grid.attach(label, 0, 0, 1, 1)
            self.spinbuttonAmount = Gtk.SpinButton()
            self.spinbuttonAmount.set_increments(100000, 1000000)
            self.spinbuttonAmount.connect("value-changed", self.on_amount_changed)
            label.set_mnemonic_widget(self.spinbuttonAmount)
            grid.attach(self.spinbuttonAmount, 1, 0, 1, 1)

            label = uigtk.widgets.Label("Loan _Period", leftalign=True)
            grid.attach(label, 0, 1, 1, 1)
            self.spinbuttonPeriod = Gtk.SpinButton()
            self.spinbuttonPeriod.set_range(1, 5)
            self.spinbuttonPeriod.set_increments(1, 1)
            self.spinbuttonPeriod.set_numeric(False)
            self.spinbuttonPeriod.connect("output", self.format_repayment_output)
            label.set_mnemonic_widget(self.spinbuttonPeriod)
            grid.attach(self.spinbuttonPeriod, 1, 1, 1, 1)

            buttonbox = uigtk.widgets.ButtonBox()
            buttonbox.set_hexpand(True)
            buttonbox.set_layout(Gtk.ButtonBoxStyle.END)
            self.attach(buttonbox, 0, 2, 1, 1)

            self.buttonApply = uigtk.widgets.Button("_Apply")
            self.buttonApply.set_sensitive(False)
            self.buttonApply.set_tooltip_text("Apply specified loan amount with current interest rate.")
            buttonbox.add(self.buttonApply)

        def on_amount_changed(self, spinbutton):
            '''
            Update apply button if loan amount is greater than zero.
            '''
            sensitive = spinbutton.get_value() > 0
            self.buttonApply.set_sensitive(sensitive)

        def format_repayment_output(self, spinbutton):
            '''
            Format year string onto period spinbutton.
            '''
            value = spinbutton.get_value_as_int()

            if value > 1:
                text = "Years"
            else:
                text = "Year"

            spinbutton.set_text("%i %s" % (value, text))

            return True

    class LoanRepayment(uigtk.widgets.Grid):
        def __init__(self):
            uigtk.widgets.Grid.__init__(self)

            grid = uigtk.widgets.Grid()
            self.attach(grid, 0, 0, 1, 1)

            label = uigtk.widgets.Label("Outstanding Loan", leftalign=True)
            grid.attach(label, 0, 0, 1, 1)
            self.labelOutstanding = uigtk.widgets.Label(leftalign=True)
            grid.attach(self.labelOutstanding, 1, 0, 1, 1)

            label = uigtk.widgets.Label("Repay _Amount", leftalign=True)
            grid.attach(label, 0, 1, 1, 1)
            self.spinbuttonRepay = Gtk.SpinButton()
            self.spinbuttonRepay.set_increments(100000, 1000000)
            self.spinbuttonRepay.set_value(0)
            self.spinbuttonRepay.connect("value-changed", self.on_repay_changed)
            label.set_mnemonic_widget(self.spinbuttonRepay)
            grid.attach(self.spinbuttonRepay, 1, 1, 1, 1)

            buttonbox = uigtk.widgets.ButtonBox()
            buttonbox.set_hexpand(True)
            buttonbox.set_layout(Gtk.ButtonBoxStyle.END)
            self.attach(buttonbox, 0, 1, 2, 1)

            self.buttonRepay = uigtk.widgets.Button("_Repay")
            self.buttonRepay.set_sensitive(False)
            self.buttonRepay.set_tooltip_text("Repay specified amount of outstanding loan.")
            buttonbox.add(self.buttonRepay)

        def on_repay_changed(self, spinbutton):
            '''
            Update repay button if repay amount is greater than zero.
            '''
            sensitive = spinbutton.get_value() > 0
            self.buttonRepay.set_sensitive(sensitive)

        def update_interface(self):
            '''
            Update range of spinbutton for repayment.
            '''
            loan = data.currency.get_amount(self.club.finances.loan.amount)
            loan = "%s%s" % (data.currency.get_currency_symbol(), data.currency.get_comma_value(loan))

            self.labelOutstanding.set_label(loan)
            self.spinbuttonRepay.set_range(0, self.club.finances.loan.amount)

    def __init__(self):
        uigtk.widgets.CommonFrame.__init__(self, "Loan")
        self.set_vexpand(False)

        label = uigtk.widgets.Label("A loan can be taken out to provide extra funds for a club, in order to purchase players and improve stadia. The interest is charged at a percentage agreed when the loan is taken out.", leftalign=True)
        label.set_width_chars(40)
        label.set_xalign(0)
        label.set_line_wrap(True)
        self.grid.attach(label, 0, 0, 1, 1)

        self.labelStatus = uigtk.widgets.Label(leftalign=True)
        self.labelStatus.set_line_wrap(True)
        self.grid.attach(self.labelStatus, 0, 2, 1, 1)

        self.stack = Gtk.Stack()
        self.grid.attach(self.stack, 0, 3, 1, 1)

        self.application = self.LoanApplication()
        self.application.buttonApply.connect("clicked", self.on_apply_clicked)
        self.stack.add_named(self.application, "application")

        self.repayment = self.LoanRepayment()
        self.repayment.buttonRepay.connect("clicked", self.on_repay_clicked)
        self.stack.add_named(self.repayment, "repayment")

    def on_apply_clicked(self, *args):
        '''
        Claim loan for specified amount and repayment period.
        '''
        amount = self.application.spinbuttonAmount.get_value_as_int()

        loan = data.currency.get_amount(amount)
        loan = "%s%s" % (data.currency.get_currency_symbol(), data.currency.get_comma_value(loan))

        period = self.application.spinbuttonPeriod.get_value_as_int()

        dialog = self.application.LoanDialog(loan, self.club.finances.loan.interest, period)

        if dialog.show():
            self.club.finances.loan.amount = amount
            self.club.finances.loan.period = period

            self.application.spinbuttonAmount.set_value(0)
            self.application.spinbuttonPeriod.set_value(1)

            self.club.accounts.deposit(amount, category="loan")

            self.stack.set_visible_child_name("repayment")
            self.repayment.update_interface()

    def on_repay_clicked(self, *args):
        '''
        Repay defined loan amount.
        '''
        repayment = self.repayment.spinbuttonRepay.get_value_as_int()

        if self.club.accounts.request(repayment):
            self.club.finances.loan.amount -= repayment

            self.club.accounts.withdraw(repayment, category="loan")

            self.repayment.spinbuttonRepay.set_range(0, self.club.finances.loan.amount)
            self.repayment.spinbuttonRepay.set_value(0)
            self.repayment.update_interface()

            if self.club.finances.loan.amount == 0:
                self.stack.set_visible_child_name("application")

    def run(self):
        self.club = data.clubs.get_club_by_id(data.user.team)

        self.application.club = self.club
        self.repayment.club = self.club

        self.stack.set_visible_child_name("application")

        maximum = self.club.finances.loan.get_maximum_loan()
        amount = data.currency.get_amount(maximum)
        amount = "%s%s" % (data.currency.get_currency_symbol(), data.currency.get_comma_value(amount))

        self.labelStatus.set_label("The maximum loan allowed at this time is %s with an interest rate of %i%%." % (amount, self.club.finances.loan.interest))

        self.application.spinbuttonAmount.set_range(0, maximum)
        self.application.spinbuttonAmount.set_value(self.club.finances.loan.amount)
        self.application.spinbuttonPeriod.set_value(self.club.finances.loan.period)


class Overdraft(uigtk.widgets.CommonFrame):
    class OverdraftDialog(Gtk.MessageDialog):
        def __init__(self, amount, interest):
            Gtk.MessageDialog.__init__(self)
            self.set_transient_for(data.window)
            self.set_modal(True)
            self.set_title("Confirm Overdraft")
            self.set_property("message-type", Gtk.MessageType.QUESTION)
            self.set_markup("Raise overdraft to %s with a %i%% interest charge?" % (amount, interest))
            self.add_button("_Cancel", Gtk.ResponseType.CANCEL)
            self.add_button("C_onfirm", Gtk.ResponseType.OK)
            self.set_default_response(Gtk.ResponseType.CANCEL)

        def show(self):
            state = self.run() == Gtk.ResponseType.OK
            self.destroy()

            return state

    def __init__(self):
        uigtk.widgets.CommonFrame.__init__(self, "Overdraft")
        self.set_vexpand(False)

        label = uigtk.widgets.Label("An overdraft can be applied for to provide extra cash reserves for the club, up to an amount determined by the assets of the club. A percentage is charged on the amount owed.", leftalign=True)
        label.set_xalign(0)
        label.set_line_wrap(True)
        self.grid.attach(label, 0, 0, 1, 1)

        self.labelStatus = uigtk.widgets.Label(leftalign=True)
        self.labelStatus.set_line_wrap(True)
        self.grid.attach(self.labelStatus, 0, 1, 1, 1)

        grid = uigtk.widgets.Grid()
        self.grid.attach(grid, 0, 2, 1, 1)

        label = uigtk.widgets.Label("_Overdraft Amount", leftalign=True)
        grid.attach(label, 0, 0, 1, 1)
        self.spinbuttonOverdraft = uigtk.widgets.SpinButton()
        self.spinbuttonOverdraft.set_increments(100000, 1000000)
        self.spinbuttonOverdraft.connect("value-changed", self.on_overdraft_changed)
        label.set_mnemonic_widget(self.spinbuttonOverdraft)
        grid.attach(self.spinbuttonOverdraft, 1, 0, 1, 1)

        buttonbox = uigtk.widgets.ButtonBox()
        buttonbox.set_layout(Gtk.ButtonBoxStyle.END)
        self.grid.attach(buttonbox, 0, 3, 1, 1)

        self.buttonApply = uigtk.widgets.Button("_Apply")
        self.buttonApply.set_sensitive(False)
        self.buttonApply.set_tooltip_text("Apply overdraft for specified amount.")
        self.buttonApply.connect("clicked", self.on_apply_clicked)
        buttonbox.add(self.buttonApply)

    def on_overdraft_changed(self, spinbutton):
        '''
        Change sensitivity of apply button.
        '''
        sensitive = spinbutton.get_value_as_int() > 0
        self.buttonApply.set_sensitive(sensitive)

    def on_apply_clicked(self, *args):
        '''
        Ask user to setup use of overdraft.
        '''
        amount = self.spinbuttonOverdraft.get_value_as_int()
        amount = "%s%s" % (data.currency.get_currency_symbol(), data.currency.get_comma_value(amount))

        dialog = self.OverdraftDialog(amount, self.club.finances.overdraft.interest)

        if dialog.show():
            self.club.finances.overdraft.amount = self.spinbuttonOverdraft.get_value_as_int()

    def run(self):
        self.club = data.clubs.get_club_by_id(data.user.team)

        maximum = self.club.finances.overdraft.get_maximum_overdraft()
        self.spinbuttonOverdraft.set_range(0, maximum)

        amount = data.currency.get_amount(maximum)
        amount = "%s%s" % (data.currency.get_currency_symbol(), data.currency.get_comma_value(amount))

        self.labelStatus.set_label("The maximum overdraft allowed at this time is %s with an interest rate of %i%%." % (amount, self.club.finances.overdraft.interest))

        self.spinbuttonOverdraft.set_value(self.club.finances.overdraft.amount)


class Grant(uigtk.widgets.CommonFrame):
    def __init__(self):
        uigtk.widgets.CommonFrame.__init__(self, "Grant")
        self.set_vexpand(False)

        label = uigtk.widgets.Label("Stadium improvement grants are available for clubs to improve features of their stadium, or the shops outside. Certain criteria must be met before a grant can be considered, including current capacity, average attedances, existing club financials, and the club reputation.", leftalign=True)
        label.set_xalign(0)
        label.set_line_wrap(True)
        self.grid.attach(label, 0, 0, 1, 1)

        self.labelGrant = uigtk.widgets.Label(leftalign=True)
        self.grid.attach(self.labelGrant, 0, 1, 1, 1)

        self.gridGrant = uigtk.widgets.Grid()
        self.grid.attach(self.gridGrant, 0, 2, 1, 1)

        label = uigtk.widgets.Label("_Grant Amount", leftalign=True)
        self.gridGrant.attach(label, 0, 0, 1, 1)
        self.spinbuttonGrant = uigtk.widgets.SpinButton()
        self.spinbuttonGrant.set_increments(100000, 1000000)
        self.spinbuttonGrant.set_sensitive(False)
        self.spinbuttonGrant.set_tooltip_text("Amount of grant money to request.")
        label.set_mnemonic_widget(self.spinbuttonGrant)
        self.gridGrant.attach(self.spinbuttonGrant, 1, 0, 1, 1)

        buttonbox = uigtk.widgets.ButtonBox()
        buttonbox.set_hexpand(True)
        buttonbox.set_layout(Gtk.ButtonBoxStyle.END)
        self.grid.attach(buttonbox, 0, 3, 1, 1)

        self.buttonApply = uigtk.widgets.Button("_Apply")
        self.buttonApply.set_sensitive(False)
        self.buttonApply.connect("clicked", self.on_apply_clicked)
        buttonbox.add(self.buttonApply)

    def on_apply_clicked(self, *args):
        pass

    def run(self):
        club = data.clubs.get_club_by_id(data.user.team)

        if club.finances.grant.get_grant_available():
            self.labelGrant.set_markup("<b>Grant is available.</b>")
            self.spinbuttonGrant.set_sensitive(True)
            self.buttonApply.set_sensitive(True)
        else:
            self.labelGrant.set_markup("<b>The grant is currently not available to our club.</b>")
            self.spinbuttonGrant.set_sensitive(False)
            self.buttonApply.set_sensitive(False)


class Flotation(uigtk.widgets.CommonFrame):
    class FloatDialog(Gtk.MessageDialog):
        def __init__(self):
            Gtk.MessageDialog.__init__(self)
            self.set_transient_for(data.window)
            self.set_modal(True)
            self.set_title("Float Club")
            self.set_property("message-type", Gtk.MessageType.QUESTION)
            self.set_markup("<span size='12000'><b>Do you really want to float the club?</b></span>")
            self.format_secondary_text("Achieving the estimated amount will require good performances on and off the pitch.")
            self.add_button("_Do Not Float", Gtk.ResponseType.CANCEL)
            self.add_button("_Float", Gtk.ResponseType.OK)
            self.set_default_response(Gtk.ResponseType.CANCEL)

        def show(self):
            state = self.run() == Gtk.ResponseType.OK
            self.destroy()

            return state

    def __init__(self):
        uigtk.widgets.CommonFrame.__init__(self, "Flotation")
        self.set_vexpand(False)

        label = uigtk.widgets.Label("A club floated on the stock market generates a lot of initial money and is owned by the shareholders. The initial amount depends on the overall performance of the club.", leftalign=True)
        label.set_xalign(0)
        label.set_line_wrap(True)
        self.grid.attach(label, 0, 0, 1, 1)

        label = uigtk.widgets.Label("Once the club has been floated on the stock market, it can not be taken private again.", leftalign=True)
        label.set_line_wrap(True)
        self.grid.attach(label, 0, 1, 1, 1)

        self.labelStatus = uigtk.widgets.Label(leftalign=True)
        label.set_line_wrap(True)
        self.grid.attach(self.labelStatus, 0, 2, 1, 1)

        buttonbox = Gtk.ButtonBox()
        buttonbox.set_layout(Gtk.ButtonBoxStyle.END)
        self.grid.attach(buttonbox, 0, 3, 1, 1)

        self.buttonFloat = uigtk.widgets.Button("_Float")
        self.buttonFloat.connect("clicked", self.on_float_clicked)
        buttonbox.add(self.buttonFloat)

    def on_float_clicked(self, *args):
        '''
        Ask user to begin flotation process.
        '''
        dialog = self.FloatDialog()

        if dialog.show():
            self.club.finances.flotation.set_initiate_float()
            self.buttonFloat.set_sensitive(False)

    def run(self):
        self.club = data.clubs.get_club_by_id(data.user.team)

        amount = self.club.finances.flotation.get_float_amount()
        amount = data.currency.get_amount(amount)
        amount = "%s%s" % (data.currency.get_currency_symbol(), data.currency.get_comma_value(amount))

        if not self.club.finances.flotation.public:
            self.buttonFloat.set_sensitive(True)
            self.labelStatus.set_markup("<b>Floating the club at this time would raise in the region of %s.</b>" % (amount))
        else:
            self.buttonFloat.set_sensitive(False)
