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
import dialogs
import display
import game
import news
import widgets


def transfer():
    '''
    Process transfer negotiations for each club, and update loan periods.
    '''
    for negotiation in game.negotiations.values():
        negotiation.update()

    for loan in game.loans.values():
        loan.update()


class Negotiation:
    def __init__(self):
        self.negotiationid = 0
        self.playerid = 0
        self.status = 0
        self.timeout = random.randint(1, 4)
        self.transfer_type = 0
        self.club = None
        self.date = game.date.get_string_date()

    def enquiry_initiate(self):
        '''
        Initiate transfer enquiry dialog for transfers, loans and free
        transfers.
        '''
        player = game.players[self.playerid]

        name = player.get_name(mode=1)
        club = player.get_club()

        dialog = Gtk.MessageDialog()
        dialog.set_transient_for(game.window)
        dialog.set_title("Transfer Enquiry")
        dialog.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        dialog.add_button("_Approach", Gtk.ResponseType.OK)
        dialog.set_default_response(Gtk.ResponseType.OK)

        infobar = Gtk.InfoBar()
        infobar.set_message_type(Gtk.MessageType.WARNING)
        dialog.get_message_area().add(infobar)

        label = Gtk.Label("%s is currently injured. He is expected to be out for %i weeks." % (name, player.injury_period))
        infobar.get_content_area().add(label)

        if self.transfer_type == 0:
            text = "Approach %s for the purchase of %s?" % (club, name)
        elif self.transfer_type == 1:
            text = "Approach %s for the loan of %s?" % (club, name)
        elif self.transfer_type == 2:
            text = "Approach %s for free transfer?" % (name)

        dialog.set_markup(text)

        visible = player.injury_period > 0
        infobar.set_visible(visible)

        state = False

        if dialog.run() == Gtk.ResponseType.OK:
            state = True

        dialog.destroy()

        return state

    def cancel_transfer(self):
        del game.negotiations[self.negotiationid]

    def response(self):
        if self.transfer_type == 0:
            if self.status == 1:
                self.rejection(transfer=0, index=0)
                del game.negotiations[self.negotiationid]
            elif self.status == 2:
                self.transfer_enquiry_accepted()
            elif self.status == 4:
                self.rejection(transfer=0, index=1)
                del game.negotiations[self.negotiationid]
            elif self.status == 5:
                self.transfer_offer_accepted()
            elif self.status == 7:
                self.rejection(transfer=0, index=2)
                del game.negotiations[self.negotiationid]
            elif self.status == 8:
                self.transfer_contract_accepted()
        elif self.transfer_type == 1:
            if self.status == 1:
                self.rejection(transfer=1, index=0)
                del game.negotiations[self.negotiationid]
            elif self.status == 2:
                self.loan_enquiry_accepted()
            elif self.status == 4:
                self.rejection(transfer=1, index=1)
                del game.negotiations[self.negotiationid]
            elif self.status == 5:
                self.loan_offer_accepted()
        elif self.transfer_type == 2:
            if self.status in (4, 7, 9):
                del game.negotiations[self.negotiationid]
            elif self.status == 10:
                self.transfer_offer_accepted()
            elif self.status == 8:
                self.transfer_contract_accepted()

    def transfer_enquiry_accepted(self):
        player = game.players[self.playerid]

        name = player.get_name(mode=1)
        club = player.get_club()

        dialog = Gtk.Dialog()
        dialog.set_transient_for(game.window)
        dialog.set_border_width(5)
        dialog.set_resizable(False)
        dialog.set_title("Enquiry Accepted")
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
        spinbuttonAmount.set_value(player.value * 1.10)
        grid.attach(spinbuttonAmount, 1, 1, 1, 1)

        dialog.show_all()
        response = dialog.run()

        if response == Gtk.ResponseType.ACCEPT:
            if self.transfer_type == 0:
                self.status = 3
                self.amount = spinbuttonAmount.get_value_as_int()
                self.timeout = random.randint(1, 4)
            elif self.transfer_type == 2:
                self.status = 3
                self.timeout = random.randint(1, 4)
        elif response == Gtk.ResponseType.REJECT:
            del game.negotiations[self.negotiationid]

        dialog.destroy()

    def transfer_offer_accepted(self):
        player = game.players[self.playerid]

        name = player.get_name(mode=1)
        wage = calculator.wage(self.playerid)
        wage = calculator.wage_rounder(wage)
        leaguewin, leaguerunnerup, winbonus, goalbonus = calculator.bonus(wage)

        dialog = Gtk.Dialog()
        dialog.set_transient_for(game.window)
        dialog.set_border_width(5)
        dialog.set_resizable(False)
        dialog.set_title("Offer Accepted")
        dialog.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        dialog.add_button("_Offer", Gtk.ResponseType.OK)
        dialog.set_default_response(Gtk.ResponseType.OK)

        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)
        dialog.vbox.add(grid)

        if self.transfer_type == 0:
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

            self.wage = spinbuttonWage.get_value_as_int()
            self.bonus = (leaguechampions, leaguerunnerup, winbonus, goalbonus)
            self.contract = spinbuttonContract.get_value_as_int() * 52
            self.status = 6
            self.timeout = random.randint(1, 4)
        elif response == Gtk.ResponseType.CANCEL:
            del game.negotiations[self.negotiationid]

        dialog.destroy()

    def transfer_contract_accepted(self):
        player = game.players[self.playerid]

        name = player.get_name(mode=1)

        messagedialog = Gtk.MessageDialog(type=Gtk.MessageType.QUESTION)
        messagedialog.set_transient_for(game.window)
        messagedialog.set_title("Contract Accepted")
        messagedialog.add_button("C_ancel", Gtk.ResponseType.CANCEL)
        messagedialog.add_button("_Confirm", Gtk.ResponseType.OK)
        messagedialog.set_default_response(Gtk.ResponseType.OK)

        if self.transfer_type == 0:
            club = player.get_club()
            messagedialog.set_markup("Confirm signing of %s from %s for %s?" % (name, club, self.amount))
        elif self.transfer_type == 2:
            messagedialog.set_markup("Confirm signing of %s on free transfer?" % (name))

        response = messagedialog.run()

        if response == Gtk.ResponseType.OK:
            if check(self.negotiationid) == 0:
                self.move()

                if self.transfer_type == 0:
                    game.clubs[game.teamid].accounts.withdraw(self.amount, "transfers")
        elif response == Gtk.ResponseType.CANCEL:
            del game.negotiations[self.negotiationid]

        messagedialog.destroy()

    def loan_enquiry_accepted(self):
        def season_toggled(checkbutton):
            spinbuttonWeeks.set_sensitive(not checkbutton.get_active())

        player = game.players[self.playerid]

        name = player.get_name(mode=1)
        club = player.get_club()

        dialog = Gtk.Dialog()
        dialog.set_transient_for(game.window)
        dialog.set_border_width(5)
        dialog.set_resizable(False)
        dialog.set_title("Loan Offer")
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

            self.status = 3
            self.timeout = random.randint(1, 4)

            if checkbuttonSeason.get_active():
                self.weeks = -1
            else:
                self.weeks = spinbuttonWeeks.get_value_as_int()
        elif response == Gtk.ResponseType.REJECT:
            del game.negotiations[self.negotiationid]

        dialog.destroy()

    def loan_offer_accepted(self):
        player = game.players[self.playerid]

        name = player.get_name(mode=1)
        club = player.get_club()

        messagedialog = Gtk.MessageDialog(type=Gtk.MessageType.QUESTION)
        messagedialog.set_transient_for(game.window)
        messagedialog.set_title("Loan Accepted")
        messagedialog.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        messagedialog.add_button("C_onfirm", Gtk.ResponseType.OK)
        messagedialog.set_default_response(Gtk.ResponseType.OK)
        messagedialog.set_markup("Confirm signing of %s from %s on loan?" % (name, club))

        response = messagedialog.run()

        if response == Gtk.ResponseType.OK:
            if check(self.negotiationid) == 0:
                self.move()
        elif response == Gtk.ResponseType.CANCEL:
            del game.negotiations[self.negotiationid]

        messagedialog.destroy()

    def rejection(self, transfer, index):
        '''
        Display details about negotiation being rejected.
        '''
        player = game.players[self.playerid]
        name = player.get_name(mode=1)

        message = (("Your enquiry into the availability of %s has been turned down, as the club does wish to transfer him at this moment in time." % (name),
                    "The transfer negotiations for %s have broken down, as the club believe he is worth more than has been offered." % (name),
                    "%s has rejected the contract offered to him as he wishes to stay at his current club." % (name)),
                   ("The enquiry lodged into the loan availability of %s has been rejected as the club does not wish to loan him." % (name),
                    "Negotiations for the loan move of %s have been cancelled as the club do not wish to loan for that length of time." % (name))
                  )
        title = ("Transfer Offer", "Loan Offer")[transfer]

        messagedialog = Gtk.MessageDialog(type=Gtk.MessageType.INFO)
        messagedialog.set_transient_for(game.window)
        messagedialog.set_title(title)
        messagedialog.add_button("_Close", Gtk.ResponseType.CLOSE)
        messagedialog.set_markup(message[transfer][index])

        messagedialog.run()
        messagedialog.destroy()

    def update(self):
        if self.timeout > 0:
            self.timeout -= 1

            if self.transfer_type != 2:
                if self.timeout == 0:
                    if self.status == 0:
                        consider_enquiry(self.negotiationid)
                    elif self.status == 3:
                        consider_offer(self.negotiationid)
                    elif self.status == 6 or self.status == 9:
                        consider_contract(self.negotiationid)
            else:
                if self.timeout == 0:
                    if self.status == 0:
                        consider_enquiry(self.negotiationid)
                    elif self.status == 6:
                        consider_contract(self.negotiationid)
        elif self.timeout == 0:
            if self.status in (1, 4, 7, 10):
                remove.append(self.negotiationid)

    def move(self):
        '''
        Move player between clubs when completing transfer, loan or free
        transfer.
        '''
        negotiation = game.negotiations[self.negotiationid]

        player = game.players[self.playerid]
        old_club = player.club
        new_club = negotiation.club

        # Remove from squad
        if negotiation.transfer_type == 0:
            game.clubs[old_club].squad.remove(self.playerid)
        elif negotiation.transfer_type == 1:
            loan = Loan()
            loan.playerid = self.playerid
            loan.parent_club = player.club
            loan.period = negotiation.weeks
            game.loans[self.playerid] = loan

            game.clubs[old_club].squad.remove(self.playerid)

        # Remove player from individual training
        if negotiation.transfer_type != 2:
            if self.playerid in game.clubs[old_club].individual_training:
                del game.clubs[old_club].individual_training[self.playerid]

        player.club = new_club

        if player.club:
            game.clubs[player.club].squad.append(self.playerid)

        # Reset transfer status
        player.transfer = [False, False]

        if negotiation.transfer_type in (0, 2):
            player.not_for_sale = False
        else:
            player.not_for_sale = True

        # Add player to list of transfers
        name = player.get_name()

        if negotiation.transfer_type != 2:
            new_club = game.clubs[new_club].name
        else:
            new_club = "N/A"

        if negotiation.transfer_type == 0:
            old_club = game.clubs[old_club].name
            fee = display.value(negotiation.amount)
        elif negotiation.transfer_type == 1:
            old_club = game.clubs[old_club].name
            fee = "Loan"
        elif negotiation.transfer_type == 2:
            old_club = ""
            fee = "Free Transfer"

        season = game.date.get_season()
        games = "%i/%i" % (player.appearances, player.substitute)

        game.transfers.append([name, old_club, new_club, fee])
        player.history.append([season,
                               old_club,
                               games,
                               player.goals,
                               player.assists,
                               player.man_of_the_match])

        del game.negotiations[self.negotiationid]


class Loan:
    def __init__(self):
        self.playerid = 0
        self.parent_club = None
        self.period = 0

    def update(self):
        '''
        Decrement number of weeks remaining on loan, and return player to
        parent club if loan period has expired.
        '''
        if self.period > 0:
            self.period -= 1

            if self.period in (4, 8, 12):
                player = game.players[self.playerid]
                name = player.get_name(mode=1)
                club = game.clubs[self.parent_club].name

                game.news.publish("LA01", player=name, team=club, weeks=self.period)
        else:
            self.end_loan()

    def extend_loan_valid(self):
        state = self.period != -1

        return state

    def extend_loan(self):
        '''
        Display dialog with the option for defining how long the player wishes to
        extend the loan period.
        '''
        player = game.players[self.playerid]
        name = player.get_name(mode=1)

        if self.extend_loan_valid():
            dialog = Gtk.Dialog()
            dialog.set_transient_for(game.window)
            dialog.set_border_width(5)
            dialog.set_resizable(False)
            dialog.set_title("Extend Loan")
            dialog.add_button("_Cancel", Gtk.ResponseType.CANCEL)
            dialog.add_button("_Extend", Gtk.ResponseType.OK)
            dialog.set_default_response(Gtk.ResponseType.OK)

            grid = Gtk.Grid()
            grid.set_row_spacing(5)
            grid.set_column_spacing(5)
            dialog.vbox.add(grid)

            label = widgets.AlignedLabel("Extend loan deal for %s." % (name))
            grid.attach(label, 0, 0, 3, 1)

            label = widgets.AlignedLabel("Period:")
            label.set_hexpand(False)
            grid.attach(label, 0, 1, 1, 1)

            spinbutton = Gtk.SpinButton()
            spinbutton.set_range(0, len(constants.dates) - game.dateindex)
            spinbutton.set_value(4)
            spinbutton.set_increments(1, 1)
            grid.attach(spinbutton, 1, 1, 1, 1)

            dialog.show_all()

            if dialog.run() == Gtk.ResponseType.OK:
                if consider_extension(self.playerid):
                    game.loans[self.playerid].period += spinbutton.get_value_as_int()

            dialog.destroy()
        else:
            messagedialog = Gtk.MessageDialog(type=Gtk.MessageType.INFO)
            messagedialog.set_transient_for(game.window)
            messagedialog.set_markup("%s is already on loan until the end of the season." % (name))
            messagedialog.add_button("_Close", Gtk.ResponseType.CLOSE)
            messagedialog.run()
            messagedialog.destroy()

    def cancel_loan(self):
        player = game.players[self.playerid]
        name = player.get_name(mode=1)

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

    def end_loan(self):
        '''
        Cleanup details of loan and reassign player back to parent club.
        '''
        player = game.players[self.playerid]

        # Remove player from squad of loaned club
        game.clubs[player.club].squad.remove(self.playerid)

        # Remove from individual training if added
        if self.playerid in game.clubs[player.club].individual_training:
            del game.clubs[player.club].individual_training[self.playerid]

        # Set club back to parent club
        player.club = self.parent_club

        name = player.get_name(mode=1)
        club = game.clubs[player.club].name
        game.news.publish("LE01", player=name, team=club)

        # Delete loan information
        del game.loans[self.playerid]


def make_enquiry(playerid, transfer_type):
    '''
    Construct the enquiry object for the appropriate transfer type, and generate
    a random timeout for when the response will be received.
    '''
    for negotiation in game.negotiations.values():
        if playerid == negotiation.playerid:
            if game.teamid == negotiation.club:
                dialogs.error(9)

                return

    negotiation = Negotiation()
    negotiation.negotiationid = game.negotiationid
    negotiation.playerid = playerid
    negotiation.club = game.teamid
    negotiation.transfer_type = transfer_type

    if negotiation.enquiry_initiate():
        game.negotiations[game.negotiationid] = negotiation

        game.negotiationid += 1
        game.clubs[game.teamid].shortlist.add(playerid)


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

    if negotiation.club != 0:
        if len(game.clubs[negotiation.club].squad) <= 16:
            error = 1
        elif len(game.clubs[negotiation.club].squad) >= 30:
            error = 2

    return error


def consider_enquiry(negotiationid):
    '''
    Take account of type of offer (purchase / loan) and determine
    whether transfer of player is acceptable based on remaining squad.
    '''
    negotiation = game.negotiations[negotiationid]
    player = game.players[negotiation.playerid]
    name = player.get_name(mode=1)

    if player.club:
        club = game.clubs[player.club]

        # Requires logic for transfer status
        points = game.clubs[game.teamid].reputation - club.reputation
        points += random.randint(-3, 3)

        # Prevent club from selling/loaning if they do not meet minimum
        if check(negotiationid) != 0:
            game.news.publish("TE01", player=name, team=club.name)
        else:
            if negotiation.transfer_type == 0:
                if points <= 0:
                    negotiation.status = 1
                    negotiation.timeout = random.randint(1, 4)
                    game.news.publish("TO01", player=name, team=club.name)
                else:
                    negotiation.status = 2
                    game.news.publish("TO02", player=name, team=club.name)
            elif negotiation.transfer_type == 1:
                if points <= 0:
                    negotiation.status = 1
                    negotiation.timeout = random.randint(1, 4)
                    game.news.publish("LO01", player=name, team=club.name)
                else:
                    negotiation.status = 2
                    game.news.publish("LO02", player=name, team=club.name)
    else:
        # Free transfer
        points = random.randint(1, 3)  ## Needs proper AI

        if points <= 0:
            negotiation.status = 9
            game.news.publish("TO09", player=name)
        else:
            negotiation.status = 10
            negotiation.timeout = random.randint(1, 4)
            game.news.publish("TO10", player=name)


def consider_offer(negotiationid):
    '''
    Determine whether the offer is suitable, and announce to the user whether it
    is or not.
    '''
    negotiation = game.negotiations[negotiationid]

    player = game.players[negotiation.playerid]
    name = player.get_name(mode=1)
    club = game.clubs[player.club]

    points = random.randint(0, 10)  ## Needs replacing for proper AI

    if negotiation.transfer_type == 0:
        if negotiation.amount >= player.value * 1.1:
            negotiation.status = 5
            game.news.publish("TO05", player=name, team=club.name)
        else:
            negotiation.status = 4
            negotiation.timeout = random.randint(1, 4)
            game.news.publish("TO06", player=name, team=club.name)
    elif negotiation.transfer_type == 1:
        if points >= 0:
            negotiation.status = 5
            game.news.publish("LO04", player=name, team=club.name)
        else:
            negotiation.status = 4
            negotiation.timeout = random.randint(1, 4)
            game.news.publish("LO03", player=name, team=club.name)


def consider_contract(negotiationid):
    '''
    Determine whether the contract offered is appropriate, and whether the
    player wishes to make the move.
    '''
    negotiation = game.negotiations[negotiationid]
    player = game.players[negotiation.playerid]
    name = player.get_name(mode=1)

    points = random.randint(0, 10)  ## Needs replacing for proper AI

    if negotiation.transfer_type == 0:
        club = game.clubs[player.club]

        if points >= 0:
            negotiation.status = 8
            game.news.publish("TO08", player=name)
        else:
            negotiation.status = 7
            negotiation.timeout = random.randint(1, 4)
            game.news.publish("TO07", player=name, team=club.name)
    elif negotiation.transfer_type == 2:
        if points >= 0:
            negotiation.status = 8
            game.news.publish("TO08", player=name)
        else:
            negotiation.status = 7
            negotiation.timeout = random.randint(1, 4)
            game.news.publish("TO10", player=name)


def consider_extension(playerid):
    '''
    Determine whether the parent club of the player will agree to a
    loan extension.
    '''
    state = True

    return state
