#!/usr/bin/env python3

from gi.repository import Gtk

import data
import uigtk.widgets


class Finances(uigtk.widgets.Grid):
    def __init__(self):
        uigtk.widgets.Grid.__init__(self)
        self.set_column_homogeneous(True)

        grid = uigtk.widgets.Grid()
        self.attach(grid, 0, 0, 1, 1)

        self.loan = Loan()
        grid.attach(self.loan, 0, 0, 1, 1)
        self.grant = Grant()
        grid.attach(self.grant, 0, 1, 1, 1)

        grid = uigtk.widgets.Grid()
        self.attach(grid, 1, 0, 1, 1)

        self.overdraft = Overdraft()
        grid.attach(self.overdraft, 1, 0, 1, 1)
        self.flotation = Flotation()
        grid.attach(self.flotation, 1, 1, 1, 1)

    def run(self):
        self.loan.run()
        self.overdraft.run()
        self.grant.run()
        self.flotation.run()
        self.show_all()


class Loan(uigtk.widgets.CommonFrame):
    class LoanDialog(Gtk.MessageDialog):
        def __init__(self, amount, interest):
            Gtk.MessageDialog.__init__(self)
            self.set_transient_for(data.window)
            self.set_modal(True)
            self.set_title("Confirm Loan")
            self.set_property("message-type", Gtk.MessageType.QUESTION)
            self.set_markup("Apply for loan of %s at %i%% interest?" % (amount, interest))
            self.add_button("_Cancel", Gtk.ResponseType.CANCEL)
            self.add_button("C_onfirm", Gtk.ResponseType.OK)
            self.set_default_response(Gtk.ResponseType.CANCEL)

        def show(self):
            state = self.run() == Gtk.ResponseType.OK
            self.destroy()

            return state

    def __init__(self):
        uigtk.widgets.CommonFrame.__init__(self, "Loan")
        self.set_vexpand(False)

        label = uigtk.widgets.Label("A loan can be taken out to provide extra funds for a club, in order to purchase players and improve stadia. The interest is charged at a percentage agreed when the loan is taken out.", leftalign=True)
        label.set_width_chars(40)
        label.set_xalign(0)
        label.set_line_wrap(True)
        self.grid.attach(label, 0, 0, 1, 1)

        sizegroup = Gtk.SizeGroup()
        sizegroup.set_mode(Gtk.SizeGroupMode.HORIZONTAL)

        grid = uigtk.widgets.Grid()
        self.grid.attach(grid, 0, 2, 1, 1)

        label = uigtk.widgets.Label("_Loan Amount", leftalign=True)
        sizegroup.add_widget(label)
        grid.attach(label, 0, 0, 1, 1)
        self.spinbuttonAmount = Gtk.SpinButton()
        self.spinbuttonAmount.set_increments(100000, 1000000)
        self.spinbuttonAmount.connect("value-changed", self.on_amount_changed)
        label.set_mnemonic_widget(self.spinbuttonAmount)
        grid.attach(self.spinbuttonAmount, 1, 0, 1, 1)

        label = uigtk.widgets.Label("_Repayment Period", leftalign=True)
        sizegroup.add_widget(label)
        grid.attach(label, 0, 1, 1, 1)
        self.spinbuttonPeriod = Gtk.SpinButton()
        self.spinbuttonPeriod.set_range(1, 5)
        self.spinbuttonPeriod.set_increments(1, 1)
        label.set_mnemonic_widget(self.spinbuttonPeriod)
        grid.attach(self.spinbuttonPeriod, 1, 1, 1, 1)

        buttonbox = uigtk.widgets.ButtonBox()
        buttonbox.set_layout(Gtk.ButtonBoxStyle.END)
        self.grid.attach(buttonbox, 0, 3, 1, 1)

        self.buttonApply = uigtk.widgets.Button("_Apply")
        self.buttonApply.set_sensitive(False)
        self.buttonApply.set_tooltip_text("Apply specified loan amount with current interest rate.")
        buttonbox.add(self.buttonApply)

        grid = uigtk.widgets.Grid()
        self.grid.attach(grid, 0, 4, 1, 1)

        label = uigtk.widgets.Label("Repay _Amount", leftalign=True)
        sizegroup.add_widget(label)
        grid.attach(label, 0, 0, 1, 1)
        self.spinbuttonRepay = Gtk.SpinButton()
        self.spinbuttonRepay.connect("value-changed", self.on_repay_changed)
        label.set_mnemonic_widget(self.spinbuttonRepay)
        grid.attach(self.spinbuttonRepay, 1, 0, 1, 1)

        buttonbox = uigtk.widgets.ButtonBox()
        buttonbox.set_layout(Gtk.ButtonBoxStyle.END)
        self.grid.attach(buttonbox, 0, 5, 1, 1)

        buttonRepay = uigtk.widgets.Button("_Repay")
        buttonRepay.set_sensitive(False)
        buttonRepay.set_tooltip_text("Repay specified amount of outstanding loan.")
        buttonbox.add(buttonRepay)

    def on_amount_changed(self, spinbutton):
        '''
        Update apply button if loan amount is greater than zero.
        '''
        sensitive = spinbutton.get_value() > 0
        self.buttonApply.set_sensitive(sensitive)

    def on_repay_changed(self, spinbutton):
        '''
        Update repay button if repay amount is greater than zero.
        '''
        sensitive = spinbutton.get_value() > 0
        self.buttonRepay.set_sensitive(sensitive)

    def on_apply_clicked(self, *args):
        '''
        Claim loan for specified amount and repayment period.
        '''
        pass

    def on_repay_clicked(self, *args):
        '''
        Repay defined loan amount.
        '''
        pass

    def run(self):
        club = data.clubs.get_club_by_id(data.user.team)

        maximum = club.finances.loan.get_maximum_loan()
        self.spinbuttonAmount.set_range(0, maximum)
        self.spinbuttonAmount.set_value(0)


class Overdraft(uigtk.widgets.CommonFrame):
    class OverdraftDialog(Gtk.MessageDialog):
        def __init__(self, amount, interest):
            Gtk.MessageDialog.__init__(self)
            self.set_transient_for(data.window)
            self.set_modal(True)
            self.set_title("Confirm Overdraft")
            self.set_property("message-type", Gtk.MessageType.QUESTION)
            self.set_markup("Apply for overdraft of %s at %i%% interest?" % (amount, interest))
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
        self.buttonApply.set_tooltip_text("Apply for overdraft using defined settings.")
        self.buttonApply.connect("clicked", self.on_apply_clicked)
        buttonbox.add(self.buttonApply)

    def on_overdraft_changed(self, spinbutton):
        '''
        Change sensitivity of apply button.
        '''
        sensitive = spinbutton.get_value() > 0
        self.buttonApply.set_sensitive(sensitive)

    def on_apply_clicked(self, *args):
        '''
        Ask user to setup use of overdraft.
        '''
        dialog = self.OverdraftDialog()

        if dialog.show():
            club.finances.overdraft.amount = self.spinbuttonOverdraft.get_value()

    def run(self):
        club = data.clubs.get_club_by_id(data.user.team)

        maximum = club.finances.overdraft.get_maximum_overdraft()
        self.spinbuttonOverdraft.set_range(0, maximum)

        amount = data.currency.get_currency(maximum, integer=True)

        self.labelStatus.set_label("The maximum overdraft allowed at this time is %s with an interest rate of %i%%." % (amount, club.finances.overdraft.interest))

        self.spinbuttonOverdraft.set_value(club.finances.overdraft.amount)


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
        self.spinbuttonGrant.set_tooltip_text("Amount of grant money to apply for.")
        label.set_mnemonic_widget(self.spinbuttonGrant)
        self.gridGrant.attach(self.spinbuttonGrant, 1, 0, 1, 1)

        buttonbox = uigtk.widgets.ButtonBox()
        buttonbox.set_hexpand(True)
        buttonbox.set_layout(Gtk.ButtonBoxStyle.END)
        self.grid.attach(buttonbox, 0, 3, 1, 1)

        self.buttonApply = uigtk.widgets.Button("_Apply")
        self.buttonApply.set_sensitive(False)
        buttonbox.add(self.buttonApply)

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

        amount = data.currency.get_currency(self.club.finances.flotation.get_float_amount(), integer=True)

        if not self.club.finances.flotation.public:
            self.buttonFloat.set_sensitive(True)
            self.labelStatus.set_markup("<b>Floating the club at this time would raise in the region of %s.</b>" % (amount))
        else:
            self.buttonFloat.set_sensitive(False)
