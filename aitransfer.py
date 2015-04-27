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


def transfer():
    '''
    Process AI initiated transfers. Player initiated transfer are currently
    handled by transfer.transfer().
    '''
    remove = []

    for negotiationid, negotiation in game.negotiations.items():
        if negotiationid != game.teamid:
            negotiation.update()


class Negotiation:
    def __init__(self):
        self.playerid = 0
        self.status = 0
        self.timeout = 0
        self.transfer_type = 0
        self.club = 0
        self.date = "%i/%i/%i" % (game.year, game.month, game.date)
        self.timeout = 0

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

    def offer_initialise(self):
        '''
        Set the offer details for the transfer.
        '''

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

        label = Gtk.Label("The offer can either be accepted or negotiations over the fee can continue.")
        label.set_alignment(0, 0.5)
        grid.attach(label, 0, 1, 3, 1)

        label = Gtk.Label("Fee to Negotiate:")
        grid.attach(label, 0, 2, 1, 1)
        spinbutton = Gtk.SpinButton.new_with_range(0, 25000000, 100000)
        spinbutton.set_value(self.amount)
        grid.attach(spinbutton, 1, 2, 1, 1)

        dialog.show_all()
        response = dialog.run()

        if response == Gtk.ResponseType.REJECT:
            self.cancel_transfer()

        dialog.destroy()

    def offer_negotiate(self):
        '''
        Negotiate the transfer fee for the player.
        '''

    def contract_initialise(self):
        '''
        Offer a contract to the player (transfer or free transfer only).
        '''

    def contract_response(self):
        '''
        Player response to the contract offer.
        '''

    def complete_transfer(self):
        '''
        Finialise the transfer move.
        '''

    def cancel_transfer(self):
        '''
        End the transfer negotiations and cleanup details.
        '''
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
                    self.timeout = random.randint(1, 4)
                    self.status = 2

    def response(self):
        if self.status == 0:
            self.enquiry_response()
        elif self.status == 2:
            self.offer_response()
