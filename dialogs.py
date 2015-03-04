#!/usr/bin/env python3

import gi
from gi.repository import Gtk
from gi.repository import GdkPixbuf
import os
import platform
import random
import glob

import calculator
import constants
import display
import evaluation
import fileio
import game
import money
import version
import widgets


def exit_game(leave=False):
    '''
    Setting 'leave' to True allows this save dialog to be reused for
    starting new games from the File menu.
    '''
    messagedialog = Gtk.MessageDialog(type=Gtk.MessageType.QUESTION)
    messagedialog.set_transient_for(game.window)
    messagedialog.set_title("Exit Game")
    messagedialog.add_button("_Cancel", Gtk.ResponseType.CANCEL)
    messagedialog.add_button("_Do Not Save", Gtk.ResponseType.REJECT)
    messagedialog.add_button("_Save", Gtk.ResponseType.ACCEPT)
    messagedialog.set_default_response(Gtk.ResponseType.ACCEPT)
    messagedialog.set_markup("<span size='12000'><b>The game has not been saved.</b></span>")

    if leave:
        message = "Do you want to save before starting a new game?"
    else:
        message = "Do you want to save before closing?"

    messagedialog.format_secondary_text(message)

    response = messagedialog.run()

    state = True

    if response == Gtk.ResponseType.REJECT:
        state = False
    elif response == Gtk.ResponseType.ACCEPT:
        save_dialog = SaveDialog()
        state = save_dialog.display()
        save_dialog.destroy()

    messagedialog.destroy()

    return state


def about():
    path = os.path.join("resources", "logo.svg")
    icon = GdkPixbuf.Pixbuf.new_from_file_at_size(path, 64, 64)

    aboutdialog = Gtk.AboutDialog()
    aboutdialog.set_program_name("%s" % (version.NAME))
    aboutdialog.set_version("%s" % (version.VERSION))
    aboutdialog.set_comments("%s" % (version.COMMENTS))
    aboutdialog.set_website("%s" % (version.WEBSITE))
    aboutdialog.set_license_type(Gtk.License.GPL_3_0)
    aboutdialog.set_authors([version.AUTHORS])
    aboutdialog.set_logo(icon)
    aboutdialog.set_transient_for(game.window)

    aboutdialog.run()
    aboutdialog.destroy()


class OpenDialog(Gtk.FileChooserDialog):
    def __init__(self):
        Gtk.FileChooserDialog.__init__(self)
        self.set_transient_for(game.window)
        self.set_title("Open File")
        self.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("_Open", Gtk.ResponseType.OK)
        self.set_action(Gtk.FileChooserAction.OPEN)
        self.set_current_folder(game.save_location)
        self.connect("response", self.response_handler)

        filefilter = Gtk.FileFilter()
        filefilter.set_name("Saved Game")
        filefilter.add_pattern("*.osm")
        self.add_filter(filefilter)

    def display(self):
        state = False

        if self.run() == Gtk.ResponseType.OK:
            state = True

        return state

    def response_handler(self, filechooserdialog, response):
        if response == Gtk.ResponseType.OK:
            filename = self.get_filename()
            fileio.open_file(filename)

        self.hide()


class SaveDialog(Gtk.FileChooserDialog):
    def __init__(self):
        Gtk.FileChooserDialog.__init__(self)
        self.set_transient_for(game.window)
        self.set_title("Save File")
        self.set_action(Gtk.FileChooserAction.SAVE)
        self.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("_Save", Gtk.ResponseType.OK)
        self.connect("response", self.response_handler)

        filefilter = Gtk.FileFilter()
        filefilter.set_name("Saved Game")
        filefilter.add_pattern("*.osm")
        self.add_filter(filefilter)

    def display(self):
        self.set_current_folder(game.save_location)
        self.show_all()

        state = True

        if self.run() == Gtk.ResponseType.OK:
            state = False

        return state

    def response_handler(self, filechooserdialog, response):
        if response == Gtk.ResponseType.OK:
            if self.confirm_overwrite() == Gtk.FileChooserConfirmation.ACCEPT_FILENAME:
                self.hide()
        else:
            self.hide()

    def confirm_overwrite(self):
        folder, filename = self.file_extension()

        items = folder.split(os.sep)
        count = len(items) - 1
        foldername = items[count]

        filepath = os.path.join(folder, filename)

        if not os.path.isfile(filepath):
            fileio.save_file(filepath)
            return Gtk.FileChooserConfirmation.ACCEPT_FILENAME

        dialog = Gtk.MessageDialog(type=Gtk.MessageType.QUESTION)
        dialog.set_transient_for(game.window)
        dialog.set_markup("<span size='12000'><b>A file named '%s' already exists. Do you want to replace it?</b></span>" % (filename))
        dialog.format_secondary_text("The file already exists in '%s'. Replacing it will overwrite its content." % (foldername))
        dialog.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        dialog.add_button("_Replace", Gtk.ResponseType.OK)
        dialog.set_default_response(Gtk.ResponseType.CANCEL)
        response = dialog.run()
        dialog.destroy()

        if response == Gtk.ResponseType.OK:
            fileio.save_file(filepath)
            return Gtk.FileChooserConfirmation.ACCEPT_FILENAME
        else:
            return Gtk.FileChooserConfirmation.SELECT_AGAIN

    def file_extension(self):
        folder = self.get_current_folder()
        filename = self.get_current_name()

        if not filename.endswith(".osm"):
            filename = "%s.osm" % (filename)

        return folder, filename


def delete_dialog():
    def load_directory(filechooserbutton=None, location=None):
        liststore.clear()

        if filechooserbutton:
            location = filechooserbutton.get_uri()
            location = location[7:]

        filenames = glob.glob("%s/*.osm" % (location))

        for filepath in filenames:
            filename = os.path.split(filepath)
            liststore.append([filepath, filename[1]])

    def selection_changed(treeselection):
        model, treepath = treeselection.get_selected_rows()

        if treepath:
            buttonDelete.set_sensitive(True)
        else:
            buttonDelete.set_sensitive(False)

    def delete_file(button):
        model, treepath = treeselection.get_selected_rows()

        for item in treepath:
            filepath = model[item][0]
            os.remove(filepath)

        load_directory(location=game.save_location)

    dialog = Gtk.Dialog()
    dialog.set_transient_for(game.window)
    dialog.set_default_size(225, 350)
    dialog.set_border_width(5)
    dialog.set_title("Delete File")
    dialog.add_button("_Close", Gtk.ResponseType.CLOSE)
    dialog.vbox.set_spacing(5)

    filechooserbutton = Gtk.FileChooserButton()
    filechooserbutton.set_action(Gtk.FileChooserAction.SELECT_FOLDER)
    filechooserbutton.set_current_folder(game.save_location)
    filechooserbutton.connect("file-set", load_directory)
    dialog.vbox.add(filechooserbutton)

    scrolledwindow = Gtk.ScrolledWindow()
    scrolledwindow.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
    dialog.vbox.add(scrolledwindow)

    buttonDelete = widgets.Button("_Delete")
    buttonDelete.set_sensitive(False)
    buttonDelete.connect("clicked", delete_file)

    liststore = Gtk.ListStore(str, str)
    treemodelsort = Gtk.TreeModelSort(liststore)
    treemodelsort.set_sort_column_id(1, Gtk.SortType.ASCENDING)
    load_directory(location=game.save_location)

    treeview = Gtk.TreeView()
    treeview.set_vexpand(True)
    treeview.set_model(treemodelsort)
    treeview.set_search_column(1)
    treeview.set_headers_visible(False)
    treeview.set_rubber_banding(True)
    treeselection = treeview.get_selection()
    treeselection.set_mode(Gtk.SelectionMode.MULTIPLE)
    treeselection.connect("changed", selection_changed)
    scrolledwindow.add(treeview)

    cellrenderertext = Gtk.CellRendererText()
    treeviewcolumn = Gtk.TreeViewColumn(None, cellrenderertext, text=1)
    treeview.append_column(treeviewcolumn)

    buttonbox = Gtk.ButtonBox()
    buttonbox.set_layout(Gtk.ButtonBoxStyle.END)
    buttonbox.add(buttonDelete)
    dialog.vbox.add(buttonbox)

    dialog.show_all()
    dialog.run()
    dialog.destroy()


def preferences_dialog():
    def music_handler(checkbutton):
        if not game.music:
            game.player.play()
            game.music = True
            game.preferences["AUDIO"]["PlayMusic"] = "True"
        elif game.music:
            game.player.stop()
            game.music = False
            game.preferences["AUDIO"]["PlayMusic"] = "False"

        game.preferences.writefile()

    def change_currency(combobox):
        game.currency = combobox.get_active_id()

        game.preferences["INTERFACE"]["Currency"] = game.currency
        game.preferences.writefile()

        game.currency = int(game.currency)

    def change_screen(combobox):
        game.start_screen = combobox.get_active_id()

        game.preferences["INTERFACE"]["StartScreen"] = game.start_screen
        game.preferences.writefile()

        game.start_screen = int(game.start_screen)

    def change_database_default(filechooserbutton):
        directory = filechooserbutton.get_uri()
        game.database_filename = directory[7:]

        game.preferences["DATABASE"]["Database"] = game.database_filename
        game.preferences.writefile()

    def change_data_location(filechooserbutton):
        directory = filechooserbutton.get_uri()
        game.data_location = directory[7:]

        game.preferences["SAVE"]["Data"] = game.data_location
        game.preferences["SAVE"]["Saves"] = os.path.join(game.data_location, "saves")
        game.preferences.writefile()

    def clear_names(button):
        filepath = os.path.join(game.data_location, "users.txt")
        open(filepath, "w")

    dialog = Gtk.Dialog()
    dialog.set_title("Preferences")
    dialog.set_transient_for(game.window)
    dialog.set_resizable(False)
    dialog.add_button("_Close", Gtk.ResponseType.OK)
    dialog.set_border_width(5)
    dialog.vbox.set_spacing(5)

    grid = Gtk.Grid()
    grid.set_row_spacing(5)
    grid.set_column_spacing(5)
    dialog.vbox.add(grid)

    checkbuttonMusic = Gtk.CheckButton("Play (annoying) USM Music in Background")
    checkbuttonMusic.set_active(game.music)
    checkbuttonMusic.connect("toggled", music_handler)
    grid.attach(checkbuttonMusic, 0, 0, 3, 1)

    label = widgets.AlignedLabel("In-Game Starting Screen")
    grid.attach(label, 0, 1, 1, 1)
    comboboxScreen = Gtk.ComboBoxText()
    comboboxScreen.append("1", "Squad")
    comboboxScreen.append("2", "Fixtures")
    comboboxScreen.append("3", "News")
    comboboxScreen.append("20", "Player Search")
    comboboxScreen.set_active_id(str(game.start_screen))
    comboboxScreen.set_tooltip_text("Choose which screen should first appear when starting new and loading saved games.")
    comboboxScreen.connect("changed", change_screen)
    grid.attach(comboboxScreen, 1, 1, 3, 1)

    label = widgets.AlignedLabel("Display Currency")
    grid.attach(label, 0, 2, 1, 1)
    comboboxCurrency = Gtk.ComboBoxText()
    comboboxCurrency.append("0", "British Pound")
    comboboxCurrency.append("1", "U.S. Dollar")
    comboboxCurrency.append("2", "Euro")
    comboboxCurrency.set_active_id(str(game.currency))
    comboboxCurrency.set_tooltip_text("The monetary currency which will be used during the game.")
    comboboxCurrency.connect("changed", change_currency)
    grid.attach(comboboxCurrency, 1, 2, 3, 1)

    # Data locations
    frame = widgets.CommonFrame("Data Locations")
    dialog.vbox.add(frame)

    grid1 = Gtk.Grid()
    grid1.set_row_spacing(5)
    grid1.set_column_spacing(5)
    frame.insert(grid1)

    label = widgets.AlignedLabel("Default Database Location")
    grid1.attach(label, 0, 0, 1, 1)
    filechooserDatabaseLocation = Gtk.FileChooserButton()
    filechooserDatabaseLocation.set_tooltip_text("Location of default database file to load.")
    filechooserDatabaseLocation.set_action(Gtk.FileChooserAction.OPEN)
    filechooserDatabaseLocation.set_filename(os.path.join("databases", game.database_filename))
    filechooserDatabaseLocation.connect("file-set", change_database_default)
    grid1.attach(filechooserDatabaseLocation, 1, 0, 1, 1)

    label = widgets.AlignedLabel("Data File Location")
    grid1.attach(label, 0, 1, 1, 1)
    filechooserSaveLocation = Gtk.FileChooserButton()
    filechooserSaveLocation.set_tooltip_text("Default location where game data is stored.")
    filechooserSaveLocation.set_action(Gtk.FileChooserAction.SELECT_FOLDER)
    filechooserSaveLocation.set_filename(game.data_location)
    filechooserSaveLocation.connect("file-set", change_data_location)
    grid1.attach(filechooserSaveLocation, 1, 1, 1, 1)

    # Manager names
    frame = widgets.CommonFrame("Manager Names")
    dialog.vbox.add(frame)

    grid1 = Gtk.Grid()
    grid1.set_column_spacing(5)
    frame.insert(grid1)

    label = widgets.AlignedLabel("Clear previously entered manager names:")
    grid1.attach(label, 0, 0, 1, 1)
    buttonbox = Gtk.ButtonBox()
    grid1.attach(buttonbox, 1, 0, 1, 1)
    buttonClear = widgets.Button("_Clear Names")
    buttonClear.connect("clicked", clear_names)
    buttonbox.add(buttonClear)

    dialog.show_all()
    dialog.run()
    dialog.destroy()


def information_dialog():
    dialog = Gtk.Dialog()
    dialog.set_transient_for(game.window)
    dialog.set_title("Information")
    dialog.set_border_width(5)
    dialog.add_button("_Close", Gtk.ResponseType.CLOSE)

    grid = Gtk.Grid()
    grid.set_row_spacing(5)
    grid.set_column_spacing(5)
    dialog.vbox.add(grid)

    label = widgets.AlignedLabel("Python version")
    grid.attach(label, 0, 0, 1, 1)
    label = widgets.AlignedLabel("%s" % (platform.python_version()))
    grid.attach(label, 1, 0, 1, 1)

    label = widgets.AlignedLabel("GTK+ version")
    grid.attach(label, 0, 1, 1, 1)
    label = widgets.AlignedLabel("%i.%i.%i" % (Gtk.MAJOR_VERSION, Gtk.MINOR_VERSION, Gtk.MICRO_VERSION))
    grid.attach(label, 1, 1, 1, 1)

    label = widgets.AlignedLabel("GObject version")
    grid.attach(label, 0, 2, 1, 1)
    label = widgets.AlignedLabel("%i.%i.%i" % (gi.version_info))
    grid.attach(label, 1, 2, 1, 1)

    dialog.show_all()
    dialog.run()
    dialog.destroy()


def help_content():
    object_name = game.active_screen.__name__
    filename = os.path.join("help", "%s.txt" % (object_name))

    try:
        fp = open(filename, "r")
        content = fp.read()
        content = content.rstrip("\n")
        fp.close()
    except FileNotFoundError:
        print("Unable to find %s help file" % (object_name))

        return

    dialog = Gtk.Dialog()
    dialog.set_title("Help Contents")
    dialog.set_transient_for(game.window)
    dialog.set_default_size(480, 320)
    dialog.add_button("_Close", Gtk.ResponseType.CLOSE)

    scrolledwindow = Gtk.ScrolledWindow()
    scrolledwindow.set_vexpand(True)
    scrolledwindow.set_hexpand(True)
    dialog.vbox.add(scrolledwindow)

    textview = Gtk.TextView()
    textview.set_editable(False)
    textview.set_wrap_mode(Gtk.WrapMode.WORD)
    textview.set_left_margin(5)
    textview.set_right_margin(5)
    scrolledwindow.add(textview)
    textbuffer = textview.get_buffer()
    textbuffer.set_text(content, -1)

    dialog.show_all()
    dialog.run()
    dialog.destroy()


def quick_sell(name, club, amount):
    messagedialog = Gtk.MessageDialog(type=Gtk.MessageType.QUESTION)
    messagedialog.set_transient_for(game.window)
    messagedialog.set_title("Quick Sell")
    messagedialog.add_button("_Cancel", Gtk.ResponseType.CANCEL)
    messagedialog.add_button("C_onfirm", Gtk.ResponseType.OK)
    messagedialog.set_default_response(Gtk.ResponseType.CANCEL)
    messagedialog.set_markup("Sell %s to %s for %s?" % (name, club, amount))

    state = False

    if messagedialog.run() == Gtk.ResponseType.OK:
        state = True

    messagedialog.destroy()

    return state


def renew_player_contract(playerid):
    '''
    When renewing a contract, the current wage and player value must be taken
    into account. Typically, renewing a contract instantly results in a 1-3
    thousand raise, however the projected wage also needs to be looked at to
    handle improvements in the players skill.

    Also look at morale, as a player with less than a certain number of points
    will not want to renew his contract.
    '''
    player = game.players[playerid]
    name = display.name(player, mode=1)

    wage = calculator.wage(playerid)
    wage = wage * 1.1
    wage = calculator.wage_rounder(wage)
    leaguewin, leaguerunnerup, winbonus, goalbonus = calculator.bonus(wage)

    if player.age < 25:
        contract = 5
    elif player.age < 29:
        contract = 4
    elif player.age < 33:
        contract = 3
    elif player.age < 35:
        contract = 2
    else:
        contract = 1

    dialog = Gtk.Dialog()
    dialog.set_transient_for(game.window)
    dialog.set_title("Renew Contract")
    dialog.set_border_width(5)
    dialog.add_button("_Cancel", Gtk.ResponseType.CANCEL)
    dialog.add_button("_Renew", Gtk.ResponseType.OK)
    dialog.set_default_response(Gtk.ResponseType.CANCEL)
    dialog.vbox.set_spacing(5)

    label = widgets.AlignedLabel("<b>%s</b> is requesting a %i year contract." % (name, contract))
    dialog.vbox.add(label)

    commonframe = widgets.CommonFrame("Details")
    dialog.vbox.add(commonframe)

    grid = Gtk.Grid()
    grid.set_row_spacing(5)
    grid.set_column_spacing(5)
    commonframe.insert(grid)

    label = widgets.AlignedLabel("Weekly Wage")
    grid.attach(label, 0, 0, 1, 1)
    spinbuttonWage = widgets.SpinButton(maximum=100000)
    spinbuttonWage.set_value(wage)
    grid.attach(spinbuttonWage, 1, 0, 1, 1)
    label = widgets.AlignedLabel("League Champions Bonus")
    grid.attach(label, 0, 1, 1, 1)
    spinbuttonLeagueChampions = widgets.SpinButton(maximum=200000)
    spinbuttonLeagueChampions.set_value(leaguewin)
    grid.attach(spinbuttonLeagueChampions, 1, 1, 1, 1)
    label = widgets.AlignedLabel("League Runner Up Bonus")
    grid.attach(label, 0, 2, 1, 1)
    spinbuttonLeagueRunnerUp = widgets.SpinButton(maximum=200000)
    spinbuttonLeagueRunnerUp.set_value(leaguerunnerup)
    grid.attach(spinbuttonLeagueRunnerUp, 1, 2, 1, 1)
    label = widgets.AlignedLabel("Win Bonus")
    grid.attach(label, 0, 3, 1, 1)
    spinbuttonWinBonus = widgets.SpinButton(maximum=10000)
    spinbuttonWinBonus.set_value(winbonus)
    grid.attach(spinbuttonWinBonus, 1, 3, 1, 1)
    label = widgets.AlignedLabel("Goal Bonus")
    grid.attach(label, 0, 4, 1, 1)
    spinbuttonGoalBonus = widgets.SpinButton(maximum=10000)
    spinbuttonGoalBonus.set_value(goalbonus)
    grid.attach(spinbuttonGoalBonus, 1, 4, 1, 1)
    label = widgets.AlignedLabel("Contract Length")
    grid.attach(label, 0, 5, 1, 1)
    spinbuttonContract = widgets.SpinButton.new_with_range(1, 5, 1)
    spinbuttonContract.set_value(contract)
    grid.attach(spinbuttonContract, 1, 5, 1, 1)

    dialog.show_all()

    state = False

    if dialog.run() == Gtk.ResponseType.OK:
        player.wage = spinbuttonWage.get_value_as_int()

        leaguechampions = spinbuttonLeagueChampions.get_value_as_int()
        leaguerunnerup = spinbuttonLeagueRunnerUp.get_value_as_int()
        winbonus = spinbuttonWinBonus.get_value_as_int()
        goalbonus = spinbuttonGoalBonus.get_value_as_int()
        player.bonus = leaguechampions, leaguerunnerup, winbonus, goalbonus
        player.contract = spinbuttonContract.get_value_as_int() * 52

        evaluation.morale(playerid, 15)

        state = True

    dialog.destroy()

    return state


def scout_report(player, status):
    message = {0: "The scouting team report that %s would not be a good signing." % (player),
              1: "%s would be considered a good signing by the scouting team." % (player),
              2: "After some scouting, %s would be an excellent addition to the squad." % (player),
              3: "The scouts report that %s would be a top prospect for the future." % (player),
              }

    messagedialog = Gtk.MessageDialog(type=Gtk.MessageType.INFO)
    messagedialog.set_transient_for(game.window)
    messagedialog.set_title("Scout Report")
    messagedialog.add_button("_Close", Gtk.ResponseType.CLOSE)
    messagedialog.set_markup(message[status])
    messagedialog.run()
    messagedialog.destroy()


def player_info(playerid):
    dialog = Gtk.Dialog()
    dialog.set_border_width(5)
    dialog.set_transient_for(game.window)
    dialog.set_title("Player Information")
    dialog.add_button("_Close", Gtk.ResponseType.CLOSE)
    dialog.vbox.set_spacing(5)

    commonframe = widgets.CommonFrame("Contract")
    dialog.vbox.add(commonframe)
    grid = Gtk.Grid()
    grid.set_row_spacing(5)
    grid.set_column_spacing(5)
    commonframe.insert(grid)

    label = widgets.AlignedLabel("Win Bonus")
    grid.attach(label, 0, 0, 1, 1)
    label = widgets.AlignedLabel("Goal Bonus")
    grid.attach(label, 0, 1, 1, 1)
    label = widgets.AlignedLabel("League Champions Bonus")
    grid.attach(label, 0, 2, 1, 1)
    label = widgets.AlignedLabel("League Runners Up Bonus")
    grid.attach(label, 0, 3, 1, 1)

    if playerid:
        bonus = game.players[playerid].bonus

        amount = display.wage(bonus[2])
        label = widgets.AlignedLabel(amount)
        grid.attach(label, 1, 0, 1, 1)
        amount = display.wage(bonus[3])
        label = widgets.AlignedLabel(amount)
        grid.attach(label, 1, 1, 1, 1)
        amount = display.wage(bonus[0])
        label = widgets.AlignedLabel(amount)
        grid.attach(label, 1, 2, 1, 1)
        amount = display.wage(bonus[1])
        label = widgets.AlignedLabel(amount)
        grid.attach(label, 1, 3, 1, 1)

    commonframe = widgets.CommonFrame("Injuries / Suspensions")
    dialog.vbox.add(commonframe)
    grid = Gtk.Grid()
    grid.set_row_spacing(5)
    grid.set_column_spacing(5)
    commonframe.insert(grid)

    label = widgets.AlignedLabel("Injury")
    grid.attach(label, 0, 0, 1, 1)
    label = widgets.AlignedLabel("Injury Period")
    grid.attach(label, 0, 1, 1, 1)
    label = widgets.AlignedLabel("Suspension")
    grid.attach(label, 0, 2, 1, 1)
    label = widgets.AlignedLabel("Suspension Period")
    grid.attach(label, 0, 3, 1, 1)

    if playerid:
        player = game.players[playerid]
        injuryid = player.injury_type
        suspensionid = player.suspension_type

        if injuryid == 0:
            injury_type = "None"
            injury_period = "N/A"
        else:
            injury_type = constants.injuries[injuryid][0]
            injury_period = "%i Weeks" % (player.injury_period)

        if suspensionid == 0:
            suspension_type = "None"
            suspension_period = "N/A"
        else:
            suspension_type = constants.suspensions[suspensionid][0]
            suspension_period = "%i Weeks" % (player.suspension_period)

        label = widgets.AlignedLabel("%s" % (injury_type))
        grid.attach(label, 1, 0, 1, 1)
        label = widgets.AlignedLabel("%s" % (injury_period))
        grid.attach(label, 1, 1, 1, 1)
        label = widgets.AlignedLabel("%s" % (suspension_type))
        grid.attach(label, 1, 2, 1, 1)
        label = widgets.AlignedLabel("%s" % (suspension_period))
        grid.attach(label, 1, 3, 1, 1)

    dialog.show_all()
    dialog.run()
    dialog.destroy()


def not_enough_players(number):
    if number == 0:
        text = "Currently there are no players chosen."
    elif number == 1:
        text = "Currently there is only %i player chosen." % (number)
    else:
        text = "Currently there are only %i players chosen." % (number)

    messagedialog = Gtk.MessageDialog(type=Gtk.MessageType.ERROR)
    messagedialog.format_secondary_text(text)
    messagedialog.set_transient_for(game.window)
    messagedialog.set_title("Not Enough Players")
    messagedialog.add_button("_Close", Gtk.ResponseType.CLOSE)
    messagedialog.set_markup("You have not selected enough players to proceed to the next game.")
    messagedialog.run()
    messagedialog.destroy()


def not_enough_subs(number):
    messagedialog = Gtk.MessageDialog(type=Gtk.MessageType.WARNING)
    messagedialog.set_transient_for(game.window)
    messagedialog.set_title("Not Enough Subs")
    messagedialog.add_button("_No", Gtk.ResponseType.NO)
    messagedialog.add_button("_Yes", Gtk.ResponseType.YES)
    messagedialog.set_default_response(Gtk.ResponseType.NO)
    messagedialog.set_markup("<span size='12000'><b>You have only selected %i out of a possible 5 subs.</b></span>" % (number))
    messagedialog.format_secondary_text("Do you wish to continue to the game?")

    answer = False

    if messagedialog.run() == Gtk.ResponseType.YES:
        answer = True

    messagedialog.destroy()

    return answer


def proceed_to_game(team):
    messagedialog = Gtk.MessageDialog(type=Gtk.MessageType.QUESTION)
    messagedialog.set_title("Proceed To Next Match")
    messagedialog.set_transient_for(game.window)
    messagedialog.add_button("_No", Gtk.ResponseType.NO)
    messagedialog.add_button("_Yes", Gtk.ResponseType.YES)
    messagedialog.set_default_response(Gtk.ResponseType.NO)
    messagedialog.set_markup("<span size='12000'><b>Proceed to next match?</b></span>")
    messagedialog.format_secondary_text("Your next match is against %s." % (team))

    response = messagedialog.run()

    proceed = False

    if response == Gtk.ResponseType.YES:
        proceed = True

    messagedialog.destroy()

    return proceed


def add_individual_training(playerid=None):
    '''
    This dialog is used for both adding and editing players within the
    individual training screen. When a playerid is passed, the player
    selection functionality is hidden and the dict containing the
    individual training details is updated rather than added to.

    Output from this function is key values which are translated in
    training.py to the correct values which are then displayed.
    '''
    def update_speciality(combobox):
        active = combobox.get_active()
        model = combobox.get_model()
        coachid = model[active][0]

        coach = game.clubs[game.teamid].coaches_hired[coachid]

        if coach.speciality == 0:
            speciality = "Keeping"
        elif coach.speciality == 1:
            speciality = "Tackling, Stamina"
        elif coach.speciality == 2:
            speciality = "Passing, Ball Control"
        elif coach.speciality == 3:
            speciality = "Shooting"
        elif coach.speciality == 4:
            speciality = "Fitness, Pace, Stamina"
        elif coach.speciality == 5:
            speciality = "All"

        labelSpeciality.set_label(speciality)

    dialog = Gtk.Dialog()
    dialog.set_title("Individual Training")
    dialog.set_transient_for(game.window)
    dialog.add_button("_Cancel", Gtk.ResponseType.CANCEL)

    if playerid == None:
        dialog.add_button("_Add", Gtk.ResponseType.OK)
    else:
        dialog.add_button("_Edit", Gtk.ResponseType.OK)

    dialog.set_default_response(Gtk.ResponseType.OK)

    liststorePlayer = Gtk.ListStore(int, str)

    for item in game.clubs[game.teamid].squad:
        player = game.players[item]
        name = display.name(player)

        liststorePlayer.append([item, name])

    liststoreCoach = Gtk.ListStore(int, str)

    for coachid, coach in game.clubs[game.teamid].coaches_hired.items():
        liststoreCoach.append([coachid, coach.name])

    grid = Gtk.Grid()
    grid.set_border_width(5)
    grid.set_row_spacing(5)
    grid.set_column_spacing(5)
    dialog.vbox.add(grid)

    for count, text in enumerate(("Coach", "Skill", "Intensity")):
        label = widgets.AlignedLabel("%s" % (text))
        grid.attach(label, 0, count + 1, 1, 1)

    cellrenderertext = Gtk.CellRendererText()

    if not playerid:
        label = widgets.AlignedLabel("Player")
        grid.attach(label, 0, 0, 1, 1)

        comboboxPlayer = Gtk.ComboBox()
        comboboxPlayer.set_model(liststorePlayer)
        comboboxPlayer.set_active(0)
        comboboxPlayer.pack_start(cellrenderertext, True)
        comboboxPlayer.add_attribute(cellrenderertext, "text", 1)
        grid.attach(comboboxPlayer, 1, 0, 1, 1)

    comboboxCoach = Gtk.ComboBox()
    comboboxCoach.set_model(liststoreCoach)
    comboboxCoach.connect("changed", update_speciality)
    comboboxCoach.pack_start(cellrenderertext, True)
    comboboxCoach.add_attribute(cellrenderertext, "text", 1)
    grid.attach(comboboxCoach, 1, 1, 1, 1)

    label = widgets.AlignedLabel("Specialities:")
    grid.attach(label, 2, 1, 1, 1)
    labelSpeciality = widgets.AlignedLabel()
    grid.attach(labelSpeciality, 3, 1, 1, 1)

    comboboxSkill = Gtk.ComboBoxText()

    for count, item in enumerate(constants.skill):
        comboboxSkill.append(str(count), item)

    comboboxSkill.append("9", "Fitness")
    comboboxSkill.set_active(0)
    grid.attach(comboboxSkill, 1, 2, 1, 1)

    grid1 = Gtk.Grid()
    grid1.set_column_spacing(5)
    grid.attach(grid1, 1, 3, 2, 1)

    intensity_widget = []
    radiobuttonIntensityLow = Gtk.RadioButton("Low")
    intensity_widget.append(radiobuttonIntensityLow)
    grid1.attach(radiobuttonIntensityLow, 0, 0, 1, 1)
    radiobuttonIntensityMedium = Gtk.RadioButton("Medium")
    radiobuttonIntensityMedium.join_group(radiobuttonIntensityLow)
    radiobuttonIntensityMedium.set_active(True)
    intensity_widget.append(radiobuttonIntensityMedium)
    grid1.attach(radiobuttonIntensityMedium, 1, 0, 1, 1)
    radiobuttonIntensityHigh = Gtk.RadioButton("High")
    radiobuttonIntensityHigh.join_group(radiobuttonIntensityLow)
    intensity_widget.append(radiobuttonIntensityHigh)
    grid1.attach(radiobuttonIntensityHigh, 2, 0, 1, 1)

    # Set values when editing
    if playerid:
        training = game.clubs[game.teamid].individual_training
        training = training[playerid]

        # Set value for coach within combobox
        count = 0
        for key, item in game.clubs[game.teamid].coaches_hired.items():
            if key == training[0]:
                comboboxCoach.set_active(count)

            count += 1

        comboboxSkill.set_active(training[1])
        intensity_widget[training[2]].set_active(True)
    else:
        # Required to set default specialities for coach
        # Do not remove unless setting it another "smarter" way
        comboboxCoach.set_active(0)

    dialog.show_all()

    training = None

    if dialog.run() == Gtk.ResponseType.OK:
        if not playerid:
            active = comboboxPlayer.get_active()
            playerid = liststorePlayer[active][0]

        # Coach
        active = comboboxCoach.get_active()
        model = comboboxCoach.get_model()
        coach = model[active][0]

        # Skill
        skill = int(comboboxSkill.get_active_id())

        # Intensity
        if radiobuttonIntensityLow.get_active():
            intensity = 0
        elif radiobuttonIntensityMedium.get_active():
            intensity = 1
        else:
            intensity = 2

        training = (playerid, coach, skill, intensity)

    dialog.destroy()

    return training


def remove_individual_training(playerid):
    player = game.players[playerid]
    name = display.name(player, mode=1)

    messagedialog = Gtk.MessageDialog(type=Gtk.MessageType.QUESTION)
    messagedialog.set_title("Individual Training")
    messagedialog.set_transient_for(game.window)
    messagedialog.add_button("_Cancel", Gtk.ResponseType.CANCEL)
    messagedialog.add_button("_Remove", Gtk.ResponseType.OK)
    messagedialog.set_default_response(Gtk.ResponseType.CANCEL)
    messagedialog.set_markup("Remove %s from individual training?" % (name))

    state = False

    if messagedialog.run() == Gtk.ResponseType.OK:
        training = game.clubs[game.teamid].individual_training
        del(training[playerid])

        state = True

    messagedialog.destroy()

    return state


def withdraw_transfer(negotiationid):
    playerid = game.negotiations[negotiationid].playerid
    player = game.players[playerid]
    name = display.name(player, mode=1)

    messagedialog = Gtk.MessageDialog(type=Gtk.MessageType.QUESTION)
    messagedialog.set_transient_for(game.window)
    messagedialog.set_title("Withdraw Transfer Offer")
    messagedialog.add_button("_Cancel", Gtk.ResponseType.CANCEL)
    messagedialog.add_button("_Withdraw", Gtk.ResponseType.OK)
    messagedialog.set_default_response(Gtk.ResponseType.CANCEL)
    messagedialog.set_markup("Withdraw transfer offer for %s?" % (name))

    state = False

    if messagedialog.run() == Gtk.ResponseType.OK:
        state = True

    messagedialog.destroy()

    return state


def remove_from_shortlist(playerid):
    player = game.players[playerid]
    name = display.name(player, mode=1)

    messagedialog = Gtk.MessageDialog(type=Gtk.MessageType.QUESTION)
    messagedialog.set_title("Cancel Transfer")
    messagedialog.set_transient_for(game.window)
    messagedialog.add_button("_Cancel", Gtk.ResponseType.CANCEL)
    messagedialog.add_button("_Remove", Gtk.ResponseType.OK)
    messagedialog.set_default_response(Gtk.ResponseType.CANCEL)
    messagedialog.set_markup("Remove %s from shortlist?" % (name))

    state = False

    if messagedialog.run() == Gtk.ResponseType.OK:
        state = True

    messagedialog.destroy()

    return state


def confirm_stadium(cost):
    cost = display.currency(cost)

    messagedialog = Gtk.MessageDialog(type=Gtk.MessageType.QUESTION)
    messagedialog.set_transient_for(game.window)
    messagedialog.set_title("Upgrade Stadium")
    messagedialog.add_button("_Cancel", Gtk.ResponseType.CANCEL)
    messagedialog.add_button("_Build", Gtk.ResponseType.OK)
    messagedialog.set_default_response(Gtk.ResponseType.CANCEL)
    messagedialog.set_markup("Begin the construction of upgrades to the stadium at cost of %s?" % (cost))

    state = False

    if messagedialog.run() == Gtk.ResponseType.OK:
        state = True

    messagedialog.destroy()

    return state


def confirm_building(cost):
    cost = display.currency(cost)

    messagedialog = Gtk.MessageDialog(type=Gtk.MessageType.QUESTION)
    messagedialog.set_transient_for(game.window)
    messagedialog.set_title("Upgrade Building")
    messagedialog.add_button("_Cancel", Gtk.ResponseType.CANCEL)
    messagedialog.add_button("_Build", Gtk.ResponseType.OK)
    messagedialog.set_default_response(Gtk.ResponseType.CANCEL)
    messagedialog.set_markup("Begin the construction of new buildings at a cost of %s?" % (cost))

    state = False

    if messagedialog.run() == Gtk.ResponseType.OK:
        state = True

    messagedialog.destroy()

    return state


def confirm_training(cost):
    display_cost = display.currency(cost)

    messagedialog = Gtk.MessageDialog(type=Gtk.MessageType.QUESTION)
    messagedialog.set_transient_for(game.window)
    messagedialog.set_title("Confirm Training")
    messagedialog.add_button("_Cancel", Gtk.ResponseType.CANCEL)
    messagedialog.add_button("C_onfirm", Gtk.ResponseType.OK)
    messagedialog.set_default_response(Gtk.ResponseType.CANCEL)
    messagedialog.set_markup("Arrange for trip to training camp at a cost of %s?" % (display_cost))

    state = False

    if messagedialog.run() == Gtk.ResponseType.OK:
        state = True

    messagedialog.destroy()

    return state


def hire_staff(index, name):
    staff_type = {0: "Coach", 1: "Scout"}

    messagedialog = Gtk.MessageDialog(type=Gtk.MessageType.QUESTION)
    messagedialog.set_transient_for(game.window)
    messagedialog.set_title("Hire %s" % (staff_type[index]))
    messagedialog.add_button("_Cancel", Gtk.ResponseType.CANCEL)
    messagedialog.add_button("_Hire", Gtk.ResponseType.YES)
    messagedialog.set_default_response(Gtk.ResponseType.CANCEL)
    messagedialog.set_markup("Hire %s %s?" % (staff_type[index], name))

    state = False

    if messagedialog.run() == Gtk.ResponseType.YES:
        state = True

    messagedialog.destroy()

    return state


def fire_staff(index, name, payout):
    staff_type = {0: "Coach", 1: "Scout"}

    payout = display.currency(payout)

    messagedialog = Gtk.MessageDialog(type=Gtk.MessageType.QUESTION)
    messagedialog.set_transient_for(game.window)
    messagedialog.set_title("Fire %s" % staff_type[index])
    messagedialog.add_button("_Cancel", Gtk.ResponseType.CANCEL)
    messagedialog.add_button("_Fire", Gtk.ResponseType.YES)
    messagedialog.set_default_response(Gtk.ResponseType.CANCEL)
    messagedialog.set_markup("Fire %s %s at a cost of %s?" % (staff_type[index], name, payout))

    state = False

    if messagedialog.run() == Gtk.ResponseType.YES:
        state = True

    messagedialog.destroy()

    return state


def fire_staff_error(name, number):
    messagedialog = Gtk.MessageDialog(type=Gtk.MessageType.ERROR)
    messagedialog.set_title("Fire Staff")
    messagedialog.set_transient_for(game.window)
    messagedialog.add_button("_Close", Gtk.ResponseType.CLOSE)
    messagedialog.set_markup("Unable to fire %s as he is currently individual training %i players. Please reassign the players to other coaches and try again." % (name, number))
    messagedialog.run()
    messagedialog.destroy()


def renew_staff_contract(name, year, amount):
    amount = display.currency(amount)

    messagedialog = Gtk.MessageDialog(type=Gtk.MessageType.QUESTION)
    messagedialog.set_transient_for(game.window)
    messagedialog.set_title("Renew Contract")
    messagedialog.add_button("_Reject", Gtk.ResponseType.REJECT)
    messagedialog.add_button("_Accept", Gtk.ResponseType.ACCEPT)
    messagedialog.set_default_response(Gtk.ResponseType.REJECT)
    messagedialog.set_markup("%s is requesting a %i year contract and %s per week." % (name, year, amount))

    state = False

    if messagedialog.run() == Gtk.ResponseType.ACCEPT:
        state = True

    messagedialog.destroy()

    return state


def renew_staff_contract_error(staff):
    messagedialog = Gtk.MessageDialog(type=Gtk.MessageType.ERROR)
    messagedialog.set_transient_for(game.window)
    messagedialog.set_title("Renew Contract")
    messagedialog.add_button("_Close", Gtk.ResponseType.CLOSE)
    messagedialog.set_markup("%s has decided to retire once his current contract expires, and will not negotiate an extension." % (staff.name))

    messagedialog.run()
    messagedialog.destroy()


def improve_wage(name, amount):
    amount = display.currency(amount)

    messagedialog = Gtk.MessageDialog(type=Gtk.MessageType.QUESTION)
    messagedialog.set_transient_for(game.window)
    messagedialog.set_title("Improve Wage")
    messagedialog.add_button("_Reject", Gtk.ResponseType.REJECT)
    messagedialog.add_button("_Accept", Gtk.ResponseType.ACCEPT)
    messagedialog.set_default_response(Gtk.ResponseType.REJECT)
    messagedialog.set_markup("Increase wages for %s to %s per week?" % (name, amount))

    state = False

    if messagedialog.run() == Gtk.ResponseType.ACCEPT:
        state = True

    messagedialog.destroy()

    return state


def cancel_loan(name):
    messagedialog = Gtk.MessageDialog(type=Gtk.MessageType.QUESTION)
    messagedialog.set_transient_for(game.window)
    messagedialog.set_title("Cancel Loan")
    messagedialog.add_button("_Do Not Cancel", Gtk.ResponseType.REJECT)
    messagedialog.add_button("_Cancel Loan", Gtk.ResponseType.ACCEPT)
    messagedialog.set_default_response(Gtk.ResponseType.REJECT)
    messagedialog.set_markup("<span size='12000'><b>Cancel loan contract for %s?</b></span>" % (name))
    messagedialog.format_secondary_text("The player will be returned to his parent club.")

    state = False

    if messagedialog.run() == Gtk.ResponseType.ACCEPT:
        state = True

    messagedialog.destroy()

    return state


def player_filter():
    def value_changed(spinbutton):
        minimum = spinbuttonMinValue.get_value_as_int()
        spinbuttonMaxValue.set_range(minimum, 100000000)

    dialog = Gtk.Dialog()
    dialog.set_title("Filter Players")
    dialog.add_button("_Cancel", Gtk.ResponseType.CANCEL)
    dialog.add_button("_Filter", Gtk.ResponseType.OK)
    dialog.set_default_response(Gtk.ResponseType.OK)
    dialog.set_transient_for(game.window)
    dialog.set_border_width(5)
    dialog.vbox.set_spacing(5)

    checkbuttonShowOwnPlayers = Gtk.CheckButton("Display %s players in player search" % (game.clubs[game.teamid].name))
    checkbuttonShowOwnPlayers.set_active(game.player_filter[0])
    dialog.vbox.add(checkbuttonShowOwnPlayers)

    commonframe = widgets.CommonFrame(title="Personal")
    dialog.vbox.add(commonframe)

    grid = Gtk.Grid()
    grid.set_row_spacing(5)
    grid.set_column_spacing(5)
    commonframe.insert(grid)

    label = widgets.AlignedLabel("Position")
    grid.attach(label, 0, 1, 1, 1)
    comboboxPosition = Gtk.ComboBoxText()
    comboboxPosition.append("0", "All")
    comboboxPosition.append("1", "Goalkeeper")
    comboboxPosition.append("2", "Defender")
    comboboxPosition.append("3", "Midfielder")
    comboboxPosition.append("4", "Attacker")
    comboboxPosition.set_active(game.player_filter[1])
    grid.attach(comboboxPosition, 1, 1, 1, 1)

    label = widgets.AlignedLabel("Value")
    grid.attach(label, 0, 2, 1, 1)
    spinbuttonMinValue = Gtk.SpinButton.new_with_range(0, 100000000, 100000)
    spinbuttonMinValue.set_snap_to_ticks(True)
    spinbuttonMinValue.set_value(game.player_filter[2][0])
    spinbuttonMinValue.connect("value-changed", value_changed)
    grid.attach(spinbuttonMinValue, 1, 2, 1, 1)
    spinbuttonMaxValue = Gtk.SpinButton.new_with_range(0, 100000000, 100000)
    spinbuttonMaxValue.set_value(game.player_filter[2][1])
    spinbuttonMaxValue.set_snap_to_ticks(True)
    spinbuttonMaxValue.connect("value-changed", value_changed)
    grid.attach(spinbuttonMaxValue, 2, 2, 1, 1)

    label = widgets.AlignedLabel("Age")
    grid.attach(label, 0, 3, 1, 1)
    spinbuttonMinAge = Gtk.SpinButton.new_with_range(16, 50, 1)
    spinbuttonMinAge.set_value(game.player_filter[3][0])
    grid.attach(spinbuttonMinAge, 1, 3, 1, 1)
    spinbuttonMaxAge = Gtk.SpinButton.new_with_range(16, 50, 1)
    spinbuttonMaxAge.set_value(game.player_filter[3][1])
    grid.attach(spinbuttonMaxAge, 2, 3, 1, 1)

    label = widgets.AlignedLabel("Status")
    grid.attach(label, 0, 4, 1, 1)
    comboboxStatus = Gtk.ComboBoxText()
    comboboxStatus.append("0", "All Players")
    comboboxStatus.append("1", "Transfer Listed")
    comboboxStatus.append("2", "Loan Listed")
    comboboxStatus.append("3", "Out of Contract")
    comboboxStatus.append("4", "One Year or Less Remaining on Contract")
    comboboxStatus.set_active(game.player_filter[4])
    grid.attach(comboboxStatus, 1, 4, 3, 1)

    commonframe = widgets.CommonFrame(title="Skills")
    dialog.vbox.add(commonframe)

    grid = Gtk.Grid()
    grid.set_row_spacing(5)
    grid.set_column_spacing(5)
    commonframe.insert(grid)

    label = widgets.AlignedLabel("Keeping")
    grid.attach(label, 0, 0, 1, 1)
    spinbuttonKPMin = Gtk.SpinButton.new_with_range(0, 99, 1)
    spinbuttonKPMin.set_value(game.player_filter[5][0])
    grid.attach(spinbuttonKPMin, 1, 0, 1, 1)
    spinbuttonKPMax = Gtk.SpinButton.new_with_range(0, 99, 1)
    spinbuttonKPMax.set_value(game.player_filter[5][1])
    grid.attach(spinbuttonKPMax, 2, 0, 1, 1)
    label = widgets.AlignedLabel("Tackling")
    grid.attach(label, 0, 1, 1, 1)
    spinbuttonTKMin = Gtk.SpinButton.new_with_range(0, 99, 1)
    spinbuttonTKMin.set_value(game.player_filter[6][0])
    grid.attach(spinbuttonTKMin, 1, 1, 1, 1)
    spinbuttonTKMax = Gtk.SpinButton.new_with_range(0, 99, 1)
    spinbuttonTKMax.set_value(game.player_filter[6][1])
    grid.attach(spinbuttonTKMax, 2, 1, 1, 1)
    label = widgets.AlignedLabel("Passing")
    grid.attach(label, 0, 2, 1, 1)
    spinbuttonPSMin = Gtk.SpinButton.new_with_range(0, 99, 1)
    spinbuttonPSMin.set_value(game.player_filter[7][0])
    grid.attach(spinbuttonPSMin, 1, 2, 1, 1)
    spinbuttonPSMax = Gtk.SpinButton.new_with_range(0, 99, 1)
    spinbuttonPSMax.set_value(game.player_filter[7][1])
    grid.attach(spinbuttonPSMax, 2, 2, 1, 1)
    label = widgets.AlignedLabel("Shooting")
    grid.attach(label, 4, 0, 1, 1)
    spinbuttonSHMin = Gtk.SpinButton.new_with_range(0, 99, 1)
    spinbuttonSHMin.set_value(game.player_filter[8][0])
    grid.attach(spinbuttonSHMin, 5, 0, 1, 1)
    spinbuttonSHMax = Gtk.SpinButton.new_with_range(0, 99, 1)
    spinbuttonSHMax.set_value(game.player_filter[8][1])
    grid.attach(spinbuttonSHMax, 6, 0, 1, 1)
    label = widgets.AlignedLabel("Heading")
    grid.attach(label, 4, 1, 1, 1)
    spinbuttonHDMin = Gtk.SpinButton.new_with_range(0, 99, 1)
    spinbuttonHDMin.set_value(game.player_filter[9][0])
    grid.attach(spinbuttonHDMin, 5, 1, 1, 1)
    spinbuttonHDMax = Gtk.SpinButton.new_with_range(0, 99, 1)
    spinbuttonHDMax.set_value(game.player_filter[9][1])
    grid.attach(spinbuttonHDMax, 6, 1, 1, 1)
    label = widgets.AlignedLabel("Pace")
    grid.attach(label, 4, 2, 1, 1)
    spinbuttonPCMin = Gtk.SpinButton.new_with_range(0, 99, 1)
    spinbuttonPCMin.set_value(game.player_filter[10][0])
    grid.attach(spinbuttonPCMin, 5, 2, 1, 1)
    spinbuttonPCMax = Gtk.SpinButton.new_with_range(0, 99, 1)
    spinbuttonPCMax.set_value(game.player_filter[10][1])
    grid.attach(spinbuttonPCMax, 6, 2, 1, 1)
    label = widgets.AlignedLabel("Stamina")
    grid.attach(label, 8, 0, 1, 1)
    spinbuttonSTMin = Gtk.SpinButton.new_with_range(0, 99, 1)
    spinbuttonSTMin.set_value(game.player_filter[11][0])
    grid.attach(spinbuttonSTMin, 9, 0, 1, 1)
    spinbuttonSTMax = Gtk.SpinButton.new_with_range(0, 99, 1)
    spinbuttonSTMax.set_value(game.player_filter[11][1])
    grid.attach(spinbuttonSTMax, 10, 0, 1, 1)
    label = widgets.AlignedLabel("Ball Control")
    grid.attach(label, 8, 1, 1, 1)
    spinbuttonBCMin = Gtk.SpinButton.new_with_range(0, 99, 1)
    spinbuttonBCMin.set_value(game.player_filter[12][0])
    grid.attach(spinbuttonBCMin, 9, 1, 1, 1)
    spinbuttonBCMax = Gtk.SpinButton.new_with_range(0, 99, 1)
    spinbuttonBCMax.set_value(game.player_filter[12][1])
    grid.attach(spinbuttonBCMax, 10, 1, 1, 1)
    label = widgets.AlignedLabel("Set Pieces")
    grid.attach(label, 8, 2, 1, 1)
    spinbuttonSPMin = Gtk.SpinButton.new_with_range(0, 99, 1)
    spinbuttonSPMin.set_value(game.player_filter[13][0])
    grid.attach(spinbuttonSPMin, 9, 2, 1, 1)
    spinbuttonSPMax = Gtk.SpinButton.new_with_range(0, 99, 1)
    spinbuttonSPMax.set_value(game.player_filter[13][1])
    grid.attach(spinbuttonSPMax, 10, 2, 1, 1)

    separator = Gtk.Separator()
    separator.set_orientation(Gtk.Orientation.VERTICAL)
    grid.attach(separator, 3, 0, 1, 3)
    separator = Gtk.Separator()
    separator.set_orientation(Gtk.Orientation.VERTICAL)
    grid.attach(separator, 7, 0, 1, 3)

    dialog.show_all()

    if dialog.run() == Gtk.ResponseType.OK:
        display_own_players = checkbuttonShowOwnPlayers.get_active()
        position = int(comboboxPosition.get_active())
        value_min = spinbuttonMinValue.get_value_as_int()
        value_max = spinbuttonMaxValue.get_value_as_int()
        age_min = spinbuttonMinAge.get_value_as_int()
        age_max = spinbuttonMaxAge.get_value_as_int()
        status = int(comboboxStatus.get_active())

        keeping = (spinbuttonKPMin.get_value_as_int(),
                   spinbuttonKPMax.get_value_as_int())
        tackling = (spinbuttonTKMin.get_value_as_int(),
                    spinbuttonTKMax.get_value_as_int())
        passing = (spinbuttonPSMin.get_value_as_int(),
                   spinbuttonPSMax.get_value_as_int())
        shooting = (spinbuttonSHMin.get_value_as_int(),
                    spinbuttonSHMax.get_value_as_int())
        heading = (spinbuttonHDMin.get_value_as_int(),
                   spinbuttonHDMax.get_value_as_int())
        pace = (spinbuttonPCMin.get_value_as_int(),
                spinbuttonPCMax.get_value_as_int())
        stamina = (spinbuttonSTMin.get_value_as_int(),
                   spinbuttonSTMax.get_value_as_int())
        ballcontrol = (spinbuttonBCMin.get_value_as_int(),
                       spinbuttonBCMax.get_value_as_int())
        setpieces = (spinbuttonSPMin.get_value_as_int(),
                     spinbuttonSPMax.get_value_as_int())

        game.player_filter = (display_own_players,
                              position,
                              (value_min, value_max),
                              (age_min, age_max),
                              status,
                              keeping,
                              tackling,
                              passing,
                              shooting,
                              heading,
                              pace,
                              stamina,
                              ballcontrol,
                              setpieces,)

    dialog.destroy()


def squad_filter():
    dialog = Gtk.Dialog()
    dialog.set_transient_for(game.window)
    dialog.set_title("Filter Squad")
    dialog.add_button("_Cancel", Gtk.ResponseType.CANCEL)
    dialog.add_button("_Filter", Gtk.ResponseType.OK)
    dialog.set_default_response(Gtk.ResponseType.OK)
    dialog.set_border_width(5)

    grid = Gtk.Grid()
    grid.set_row_spacing(5)
    grid.set_column_spacing(5)
    dialog.vbox.add(grid)

    label = widgets.AlignedLabel("Position")
    grid.attach(label, 0, 0, 1, 1)
    comboboxPosition = Gtk.ComboBoxText()
    comboboxPosition.append("0", "All")
    comboboxPosition.append("1", "Goalkeeper")
    comboboxPosition.append("2", "Defender")
    comboboxPosition.append("3", "Midfielder")
    comboboxPosition.append("4", "Attacker")
    comboboxPosition.set_active(game.squad_filter[0])
    grid.attach(comboboxPosition, 1, 0, 1, 1)

    checkbuttonAvailable = Gtk.CheckButton("Show Only Available Players")
    checkbuttonAvailable.set_tooltip_text("Injured or suspended players will not be displayed")
    checkbuttonAvailable.set_active(game.squad_filter[1])
    grid.attach(checkbuttonAvailable, 0, 1, 3, 1)

    dialog.show_all()

    if dialog.run() == Gtk.ResponseType.OK:
        position = int(comboboxPosition.get_active())
        available = checkbuttonAvailable.get_active()

        game.squad_filter = (position, available)

    dialog.destroy()


def sponsorship():
    club = game.clubs[game.teamid]

    status = club.sponsor_status
    company, period, cost = club.sponsor_offer

    display_cost = display.currency(cost)

    message = ("There are currently no club sponsorship offers.",
               "%s have made a %s year offer worth %s." % (company, period, display_cost),
               "The deal with %s runs for another %s years." % (company, period))

    text = message[status]

    messagedialog = Gtk.MessageDialog()
    messagedialog.set_title("Sponsorship")
    messagedialog.set_transient_for(game.window)
    messagedialog.set_markup(message[status])

    if status == 1:
        messagedialog.add_button("_Reject", Gtk.ResponseType.REJECT)
        messagedialog.add_button("_Accept", Gtk.ResponseType.ACCEPT)
        messagedialog.set_default_response(Gtk.ResponseType.ACCEPT)
    else:
        messagedialog.add_button("_Close", Gtk.ResponseType.CLOSE)
        messagedialog.set_default_response(Gtk.ResponseType.CLOSE)

    response = messagedialog.run()

    if response == Gtk.ResponseType.ACCEPT:
        company, period, cost = club.sponsor_offer
        club.sponsor_status = 2
        money.deposit(cost, 1)
    elif response == Gtk.ResponseType.REJECT:
        club.sponsor_status = 0
        game.sponsor_timeout = random.randint(4, 6)

    messagedialog.destroy()


def float_club(amount):
    amount = display.currency(amount)

    messagedialog = Gtk.MessageDialog(type=Gtk.MessageType.QUESTION)
    messagedialog.set_title("Float Club")
    messagedialog.set_transient_for(game.window)
    messagedialog.add_button("_No", Gtk.ResponseType.NO)
    messagedialog.add_button("_Yes", Gtk.ResponseType.YES)
    messagedialog.set_default_response(Gtk.ResponseType.NO)
    messagedialog.set_markup("<span size='12000'><b>Are you sure you want to float the club publically?</b></span>")
    messagedialog.format_secondary_text("The amount raised will be in the region of %s." % (amount))

    state = False

    if messagedialog.run() == Gtk.ResponseType.YES:
        state = True

    messagedialog.destroy()

    return state


def comparison():
    dialog = Gtk.Dialog()
    dialog.set_transient_for(game.window)
    dialog.set_border_width(5)
    dialog.set_title("Player Comparison")
    dialog.add_button("_Close", Gtk.ResponseType.CLOSE)
    dialog.set_default_response(Gtk.ResponseType.CLOSE)

    grid = Gtk.Grid()
    grid.set_row_spacing(5)
    grid.set_column_spacing(10)
    dialog.vbox.add(grid)

    player1 = game.players[game.comparison[0]]
    skills1 = (player1.keeping,
               player1.tackling,
               player1.passing,
               player1.shooting,
               player1.heading,
               player1.pace,
               player1.stamina,
               player1.ball_control,
               player1.set_pieces)
    player2 = game.players[game.comparison[1]]
    skills2 = (player2.keeping,
               player2.tackling,
               player2.passing,
               player2.shooting,
               player2.heading,
               player2.pace,
               player2.stamina,
               player2.ball_control,
               player2.set_pieces)

    for count, title in enumerate(("Name",
                                   "Age",
                                   "Position",
                                   "Keeping",
                                   "Tackling",
                                   "Passing",
                                   "Shooting",
                                   "Heading",
                                   "Pace",
                                   "Stamina",
                                   "Ball Control",
                                   "Set Pieces")):
        label = Gtk.Label("<b>%s</b>" % (title))
        label.set_use_markup(True)
        grid.attach(label, count, 0, 1, 1)

    name = display.name(player1)
    label = widgets.AlignedLabel("%s" % (name))
    grid.attach(label, 0, 1, 1, 1)
    name = display.name(player2)
    label = widgets.AlignedLabel("%s" % (name))
    grid.attach(label, 0, 2, 1, 1)

    label = Gtk.Label("%i" % (player1.age))
    grid.attach(label, 1, 1, 1, 1)
    label = Gtk.Label("%i" % (player2.age))
    grid.attach(label, 1, 2, 1, 1)

    label = Gtk.Label("%s" % (player1.position))
    grid.attach(label, 2, 1, 1, 1)
    label = Gtk.Label("%s" % (player2.position))
    grid.attach(label, 2, 2, 1, 1)

    for count in range(0, 9):
        label1 = Gtk.Label()
        label1.set_use_markup(True)
        label2 = Gtk.Label()
        label2.set_use_markup(True)

        if skills1[count] > skills2[count]:
            label1.set_markup("<b>%i</b>" % skills1[count])
            label2.set_markup("%i" % skills2[count])
        elif skills1[count] < skills2[count]:
            label1.set_markup("%i" % skills1[count])
            label2.set_markup("<b>%i</b>" % skills2[count])
        else:
            label1.set_markup("%i" % skills1[count])
            label2.set_markup("%i" % skills2[count])

        grid.attach(label1, count + 3, 1, 1, 1)
        grid.attach(label2, count + 3, 2, 1, 1)

    dialog.show_all()
    dialog.run()
    dialog.destroy()


def end_of_season():
    dialog = Gtk.Dialog()
    dialog.set_transient_for(game.window)
    dialog.set_title("End of Season")
    dialog.set_border_width(5)
    dialog.add_button("_Close", Gtk.ResponseType.OK)
    dialog.set_default_response(Gtk.ResponseType.OK)

    grid = Gtk.Grid()
    grid.set_row_spacing(5)
    grid.set_column_spacing(5)
    dialog.vbox.add(grid)

    clubid = display.find_champion()
    champion = game.clubs[clubid].name

    label = widgets.AlignedLabel("League Champion")
    grid.attach(label, 0, 0, 1, 1)
    label = widgets.AlignedLabel()
    label.set_markup("<span size='16000' weight='bold'>%s</span>" % (champion))
    grid.attach(label, 1, 0, 1, 1)

    top = display.top_scorer()
    player = game.players[top[0]]
    name = display.name(player, mode=1)
    goals = top[1]

    label = widgets.AlignedLabel("Top Goalscorer")
    grid.attach(label, 0, 1, 1, 1)
    label = widgets.AlignedLabel()
    label.set_markup("<span size='16000' weight='bold'>%s (%i)</span>" % (name, goals))
    grid.attach(label, 1, 1, 1, 1)

    top = display.top_assister()
    player = game.players[top[0]]
    name = display.name(player, mode=1)
    assists = top[1]

    label = widgets.AlignedLabel("Top Assister")
    grid.attach(label, 0, 2, 1, 1)
    label = widgets.AlignedLabel()
    label.set_markup("<span size='16000' weight='bold'>%s (%i)</span>" % (name, assists))
    grid.attach(label, 1, 2, 1, 1)

    top = display.player_of_the_season()
    player = game.players[top[0]]
    name = display.name(player, mode=1)

    label = widgets.AlignedLabel("Player of the Season")
    grid.attach(label, 0, 3, 1, 1)
    label = widgets.AlignedLabel()
    label.set_markup("<span size='16000' weight='bold'>%s</span>" % (name))
    grid.attach(label, 1, 3, 1, 1)

    dialog.show_all()
    dialog.run()
    dialog.destroy()


class NameChange(Gtk.Dialog):
    def __init__(self):
        self.state = False

        Gtk.Dialog.__init__(self)
        self.set_title("Manager Name")
        self.set_transient_for(game.window)
        self.set_border_width(5)
        self.set_resizable(False)
        self.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("_Apply", Gtk.ResponseType.APPLY)
        self.set_default_response(Gtk.ResponseType.APPLY)
        self.connect("response", self.response_handler)

        grid = Gtk.Grid()
        grid.set_column_spacing(5)
        self.vbox.add(grid)

        label = widgets.Label("Change Your Manager _Name:")
        grid.attach(label, 0, 0, 1, 1)

        self.liststoreName = Gtk.ListStore(str)

        combobox = Gtk.ComboBoxText.new_with_entry()
        combobox.set_model(self.liststoreName)
        self.entry = combobox.get_child()
        self.entry.set_text(game.clubs[game.teamid].manager)
        label.set_mnemonic_widget(combobox)
        grid.attach(combobox, 1, 0, 1, 1)

    def display(self):
        for name in fileio.read_names():
            self.liststoreName.append([name])

        self.show_all()
        self.run()

        return self.state

    def response_handler(self, dialog, response):
        if response == Gtk.ResponseType.APPLY:
            name = self.entry.get_text()

            game.clubs[game.teamid].manager = name
            fileio.write_names(name, "a")

            add = True

            for count, item in enumerate(self.liststoreName):
                if item[0] == game.clubs[game.teamid].manager:
                    add = False

                    del(self.liststoreName[count])
                    self.liststoreName.prepend([game.clubs[game.teamid].manager])

            if add:
                self.liststoreName.prepend([game.clubs[game.teamid].manager])

            names = [key[0] for key in self.liststoreName]
            fileio.write_names(names)

            self.state = True

        self.destroy()


def file_not_found_error():
    messagedialog = Gtk.MessageDialog()
    messagedialog.set_transient_for(game.window)
    messagedialog.set_title("Editor Not Available")
    messagedialog.add_button("_Close", Gtk.ResponseType.CLOSE)
    messagedialog.set_markup("<span size='12000'><b>Data Editor is not installed.</b></span>")
    messagedialog.format_secondary_text("Place the editor folder into this directory.")
    messagedialog.run()
    messagedialog.destroy()


def error(errorid):
    error = constants.errors[errorid]
    message_text = error[0]
    message_title = error[1]
    message_type = error[2]

    messagedialog = Gtk.MessageDialog(type=message_type)
    messagedialog.set_transient_for(game.window)
    messagedialog.set_title(message_title)
    messagedialog.add_button("_Close", Gtk.ResponseType.CLOSE)
    messagedialog.set_default_response(Gtk.ResponseType.CLOSE)
    messagedialog.set_markup(message_text)
    messagedialog.run()
    messagedialog.destroy()


class Opposition(Gtk.Dialog):
    def __init__(self):
        Gtk.Dialog.__init__(self)
        self.set_transient_for(game.window)
        self.set_border_width(5)
        self.set_default_size(200, 350)
        self.set_title("View Opposition")
        self.add_button("_Close", Gtk.ResponseType.CLOSE)
        self.connect("response", self.response_handler)

        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)
        self.vbox.add(grid)

        grid2 = Gtk.Grid()
        grid2.set_column_spacing(5)
        grid.attach(grid2, 0, 0, 1, 1)

        self.liststoreClubs = Gtk.ListStore(str, str)
        treemodelsort = Gtk.TreeModelSort(self.liststoreClubs)
        treemodelsort.set_sort_column_id(1, Gtk.SortType.ASCENDING)

        label = widgets.Label("Opposition")
        grid2.attach(label, 0, 0, 1, 1)
        cellrenderertext = Gtk.CellRendererText()
        self.combobox = Gtk.ComboBox()
        self.combobox.set_model(treemodelsort)
        self.combobox.set_id_column(0)
        self.combobox.connect("changed", self.combobox_changed)
        self.combobox.pack_start(cellrenderertext, True)
        self.combobox.add_attribute(cellrenderertext, "text", 1)
        grid2.attach(self.combobox, 1, 0, 1, 1)

        commonframe = widgets.CommonFrame("Details")
        grid.attach(commonframe, 0, 1, 1, 1)

        grid1 = Gtk.Grid()
        grid1.set_row_spacing(5)
        grid1.set_column_spacing(5)
        commonframe.insert(grid1)

        label = widgets.AlignedLabel("Name")
        grid1.attach(label, 0, 0, 1, 1)
        self.labelName = widgets.AlignedLabel()
        grid1.attach(self.labelName, 1, 0, 1, 1)

        label = widgets.AlignedLabel("Position")
        grid1.attach(label, 0, 1, 1, 1)
        self.labelPosition = widgets.AlignedLabel()
        grid1.attach(self.labelPosition, 1, 1, 1, 1)

        label = widgets.AlignedLabel("Form")
        grid1.attach(label, 0, 2, 1, 1)
        self.labelForm = widgets.AlignedLabel()
        grid1.attach(self.labelForm, 1, 2, 1, 1)

        commonframe = widgets.CommonFrame("Squad")
        grid.attach(commonframe, 1, 1, 2, 2)

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        commonframe.insert(scrolledwindow)

        self.liststoreSquad = Gtk.ListStore(str)
        treemodelsort = Gtk.TreeModelSort(self.liststoreSquad)
        treemodelsort.set_sort_column_id(0, Gtk.SortType.ASCENDING)

        treeview = Gtk.TreeView()
        treeview.set_vexpand(True)
        treeview.set_hexpand(True)
        treeview.set_headers_visible(False)
        treeview.set_model(treemodelsort)
        treeview.set_enable_search(False)
        treeview.set_search_column(-1)
        treeselection = treeview.get_selection()
        treeselection.set_mode(Gtk.SelectionMode.NONE)
        cellrenderertext = Gtk.CellRendererText()
        treeviewcolumn = Gtk.TreeViewColumn(None,
                                            cellrenderertext,
                                            text=0)
        treeview.append_column(treeviewcolumn)
        scrolledwindow.add(treeview)

    def display(self):
        self.liststoreClubs.clear()

        for clubid, club in game.clubs.items():
            if clubid != game.teamid:
                self.liststoreClubs.append([str(clubid), club.name])

        self.combobox.set_active(0)

        self.show_all()
        self.run()

    def combobox_changed(self, combobox):
        club = int(combobox.get_active_id())

        self.update_data(club)

    def update_data(self, clubid):
        club = game.clubs[clubid]

        position = display.find_position(clubid)

        self.labelName.set_label(club.name)
        self.labelPosition.set_label(position)
        self.labelForm.set_label("".join(club.form))

        self.liststoreSquad.clear()

        for playerid in club.squad:
            player = game.players[playerid]
            name = display.name(player)
            self.liststoreSquad.append([name])

    def response_handler(self, dialog, response):
        self.destroy()
