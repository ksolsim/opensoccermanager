#!/usr/bin/env python3

from gi.repository import Gtk

import data


class Sponsorship(Gtk.MessageDialog):
    '''
    Base message dialog class for use by other Sponsorship dialogs.
    '''
    def __init__(self):
        Gtk.MessageDialog.__init__(self)
        self.set_transient_for(data.window)
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
        club = data.clubs.get_club_by_id(data.user.team)
        amount = data.currency.get_currency(club.sponsorship.offer.amount, integer=True)

        Sponsorship.__init__(self)
        self.add_button("_Reject Deal", Gtk.ResponseType.REJECT)
        self.add_button("_Accept Deal", Gtk.ResponseType.ACCEPT)
        self.set_default_response(Gtk.ResponseType.ACCEPT)
        self.set_markup("<span size='12000'><b>%s have made a %i year offer worth %s.</b></span>" % (club.sponsorship.offer.company, club.sponsorship.offer.period, amount))
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
        club = data.clubs.get_club_by_id(data.user.team)

        if club.sponsorship.offer.period > 1:
            message = "The current sponsorship deal with %s will run for %i weeks." % (club.sponsorship.offer.company, club.sponsorship.offer.period)
        else:
            message = "The current sponsorship deal expires next week."

        Sponsorship.__init__(self)
        self.add_button("_Close", Gtk.ResponseType.CLOSE)
        self.set_markup(message)
        self.connect("response", self.on_response)

        self.show()

    def on_response(self, *args):
        self.destroy()
