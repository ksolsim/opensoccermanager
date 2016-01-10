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


class QuitDialog(Gtk.MessageDialog):
    '''
    Dialog displayed when quitting the game but no active game is running.
    '''
    def __init__(self):
        Gtk.MessageDialog.__init__(self)
        self.set_transient_for(data.window)
        self.set_modal(True)
        self.set_title("Quit Game")
        self.set_property("message-type", Gtk.MessageType.QUESTION)
        self.set_markup("Do you want to quit the game?")
        self.add_button("_Do Not Quit", Gtk.ResponseType.CANCEL)
        self.add_button("_Quit", Gtk.ResponseType.OK)
        self.set_default_response(Gtk.ResponseType.CANCEL)

    def show(self):
        self.run()


class UnsavedDialog(Gtk.MessageDialog):
    '''
    Dialog shown when quitting the game and an unsaved game may be lost.
    '''
    def __init__(self):
        Gtk.MessageDialog.__init__(self)
        self.set_transient_for(data.window)
        self.set_modal(True)
        self.set_title("Quit Game")
        self.set_property("message-type", Gtk.MessageType.QUESTION)
        self.set_markup("<span size='12000'><b>The game currently has unsaved data.</b></span>")
        self.format_secondary_text("Do you wish to save the game?")
        self.add_button("_Do Not Save", Gtk.ResponseType.REJECT)
        self.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("_Save Game", Gtk.ResponseType.ACCEPT)
        self.set_default_response(Gtk.ResponseType.ACCEPT)

    def show(self):
        self.run()
