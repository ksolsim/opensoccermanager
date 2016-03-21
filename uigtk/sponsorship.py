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

import data


class Sponsorship(Gtk.MessageDialog):
    '''
    Base message dialog class for use by other Sponsorship dialogs.
    '''
    def __init__(self):
        Gtk.MessageDialog.__init__(self)
        self.set_transient_for(data.window)
        self.set_modal(True)
        self.set_title("Sponsorship")


class NoOffer(Sponsorship):
    '''
    Message dialog displayed when there is no sponsorship offer available.
    '''
    def __init__(self):
        Sponsorship.__init__(self)
        self.add_button("_Close", Gtk.ResponseType.CLOSE)
        self.set_markup("No sponsorship offers have recently been made to us.")
        self.connect("response", self.on_response)

        self.show()

    def on_response(self, *args):
        self.destroy()


class NegotiateOffer(Sponsorship):
    '''
    Message dialog when sponsorship offer is available for negotiation.
    '''
    def __init__(self):
        amount = data.currency.get_currency(data.user.club.sponsorship.offer.amount, integer=True)

        Sponsorship.__init__(self)
        self.add_button("_Reject Deal", Gtk.ResponseType.REJECT)
        self.add_button("_Accept Deal", Gtk.ResponseType.ACCEPT)
        self.set_default_response(Gtk.ResponseType.ACCEPT)
        self.set_markup("<span size='12000'><b>%s have made a %i year offer worth %s.</b></span>" % (data.user.club.sponsorship.offer.company, club.sponsorship.offer.period, amount))
        self.format_secondary_text("Do you wish to accept or reject this deal?")

    def show(self):
        response = self.run()

        state = -1

        if response == Gtk.ResponseType.ACCEPT:
            state = 1
        elif response == Gtk.ResponseType.REJECT:
            state = 0

        self.destroy()

        return state


class CurrentOffer(Sponsorship):
    '''
    Display message dialog when sponsorship offer is running.
    '''
    def __init__(self):
        if data.user.club.sponsorship.offer.period > 1:
            message = "The current sponsorship deal with %s will run for %i weeks." % (data.user.club.sponsorship.offer.company, data.user.club.sponsorship.offer.period)
        else:
            message = "The current sponsorship deal expires next week."

        Sponsorship.__init__(self)
        self.add_button("_Close", Gtk.ResponseType.CLOSE)
        self.set_markup(message)
        self.connect("response", self.on_response)

        self.show()

    def on_response(self, *args):
        self.destroy()
