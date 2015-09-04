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

import uigtk.window
import user


class Sponsorship(Gtk.MessageDialog):
    def __init__(self):
        Gtk.MessageDialog.__init__(self)
        self.set_transient_for(uigtk.window.window)
        self.set_title("Sponsorship")
        self.connect("response", self.on_response)

    def on_response(self, dialog, response):
        club = user.get_user_club()

        if response == Gtk.ResponseType.ACCEPT:
            club.sponsorship.accept()
        elif response == Gtk.ResponseType.REJECT:
            club.sponsorship.reject()

        self.destroy()

    def display(self):
        club = user.get_user_club()

        if club.sponsorship.status in (0, 2):
            if club.sponsorship.status == 0:
                self.set_markup("There are currently no sponsorship offers available.")
            elif club.sponsorship.status == 2:
                company, period, amount = club.sponsorship.get_details()

                if period > 1:
                    self.set_markup("The current sponsorship deal with %s runs for %i years." % (company, period))
                else:
                    self.set_markup("The current sponsorship deal with %s runs until the end of the season." % (company, period))

            self.add_button("_Close", Gtk.ResponseType.CLOSE)
        elif club.sponsorship.status == 1:
            company, period, amount = club.sponsorship.get_details()

            self.set_markup("<span size='12000'><b>%s have made a sponsorship offer to the club.</b></span>" % (company))

            if period > 1:
                self.format_secondary_text("The deal is for %i years and is worth %s." % (period, amount))
            else:
                self.format_secondary_text("The deal is for %i year and is worth %s." % (period, amount))

            self.add_button("_Accept", Gtk.ResponseType.ACCEPT)
            self.add_button("_Reject", Gtk.ResponseType.REJECT)

        self.show_all()
