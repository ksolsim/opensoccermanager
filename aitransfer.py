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

import constants
import display
import game
import transfer


def identify():
    '''
    Identify players to purchase based on comparison to current squad.
    '''
    for clubid, club in game.clubs.items():
        if clubid != game.teamid:
            position = random.choice(constants.positions)

            other_average = 0
            squad_average = 0
            selected = 0

            potential = []

            for count, playerid in enumerate(game.clubs[clubid].squad, start=1):
                player = game.players[playerid]

                if position == player.position:
                    skills = player.skills()
                    squad_average += sum(skills) / count

                    if position == "GK":
                        squad_average = skills[0] * 2
                    elif position in ("DL", "DR", "DC", "D"):
                        squad_average = skills[1] * 2
                    elif position in ("ML", "MR", "MC", "M"):
                        squad_average = skills[2] * 2
                    elif position in ("AF", "AS"):
                        squad_average = skills[3] * 2

            for playerid, player in game.players.items():
                if position == player.position:
                    skills = player.skills()
                    other_average += sum(skills) / count

                    if position == "GK":
                        other_average = skills[0] * 2
                    elif position in ("DL", "DR", "DC", "D"):
                        other_average = skills[1] * 2
                    elif position in ("ML", "MR", "MC", "M"):
                        other_average = skills[2] * 2
                    elif position in ("AF", "AS"):
                        other_average = skills[3] * 2

                    if other_average > squad_average + 0 and other_average < squad_average + 100:
                        potential.append(playerid)

            if len(potential) > 0:
                playerid = random.choice(potential)

                negotiation = Negotiation()
                negotiation.negotiationid = game.negotiationid
                negotiation.playerid = playerid
                negotiation.club = clubid
                game.negotiations[game.negotiationid] = negotiation
                game.negotiationid += 1


class Negotiation:
    def __init__(self):
        self.negotiationid = 0
        self.playerid = 0
        self.status = 0
        self.timeout = 0
        self.transfer_type = 0
        self.club = 0
        self.date = "%i/%i/%i" % (game.year, game.month, game.date)

    def enquiry_response(self):
        '''
        Determine the response whether the selling club is willing to part with
        the player.
        '''
        club = game.clubs[self.club].name
        player = display.name(game.players[self.playerid], mode=1)

        messagedialog = Gtk.MessageDialog()
        messagedialog.set_transient_for(game.window)
        messagedialog.set_title("Transfer Enquiry")
        messagedialog.add_button("_Reject", Gtk.ResponseType.REJECT)
        messagedialog.add_button("_Accept", Gtk.ResponseType.ACCEPT)
        messagedialog.set_default_response(Gtk.ResponseType.ACCEPT)
        messagedialog.set_markup("<span size='12000'><b>%s have enquired as to the transfer of %s.</b></span>" % (club, player))
        messagedialog.format_secondary_text("Do you want to negotiate the transfer?")

        response = messagedialog.run()

        if response == Gtk.ResponseType.ACCEPT:
            self.timeout = random.randint(1, 4)
            self.status = 1
        elif response == Gtk.ResponseType.REJECT:
            self.cancel_transfer()

        messagedialog.destroy()

    def offer_response(self):
        '''
        Selling club response to the offer for the player.
        '''
        club = game.clubs[self.club].name
        amount = display.currency(self.amount)
        player = display.name(game.players[self.playerid], mode=1)

        dialog = Gtk.Dialog()
        dialog.set_transient_for(game.window)
        dialog.set_title("Transfer Offer")
        dialog.set_border_width(5)
        dialog.add_button("_Reject", Gtk.ResponseType.REJECT)
        dialog.add_button("_Negotiate", Gtk.ResponseType.OK)
        dialog.add_button("_Accept", Gtk.ResponseType.ACCEPT)
        dialog.set_default_response(Gtk.ResponseType.OK)

        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)
        dialog.vbox.add(grid)

        label = Gtk.Label()
        label.set_alignment(0, 0.5)
        label.set_markup("%s have offered <b>%s</b> for %s." % (club, amount, player))
        grid.attach(label, 0, 0, 3, 1)

        label = Gtk.Label("The offer can either be accepted, rejected or negotiations over the fee can continue.")
        label.set_alignment(0, 0.5)
        grid.attach(label, 0, 1, 3, 1)

        label = Gtk.Label("Fee to Negotiate:")
        grid.attach(label, 0, 2, 1, 1)
        spinbutton = Gtk.SpinButton.new_with_range(0, 25000000, 100000)
        spinbutton.set_value(self.amount)
        grid.attach(spinbutton, 1, 2, 1, 1)

        dialog.show_all()
        response = dialog.run()

        if response == Gtk.ResponseType.ACCEPT:
            self.timeout = random.randint(1, 4)
            self.status = 3
        elif response == Gtk.ResponseType.OK:
            self.timeout = random.randint(1, 4)
            self.status = 1
        elif response == Gtk.ResponseType.REJECT:
            self.cancel_transfer()

        dialog.destroy()

    def complete_transfer(self):
        '''
        Finialise the transfer move.
        '''
        player = display.name(game.players[self.playerid], mode=1)
        club = game.clubs[self.club].name

        messagedialog = Gtk.MessageDialog()
        messagedialog.set_transient_for(game.window)
        messagedialog.set_title("Complete Transfer")
        messagedialog.add_button("_Cancel Transfer", Gtk.ResponseType.CANCEL)

        if self.delay_allowed:
            messagedialog.add_button("_Delay Completion", 1)

        messagedialog.add_button("_Complete Transfer", Gtk.ResponseType.OK)
        messagedialog.set_markup("<span size='12000'><b>Complete transfer of %s to %s?</b></span>" % (player, club))
        messagedialog.format_secondary_text("The transfer can be delayed for a short time if necessary.")

        response = messagedialog.run()

        if response == Gtk.ResponseType.CANCEL:
            self.cancel_transfer()
        elif response == 1:
            self.delay_allowed = False
            self.timeout = random.randint(1, 4)
        elif response == Gtk.ResponseType.OK:
            self.move()

        messagedialog.destroy()

    def cancel_transfer(self):
        '''
        End the transfer negotiations and cleanup details.
        '''
        del game.negotiations[self.negotiationid]

    def move(self):
        '''
        Complete the player move and tidy data structures.
        '''
        player = game.players[self.playerid]
        old_club = game.clubs[player.club]
        new_club = game.clubs[self.club]

        # Remove player from squad and individual training
        old_club.squad.remove(self.playerid)

        if self.playerid in old_club.individual_training:
            del old_club.individual_training[self.playerid]

        player.not_for_sale = False

        # Set new club and add to squad
        player.club = self.club
        new_club.squad.append(self.playerid)

        name = display.name(player)

        if self.transfer_type != 2:
            new_club = new_club.name
        else:
            new_club = "N/A"

        if self.transfer_type == 0:
            old_club = old_club.name
            fee = display.value(self.amount)
        elif negotiation.transfer_type == 1:
            old_club = old_club.name
            fee = "Loan"
        elif self.transfer_type == 2:
            if player.club == 0:
                old_club = old_club.name
            else:
                old_club = ""

            fee = "Free Transfer"

        club = old_club
        season = "%i/%i" % (game.year, game.year + 1)
        games = "%i/%i" % (player.appearances, player.substitute)

        game.transfers.append([name, old_club, new_club, fee])
        player.history.append([season,
                               club,
                               games,
                               player.goals,
                               player.assists,
                               player.man_of_the_match])

        del game.negotiations[self.negotiationid]

    def update(self):
        '''
        Update the transfer negotiation timeout and status.
        '''
        if self.timeout > 0:
            self.timeout -= 1

            if self.timeout == 0:
                if self.status == 1:
                    self.amount = game.players[self.playerid].value
                    self.status = 2
                elif self.status == 3:
                    self.status = 4
                    self.delay_allowed = True

    def response(self):
        '''
        Handle appropriate response on status.
        '''
        if self.status == 0:
            self.enquiry_response()
        elif self.status == 2:
            self.offer_response()
        elif self.status == 4:
            self.complete_transfer()
