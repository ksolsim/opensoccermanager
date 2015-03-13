#!/usr/bin/env python3

from gi.repository import Gtk
import random

import calculator
import constants
import display
import evaluation
import fileio
import game
import money
import version
import widgets


def free_transfer(name, cost):
    cost = display.currency(cost)
    messagedialog = Gtk.MessageDialog(type=Gtk.MessageType.QUESTION)
    messagedialog.set_transient_for(game.window)
    messagedialog.set_title("Release On Free Transfer")
    messagedialog.add_button("_Cancel", Gtk.ResponseType.CANCEL)
    messagedialog.add_button("C_onfirm", Gtk.ResponseType.OK)
    messagedialog.set_default_response(Gtk.ResponseType.CANCEL)
    messagedialog.set_markup("Release %s from his contract?" % (name))
    messagedialog.format_secondary_text("This will cost %s to pay off his contract." % (cost))

    state = False

    if messagedialog.run() == Gtk.ResponseType.OK:
        state = True

    messagedialog.destroy()

    return state


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
        del training[playerid]

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

        label = widgets.Label("_Opposition")
        grid2.attach(label, 0, 0, 1, 1)
        cellrenderertext = Gtk.CellRendererText()
        self.combobox = Gtk.ComboBox()
        self.combobox.set_model(treemodelsort)
        self.combobox.set_id_column(0)
        self.combobox.connect("changed", self.combobox_changed)
        self.combobox.pack_start(cellrenderertext, True)
        self.combobox.add_attribute(cellrenderertext, "text", 1)
        label.set_mnemonic_widget(self.combobox)
        grid2.attach(self.combobox, 1, 0, 1, 1)

        commonframe = widgets.CommonFrame("Details")
        grid.attach(commonframe, 0, 1, 1, 1)

        grid1 = Gtk.Grid()
        grid1.set_row_spacing(5)
        grid1.set_column_spacing(5)
        commonframe.insert(grid1)

        label = widgets.AlignedLabel("Manager")
        grid1.attach(label, 0, 0, 1, 1)
        self.labelManager = widgets.AlignedLabel()
        grid1.attach(self.labelManager, 1, 0, 1, 1)

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

        self.notebook = Gtk.Notebook()
        self.notebook.set_show_tabs(False)
        commonframe.insert(self.notebook)

        cellrenderertext = Gtk.CellRendererText()

        # Squad Tab
        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_policy(Gtk.PolicyType.NEVER,
                                  Gtk.PolicyType.AUTOMATIC)
        label = widgets.Label("_Squad")
        self.notebook.append_page(scrolledwindow, label)

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
        treeviewcolumn = Gtk.TreeViewColumn(None,
                                            cellrenderertext,
                                            text=0)
        treeview.append_column(treeviewcolumn)
        scrolledwindow.add(treeview)

        # Team Selection Tab
        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_policy(Gtk.PolicyType.NEVER,
                                  Gtk.PolicyType.AUTOMATIC)
        label = widgets.Label("_Team")
        self.notebook.append_page(scrolledwindow, label)

        self.liststoreTeam = Gtk.ListStore(str, str)

        treeview = Gtk.TreeView()
        treeview.set_vexpand(True)
        treeview.set_hexpand(True)
        treeview.set_model(self.liststoreTeam)
        treeview.set_enable_search(False)
        treeview.set_search_column(-1)
        treeviewcolumn = Gtk.TreeViewColumn("Position",
                                            cellrenderertext,
                                            text=0)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Player",
                                            cellrenderertext,
                                            text=1)
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

        self.labelManager.set_label(club.manager)
        self.labelPosition.set_label(position)

        if len(club.form) > 0:
            form = "".join(club.form[-6:])
            self.labelForm.set_label(form)
        else:
            self.labelForm.set_label("N/A")

        self.liststoreSquad.clear()

        for playerid in club.squad:
            player = game.players[playerid]
            name = display.name(player)
            self.liststoreSquad.append([name])

        if game.eventindex > 0:
            self.notebook.set_show_tabs(True)
            self.liststoreTeam.clear()

            for positionid, playerid in club.team.items():
                formationid = club.tactics[0]

                if positionid < 11:
                    position = constants.formations[formationid][1][positionid]
                else:
                    position = "Sub %i" % (positionid - 10)

                if playerid != 0:
                    player = game.players[playerid]
                    name = display.name(player)
                    self.liststoreTeam.append([position, name])

    def response_handler(self, dialog, response):
        self.destroy()
