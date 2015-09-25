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
import random

import calculator
import constants
import display
import evaluation
import game
import money
import transfer
import widgets


def release_player(name, cost):
    '''
    Ask to release player and pay off remainder of contract.
    '''
    cost = display.currency(cost)
    messagedialog = Gtk.MessageDialog(type=Gtk.MessageType.QUESTION)
    messagedialog.set_transient_for(window.window)
    messagedialog.set_title("Release Player")
    messagedialog.add_button("_Cancel", Gtk.ResponseType.CANCEL)
    messagedialog.add_button("C_onfirm", Gtk.ResponseType.OK)
    messagedialog.set_default_response(Gtk.ResponseType.CANCEL)
    messagedialog.set_markup("<span size='12000'><b>Release %s from his contract?</b></span>" % (name))
    messagedialog.format_secondary_text("This will cost %s to pay off his contract." % (cost))

    state = messagedialog.run() == Gtk.ResponseType.OK

    messagedialog.destroy()

    return state


def renew_player_contract(playerid):
    '''
    Customise details of player contract renewal.
    '''
    player = game.players[playerid]
    name = player.get_name(mode=1)

    wage = calculator.wage(playerid)
    wage = wage * 1.1
    leaguewin, leaguerunnerup, winbonus, goalbonus = calculator.bonus(wage)

    age = player.get_age()

    if age < 25:
        contract = 5
    elif age < 29:
        contract = 4
    elif age < 33:
        contract = 3
    elif age < 35:
        contract = 2
    else:
        contract = 1

    dialog = Gtk.Dialog()
    dialog.set_transient_for(window.window)
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

        player.set_morale(15)

        state = True

    dialog.destroy()

    return state


def scout_report(player, status):
    message = constants.scout_report[status] % (player)

    messagedialog = Gtk.MessageDialog(type=Gtk.MessageType.INFO)
    messagedialog.set_transient_for(window.window)
    messagedialog.set_title("Scout Report")
    messagedialog.add_button("_Close", Gtk.ResponseType.CLOSE)
    messagedialog.set_markup(message)
    messagedialog.run()
    messagedialog.destroy()


def not_enough_subs(number):
    messagedialog = Gtk.MessageDialog(type=Gtk.MessageType.WARNING)
    messagedialog.set_transient_for(window.window)
    messagedialog.set_title("Not Enough Subs")
    messagedialog.add_button("_No", Gtk.ResponseType.NO)
    messagedialog.add_button("_Yes", Gtk.ResponseType.YES)
    messagedialog.set_default_response(Gtk.ResponseType.NO)
    messagedialog.set_markup("<span size='12000'><b>You have only selected %i out of a possible 5 subs.</b></span>" % (number))
    messagedialog.format_secondary_text("Do you wish to continue to the game?")

    answer = messagedialog.run() == Gtk.ResponseType.YES

    messagedialog.destroy()

    return answer


def proceed_to_game(team):
    messagedialog = Gtk.MessageDialog(type=Gtk.MessageType.QUESTION)
    messagedialog.set_title("Proceed To Next Match")
    messagedialog.set_transient_for(window.window)
    messagedialog.add_button("_No", Gtk.ResponseType.NO)
    messagedialog.add_button("_Yes", Gtk.ResponseType.YES)
    messagedialog.set_default_response(Gtk.ResponseType.NO)
    messagedialog.set_markup("<span size='12000'><b>Proceed to next match?</b></span>")
    messagedialog.format_secondary_text("Your next match is against %s." % (team))

    proceed = messagedialog.run() == Gtk.ResponseType.YES

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

        coachid = int(model[active][0])
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
    dialog.set_transient_for(window.window)
    dialog.set_border_width(5)
    dialog.set_resizable(False)
    dialog.set_title("Individual Training")
    dialog.add_button("_Cancel", Gtk.ResponseType.CANCEL)

    if not playerid:
        dialog.add_button("_Add", Gtk.ResponseType.OK)
    else:
        dialog.add_button("_Edit", Gtk.ResponseType.OK)

    dialog.set_default_response(Gtk.ResponseType.OK)

    grid = Gtk.Grid()
    grid.set_row_spacing(5)
    grid.set_column_spacing(5)
    dialog.vbox.add(grid)

    liststorePlayer = Gtk.ListStore(int, str)
    treemodelsort = Gtk.TreeModelSort(liststorePlayer)
    treemodelsort.set_sort_column_id(1, Gtk.SortType.ASCENDING)

    for item in game.clubs[game.teamid].squad:
        if item not in game.clubs[game.teamid].individual_training.keys():
            player = game.players[item]
            name = player.get_name()

            liststorePlayer.append([item, name])

    liststoreCoach = Gtk.ListStore(str, str)

    for coachid, coach in game.clubs[game.teamid].coaches_hired.items():
        liststoreCoach.append([str(coachid), coach.name])

    for count, text in enumerate(("Coach", "Skill", "Intensity")):
        label = widgets.AlignedLabel("%s" % (text))
        grid.attach(label, 0, count + 1, 1, 1)

    cellrenderertext = Gtk.CellRendererText()

    if not playerid:
        label = widgets.AlignedLabel("Player")
        grid.attach(label, 0, 0, 1, 1)

        comboboxPlayer = Gtk.ComboBox()
        comboboxPlayer.set_model(treemodelsort)
        comboboxPlayer.set_active(0)
        comboboxPlayer.pack_start(cellrenderertext, True)
        comboboxPlayer.add_attribute(cellrenderertext, "text", 1)
        grid.attach(comboboxPlayer, 1, 0, 1, 1)

    label = widgets.AlignedLabel("Specialities:")
    grid.attach(label, 2, 1, 1, 1)
    labelSpeciality = widgets.AlignedLabel()
    grid.attach(labelSpeciality, 3, 1, 1, 1)

    comboboxCoach = Gtk.ComboBox()
    comboboxCoach.set_model(liststoreCoach)
    comboboxCoach.set_id_column(0)
    comboboxCoach.pack_start(cellrenderertext, True)
    comboboxCoach.add_attribute(cellrenderertext, "text", 1)
    comboboxCoach.connect("changed", update_speciality)
    comboboxCoach.set_active(0)
    grid.attach(comboboxCoach, 1, 1, 1, 1)

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
        club = game.clubs[game.teamid]
        training = club.individual_training[playerid]

        # Set value for coach within combobox
        if training in club.coaches_hired.keys():
            comboboxCoach.set_active_id(str(training))

        comboboxSkill.set_active(training.skill)
        intensity_widget[training.intensity].set_active(True)

    dialog.show_all()

    training = None

    if dialog.run() == Gtk.ResponseType.OK:
        if not playerid:
            model = comboboxPlayer.get_model()
            active = comboboxPlayer.get_active()
            playerid = model[active][0]

        # Coach
        model = comboboxCoach.get_model()
        active = comboboxCoach.get_active()
        coachid = int(model[active][0])

        # Skill
        skill = int(comboboxSkill.get_active_id())

        # Intensity
        if radiobuttonIntensityLow.get_active():
            intensity = 0
        elif radiobuttonIntensityMedium.get_active():
            intensity = 1
        else:
            intensity = 2

        training = (playerid, coachid, skill, intensity)

    dialog.destroy()

    return training


def remove_individual_training(playerid):
    player = game.players[playerid]
    name = player.get_name(mode=1)

    messagedialog = Gtk.MessageDialog(type=Gtk.MessageType.QUESTION)
    messagedialog.set_title("Individual Training")
    messagedialog.set_transient_for(window.window)
    messagedialog.add_button("_Cancel", Gtk.ResponseType.CANCEL)
    messagedialog.add_button("_Remove", Gtk.ResponseType.OK)
    messagedialog.set_default_response(Gtk.ResponseType.CANCEL)
    messagedialog.set_markup("Remove %s from individual training?" % (name))

    state = False

    if messagedialog.run() == Gtk.ResponseType.OK:
        training = game.clubs[game.teamid].individual_training
        del training[playerid]

        state = True

    messagedialog.destroy()

    return state


def withdraw_transfer(negotiationid):
    '''
    Confirm that the user wishes to withdraw from the transfer negotiations.
    '''
    playerid = game.negotiations[negotiationid].playerid
    player = game.players[playerid]
    name = player.get_name(mode=1)

    messagedialog = Gtk.MessageDialog(type=Gtk.MessageType.QUESTION)
    messagedialog.set_transient_for(window.window)
    messagedialog.set_title("Withdraw Transfer Offer")
    messagedialog.add_button("_Cancel", Gtk.ResponseType.CANCEL)
    messagedialog.add_button("_Withdraw", Gtk.ResponseType.OK)
    messagedialog.set_default_response(Gtk.ResponseType.CANCEL)
    messagedialog.set_markup("Withdraw transfer offer for %s?" % (name))

    state = messagedialog.run() == Gtk.ResponseType.OK

    messagedialog.destroy()

    return state


def cancel_transfer(negotiationid):
    '''
    Confirm that the user wants to end transfer negotiations.
    '''
    playerid = game.negotiations[negotiationid].playerid
    player = game.players[playerid]
    name = player.get_name(mode=1)

    messagedialog = Gtk.MessageDialog(type=Gtk.MessageType.QUESTION)
    messagedialog.set_transient_for(window.window)
    messagedialog.set_title("End Transfer Negotiations")
    messagedialog.add_button("_Do Not End", Gtk.ResponseType.CANCEL)
    messagedialog.add_button("_End", Gtk.ResponseType.OK)
    messagedialog.set_default_response(Gtk.ResponseType.CANCEL)
    messagedialog.set_markup("End transfer negotiations for %s?" % (name))

    state = messagedialog.run() == Gtk.ResponseType.OK

    messagedialog.destroy()

    return state


def remove_from_shortlist(playerid):
    player = game.players[playerid]
    name = player.get_name(mode=1)

    messagedialog = Gtk.MessageDialog(type=Gtk.MessageType.QUESTION)
    messagedialog.set_title("Remove From Shortlist")
    messagedialog.set_transient_for(window.window)
    messagedialog.add_button("_Cancel", Gtk.ResponseType.CANCEL)
    messagedialog.add_button("_Remove", Gtk.ResponseType.OK)
    messagedialog.set_default_response(Gtk.ResponseType.CANCEL)
    messagedialog.set_markup("<span size='12000'><b>Remove %s from shortlist?</b></span>" % (name))
    messagedialog.format_secondary_text("Removal will not cancel any ongoing transfer negotiations.")

    state = messagedialog.run() == Gtk.ResponseType.OK

    messagedialog.destroy()

    return state


def confirm_stadium(cost):
    cost = display.currency(cost)

    messagedialog = Gtk.MessageDialog(type=Gtk.MessageType.QUESTION)
    messagedialog.set_transient_for(window.window)
    messagedialog.set_title("Upgrade Stadium")
    messagedialog.add_button("_Cancel", Gtk.ResponseType.CANCEL)
    messagedialog.add_button("_Build", Gtk.ResponseType.OK)
    messagedialog.set_default_response(Gtk.ResponseType.CANCEL)
    messagedialog.set_markup("Begin the construction of upgrades to the stadium at cost of %s?" % (cost))

    state = messagedialog.run() == Gtk.ResponseType.OK

    messagedialog.destroy()

    return state


def confirm_building(cost):
    cost = display.currency(cost)

    messagedialog = Gtk.MessageDialog(type=Gtk.MessageType.QUESTION)
    messagedialog.set_transient_for(window.window)
    messagedialog.set_title("Upgrade Building")
    messagedialog.add_button("_Cancel", Gtk.ResponseType.CANCEL)
    messagedialog.add_button("_Build", Gtk.ResponseType.OK)
    messagedialog.set_default_response(Gtk.ResponseType.CANCEL)
    messagedialog.set_markup("Begin the construction of new buildings at a cost of %s?" % (cost))

    state = messagedialog.run() == Gtk.ResponseType.OK

    messagedialog.destroy()

    return state


def confirm_training(cost):
    display_cost = display.currency(cost)

    messagedialog = Gtk.MessageDialog(type=Gtk.MessageType.QUESTION)
    messagedialog.set_transient_for(window.window)
    messagedialog.set_title("Confirm Training")
    messagedialog.add_button("_Cancel", Gtk.ResponseType.CANCEL)
    messagedialog.add_button("C_onfirm", Gtk.ResponseType.OK)
    messagedialog.set_default_response(Gtk.ResponseType.CANCEL)
    messagedialog.set_markup("Arrange for trip to training camp at a cost of %s?" % (display_cost))

    state = messagedialog.run() == Gtk.ResponseType.OK

    messagedialog.destroy()

    return state


def hire_staff(index, name):
    staff_type = {0: "Coach", 1: "Scout"}

    messagedialog = Gtk.MessageDialog(type=Gtk.MessageType.QUESTION)
    messagedialog.set_transient_for(window.window)
    messagedialog.set_title("Hire %s" % (staff_type[index]))
    messagedialog.add_button("_Cancel", Gtk.ResponseType.CANCEL)
    messagedialog.add_button("_Hire", Gtk.ResponseType.YES)
    messagedialog.set_default_response(Gtk.ResponseType.CANCEL)
    messagedialog.set_markup("Hire %s %s?" % (staff_type[index], name))

    state = messagedialog.run() == Gtk.ResponseType.YES

    messagedialog.destroy()

    return state


def fire_staff(index, name, payout):
    staff_type = {0: "Coach", 1: "Scout"}

    payout = display.currency(payout)

    messagedialog = Gtk.MessageDialog(type=Gtk.MessageType.QUESTION)
    messagedialog.set_transient_for(window.window)
    messagedialog.set_title("Fire %s" % staff_type[index])
    messagedialog.add_button("_Cancel", Gtk.ResponseType.CANCEL)
    messagedialog.add_button("_Fire", Gtk.ResponseType.OK)
    messagedialog.set_default_response(Gtk.ResponseType.CANCEL)
    messagedialog.set_markup("Fire %s %s at a cost of %s?" % (staff_type[index], name, payout))

    state = messagedialog.run() == Gtk.ResponseType.OK

    messagedialog.destroy()

    return state


def fire_staff_error(name, number):
    messagedialog = Gtk.MessageDialog(type=Gtk.MessageType.ERROR)
    messagedialog.set_title("Fire Staff")
    messagedialog.set_transient_for(window.window)
    messagedialog.add_button("_Close", Gtk.ResponseType.CLOSE)
    messagedialog.set_markup("Unable to fire %s as he is currently individual training %i players. Please reassign the players to other coaches and try again." % (name, number))
    messagedialog.run()
    messagedialog.destroy()


def renew_staff_contract(name, year, amount):
    amount = display.currency(amount)

    messagedialog = Gtk.MessageDialog(type=Gtk.MessageType.QUESTION)
    messagedialog.set_transient_for(window.window)
    messagedialog.set_title("Renew Contract")
    messagedialog.add_button("_Reject", Gtk.ResponseType.REJECT)
    messagedialog.add_button("_Accept", Gtk.ResponseType.ACCEPT)
    messagedialog.set_default_response(Gtk.ResponseType.REJECT)
    messagedialog.set_markup("%s is requesting a %i year contract and %s per week." % (name, year, amount))

    state = messagedialog.run() == Gtk.ResponseType.ACCEPT

    messagedialog.destroy()

    return state


def renew_staff_contract_error(staff):
    messagedialog = Gtk.MessageDialog(type=Gtk.MessageType.ERROR)
    messagedialog.set_transient_for(window.window)
    messagedialog.set_title("Renew Contract")
    messagedialog.add_button("_Close", Gtk.ResponseType.CLOSE)
    messagedialog.set_markup("%s has decided to retire once his current contract expires, and will not negotiate an extension." % (staff.name))
    messagedialog.run()
    messagedialog.destroy()


def improve_wage(name, amount):
    amount = display.currency(amount)

    messagedialog = Gtk.MessageDialog(type=Gtk.MessageType.QUESTION)
    messagedialog.set_transient_for(window.window)
    messagedialog.set_title("Improve Wage")
    messagedialog.add_button("_Reject", Gtk.ResponseType.REJECT)
    messagedialog.add_button("_Accept", Gtk.ResponseType.ACCEPT)
    messagedialog.set_default_response(Gtk.ResponseType.REJECT)
    messagedialog.set_markup("Increase wages for %s to %s per week?" % (name, amount))

    state = messagedialog.run() == Gtk.ResponseType.ACCEPT

    messagedialog.destroy()

    return state


def sponsorship():
    club = game.clubs[game.teamid]

    messagedialog = Gtk.MessageDialog()
    messagedialog.set_title("Sponsorship")
    messagedialog.set_transient_for(window.window)

    if club.sponsorship.status == 0:
        messagedialog.set_markup("There are currently no club sponsorship offers.")

        messagedialog.add_button("_Close", Gtk.ResponseType.CLOSE)
        messagedialog.set_default_response(Gtk.ResponseType.CLOSE)
    elif club.sponsorship.status == 1:
        details = club.sponsorship.get_details()

        messagedialog.set_markup("%s have made a %s year offer worth %s." % details)
        messagedialog.add_button("_Reject", Gtk.ResponseType.REJECT)
        messagedialog.add_button("_Accept", Gtk.ResponseType.ACCEPT)
        messagedialog.set_default_response(Gtk.ResponseType.ACCEPT)
    else:
        details = club.sponsorship.get_details()

        if details[1] == 1:
            messagedialog.set_markup("The deal with %s runs for another year." % (details[0]))
        else:
            messagedialog.set_markup("The deal with %s runs for another %s years." % (details[0], details[1]))

        messagedialog.add_button("_Close", Gtk.ResponseType.CLOSE)
        messagedialog.set_default_response(Gtk.ResponseType.CLOSE)

    response = messagedialog.run()

    if response == Gtk.ResponseType.ACCEPT:
        club.sponsorship.accept()
    elif response == Gtk.ResponseType.REJECT:
        club.sponsorship.reject()

    messagedialog.destroy()


def float_club(amount):
    amount = display.currency(amount)

    messagedialog = Gtk.MessageDialog(type=Gtk.MessageType.QUESTION)
    messagedialog.set_title("Float Club")
    messagedialog.set_transient_for(window.window)
    messagedialog.add_button("_No", Gtk.ResponseType.NO)
    messagedialog.add_button("_Yes", Gtk.ResponseType.YES)
    messagedialog.set_default_response(Gtk.ResponseType.NO)
    messagedialog.set_markup("<span size='12000'><b>Are you sure you want to float the club publically?</b></span>")
    messagedialog.format_secondary_text("The amount raised will be in the region of %s." % (amount))

    state = messagedialog.run() == Gtk.ResponseType.YES

    messagedialog.destroy()

    return state


def end_of_season():
    dialog = Gtk.Dialog()
    dialog.set_transient_for(window.window)
    dialog.set_title("End of Season")
    dialog.set_border_width(5)
    dialog.add_button("_Close", Gtk.ResponseType.OK)
    dialog.set_default_response(Gtk.ResponseType.OK)

    grid = Gtk.Grid()
    grid.set_row_spacing(5)
    grid.set_column_spacing(5)
    dialog.vbox.add(grid)

    clubid = game.standings.find_champion()
    champion = game.clubs[clubid].name

    label = widgets.AlignedLabel("League Champion")
    grid.attach(label, 0, 0, 1, 1)
    label = widgets.AlignedLabel()
    label.set_markup("<span size='16000' weight='bold'>%s</span>" % (champion))
    grid.attach(label, 1, 0, 1, 1)

    top = display.top_scorer()
    player = game.players[top[0]]
    name = player.get_name(mode=1)
    goals = top[1]

    label = widgets.AlignedLabel("Top Goalscorer")
    grid.attach(label, 0, 1, 1, 1)
    label = widgets.AlignedLabel()
    label.set_markup("<span size='16000' weight='bold'>%s (%i)</span>" % (name, goals))
    grid.attach(label, 1, 1, 1, 1)

    top = display.top_assister()
    player = game.players[top[0]]
    name = player.get_name(mode=1)
    assists = top[1]

    label = widgets.AlignedLabel("Top Assister")
    grid.attach(label, 0, 2, 1, 1)
    label = widgets.AlignedLabel()
    label.set_markup("<span size='16000' weight='bold'>%s (%i)</span>" % (name, assists))
    grid.attach(label, 1, 2, 1, 1)

    top = display.player_of_the_season()
    player = game.players[top[0]]
    name = player.get_name(mode=1)

    label = widgets.AlignedLabel("Player of the Season")
    grid.attach(label, 0, 3, 1, 1)
    label = widgets.AlignedLabel()
    label.set_markup("<span size='16000' weight='bold'>%s</span>" % (name))
    grid.attach(label, 1, 3, 1, 1)

    dialog.show_all()
    dialog.run()
    dialog.destroy()


def editor_not_found_error():
    '''
    Shown when editor folder is not installed.
    '''
    messagedialog = Gtk.MessageDialog()
    messagedialog.set_transient_for(window.window)
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
    messagedialog.set_transient_for(window.window)
    messagedialog.set_title(message_title)
    messagedialog.add_button("_Close", Gtk.ResponseType.CLOSE)
    messagedialog.set_default_response(Gtk.ResponseType.CLOSE)
    messagedialog.set_markup(message_text)
    messagedialog.run()
    messagedialog.destroy()
