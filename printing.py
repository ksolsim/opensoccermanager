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
import cairo

import constants
import display
import game
import widgets


class PrintType(Gtk.Dialog):
    def __init__(self):
        Gtk.Dialog.__init__(self)
        self.set_transient_for(game.window)
        self.set_title("Print")
        self.set_resizable(False)
        self.set_border_width(5)
        self.add_button("_Close", Gtk.ResponseType.CLOSE)
        self.add_button("_Print", Gtk.ResponseType.OK)
        self.set_default_response(Gtk.ResponseType.CLOSE)
        self.connect("response", self.response_handler)

        grid = Gtk.Grid()
        grid.set_column_spacing(5)
        self.vbox.add(grid)

        label = widgets.Label("Select Information To Print")
        grid.attach(label, 0, 0, 1, 1)

        self.combobox = Gtk.ComboBoxText()
        self.combobox.append("0", "Squad")
        self.combobox.append("1", "Fixtures & Reults")
        self.combobox.append("3", "Accounts")
        self.combobox.set_active(0)
        grid.attach(self.combobox, 1, 0, 1, 1)

    def display(self):
        if len(game.clubs[game.teamid].shortlist) > 0:
            self.combobox.insert(2, "2", "Shortlist")

        self.show_all()
        self.run()

    def response_handler(self, dialog, response):
        if response == Gtk.ResponseType.OK:
            active = self.combobox.get_active_id()
            operation = PrintOperation(parent=self, info=active)
        else:
            self.destroy()


class PrintOperation(Gtk.PrintOperation):
    def __init__(self, parent, info):
        Gtk.PrintOperation.__init__(self)

        self.info = info

        self.pagesetup = Gtk.PageSetup()

        if self.info == "0":
            self.pagesetup.set_orientation(Gtk.PageOrientation.LANDSCAPE)
            self.set_job_name("OpenSoccerManager - Squad")
        elif self.info == "1":
            self.pagesetup.set_orientation(Gtk.PageOrientation.PORTRAIT)
            self.set_job_name("OpenSoccerManager - Fixtures")
        elif self.info == "2":
            self.pagesetup.set_orientation(Gtk.PageOrientation.LANDSCAPE)
            self.set_job_name("OpenSoccerManager - Shortlist")
        elif self.info == "3":
            self.pagesetup.set_orientation(Gtk.PageOrientation.PORTRAIT)
            self.set_job_name("OpenSoccerManager - Accounts")

        self.set_n_pages(1)
        self.set_default_page_setup(self.pagesetup)
        self.connect("draw-page", self.draw_page)
        result = self.run(Gtk.PrintOperationAction.PRINT_DIALOG, parent)

    def draw_page(self, operation, context, page):
        if self.info == "0":
            context = SquadContext(context)
        elif self.info == "1":
            context = FixtureContext(context)
        elif self.info == "2":
            context = ShortlistContext(context)
        elif self.info == "3":
            context = AccountsContext(context)

        return


class FixtureContext:
    def __init__(self, context):
        context = context.get_cairo_context()
        context.set_font_size(8)

        # Draw column titles
        context.select_font_face("Droid Sans Mono",
                                 cairo.FONT_SLANT_NORMAL,
                                 cairo.FONT_WEIGHT_BOLD)

        context.move_to(10, 10)
        context.show_text("Fixture")
        context.move_to(225, 10)
        context.show_text("Venue")
        context.move_to(350, 10)
        context.show_text("Result")

        context.select_font_face("Droid Sans Mono",
                                 cairo.FONT_SLANT_NORMAL,
                                 cairo.FONT_WEIGHT_NORMAL)

        x, y, = 10, 25

        results_count = len(game.results)

        for week_count, week in enumerate(game.fixtures):
            for fixture in week:
                if game.teamid in fixture:
                    context.move_to(x, y)
                    match = "%s vs %s" % (game.clubs[fixture[0]].name,
                                          game.clubs[fixture[1]].name)
                    context.show_text("%s" % (match))

                    context.move_to(225, y)
                    stadiumid = game.clubs[fixture[0]].stadium
                    stadium = game.stadiums[stadiumid].name
                    context.show_text("%s" % (stadium))

                    context.move_to(350, y)

                    if week_count + 1 <= results_count:
                        for match in game.results[week_count]:
                            if game.teamid in (match[0], match[3]):
                                context.show_text("%i - %i" % (match[1], match[2]))

                    y += 15


class SquadContext:
    def __init__(self, context):
        context = context.get_cairo_context()
        context.set_font_size(8)

        # Draw column titles
        context.select_font_face("Droid Sans Mono",
                                 cairo.FONT_SLANT_NORMAL,
                                 cairo.FONT_WEIGHT_BOLD)

        context.move_to(10, 10)
        context.show_text("Name")
        context.move_to(180, 10)
        context.show_text("Position")
        context.move_to(230, 10)
        context.show_text("Nationality")

        for count, item in enumerate(constants.short_skill, start=1):
            context.move_to(320 + (count * 20), 10)
            context.show_text("%s" % (item))

        context.move_to(530, 10)
        context.show_text("Value")
        context.move_to(580, 10)
        context.show_text("Wage")
        context.move_to(630, 10)
        context.show_text("Contract")
        context.move_to(700, 10)
        context.show_text("Apps")
        context.move_to(730, 10)
        context.show_text("Goals")
        context.move_to(760, 10)
        context.show_text("Assists")

        context.select_font_face("Droid Sans Mono",
                                 cairo.FONT_SLANT_NORMAL,
                                 cairo.FONT_WEIGHT_NORMAL)

        x, y = 10, 25

        for playerid in game.clubs[game.teamid].squad:
            player = game.players[playerid]

            context.move_to(x, y)
            name = display.name(player)
            context.show_text("%s" % (name))

            context.move_to(180, y)
            context.show_text("%s" % (player.position))

            context.move_to(230, y)
            nationality = display.nation(player.nationality)
            context.show_text("%s" % (nationality))

            for count, skill in enumerate(player.skills(), start=1):
                context.move_to(320 + (count * 20), y)
                context.show_text("%i" % (skill))

            context.move_to(530, y)
            value = display.value(player.value)
            context.show_text("%s" % (value))

            context.move_to(580, y)
            wage = display.wage(player.wage)
            context.show_text("%s" % (wage))

            context.move_to(630, y)
            context.show_text("%i Weeks" % (player.contract))

            context.move_to(700, y)
            context.show_text("%i (%i)" % (player.appearances, player.substitute))

            context.move_to(730, y)
            context.show_text("%i" % (player.goals))

            context.move_to(760, y)
            context.show_text("%i" % (player.assists))

            y += 15


class ShortlistContext:
    def __init__(self, context):
        context = context.get_cairo_context()
        context.set_font_size(8)

        # Draw column titles
        context.select_font_face("Droid Sans Mono",
                                 cairo.FONT_SLANT_NORMAL,
                                 cairo.FONT_WEIGHT_BOLD)

        context.move_to(10, 10)
        context.show_text("Name")
        context.move_to(165, 10)
        context.show_text("Position")
        context.move_to(220, 10)
        context.show_text("Club")
        context.move_to(340, 10)
        context.show_text("Nationality")
        context.move_to(420, 10)
        context.show_text("Value")
        context.move_to(460, 10)
        context.show_text("Wage")
        context.move_to(500, 10)
        context.show_text("Contract")

        for count, item in enumerate(constants.short_skill, start=1):
            context.move_to(550 + (count * 20), 10)
            context.show_text("%s" % (item))

        context.select_font_face("Droid Sans Mono",
                                 cairo.FONT_SLANT_NORMAL,
                                 cairo.FONT_WEIGHT_NORMAL)

        x, y = 10, 25

        for playerid in game.clubs[game.teamid].shortlist:
            player = game.players[playerid]

            context.move_to(x, y)
            name = display.name(player)
            context.show_text("%s" % (name))

            context.move_to(165, y)
            context.show_text("%s" % (player.position))

            context.move_to(220, y)
            club = game.clubs[player.club].name
            context.show_text("%s" % (club))

            context.move_to(340, y)
            nationality = game.nations[player.nationality].name
            context.show_text("%s" % (nationality))

            context.move_to(420, y)
            value = display.value(player.value)
            context.show_text("%s" % (value))

            context.move_to(460, y)
            wage = display.wage(player.wage)
            context.show_text("%s" % (wage))

            context.move_to(500, y)
            context.show_text("%i Weeks" % (player.contract))

            for count, skill in enumerate(player.skills(), start=1):
                context.move_to(550 + (count * 20), y)
                context.show_text("%i" % (skill))

            y += 15


class AccountsContext:
    def __init__(self, context):
        context = context.get_cairo_context()
        context.set_font_size(8)

        # Draw column titles
        context.select_font_face("Droid Sans Mono",
                                 cairo.FONT_SLANT_NORMAL,
                                 cairo.FONT_WEIGHT_BOLD)

        # Income
        context.move_to(10, 10)
        context.show_text("INCOME")

        context.move_to(25, 40)
        context.show_text("Category")
        context.move_to(250, 40)
        context.show_text("Week")
        context.move_to(400, 40)
        context.show_text("Season")

        context.move_to(25, 60)
        context.show_text("Prize Money")
        context.move_to(25, 75)
        context.show_text("Sponsorship")
        context.move_to(25, 90)
        context.show_text("Advertising")
        context.move_to(25, 105)
        context.show_text("Merchandise")
        context.move_to(25, 120)
        context.show_text("Catering")
        context.move_to(25, 135)
        context.show_text("Ticket Sales")
        context.move_to(25, 150)
        context.show_text("Transfer Fees")
        context.move_to(25, 165)
        context.show_text("Loan")
        context.move_to(25, 180)
        context.show_text("Television Money")

        context.move_to(25, 210)
        context.show_text("Total Income")

        # Expenditure
        context.move_to(10, 250)
        context.show_text("EXPENDITURE")

        context.move_to(25, 280)
        context.show_text("Category")
        context.move_to(250, 280)
        context.show_text("Week")
        context.move_to(400, 280)
        context.show_text("Season")

        context.move_to(25, 300)
        context.show_text("Fines")
        context.move_to(25, 315)
        context.show_text("Stadium")
        context.move_to(25, 330)
        context.show_text("Staff Wages")
        context.move_to(25, 345)
        context.show_text("Player Wages")
        context.move_to(25, 360)
        context.show_text("Transfer Fees")
        context.move_to(25, 375)
        context.show_text("Merchandise")
        context.move_to(25, 390)
        context.show_text("Catering")
        context.move_to(25, 405)
        context.show_text("Loan Repayment")
        context.move_to(25, 420)
        context.show_text("Overdraft Repayment")
        context.move_to(25, 435)
        context.show_text("Training")

        context.move_to(25, 465)
        context.show_text("Total Expenditure")

        context.select_font_face("Droid Sans Mono",
                                 cairo.FONT_SLANT_NORMAL,
                                 cairo.FONT_WEIGHT_NORMAL)

        y = 60

        # Amounts
        for count in range(0, 9):
            context.move_to(250, y)

            amount = display.currency(game.clubs[game.teamid].accounts[count][0])
            context.show_text("%s" % (amount))

            context.move_to(400, y)

            amount = display.currency(game.clubs[game.teamid].accounts[count][1])
            context.show_text("%s" % (amount))

            y += 15

        y = 300

        for count in range(9, 19):
            context.move_to(250, y)

            amount = display.currency(game.clubs[game.teamid].accounts[count][0])
            context.show_text("%s" % (amount))

            context.move_to(400, y)

            amount = display.currency(game.clubs[game.teamid].accounts[count][1])
            context.show_text("%s" % (amount))

            y += 15

        # Total
        context.move_to(400, 210)
        total = display.currency(game.clubs[game.teamid].income)
        context.show_text("%s" % (total))

        context.move_to(400, 465)
        total = display.currency(game.clubs[game.teamid].expenditure)
        context.show_text("%s" % (total))

        context.select_font_face("Droid Sans Mono",
                                 cairo.FONT_SLANT_NORMAL,
                                 cairo.FONT_WEIGHT_BOLD)

        context.move_to(10, 500)
        context.show_text("TOTAL")

        context.select_font_face("Droid Sans Mono",
                                 cairo.FONT_SLANT_NORMAL,
                                 cairo.FONT_WEIGHT_NORMAL)

        context.move_to(150, 500)
        total = display.currency(game.clubs[game.teamid].balance)
        context.show_text("%s" % (total))
