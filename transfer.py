#!/usr/bin/env python3

from gi.repository import Gtk
import random

import calculator
import constants
import dialogs
import display
import game
import money
import news
import widgets


class Negotiation():
    pass


def make_enquiry(playerid, transfer_type):
    for negotiationid in game.negotiations:
        if playerid == game.negotiations[negotiationid].playerid:
            dialogs.error(9)

            return

    state = enquiry_dialog(playerid, transfer_type)

    if state:
        negotiation = Negotiation()
        negotiation.playerid = playerid
        negotiation.date = "%i/%i/%i" % (game.year, game.month, game.date)
        negotiation.transfer_type = transfer_type
        negotiation.status = 0
        negotiation.timeout = random.randint(1, 4)
        negotiation.club = game.teamid
        game.negotiations[game.negotiationid] = negotiation

        game.negotiationid += 1
        game.clubs[game.teamid].shortlist.add(playerid)


def ai_enquiry():
    position = random.choice((("GK", 3), ("DL", 2), ("DR", 2), ("DC", 4), ("D", 0), ("ML", 2), ("MR", 2), ("MC", 4), ("M", 0), ("AS", 2), ("AF", 2)))

    count = 0

    for clubid in game.clubs:
        squad = game.clubs[clubid].squad

        for playerid in squad:
            player = game.players[playerid]

            if player.position == position[0]:
                count += 1

        if count < position[1]:
            suggestion = position[0]


def enquiry_dialog(playerid, index):
    '''
    Initiate transfer enquiry dialog for transfers, loans and free
    transfers.
    '''
    player = game.players[playerid]
    name = display.name(player, mode=1)
    transfer = ("purchase", "loan", "free transfer")[index]
    club = display.club(player.club)

    messagedialog = Gtk.MessageDialog(type=Gtk.MessageType.QUESTION)
    messagedialog.set_transient_for(game.window)
    messagedialog.set_title("Transfer Offer")
    messagedialog.add_button("_Cancel", Gtk.ResponseType.CANCEL)
    messagedialog.add_button("_Approach", Gtk.ResponseType.OK)
    messagedialog.set_default_response(Gtk.ResponseType.OK)

    if index == 2:
        messagedialog.set_markup("Approach %s for %s?" % (name, transfer))
    else:
        messagedialog.set_markup("Approach %s for %s from %s?" % (name, transfer, club))

    state = False

    if messagedialog.run() == Gtk.ResponseType.OK:
        state = True

    messagedialog.destroy()

    return state


def check(negotiationid):
    '''
    Check whether both teams meet the minimum required and maximum
    allowed prior to transfer completion.
    '''
    error = 0

    negotiation = game.negotiations[negotiationid]

    if negotiation.transfer_type != 2:
        player = game.players[negotiation.playerid]

        if len(game.clubs[player.club].squad) <= 16:
            error = 1
        elif len(game.clubs[player.club].squad) >= 30:
            error = 2

    if len(game.clubs[negotiation.club].squad) <= 16:
        error = 1
    elif len(game.clubs[negotiation.club].squad) >= 30:
        error = 2

    return error


def move(negotiationid):
    '''
    Move player between clubs when completing transfer, loan or free
    transfer.
    '''
    negotiation = game.negotiations[negotiationid]

    playerid = negotiation.playerid
    player = game.players[playerid]
    old_club = player.club
    new_club = negotiation.club

    # Remove from squad
    if negotiation.transfer_type == 0:
        game.clubs[old_club].squad.remove(playerid)
    elif negotiation.transfer_type == 1:
        game.loans[negotiation.playerid] = [old_club, negotiation.weeks]
        game.clubs[old_club].squad.remove(playerid)

    # Remove player from individual training
    if negotiation.transfer_type != 2:
        if playerid in game.clubs[old_club].individual_training:
            del(game.clubs[old_club].individual_training[playerid])

    player.club = new_club
    game.clubs[new_club].squad.append(playerid)

    # Reset transfer status
    player.transfer = [False, False]

    if negotiation.transfer_type in (0, 2):
        player.not_for_sale = False
    else:
        player.not_for_sale = True

    # Add player to list of transfers
    name = display.name(player)
    new_club = game.clubs[new_club].name

    if negotiation.transfer_type == 0:
        old_club = game.clubs[old_club].name
        fee = display.value(negotiation.amount)
    elif negotiation.transfer_type == 1:
        old_club = game.clubs[old_club].name
        fee = "Loan"
    elif negotiation.transfer_type == 2:
        old_club = ""
        fee = "Free Transfer"

    game.transfers.append([name, old_club, new_club, fee])

    del(game.negotiations[negotiationid])


def transfer():
    '''
    Process negotiations for each club, and each individual negotiation
    '''
    remove = []

    for negotiationid, negotiation in game.negotiations.items():
        if negotiation.timeout > 0:
            negotiation.timeout -= 1

            if negotiation.transfer_type != 2:
                if negotiation.timeout == 0 and negotiation.status == 0:
                    consider_enquiry(negotiationid)
                elif negotiation.timeout == 0 and negotiation.status == 3:
                    consider_offer(negotiationid)
                elif negotiation.timeout == 0 and negotiation.status == 6 or negotiation.status == 9:
                    consider_contract(negotiationid)
            else:
                if negotiation.timeout == 0 and negotiation.status == 0:
                    consider_enquiry(negotiationid)
                elif negotiation.timeout == 0 and negotiation.status == 6:
                    consider_contract(negotiationid)

        if negotiation.timeout == 0:
            if negotiation.status in (1, 4, 7, 10):
                remove.append(negotiationid)

    for key in remove:
        del(game.negotiations[key])


def consider_enquiry(negotiationid):
    '''
    Take account of type of offer (purchase / loan) and determine
    whether transfer of player is acceptable based on remaining squad.
    '''
    negotiation = game.negotiations[negotiationid]
    player = game.players[negotiation.playerid]
    name = display.name(player, mode=1)

    if player.club != 0:
        club = game.clubs[player.club]

        # Requires logic for transfer status
        points = game.clubs[game.teamid].reputation - club.reputation
        points += random.randint(-3, 3)

        # Prevent club from selling/loaning if they do not meet minimum
        if check(negotiationid) != 0:
            news.publish("TE01", player=name, team=club.name)
        else:
            if negotiation.transfer_type == 0:
                if points <= 0:
                    negotiation.status = 1
                    negotiation.timeout = random.randint(1, 4)
                    news.publish("TO01", player=name, team=club.name)
                else:
                    negotiation.status = 2
                    news.publish("TO02", player=name, team=club.name)
            elif negotiation.transfer_type == 1:
                if points <= 0:
                    negotiation.status = 1
                    negotiation.timeout = random.randint(1, 4)
                    news.publish("LO01", player=name, team=club.name)
                else:
                    negotiation.status = 2
                    news.publish("LO02", player=name, team=club.name)
    else:
        # Free transfer
        points = random.randint(1, 3)  ## Needs proper AI

        if points <= 0:
            negotiation.status = 9
            news.publish("TO09", player=name)
        else:
            negotiation.status = 10
            negotiation.timeout = random.randint(1, 4)
            news.publish("TO10", player=name)


def consider_offer(negotiationid):
    negotiation = game.negotiations[negotiationid]

    player = game.players[negotiation.playerid]
    name = display.name(player, mode=1)
    club = game.clubs[player.club]

    points = random.randint(0, 10)  ## Needs replacing for proper AI

    if negotiation.transfer_type == 0:
        if negotiation.amount >= player.value * 1.1:
            negotiation.status = 5
            news.publish("TO05", player=name, team=club.name)
        else:
            negotiation.status = 4
            negotiation.timeout = random.randint(1, 4)
            news.publish("TO06", player=name, team=club.name)
    elif negotiation.transfer_type == 1:
        if points >= 0:
            negotiation.status = 5
            news.publish("LO04", player=name, team=club.name)
        else:
            negotiation.status = 4
            negotiation.timeout = random.randint(1, 4)
            news.publish("LO03", player=name, team=club.name)


def consider_contract(negotiationid):
    negotiation = game.negotiations[negotiationid]
    player = game.players[negotiation.playerid]
    name = display.name(player, mode=1)

    points = random.randint(0, 10)  ## Needs replacing for proper AI

    if negotiation.transfer_type == 0:
        club = game.clubs[player.club]

        if points >= 0:
            negotiation.status = 8
            news.publish("TO08", player=name)
        else:
            negotiation.status = 7
            negotiation.timeout = random.randint(1, 4)
            news.publish("TO07", player=name, team=club.name)
    elif negotiation.transfer_type == 2:
        if points >= 0:
            negotiation.status = 8
            news.publish("TO08", player=name)
        else:
            negotiation.status = 7
            negotiation.timeout = random.randint(1, 4)
            news.publish("TO10", player=name)


def transfer_enquiry_accepted(negotiationid):
    negotiation = game.negotiations[negotiationid]
    playerid = negotiation.playerid
    player = game.players[playerid]

    name = display.name(player, mode=1)
    club = game.clubs[player.club].name
    amount = game.players[playerid].value

    dialog = Gtk.Dialog()
    dialog.set_transient_for(game.window)
    dialog.set_title("Enquiry Accepted")
    dialog.set_border_width(5)
    dialog.add_button("_Withdraw", Gtk.ResponseType.REJECT)
    dialog.add_button("_Offer", Gtk.ResponseType.ACCEPT)
    dialog.set_default_response(Gtk.ResponseType.ACCEPT)

    grid = Gtk.Grid()
    grid.set_row_spacing(5)
    grid.set_column_spacing(5)
    dialog.vbox.add(grid)

    label = widgets.AlignedLabel("The offer for %s has been accepted.\n%s would like to negotiate a fee for the transfer." % (name, club))
    grid.attach(label, 0, 0, 2, 1)
    label = widgets.AlignedLabel("Enter the amount to offer for the player:")
    grid.attach(label, 0, 1, 1, 1)
    spinbuttonAmount = Gtk.SpinButton.new_with_range(0, 999999999, 100000)
    spinbuttonAmount.set_value(amount * 1.10)
    grid.attach(spinbuttonAmount, 1, 1, 1, 1)

    dialog.show_all()
    response = dialog.run()

    if response == Gtk.ResponseType.ACCEPT:
        if negotiation.transfer_type == 0:
            negotiation.status = 3
            negotiation.amount = spinbuttonAmount.get_value_as_int()
            negotiation.timeout = random.randint(1, 4)
        elif negotiation.transfer_type == 2:
            negotiation.status = 3
            negotiation.timeout = random.randint(1, 4)
    elif response == Gtk.ResponseType.REJECT:
        del(game.negotiations[negotiationid])

    dialog.destroy()


def transfer_offer_accepted(negotiationid):
    negotiation = game.negotiations[negotiationid]
    playerid = negotiation.playerid
    player = game.players[playerid]

    name = display.name(player, mode=1)
    wage = calculator.wage(playerid)
    wage = calculator.wage_rounder(wage)
    leaguewin, leaguerunnerup, winbonus, goalbonus = calculator.bonus(wage)

    dialog = Gtk.Dialog()
    dialog.set_title("Offer Accepted")
    dialog.set_transient_for(game.window)
    dialog.set_border_width(5)
    dialog.add_button("_Cancel", Gtk.ResponseType.CANCEL)
    dialog.add_button("_Offer", Gtk.ResponseType.OK)
    dialog.set_default_response(Gtk.ResponseType.OK)

    grid = Gtk.Grid()
    grid.set_row_spacing(5)
    grid.set_column_spacing(5)
    dialog.vbox.add(grid)

    if negotiation.transfer_type == 0:
        label = widgets.AlignedLabel("We are pleased to accept the offer for %s." % (name))
        grid.attach(label, 0, 0, 1, 1)

    label = widgets.AlignedLabel("%s has specified the following contract:" % (name))
    grid.attach(label, 0, 1, 1, 1)

    child_grid = Gtk.Grid()
    child_grid.set_row_spacing(5)
    child_grid.set_column_spacing(5)
    grid.attach(child_grid, 0, 2, 2, 1)

    label = widgets.AlignedLabel("Weekly Wage")
    child_grid.attach(label, 0, 0, 1, 1)
    spinbuttonWage = Gtk.SpinButton.new_with_range(0, 99999, 100)
    spinbuttonWage.set_value(wage)
    child_grid.attach(spinbuttonWage, 1, 0, 1, 1)
    label = widgets.AlignedLabel("League Champions Bonus")
    child_grid.attach(label, 0, 1, 1, 1)
    spinbuttonLeagueChampions = Gtk.SpinButton.new_with_range(0, 99999, 100)
    spinbuttonLeagueChampions.set_value(leaguewin)
    child_grid.attach(spinbuttonLeagueChampions, 1, 1, 1, 1)
    label = widgets.AlignedLabel("League Runner Up Bonus")
    child_grid.attach(label, 0, 2, 1, 1)
    spinbuttonLeagueRunnerUp = Gtk.SpinButton.new_with_range(0, 99999, 100)
    spinbuttonLeagueRunnerUp.set_value(leaguerunnerup)
    child_grid.attach(spinbuttonLeagueRunnerUp, 1, 2, 1, 1)
    label = widgets.AlignedLabel("Win Bonus")
    child_grid.attach(label, 0, 3, 1, 1)
    spinbuttonWinBonus = Gtk.SpinButton.new_with_range(0, 99999, 100)
    spinbuttonWinBonus.set_value(winbonus)
    child_grid.attach(spinbuttonWinBonus, 1, 3, 1, 1)
    label = widgets.AlignedLabel("Goal Bonus")
    child_grid.attach(label, 0, 4, 1, 1)
    spinbuttonGoalBonus = Gtk.SpinButton.new_with_range(0, 99999, 100)
    spinbuttonGoalBonus.set_value(goalbonus)
    child_grid.attach(spinbuttonGoalBonus, 1, 4, 1, 1)
    label = widgets.AlignedLabel("Contract Length")
    child_grid.attach(label, 0, 5, 1, 1)
    spinbuttonContract = Gtk.SpinButton.new_with_range(1, 5, 1)
    spinbuttonContract.set_value(3)
    child_grid.attach(spinbuttonContract, 1, 5, 1, 1)

    dialog.show_all()
    response = dialog.run()

    if response == Gtk.ResponseType.OK:
        leaguechampions = spinbuttonLeagueChampions.get_value_as_int()
        leaguerunnerup = spinbuttonLeagueRunnerUp.get_value_as_int()
        winbonus = spinbuttonWinBonus.get_value_as_int()
        goalbonus = spinbuttonGoalBonus.get_value_as_int()

        negotiation.wage = spinbuttonWage.get_value_as_int()
        negotiation.bonus = (leaguechampions, leaguerunnerup, winbonus, goalbonus)
        negotiation.contract = spinbuttonContract.get_value_as_int() * 52
        negotiation.status = 6
        negotiation.timeout = random.randint(1, 4)
    elif response == Gtk.ResponseType.CANCEL:
        del(game.negotiations[negotiationid])

    dialog.destroy()


def transfer_contract_accepted(negotiationid):
    negotiation = game.negotiations[negotiationid]
    playerid = negotiation.playerid
    player = game.players[playerid]

    name = display.name(player, mode=1)

    messagedialog = Gtk.MessageDialog(type=Gtk.MessageType.QUESTION)
    messagedialog.set_transient_for(game.window)
    messagedialog.set_title("Contract Accepted")
    messagedialog.add_button("C_ancel", Gtk.ResponseType.CANCEL)
    messagedialog.add_button("_Confirm", Gtk.ResponseType.OK)
    messagedialog.set_default_response(Gtk.ResponseType.OK)

    if negotiation.transfer_type == 0:
        club = display.club(player.club)
        amount = game.negotiations[negotiationid].amount
        messagedialog.set_markup("Confirm signing of %s from %s for %s?" % (name, club, amount))
    elif negotiation.transfer_type == 2:
        messagedialog.set_markup("Confirm signing of %s on free transfer?" % (name))

    response = messagedialog.run()

    if response == Gtk.ResponseType.OK:
        if check(negotiationid) == 0:
            move(negotiationid)

            if negotiation.transfer_type == 0:
                money.withdraw(amount, 13)
    elif response == Gtk.ResponseType.CANCEL:
        del(game.negotiations[negotiationid])

    messagedialog.destroy()


def loan_enquiry_accepted(negotiationid):
    def season_toggled(checkbutton):
        spinbuttonWeeks.set_sensitive(not checkbutton.get_active())

    playerid = game.negotiations[negotiationid].playerid
    player = game.players[playerid]
    name = display.name(player, mode=1)
    club = game.clubs[player.club].name
    amount = game.players[playerid].value

    dialog = Gtk.Dialog()
    dialog.set_transient_for(game.window)
    dialog.set_title("Loan Offer")
    dialog.set_border_width(5)
    dialog.add_button("_Withdraw", Gtk.ResponseType.REJECT)
    dialog.add_button("_Offer", Gtk.ResponseType.ACCEPT)
    dialog.set_default_response(Gtk.ResponseType.ACCEPT)

    grid = Gtk.Grid()
    grid.set_row_spacing(5)
    grid.set_column_spacing(5)
    dialog.vbox.add(grid)

    label = widgets.AlignedLabel("The offer for %s has been accepted.\n%s would like to arrange the details of the loan." % (name, club))
    grid.attach(label, 0, 0, 2, 1)

    checkbuttonSeason = Gtk.CheckButton("Season-Long Loan")
    checkbuttonSeason.set_active(True)
    checkbuttonSeason.connect("toggled", season_toggled)
    grid.attach(checkbuttonSeason, 0, 1, 2, 1)
    label = widgets.AlignedLabel("Number of weeks to loan:")
    grid.attach(label, 0, 2, 1, 1)
    spinbuttonWeeks = Gtk.SpinButton.new_with_range(1, len(constants.dates), 1)
    spinbuttonWeeks.set_value(4)
    spinbuttonWeeks.set_sensitive(False)
    grid.attach(spinbuttonWeeks, 1, 2, 1, 1)

    dialog.show_all()
    response = dialog.run()

    if response == Gtk.ResponseType.ACCEPT:
        if player.contract < spinbuttonWeeks.get_value_as_int():
            dialogs.error(14)

        game.negotiations[negotiationid].status = 3
        game.negotiations[negotiationid].timeout = random.randint(1, 4)

        if checkbuttonSeason.get_active():
            game.negotiations[negotiationid].weeks = -1
        else:
            game.negotiations[negotiationid].weeks = spinbuttonWeeks.get_value_as_int()
    elif response == Gtk.ResponseType.REJECT:
        del(game.negotiations[negotiationid])

    dialog.destroy()


def loan_offer_accepted(negotiationid):
    playerid = game.negotiations[negotiationid].playerid
    player = game.players[playerid]

    name = display.name(player, mode=1)
    club = game.clubs[player.club].name

    messagedialog = Gtk.MessageDialog(type=Gtk.MessageType.QUESTION)
    messagedialog.set_transient_for(game.window)
    messagedialog.set_title("Loan Accepted")
    messagedialog.add_button("_Cancel", Gtk.ResponseType.CANCEL)
    messagedialog.add_button("C_onfirm", Gtk.ResponseType.OK)
    messagedialog.set_default_response(Gtk.ResponseType.OK)
    messagedialog.set_markup("Confirm signing of %s from %s on loan?" % (name, club))

    response = messagedialog.run()

    if response == Gtk.ResponseType.OK:
        if check(negotiationid) == 0:
            move(negotiationid)
    elif response == Gtk.ResponseType.CANCEL:
        del(game.negotiations[negotiationid])

    messagedialog.destroy()


def transfer_enquiry_respond(negotiationid):
    negotiation = game.negotiations[negotiationid]
    club = game.clubs[negotiation.club].name
    player = game.players[negotiation.playerid]
    name = display.name(player, mode=1)

    dialog = Gtk.Dialog()
    dialog.set_border_width(5)
    dialog.set_transient_for(game.window)
    dialog.set_title("Transfer Enquiry")
    dialog.add_button("_Reject", Gtk.ResponseType.REJECT)
    dialog.add_button("_Accept", Gtk.ResponseType.ACCEPT)
    dialog.set_default_response(Gtk.ResponseType.REJECT)

    grid = Gtk.Grid()
    grid.set_row_spacing(5)
    grid.set_column_spacing(5)
    dialog.vbox.add(grid)

    label = widgets.AlignedLabel()
    label.set_markup("<b>%s</b> have submitted an enquiry for <b>%s</b>." % (club, name))
    label.set_use_markup(True)
    grid.attach(label, 0, 0, 3, 1)

    label = widgets.AlignedLabel()
    label.set_label("The enquiry can be rejected, or you can specify a fee to sell the player for?")
    grid.attach(label, 0, 1, 3, 1)

    label = widgets.AlignedLabel("Sale Amount")
    grid.attach(label, 0, 2, 1, 1)
    spinbuttonAmount = Gtk.SpinButton.new_with_range(0, 99999999, 100000)
    grid.attach(spinbuttonAmount, 1, 2, 1, 1)

    dialog.show_all()
    response = dialog.run()

    if response == Gtk.ResponseType.ACCEPT:
        negotiation.amount = spinbuttonAmount.get_value_as_int()
        negotiation.status = 1
        negotiation.timeout = random.randint(1, 4)
    else:
        del(game.negotiations[negotiationid])

    dialog.destroy()


def transfer_offer_respond(negotiationid):
    negotiation = game.negotiations[negotiationid]
    club = game.clubs[negotiation.club].name
    player = game.players[negotiation.playerid]
    name = display.name(player, mode=1)

    dialog = Gtk.Dialog()
    dialog.set_border_width(5)
    dialog.set_transient_for(game.window)
    dialog.set_title("Transfer Offer")
    dialog.add_button("_Reject", Gtk.ResponseType.REJECT)
    dialog.add_button("_Negotiate", Gtk.ResponseType.OK)
    dialog.add_button("_Accept", Gtk.ResponseType.ACCEPT)
    dialog.set_default_response(Gtk.ResponseType.REJECT)

    grid = Gtk.Grid()
    grid.set_row_spacing(5)
    grid.set_column_spacing(5)
    dialog.vbox.add(grid)

    label = widgets.AlignedLabel()
    label.set_label("<b>%s</b> have made an offer for <b>%s</b>." % (club, name))
    grid.attach(label, 0, 0, 2, 1)
    label = widgets.AlignedLabel()
    label.set_label("The club have offered:")
    grid.attach(label, 0, 1, 1, 1)
    spinbuttonAmount = Gtk.SpinButton.new_with_range(0, 99999999, 100000)
    spinbuttonAmount.set_value(player.value)
    grid.attach(spinbuttonAmount, 1, 1, 1, 1)

    dialog.show_all()
    response = dialog.run()

    if response == Gtk.ResponseType.ACCEPT:
        negotiation.status = 3
        negotiation.timeout = random.randint(1, 4)
    elif response == Gtk.ResponseType.OK:
        negotiation.status = 1
        negotiation.timeout = random.randint(1, 4)
    else:
        del(game.negotiations[negotiationid])

    dialog.destroy()


def transfer_confirm_respond(negotiationid):
    negotiation = game.negotiations[negotiationid]
    club = game.clubs[negotiation.club].name
    player = game.players[negotiation.playerid]
    name = display.name(player, mode=1)

    messagedialog = Gtk.MessageDialog()
    messagedialog.set_title("Transfer Completion")
    messagedialog.set_transient_for(game.window)
    messagedialog.add_button("C_ancel Transfer", Gtk.ResponseType.CANCEL)
    messagedialog.add_button("_Complete Transfer", Gtk.ResponseType.OK)
    messagedialog.set_markup("Complete transfer of %s to %s?" % (name, club))

    if messagedialog.run() == Gtk.ResponseType.OK:
        if check(negotiationid) == 0:
            move(negotiationid)
    else:
        del(game.negotiations[game.negotiationid])

    messagedialog.destroy()


def extend_loan(playerid):
    player = game.players[playerid]
    name = display.name(player, mode=1)

    dialog = Gtk.Dialog()
    dialog.set_title("Extend Loan")
    dialog.set_transient_for(game.window)
    dialog.set_border_width(5)
    dialog.add_button("_Cancel", Gtk.ResponseType.CANCEL)
    dialog.add_button("_Extend", Gtk.ResponseType.OK)
    dialog.set_default_response(Gtk.ResponseType.OK)

    grid = Gtk.Grid()
    grid.set_row_spacing(5)
    grid.set_column_spacing(5)
    dialog.vbox.add(grid)

    label = widgets.AlignedLabel("Extend loan deal for %s:" % (name))
    grid.attach(label, 0, 0, 3, 1)

    label = widgets.AlignedLabel("Period:")
    grid.attach(label, 0, 1, 1, 1)

    spinbutton = Gtk.SpinButton()
    spinbutton.set_range(0, len(constants.dates) - game.dateindex)
    spinbutton.set_value(4)
    spinbutton.set_increments(1, 1)
    grid.attach(spinbutton, 1, 1, 1, 1)

    dialog.show_all()

    if dialog.run() == Gtk.ResponseType.OK:
        state = consider_extension(playerid)

        if state:
            game.loans[playerid][1] += spinbutton.get_value_as_int()

    dialog.destroy()


def consider_extension(playerid):
    '''
    Determine whether the parent club of the player will agree to a
    loan extension.
    '''
    state = 0

    if game.loans[playerid][1] == -1:
        dialogs.error(11)
        state = 1
    else:
        points = 0

        if points <= 0:
            dialogs.error(11)
            state = 1

    return state


def end_loan(playerid):
    player = game.players[playerid]

    # Remove player from squad of loaned club
    game.clubs[player.club].squad.remove(playerid)

    # Remove from individual training if added
    if playerid in game.clubs[player.club].individual_training:
        del(game.clubs[player.club].individual_training[playerid])

    # Set club back to parent club
    player.club = game.loans[playerid][0]

    # Delete loan information
    del(game.loans[playerid])

    name = display.name(player, mode=1)
    club = game.clubs[player.club].name
    news.publish("LE01", player=name, team=club)


def process_loan():
    '''
    Decrement number of weeks remaining on loan, and return player to
    parent club if loan period has expired.
    '''
    for playerid, value in game.loans.items():
        if value[1] > 0:
            value[1] -= 1
        elif value[1] == 0:
            end_loan(playerid)

        player = game.players[playerid]
        name = display.name(player, mode=1)
        club = game.clubs[value[0]].name

        if value[1] in (12, 8, 4):
            news.publish("LA01", player=name, team=club, weeks=value[1])


def rejection(negotiationid, transfer, index):
    '''
    This function handles rejection of the enquiry, amount and contract
    steps of the negotiation.
    '''
    playerid = game.negotiations[negotiationid].playerid
    player = game.players[playerid]
    name = display.name(player, mode=1)

    message = (("Your enquiry into the availability of %s has been turned down, as the club does wish to transfer him at this moment in time." % (name), "The transfer negotiations for %s have broken down, as the club believe he is worth more than has been offered." % (name), "%s has rejected the contract offered to him as he wishes to stay at his current club." % (name)), ("The enquiry lodged into the loan availability of %s has been rejected as the club does not wish to loan him." % (name), "Negotiations for the loan move of %s have been cancelled as the club do not wish to loan for that length of time." % (name)))
    title = ("Transfer Offer", "Loan Offer")[transfer]

    messagedialog = Gtk.MessageDialog(type=Gtk.MessageType.INFO)
    messagedialog.set_transient_for(game.window)
    messagedialog.set_title(title)
    messagedialog.add_button("_Close", Gtk.ResponseType.CLOSE)
    messagedialog.set_markup(message[transfer][index])

    messagedialog.run()
    messagedialog.destroy()


def quick_sell(player):
    '''
    Find club to transfer quick sell player to, with a focus on finding
    a club of similar to the current owning club.
    '''
    selection = []

    current_reputation = game.clubs[player.club].reputation

    for clubid, club in game.clubs.items():
        if clubid != player.club:
            if current_reputation - 2 < club.reputation:
                selection.append(clubid)

    club = random.choice(selection)

    return club
