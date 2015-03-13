#!/usr/bin/env python3

from gi.repository import Gtk

import game
import widgets


class SearchFilter(Gtk.Dialog):
    '''
    Filtering dialog for players in the player search view.
    '''
    class Attributes(Gtk.Grid):
        def __init__(self):
            Gtk.Grid.__init__(self)
            self.set_row_spacing(5)
            self.set_column_spacing(5)

            self.minimum = Gtk.SpinButton.new_with_range(0, 99, 1)
            self.minimum.connect("value-changed", self.value_changed)
            self.attach(self.minimum, 0, 0, 1, 1)

            self.maximum = Gtk.SpinButton.new_with_range(0, 99, 1)
            self.maximum.connect("value-changed", self.value_changed)
            self.attach(self.maximum, 1, 0, 1, 1)

        def value_changed(self, spinbutton):
            '''
            Prevent the minimum value being higher than the maximum.
            '''
            minimum = self.minimum.get_value_as_int()
            self.maximum.set_range(minimum, 99)

        def display(self, minimum, maximum):
            self.minimum.set_value(minimum)
            self.maximum.set_value(maximum)

        def retrieve(self):
            minimum = self.minimum.get_value_as_int()
            maximum = self.maximum.get_value_as_int()

            return minimum, maximum

    def __init__(self):
        Gtk.Dialog.__init__(self)
        self.set_transient_for(game.window)
        self.set_title("Filter Players")
        self.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("_Filter", Gtk.ResponseType.OK)
        self.set_resizable(False)
        self.set_border_width(5)
        self.vbox.set_spacing(5)

        self.checkbuttonShowOwnPlayers = Gtk.CheckButton()
        self.checkbuttonShowOwnPlayers.set_use_underline(True)
        self.vbox.add(self.checkbuttonShowOwnPlayers)

        commonframe = widgets.CommonFrame(title="Personal")
        self.vbox.add(commonframe)

        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)
        commonframe.insert(grid)

        label = widgets.AlignedLabel("_Position")
        grid.attach(label, 0, 1, 1, 1)
        self.comboboxPosition = Gtk.ComboBoxText()
        self.comboboxPosition.append("0", "All")
        self.comboboxPosition.append("1", "Goalkeeper")
        self.comboboxPosition.append("2", "Defender")
        self.comboboxPosition.append("3", "Midfielder")
        self.comboboxPosition.append("4", "Attacker")
        label.set_mnemonic_widget(self.comboboxPosition)
        grid.attach(self.comboboxPosition, 1, 1, 1, 1)

        label = widgets.AlignedLabel("_Value")
        grid.attach(label, 0, 2, 1, 1)
        self.spinbuttonMinValue = Gtk.SpinButton.new_with_range(0, 100000000, 100000)
        self.spinbuttonMinValue.set_snap_to_ticks(True)
        self.spinbuttonMinValue.connect("value-changed", self.value_changed)
        label.set_mnemonic_widget(self.spinbuttonMinValue)
        grid.attach(self.spinbuttonMinValue, 1, 2, 1, 1)
        self.spinbuttonMaxValue = Gtk.SpinButton.new_with_range(0, 100000000, 100000)
        self.spinbuttonMaxValue.set_snap_to_ticks(True)
        self.spinbuttonMaxValue.connect("value-changed", self.value_changed)
        grid.attach(self.spinbuttonMaxValue, 2, 2, 1, 1)

        label = widgets.AlignedLabel("_Age")
        grid.attach(label, 0, 3, 1, 1)
        self.spinbuttonMinAge = Gtk.SpinButton.new_with_range(16, 50, 1)
        self.spinbuttonMinAge.connect("value-changed", self.age_changed)
        label.set_mnemonic_widget(self.spinbuttonMinAge)
        grid.attach(self.spinbuttonMinAge, 1, 3, 1, 1)
        self.spinbuttonMaxAge = Gtk.SpinButton.new_with_range(16, 50, 1)
        self.spinbuttonMaxAge.connect("value-changed", self.age_changed)
        grid.attach(self.spinbuttonMaxAge, 2, 3, 1, 1)

        label = widgets.AlignedLabel("_Status")
        grid.attach(label, 0, 4, 1, 1)
        self.comboboxStatus = Gtk.ComboBoxText()
        self.comboboxStatus.append("0", "All Players")
        self.comboboxStatus.append("1", "Transfer Listed")
        self.comboboxStatus.append("2", "Loan Listed")
        self.comboboxStatus.append("3", "Out of Contract")
        self.comboboxStatus.append("4", "One Year or Less Remaining on Contract")
        label.set_mnemonic_widget(self.comboboxStatus)
        grid.attach(self.comboboxStatus, 1, 4, 3, 1)

        commonframe = widgets.CommonFrame(title="Skills")
        self.vbox.add(commonframe)

        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)
        commonframe.insert(grid)

        label = widgets.AlignedLabel("_Keeping")
        grid.attach(label, 0, 0, 1, 1)
        self.keeping = self.Attributes()
        label.set_mnemonic_widget(self.keeping.minimum)
        grid.attach(self.keeping, 1, 0, 1, 1)
        label = widgets.AlignedLabel("_Tackling")
        grid.attach(label, 0, 1, 1, 1)
        self.tackling = self.Attributes()
        label.set_mnemonic_widget(self.tackling.minimum)
        grid.attach(self.tackling, 1, 1, 1, 1)
        label = widgets.AlignedLabel("_Passing")
        grid.attach(label, 0, 2, 1, 1)
        self.passing = self.Attributes()
        label.set_mnemonic_widget(self.passing.minimum)
        grid.attach(self.passing, 1, 2, 1, 1)
        label = widgets.AlignedLabel("_Shooting")
        grid.attach(label, 2, 0, 1, 1)
        self.shooting = self.Attributes()
        label.set_mnemonic_widget(self.shooting.minimum)
        grid.attach(self.shooting, 3, 0, 1, 1)
        label = widgets.AlignedLabel("_Pace")
        grid.attach(label, 2, 1, 1, 1)
        self.pace = self.Attributes()
        label.set_mnemonic_widget(self.pace.minimum)
        grid.attach(self.pace, 3, 1, 1, 1)
        label = widgets.AlignedLabel("_Heading")
        grid.attach(label, 2, 2, 1, 1)
        self.heading = self.Attributes()
        label.set_mnemonic_widget(self.heading.minimum)
        grid.attach(self.heading, 3, 2, 1, 1)
        label = widgets.AlignedLabel("_Stamina")
        grid.attach(label, 4, 0, 1, 1)
        self.stamina = self.Attributes()
        label.set_mnemonic_widget(self.stamina.minimum)
        grid.attach(self.stamina, 5, 0, 1, 1)
        label = widgets.AlignedLabel("_Ball Control")
        grid.attach(label, 4, 1, 1, 1)
        self.ball_control = self.Attributes()
        label.set_mnemonic_widget(self.ball_control.minimum)
        grid.attach(self.ball_control, 5, 1, 1, 1)
        label = widgets.AlignedLabel("_Set Pieces")
        grid.attach(label, 4, 2, 1, 1)
        self.set_pieces = self.Attributes()
        label.set_mnemonic_widget(self.set_pieces.minimum)
        grid.attach(self.set_pieces, 5, 2, 1, 1)

    def display(self):
        self.checkbuttonShowOwnPlayers.set_label("_Display %s Players In Player Search" % (game.clubs[game.teamid].name))
        self.checkbuttonShowOwnPlayers.set_active(game.player_filter[0])

        self.comboboxPosition.set_active(game.player_filter[1])
        self.spinbuttonMinValue.set_value(game.player_filter[2][0])
        self.spinbuttonMaxValue.set_value(game.player_filter[2][1])
        self.spinbuttonMinAge.set_value(game.player_filter[3][0])
        self.spinbuttonMaxAge.set_value(game.player_filter[3][1])
        self.comboboxStatus.set_active(game.player_filter[4])

        self.keeping.display(game.player_filter[5][0], game.player_filter[5][1])
        self.tackling.display(game.player_filter[6][0], game.player_filter[6][1])
        self.passing.display(game.player_filter[7][0], game.player_filter[7][1])
        self.shooting.display(game.player_filter[8][0], game.player_filter[8][1])
        self.pace.display(game.player_filter[9][0], game.player_filter[9][1])
        self.heading.display(game.player_filter[10][0], game.player_filter[10][1])
        self.stamina.display(game.player_filter[11][0], game.player_filter[11][1])
        self.ball_control.display(game.player_filter[12][0], game.player_filter[12][1])
        self.set_pieces.display(game.player_filter[13][0], game.player_filter[13][1])

        self.show_all()

        if self.run() == Gtk.ResponseType.OK:
            own_players = self.checkbuttonShowOwnPlayers.get_active()
            position = int(self.comboboxPosition.get_active())
            value = (self.spinbuttonMinValue.get_value_as_int(),
                     self.spinbuttonMaxValue.get_value_as_int())
            age = (self.spinbuttonMinAge.get_value_as_int(),
                   self.spinbuttonMaxAge.get_value_as_int())
            status = int(self.comboboxStatus.get_active())

            keeping = self.keeping.retrieve()
            tackling = self.tackling.retrieve()
            passing = self.passing.retrieve()
            shooting = self.shooting.retrieve()
            heading = self.heading.retrieve()
            pace = self.pace.retrieve()
            stamina = self.stamina.retrieve()
            ball_control = self.ball_control.retrieve()
            set_pieces = self.set_pieces.retrieve()

            game.player_filter = (own_players,
                                  position,
                                  value,
                                  age,
                                  status,
                                  keeping,
                                  tackling,
                                  passing,
                                  shooting,
                                  heading,
                                  pace,
                                  stamina,
                                  ball_control,
                                  set_pieces,
                                 )

    def value_changed(self, spinbutton):
        minimum = self.spinbuttonMinValue.get_value_as_int()
        maximum = self.spinbuttonMinValue.get_range()[1]
        self.spinbuttonMaxValue.set_range(minimum, maximum)

    def age_changed(self, spinbutton):
        minimum = self.spinbuttonMinAge.get_value_as_int()
        maximum = self.spinbuttonMinAge.get_range()[1]
        self.spinbuttonMaxAge.set_range(minimum, maximum)


class SquadFilter(Gtk.Dialog):
    '''
    Dialog for filtering players in the squad view.
    '''
    def __init__(self):
        Gtk.Dialog.__init__(self)
        self.set_transient_for(game.window)
        self.set_title("Filter Squad")
        self.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("_Filter", Gtk.ResponseType.OK)
        self.set_resizable(False)
        self.set_border_width(5)
        self.vbox.set_spacing(5)

        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)
        self.vbox.add(grid)

        label = widgets.AlignedLabel("_Position")
        grid.attach(label, 0, 0, 1, 1)
        self.comboboxPosition = Gtk.ComboBoxText()
        self.comboboxPosition.append("0", "All")
        self.comboboxPosition.append("1", "Goalkeeper")
        self.comboboxPosition.append("2", "Defender")
        self.comboboxPosition.append("3", "Midfielder")
        self.comboboxPosition.append("4", "Attacker")
        label.set_mnemonic_widget(self.comboboxPosition)
        grid.attach(self.comboboxPosition, 1, 0, 1, 1)

        self.checkbuttonAvailable = Gtk.CheckButton("_Show Only Available Players")
        self.checkbuttonAvailable.set_use_underline(True)
        self.checkbuttonAvailable.set_tooltip_text("Injured or suspended players will not be displayed")
        grid.attach(self.checkbuttonAvailable, 0, 1, 3, 1)

    def display(self):
        self.comboboxPosition.set_active(game.squad_filter[0])
        self.checkbuttonAvailable.set_active(game.squad_filter[1])

        self.show_all()

        if self.run() == Gtk.ResponseType.OK:
            position = int(self.comboboxPosition.get_active())
            available = self.checkbuttonAvailable.get_active()

            game.squad_filter = (position, available)
