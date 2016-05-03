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
    '''
    Box with five pixel spacing between cells.
    '''
    def __init__(self):
        Gtk.Box.__init__(self)
        self.set_spacing(5)


class ScrolledWindow(Gtk.ScrolledWindow):
    '''
    ScrolledWindow with automatic vertical scrolling and disabled horizontal.
    '''
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
    '''
    Button containing mnemonic setting enabled.
    '''
    def __init__(self, label=""):
        Gtk.Button.__init__(self)
        self.set_label(label)
        self.set_use_underline(True)


class ToggleButton(Gtk.ToggleButton):
    '''
    ToggleButton containing mnemonic setting enabled.
    '''
    def __init__(self, label=""):
        Gtk.ToggleButton.__init__(self)
        self.set_label(label)
        self.set_use_underline(True)


class CheckButton(Gtk.CheckButton):
    '''
    CheckButton containing mnemonic setting enabled.
    '''
    def __init__(self, label=""):
        Gtk.CheckButton.__init__(self)
        self.set_label(label)
        self.set_use_underline(True)


class RadioButton(Gtk.RadioButton):
    '''
    RadioButton containing mnemonic setting enabled.
    '''
    def __init__(self, label=""):
        Gtk.RadioButton.__init__(self)
        self.set_label(label)
        self.set_use_underline(True)


class SpinButton(Gtk.SpinButton):
    '''
    SpinButton with tick snapping and defined increments.
    '''
    def __init__(self, minimum=0, maximum=0):
        Gtk.SpinButton.__init__(self)
        self.set_range(minimum, maximum)
        self.set_increments(10, 100)
        self.set_snap_to_ticks(True)
        self.set_numeric(True)


class ButtonBox(Gtk.ButtonBox):
    '''
    ButtonBox with five pixel spacing between child widgets.
    '''
    def __init__(self):
        Gtk.ButtonBox.__init__(self)
        self.set_spacing(5)


class MenuItem(Gtk.MenuItem):
    '''
    MenuItem with mnemonic shortcut enabled.
    '''
    def __init__(self, label=""):
        Gtk.MenuItem.__init__(self)
        self.set_label(label)
        self.set_use_underline(True)


class CheckMenuItem(Gtk.CheckMenuItem):
    '''
    CheckMenuItem with mnemonic shortcut enabled.
    '''
    def __init__(self, label=""):
        Gtk.CheckMenuItem.__init__(self)
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
    '''
    TreeViewColumn with arguments for column, title and tooltip text.
    '''
    def __init__(self, column, title=None, tooltip=None):
        Gtk.TreeViewColumn.__init__(self)

        if tooltip:
            label = Gtk.Label()
            label.set_label(title)
            label.set_tooltip_text(tooltip)
            label.show()
            self.set_widget(label)
        elif title:
            self.set_title(title)

        cellrenderertext = Gtk.CellRendererText()
        self.pack_start(cellrenderertext, True)
        self.add_attribute(cellrenderertext, "text", column)


class TextView(Gtk.TextView):
    '''
    TextView with pre-created TextBuffer object.
    '''
    def __init__(self):
        Gtk.TextView.__init__(self)
        self.textbuffer = self.get_buffer()


class ComboBox(Gtk.ComboBox):
    '''
    ComboBox with auto-created CellRendererText object.
    '''
    def __init__(self, column):
        Gtk.ComboBox.__init__(self)

        cellrenderertext = Gtk.CellRendererText()
        self.pack_start(cellrenderertext, True)
        self.add_attribute(cellrenderertext, "text", column)
