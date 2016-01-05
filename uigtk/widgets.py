#!/usr/bin/env python3

from gi.repository import Gtk


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

        self.grid = Grid()
        self.grid.set_property("margin-left", 12)
        self.grid.set_property("margin-top", 5)
        self.grid.set_property("margin-bottom", 12)
        self.add(self.grid)

    def insert(self, child):
        self.grid.add(child)


class Grid(Gtk.Grid):
    '''
    Grid with default five pixel spacing on rows and columns.
    '''
    def __init__(self):
        Gtk.Grid.__init__(self)
        self.set_row_spacing(5)
        self.set_column_spacing(5)


class Box(Gtk.Box):
    def __init__(self):
        Gtk.Box.__init__(self)
        self.set_spacing(5)


class ScrolledWindow(Gtk.ScrolledWindow):
    def __init__(self):
        Gtk.ScrolledWindow.__init__(self)
        self.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)


class Label(Gtk.Label):
    '''
    Label with default formatting methods applied.
    '''
    def __init__(self, label="", leftalign=False, rightalign=False):
        Gtk.Label.__init__(self)
        self.set_markup(label)
        self.set_use_markup(True)
        self.set_use_underline(True)

        if leftalign:
            self.set_xalign(0)
        elif rightalign:
            self.set_xalign(1)


class Button(Gtk.Button):
    def __init__(self, label=""):
        Gtk.Button.__init__(self)
        self.set_label(label)
        self.set_use_underline(True)


class ToggleButton(Gtk.ToggleButton):
    def __init__(self, label=""):
        Gtk.ToggleButton.__init__(self)
        self.set_label(label)
        self.set_use_underline(True)


class CheckButton(Gtk.CheckButton):
    def __init__(self, label=""):
        Gtk.CheckButton.__init__(self)
        self.set_label(label)
        self.set_use_underline(True)


class RadioButton(Gtk.RadioButton):
    def __init__(self, label=""):
        Gtk.RadioButton.__init__(self)
        self.set_label(label)
        self.set_use_underline(True)


class SpinButton(Gtk.SpinButton):
    def __init__(self, minimum=0, maximum=0):
        Gtk.SpinButton.__init__(self)
        self.set_range(minimum, maximum)
        self.set_increments(10, 100)
        self.set_snap_to_ticks(True)
        self.set_numeric(True)


class ButtonBox(Gtk.ButtonBox):
    def __init__(self):
        Gtk.ButtonBox.__init__(self)
        self.set_spacing(5)


class MenuItem(Gtk.MenuItem):
    '''
    MenuItem with mnemonic activated.
    '''
    def __init__(self, label=""):
        Gtk.MenuItem.__init__(self)
        self.set_label(label)
        self.set_use_underline(True)


class TreeView(Gtk.TreeView):
    '''
    TreeView with search disabled and TreeSelection accessible.
    '''
    def __init__(self):
        Gtk.TreeView.__init__(self)
        self.set_enable_search(False)
        self.set_search_column(-1)

        self.treeselection = self.get_selection()


class TreeViewColumn(Gtk.TreeViewColumn):
    def __init__(self, title=None, column=0):
        Gtk.TreeViewColumn.__init__(self)

        if title:
            self.set_title(title)

        cellrenderertext = Gtk.CellRendererText()
        self.pack_start(cellrenderertext, True)
        self.add_attribute(cellrenderertext, "text", column)


class TextView(Gtk.TextView):
    def __init__(self):
        Gtk.TextView.__init__(self)
        self.textbuffer = self.get_buffer()


class ComboBox(Gtk.ComboBox):
    def __init__(self, column):
        Gtk.ComboBox.__init__(self)

        cellrenderertext = Gtk.CellRendererText()
        self.pack_start(cellrenderertext, True)
        self.add_attribute(cellrenderertext, "text", column)