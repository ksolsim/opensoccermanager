#!/usr/bin/env python3

from gi.repository import Gtk
import cairo

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

        combobox = Gtk.ComboBoxText()
        combobox.append("0", "Squad")
        combobox.append("1", "Fixtures")
        combobox.append("2", "Shortlist")
        combobox.set_active(0)
        grid.attach(combobox, 1, 0, 1, 1)

    def display(self):
        self.show_all()
        self.run()

    def response_handler(self, dialog, response):
        if response == Gtk.ResponseType.OK:
            operation = PrintOperation(parent=self)
        else:
            self.destroy()


class PrintOperation(Gtk.PrintOperation):
    def __init__(self, parent):
        Gtk.PrintOperation.__init__(self)
        self.set_n_pages(1)
        self.connect("draw-page", self.draw_page)
        result = self.run(Gtk.PrintOperationAction.PRINT_DIALOG, parent)

    def draw_page(self, operation=None, context=None, page=None):
        context = context.get_cairo_context()
        context.select_font_face("Droid Sans Mono",
                                 cairo.FONT_SLANT_NORMAL,
                                 cairo.FONT_WEIGHT_NORMAL)
        context.set_font_size(10)

        return
