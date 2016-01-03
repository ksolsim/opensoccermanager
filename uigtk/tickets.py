#!/usr/bin/env python3

from gi.repository import Gtk

import data
import uigtk.widgets


class Tickets(uigtk.widgets.Grid):
    def __init__(self):
        uigtk.widgets.Grid.__init__(self)

        frame = uigtk.widgets.CommonFrame("Tickets")
        self.attach(frame, 0, 0, 1, 1)

        label = uigtk.widgets.Label("League")
        frame.grid.attach(label, 1, 0, 1, 1)
        label = uigtk.widgets.Label("Cup")
        frame.grid.attach(label, 2, 0, 1, 1)
        label = uigtk.widgets.Label("Season")
        frame.grid.attach(label, 3, 0, 1, 1)

        label = uigtk.widgets.Label("Standing Uncovered", leftalign=True)
        frame.grid.attach(label, 0, 1, 1, 1)
        label = uigtk.widgets.Label("Standing Covered", leftalign=True)
        frame.grid.attach(label, 0, 2, 1, 1)
        label = uigtk.widgets.Label("Seating Uncovered", leftalign=True)
        frame.grid.attach(label, 0, 3, 1, 1)
        label = uigtk.widgets.Label("Seating Covered", leftalign=True)
        frame.grid.attach(label, 0, 4, 1, 1)
        label = uigtk.widgets.Label("Executive Box", leftalign=True)
        frame.grid.attach(label, 0, 5, 1, 1)

        for vcount in range(1, 6):
            for hcount in range(1, 4):
                scale = Gtk.Scale()
                scale.set_hexpand(True)
                scale.set_value_pos(Gtk.PositionType.BOTTOM)
                scale.set_digits(0)
                scale.set_increments(1, 10)
                scale.connect("format-value", self.format_tickets_amount)
                frame.grid.attach(scale, hcount, vcount, 1, 1)

        frame = uigtk.widgets.CommonFrame("Season Tickets")
        self.attach(frame, 0, 1, 1, 1)

        label = uigtk.widgets.Label("Capacity _Percentage Allocated For Season Tickets")
        frame.grid.attach(label, 0, 0, 1, 1)
        self.spinbuttonSeasonTickets = Gtk.SpinButton.new_with_range(0, 100, 1)
        self.spinbuttonSeasonTickets.set_numeric(False)
        self.spinbuttonSeasonTickets.set_tooltip_text("Specify the percentage of season tickets available.")
        self.spinbuttonSeasonTickets.connect("output", self.on_season_tickets_output)
        self.spinbuttonSeasonTickets.connect("value-changed", self.on_season_tickets_changed)
        label.set_mnemonic_widget(self.spinbuttonSeasonTickets)
        frame.grid.attach(self.spinbuttonSeasonTickets, 1, 0, 1, 1)

        frame = uigtk.widgets.CommonFrame("School Tickets")
        self.attach(frame, 0, 2, 1, 1)

        label = uigtk.widgets.Label("Capacity Allocated For _Free School Ticket Programme")
        frame.grid.attach(label, 0, 0, 1, 1)
        self.spinbuttonSchoolTickets = Gtk.SpinButton.new_with_range(0, 74000, 100)
        self.spinbuttonSchoolTickets.set_increments(100, 1000)
        self.spinbuttonSchoolTickets.set_snap_to_ticks(True)
        self.spinbuttonSchoolTickets.set_numeric(True)
        self.spinbuttonSchoolTickets.set_tooltip_text("Specify in 100 blocks the number of free school tickets.")
        self.spinbuttonSchoolTickets.connect("value-changed", self.on_school_tickets_changed)
        label.set_mnemonic_widget(self.spinbuttonSchoolTickets)
        frame.grid.attach(self.spinbuttonSchoolTickets, 1, 0, 1, 1)

    def format_tickets_amount(self, scale, value):
        '''
        Format ticket value for display on scale.
        '''
        return data.currency.get_currency(value, integer=True)

    def on_season_tickets_changed(self, spinbutton):
        '''
        Store season ticket value when changed.
        '''
        self.club.tickets.season_tickets = spinbutton.get_value_as_int()

    def on_school_tickets_changed(self, spinbutton):
        '''
        Store school tickets value when changed.
        '''
        self.club.tickets.school_tickets = spinbutton.get_value_as_int()

    def on_season_tickets_output(self, spinbutton):
        '''
        Format percentage sign into season ticket spinbutton output.
        '''
        spinbutton.set_text("%i%%" % (spinbutton.get_value_as_int()))

        return True

    def run(self):
        self.club = data.clubs.get_club_by_id(data.user.team)

        self.spinbuttonSeasonTickets.set_value(self.club.tickets.season_tickets)
        self.spinbuttonSchoolTickets.set_value(self.club.tickets.school_tickets)

        self.show_all()
