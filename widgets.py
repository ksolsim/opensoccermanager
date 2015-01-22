#!/usr/bin/env python3

from gi.repository import Gtk

import display
import game


class InfoTip(Gtk.Grid):
    name = ""
    nickname = ""
    chairman = ""
    balance = ""

    def __init__(self):
        Gtk.Grid.__init__(self)
        self.set_row_spacing(5)
        self.set_column_spacing(5)

        label = AlignedLabel("Name:")
        self.attach(label, 0, 0, 1, 1)
        self.labelName = AlignedLabel(self.name)
        self.attach(self.labelName, 1, 0, 1, 1)
        label = AlignedLabel("Nickame:")
        self.attach(label, 0, 1, 1, 1)
        self.labelNickname = AlignedLabel(self.nickname)
        self.attach(self.labelNickname, 1, 1, 1, 1)
        label = AlignedLabel("Chairman:")
        self.attach(label, 0, 2, 1, 1)
        self.labelChairman = AlignedLabel(self.chairman)
        self.attach(self.labelChairman, 1, 2, 1, 1)

        separator = Gtk.Separator()
        self.attach(separator, 0, 3, 3, 1)

        label = AlignedLabel("Balance:")
        self.attach(label, 0, 4, 1, 1)
        self.labelBalance = AlignedLabel()
        self.attach(self.labelBalance, 1, 4, 1, 1)

    def show(self):
        self.labelName.set_label(self.name)
        self.labelNickname.set_label(self.nickname)
        self.labelChairman.set_label(self.chairman)
        self.labelBalance.set_label(self.balance)

        self.show_all()


class Date(Gtk.Label):
    '''
    Used to the display the current date in the game.
    '''
    def __init__(self):
        def tooltip(item, x, y, keyboard_mode, tooltip):
            club = game.clubs[game.teamid]

            infotip.name = "%s" % (club.name)
            infotip.nickname = "%s" % (club.nickname)
            infotip.chairman = "%s" % (club.chairman)

            balance = display.currency(club.balance)
            infotip.balance = "%s" % (balance)

            infotip.show()

            tooltip.set_custom(infotip)

            return True

        infotip = InfoTip()

        Gtk.Label.__init__(self)
        self.set_has_tooltip(True)
        self.connect("query-tooltip", tooltip)

    def update(self):
        self.set_label("%i/%i/%i" % (game.year, game.month, game.date))


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


class SpinButton(Gtk.SpinButton):
    def __init__(self, maximum):
        Gtk.SpinButton.__init__(self)
        self.set_range(0, maximum)
        self.set_increments(10, 100)
        self.set_snap_to_ticks(True)
        self.set_numeric(True)
