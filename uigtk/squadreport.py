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


class SquadReport(Gtk.Dialog):
    def __init__(self):
        Gtk.Dialog.__init__(self)
        self.set_title("Squad Report")
        self.set_border_width(5)
        self.set_resizable(False)
        self.set_size_request(240, 240)
        self.set_transient_for(window.window)
        self.add_button("_Close", Gtk.ResponseType.CLOSE)

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_vexpand(True)
        scrolledwindow.set_policy(Gtk.PolicyType.NEVER,
                                  Gtk.PolicyType.AUTOMATIC)
        self.vbox.add(scrolledwindow)

        textview = Gtk.TextView()
        textview.set_editable(False)
        textview.set_cursor_visible(False)
        self.textbuffer = textview.get_buffer()
        scrolledwindow.add(textview)

    def display(self, errors):
        if errors.team_count < 11:
            self.textbuffer.insert_at_cursor("Not enough players selected. Currently there are %i players selected.\n\n" % (errors.team_count), -1)

        if len(errors.injuries) > 0:
            for player in errors.injuries:
                name = player.get_name(mode=1)
                self.textbuffer.insert_at_cursor("%s is unavailable for selection due to injury.\n" % (name), -1)

            self.textbuffer.insert_at_cursor("\n")

        if len(errors.suspensions) > 0:
            for player in errors.suspensions:
                name = player.get_name(mode=1)
                self.textbuffer.insert_at_cursor("%s is unavailable for selection due to suspension.\n" % (name), -1)

        self.show_all()
        self.run()
        self.destroy()
