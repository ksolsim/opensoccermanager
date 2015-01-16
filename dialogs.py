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
import music
import preferences
import version
import view
import widgets


prefs = preferences.Preferences()


def exit_game(leave=False):
    '''
    Leave allows this function to be used when simply restarting the
    game from the main menu. When set to True, the game will never exit
    but will prompt to save and then return to the main menu.
    '''
    messagedialog = Gtk.MessageDialog(type=Gtk.MessageType.QUESTION)
    messagedialog.set_transient_for(game.window)
    messagedialog.set_title("Exit Game")
    messagedialog.set_markup("The game has not been saved.")
    messagedialog.format_secondary_text("Do you want to save before closing?")
    messagedialog.add_button("_Cancel", Gtk.ResponseType.CANCEL)
    messagedialog.add_button("_Do Not Save", Gtk.ResponseType.REJECT)
    messagedialog.add_button("_Save", Gtk.ResponseType.ACCEPT)
    messagedialog.set_default_response(Gtk.ResponseType.ACCEPT)

    response = messagedialog.run()

    state = True

    if response == Gtk.ResponseType.REJECT:
        if not leave:
            Gtk.main_quit()
    elif response == Gtk.ResponseType.ACCEPT:
        state = file_dialog(1)
    else:
        state = not state

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


def file_dialog(mode):
    if mode == 0:
        title = "Open File"
        action = "_Open"
        mode = Gtk.FileChooserAction.OPEN
    elif mode == 1:
        title = "Save File"
        action = "_Save"
        mode = Gtk.FileChooserAction.SAVE

    filefilter = Gtk.FileFilter()
    filefilter.set_name("Saved Game")
    filefilter.add_pattern("*.osm")

    dialog = Gtk.FileChooserDialog()
    dialog.set_transient_for(game.window)
    dialog.set_title(title)
    dialog.add_button("_Cancel", Gtk.ResponseType.CANCEL)
    dialog.add_button(action, Gtk.ResponseType.OK)
    dialog.add_filter(filefilter)
    dialog.set_action(mode)
    dialog.set_do_overwrite_confirmation(True)
    dialog.set_current_folder(game.save_location)

    response = dialog.run()

    state = False

    if response == Gtk.ResponseType.OK:
        filename = dialog.get_filename()

        if mode == 0:
            fileio.open_file(filename)
        elif mode == 1:
            if not filename.endswith(".osm"):
                filename = "%s.osm" % (filename)

            fileio.save_file(filename)

        state = True

    dialog.destroy()

    return state


def delete_dialog():
    def load_directory(filechooserbutton=None, location=None):
        liststore.clear()

        if filechooserbutton is not None:
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
    load_directory(location=game.save_location)

    treeview = Gtk.TreeView()
    treeselection = treeview.get_selection()
    treeselection.set_mode(Gtk.SelectionMode.MULTIPLE)
    treeselection.connect("changed", selection_changed)
    treeview.set_vexpand(True)
    treeview.set_model(liststore)
    treeview.set_headers_visible(False)
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
            prefs["AUDIO"]["PlayMusic"] = "True"
        elif game.music:
            game.player.stop()
            game.music = False
            prefs["AUDIO"]["PlayMusic"] = "False"

        prefs.writefile()

    def change_currency(combobox):
        game.currency = combobox.get_active_id()

        prefs["INTERFACE"]["Currency"] = game.currency
        prefs.writefile()

        game.currency = int(game.currency)

    def change_screen(combobox):
        game.start_screen = combobox.get_active_id()

        prefs["INTERFACE"]["StartScreen"] = game.start_screen
        prefs.writefile()

        game.start_screen = int(game.start_screen)

    def change_save_location(filechooserbutton):
        directory = filechooserbutton.get_uri()

        prefs["SAVE"]["Saves"] = game.save_location
        prefs.writefile()

        game.save_location = directory[7:]

    def clear_names(button):
        filepath = os.path.join(game.data_location, "users.txt")
        open(filepath, "w")

    dialog = Gtk.Dialog()
    dialog.set_title("Preferences")
    dialog.set_transient_for(game.window)
    dialog.add_button("_OK", Gtk.ResponseType.OK)
    dialog.set_default_response(Gtk.ResponseType.OK)
    dialog.set_border_width(5)

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

    label = widgets.AlignedLabel("Save Location")
    grid.attach(label, 0, 3, 1, 1)
    filechooserLocation = Gtk.FileChooserButton()
    filechooserLocation.set_tooltip_text("The location where save files will be stored by default.")
    filechooserLocation.set_action(Gtk.FileChooserAction.SELECT_FOLDER)
    filechooserLocation.set_filename(game.save_location)
    filechooserLocation.connect("file-set", change_save_location)
    grid.attach(filechooserLocation, 1, 3, 3, 1)

    frame = widgets.CommonFrame("Manager Names")
    grid.attach(frame, 0, 4, 2, 1)
    grid1 = Gtk.Grid()
    grid1.set_column_spacing(5)
    frame.insert(grid1)
    label = widgets.AlignedLabel("Clear previously entered manager names:")
    grid1.attach(label, 0, 0, 1, 1)
    buttonClear = widgets.Button("_Clear Names")
    buttonClear.connect("clicked", clear_names)
    grid1.attach(buttonClear, 1, 0, 1, 1)

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
    messagedialog = Gtk.MessageDialog(message_format="Sell %s to %s for %s?" % (name, club, amount),
                                      type=Gtk.MessageType.QUESTION)
    messagedialog.set_transient_for(game.window)
    messagedialog.set_title("Quick Sell")
    messagedialog.add_button("_Cancel", Gtk.ResponseType.CANCEL)
    messagedialog.add_button("C_onfirm", Gtk.ResponseType.OK)
    messagedialog.set_default_response(Gtk.ResponseType.CANCEL)

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
    label.set_use_markup(True)
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

    text = message[status]

    messagedialog = Gtk.MessageDialog(message_format=text)
    messagedialog.set_transient_for(game.window)
    messagedialog.set_title("Scout Report")
    messagedialog.add_button("_Close", Gtk.ResponseType.CLOSE)
    messagedialog.set_default_response(Gtk.ResponseType.CLOSE)

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

    if playerid is not None:
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

    if playerid is not None:
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

    messagedialog = Gtk.MessageDialog(message_format="You have not selected enough players\nto proceed to the next game.",
                                      type=Gtk.MessageType.ERROR)
    messagedialog.format_secondary_text(text)
    messagedialog.set_transient_for(game.window)
    messagedialog.set_title("Not Enough Players")
    messagedialog.add_button("_Close", Gtk.ResponseType.CLOSE)

    messagedialog.run()
    messagedialog.destroy()


def not_enough_subs(number):
    messagedialog = Gtk.MessageDialog(message_format="You have only selected %i out of a possible 5 subs." % (number),
                                      type=Gtk.MessageType.WARNING)
    messagedialog.format_secondary_text("Do you wish to continue to the game?")
    messagedialog.set_transient_for(game.window)
    messagedialog.set_title("Not Enough Subs")
    messagedialog.add_button("_No", Gtk.ResponseType.NO)
    messagedialog.add_button("_Yes", Gtk.ResponseType.YES)
    messagedialog.set_default_response(Gtk.ResponseType.NO)

    response = messagedialog.run()

    answer = False

    if response == Gtk.ResponseType.YES:
        answer = True

    messagedialog.destroy()

    return answer


def proceed_to_game(team):
    messagedialog = Gtk.MessageDialog(message_format="Proceed to next match?",
                                      type=Gtk.MessageType.QUESTION)
    messagedialog.format_secondary_text("Your next match is against %s." % (team))
    messagedialog.set_title("Proceed To Next Match")
    messagedialog.set_transient_for(game.window)
    messagedialog.add_button("_No", Gtk.ResponseType.NO)
    messagedialog.add_button("_Yes", Gtk.ResponseType.YES)
    messagedialog.set_default_response(Gtk.ResponseType.NO)

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

        if coach.speciality == "Goalkeeping":
            speciality = "Keeping"
        elif coach.speciality == "Defensive":
            speciality = "Tackling, Stamina"
        elif coach.speciality == "Midfield":
            speciality = "Passing, Ball Control"
        elif coach.speciality == "Attacking":
            speciality = "Shooting"
        elif coach.speciality == "Fitness":
            speciality = "Fitness, Pace, Stamina"
        elif coach.speciality == "All":
            speciality = "All"

        labelSpeciality.set_text(speciality)

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
        name = game.players[item]
        name = display.name(name)

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

    if playerid is None:
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
    if playerid is not None:
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
        if playerid is None:
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

    messagedialog = Gtk.MessageDialog(message_format="Remove %s from individual training?" % (name),
                                      type=Gtk.MessageType.QUESTION)
    messagedialog.set_title("Individual Training")
    messagedialog.set_transient_for(game.window)
    messagedialog.add_button("_Cancel", Gtk.ResponseType.CANCEL)
    messagedialog.add_button("_Remove", Gtk.ResponseType.OK)
    messagedialog.set_default_response(Gtk.ResponseType.CANCEL)

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

    messagedialog = Gtk.MessageDialog(message_format="Begin the construction of upgrades to the stadium at cost of %s?" % (cost),
                                      type=Gtk.MessageType.QUESTION)
    messagedialog.set_transient_for(game.window)
    messagedialog.set_title("Upgrade Stadium")
    messagedialog.add_button("_Cancel", Gtk.ResponseType.CANCEL)
    messagedialog.add_button("_Build", Gtk.ResponseType.OK)
    messagedialog.set_default_response(Gtk.ResponseType.CANCEL)

    response = messagedialog.run()

    state = False

    if response == Gtk.ResponseType.OK:
        state = True

    messagedialog.destroy()

    return state


def confirm_building(cost):
    cost = display.currency(cost)

    messagedialog = Gtk.MessageDialog(message_format="Begin the construction of new buildings at a cost of %s?" % (cost),
                                      type=Gtk.MessageType.QUESTION)
    messagedialog.set_transient_for(game.window)
    messagedialog.set_title("Upgrade Building")
    messagedialog.add_button("_Cancel", Gtk.ResponseType.CANCEL)
    messagedialog.add_button("_Build", Gtk.ResponseType.OK)
    messagedialog.set_default_response(Gtk.ResponseType.CANCEL)

    state = False

    if messagedialog.run() == Gtk.ResponseType.OK:
        state = True

    messagedialog.destroy()

    return state


def confirm_training(cost):
    display_cost = display.currency(cost)

    messagedialog = Gtk.MessageDialog(message_format="Arrange for trip to training camp at a cost of %s?" % (display_cost),
                                      type=Gtk.MessageType.QUESTION)
    messagedialog.set_transient_for(game.window)
    messagedialog.set_title("Confirm Training")
    messagedialog.add_button("_Cancel", Gtk.ResponseType.CANCEL)
    messagedialog.add_button("C_onfirm", Gtk.ResponseType.OK)
    messagedialog.set_default_response(Gtk.ResponseType.CANCEL)

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
    messagedialog = Gtk.MessageDialog(message_format="Unable to fire %s as he is currently individual training %i players.\n\nPlease reassign the players to other coaches and try again." % (name, number), type=Gtk.MessageType.ERROR)
    messagedialog.set_title("Fire Staff")
    messagedialog.set_transient_for(game.window)
    messagedialog.add_button("_OK", Gtk.ResponseType.OK)

    messagedialog.run()
    messagedialog.destroy()


def renew_staff_contract(name, year, amount):
    amount = display.currency(amount)

    messagedialog = Gtk.MessageDialog(message_format="%s is requesting a %i year contract and %s per week." % (name, year, amount),
                                      type=Gtk.MessageType.QUESTION)
    messagedialog.set_transient_for(game.window)
    messagedialog.set_title("Renew Contract")
    messagedialog.add_button("_Reject", Gtk.ResponseType.REJECT)
    messagedialog.add_button("_Accept", Gtk.ResponseType.ACCEPT)
    messagedialog.set_default_response(Gtk.ResponseType.REJECT)

    state = False

    if messagedialog.run() == Gtk.ResponseType.ACCEPT:
        state = True

    messagedialog.destroy()

    return state


def improve_wage(name, amount):
    amount = display.currency(amount)

    messagedialog = Gtk.MessageDialog(message_format="Increase wages for %s to %s per week?" % (name, amount),
                                      type=Gtk.MessageType.QUESTION)
    messagedialog.set_transient_for(game.window)
    messagedialog.set_title("Improve Wage")
    messagedialog.add_button("_Reject", Gtk.ResponseType.REJECT)
    messagedialog.add_button("_Accept", Gtk.ResponseType.ACCEPT)
    messagedialog.set_default_response(Gtk.ResponseType.REJECT)

    state = False

    if messagedialog.run() == Gtk.ResponseType.ACCEPT:
        state = True

    messagedialog.destroy()

    return state


def cancel_loan(name):
    messagedialog = Gtk.MessageDialog(message_format="Cancel loan contract for %s?" % (name),
                                      type=Gtk.MessageType.QUESTION)
    messagedialog.format_secondary_text("The player will be returned to his parent club.")
    messagedialog.set_transient_for(game.window)
    messagedialog.set_title("Cancel Loan")
    messagedialog.add_button("_Do Not Cancel", Gtk.ResponseType.REJECT)
    messagedialog.add_button("_Cancel Loan", Gtk.ResponseType.ACCEPT)
    messagedialog.set_default_response(Gtk.ResponseType.REJECT)

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
    status = game.clubs[game.teamid].sponsor_status
    company, period, cost = game.clubs[game.teamid].sponsor_offer

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
        company, period, cost = game.clubs[game.teamid].sponsor_offer
        game.clubs[game.teamid].sponsor_status = 2
        money.deposit(cost, 1)
    elif response == Gtk.ResponseType.REJECT:
        game.clubs[game.teamid].sponsor_status = 0
        game.sponsor_timeout = random.randint(4, 6)

    messagedialog.destroy()


def float_club(amount):
    amount = display.currency(amount)

    messagedialog = Gtk.MessageDialog(message_format="Are you sure you want to float the club publically?",
                                      type=Gtk.MessageType.QUESTION)
    messagedialog.format_secondary_text("The amount raised will be in the region of %s." % (amount))
    messagedialog.set_title("Float Club")
    messagedialog.set_transient_for(game.window)
    messagedialog.add_button("_No", Gtk.ResponseType.NO)
    messagedialog.add_button("_Yes", Gtk.ResponseType.YES)
    messagedialog.set_default_response(Gtk.ResponseType.NO)

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


def name_change():
    dialog = Gtk.Dialog()
    dialog.set_title("Manager Name")
    dialog.set_transient_for(game.window)
    dialog.set_border_width(5)
    dialog.add_button("_Cancel", Gtk.ResponseType.CANCEL)
    dialog.add_button("_Apply", Gtk.ResponseType.APPLY)
    dialog.set_default_response(Gtk.ResponseType.APPLY)

    grid = Gtk.Grid()
    grid.set_column_spacing(5)
    dialog.vbox.add(grid)

    label = Gtk.Label("Change your manager name:")
    grid.attach(label, 0, 0, 1, 1)

    liststoreName = Gtk.ListStore(str)

    combobox = Gtk.ComboBoxText.new_with_entry()
    combobox.set_model(liststoreName)
    entry = combobox.get_child()
    entry.set_text(game.clubs[game.teamid].manager)
    grid.attach(combobox, 1, 0, 1, 1)

    [liststoreName.append([name]) for name in fileio.read_names()]

    dialog.show_all()

    state = False

    if dialog.run() == Gtk.ResponseType.APPLY:
        name = entry.get_text()

        game.clubs[game.teamid].manager = name
        fileio.write_names(name, "a")

        add = True

        for count, item in enumerate(liststoreName):
            if item[0] == game.clubs[game.teamid].manager:
                add = False

                del(liststoreName[count])
                liststoreName.prepend([game.clubs[game.teamid].manager])

        if add:
            liststoreName.prepend([game.clubs[game.teamid].manager])

        names = [key[0] for key in liststoreName]
        fileio.write_names(names)

        state = True

    dialog.destroy()

    return state


def loan_period():
    messagedialog = Gtk.MessageDialog(type=Gtk.MessageType.WARNING)
    messagedialog.set_transient_for(game.window)
    messagedialog.set_title("Loan Period Warning")
    messagedialog.add_button("_Close", Gtk.ResponseType.CLOSE)
    messagedialog.set_markup("The loan period entered is longer than the players remaining contract length. The loan negotiations will continue however the players contract may expire before the agreed end of the loan period if his parent club and the player do not agree a new contract.")

    messagedialog.run()
    messagedialog.destroy()


def file_not_found_error():
    messagedialog = Gtk.MessageDialog()
    messagedialog.set_transient_for(game.window)
    messagedialog.set_title("Editor Not Available")
    messagedialog.add_button("_Close", Gtk.ResponseType.CLOSE)
    messagedialog.set_markup("Data Editor is not installed.")
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
