#!/usr/bin/env python3

from gi.repository import Gtk

import uigtk.widgets


class FilterButtons(uigtk.widgets.ButtonBox):
    '''
    Shared combination of filter and reset buttons for list screens.
    '''
    def __init__(self):
        uigtk.widgets.ButtonBox.__init__(self)
        self.set_layout(Gtk.ButtonBoxStyle.END)

        self.buttonFilter = uigtk.widgets.Button("_Filter")
        self.buttonFilter.set_tooltip_text("Filter visible players according to criteria.")
        self.add(self.buttonFilter)

        self.buttonReset = uigtk.widgets.Button("_Reset")
        self.buttonReset.set_sensitive(False)
        self.buttonReset.set_tooltip_text("Reset any applied filters.")
        self.add(self.buttonReset)


class ColumnViews(uigtk.widgets.Grid):
    '''
    Selector for changing visible columns in list screens.
    '''
    def __init__(self):
        uigtk.widgets.Grid.__init__(self)

        label = uigtk.widgets.Label("_View")
        self.attach(label, 2, 0, 1, 1)
        self.comboboxView = Gtk.ComboBoxText()
        self.comboboxView.append("0", "Personal")
        self.comboboxView.append("1", "Skill")
        self.comboboxView.append("2", "Form")
        self.comboboxView.set_active(1)
        self.comboboxView.set_tooltip_text("Change visible columns of information.")
        label.set_mnemonic_widget(self.comboboxView)
        self.attach(self.comboboxView, 3, 0, 1, 1)
