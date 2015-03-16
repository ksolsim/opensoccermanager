#!/usr/bin/env python3

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
        self.info = info

        self.pagesetup = Gtk.PageSetup()

        Gtk.PrintOperation.__init__(self)
        self.set_n_pages(1)
        self.set_default_page_setup(self.pagesetup)
        self.connect("draw-page", self.draw_page)
        result = self.run(Gtk.PrintOperationAction.PRINT_DIALOG, parent)

    def draw_page(self, operation, context, page):
        if self.info == "0":
            self.pagesetup.set_orientation(Gtk.PageOrientation.LANDSCAPE)
            self.set_job_name("OpenSoccerManager - Squad")
            context = SquadContext(context)
        elif self.info == "1":
            self.pagesetup.set_orientation(Gtk.PageOrientation.PORTRAIT)
            self.set_job_name("OpenSoccerManager - Fixtures")
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
