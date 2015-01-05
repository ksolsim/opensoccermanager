#!/usr/bin/env python

from gi.repository import Gtk

import game


class InfoTip(Gtk.Grid):
    def __init__(self):
        Gtk.Grid.__init__(self)
        self.set_row_spacing(5)
        self.set_column_spacing(5)

        label = AlignedLabel("Name:")
        self.attach(label, 0, 0, 1, 1)
        label = AlignedLabel("%s" % (game.clubs[game.teamid].name))
        self.attach(label, 1, 0, 1, 1)
        label = AlignedLabel("Nickame:")
        self.attach(label, 0, 1, 1, 1)
        label = AlignedLabel("%s" % (game.clubs[game.teamid].nickname))
        self.attach(label, 1, 1, 1, 1)
        label = AlignedLabel("Chairman:")
        self.attach(label, 0, 2, 1, 1)
        label = AlignedLabel("%s" % (game.clubs[game.teamid].chairman))
        self.attach(label, 1, 2, 1, 1)

        separator = Gtk.Separator()
        self.attach(separator, 0, 3, 3, 1)

        label = AlignedLabel("Balance:")
        self.attach(label, 0, 4, 1, 1)
        label = AlignedLabel("£%.0f" % (game.clubs[game.teamid].balance))
        self.attach(label, 1, 4, 1, 1)

        self.show_all()


class Date(Gtk.Label):
    '''
    Used to the display the current date in the game.
    '''
    def __init__(self):
        def tooltip(item, x, y, keyboard_mode, tooltip):
            infotip = InfoTip()
            tooltip.set_custom(infotip)

            return True

        Gtk.Label.__init__(self)
        self.set_has_tooltip(True)
        self.connect("query-tooltip", tooltip)


class News(Gtk.Button):
    '''
    Provide a button to quickly jump to news when unread items are
    available.
    '''
    def __init__(self):
        Gtk.Button.__init__(self)
        self.set_label("_Unread news available")
        self.set_use_underline(True)
        self.set_relief(Gtk.ReliefStyle.NONE)


class CommonFrame(Gtk.Frame):
    '''
    Tidy frame widget for use in dialogs to group widgets.
    '''
    def __init__(self, title=None):
        Gtk.Frame.__init__(self)
        self.set_shadow_type(Gtk.ShadowType.NONE)

        label = Gtk.Label("<b>%s</b>" % (title))
        label.set_use_markup(True)
        self.set_label_widget(label)

        self.grid = Gtk.Grid()
        self.grid.set_property("margin-left", 12)
        self.grid.set_property("margin-top", 5)
        self.add(self.grid)

    def insert(self, child):
        self.grid.attach(child, 0, 0, 1, 1)


class AlignedLabel(Gtk.Label):
    def __init__(self, label="", xalign=0, yalign=0.5):
        Gtk.Label.__init__(self)
        self.set_markup(label)
        self.set_use_markup(True)
        self.set_alignment(xalign, yalign)


class MenuItem(Gtk.MenuItem):
    def __init__(self, label=""):
        Gtk.MenuItem.__init__(self)
        self.set_label(label)
        self.set_use_underline(True)


class Button(Gtk.Button):
    def __init__(self, label=""):
        Gtk.Button.__init__(self)
        self.set_label(label)
        self.set_use_underline(True)
