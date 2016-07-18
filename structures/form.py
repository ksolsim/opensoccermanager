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


class Form:
    '''
    Club form object used to store characters for wins, losses, and draws.
    '''
    def __init__(self):
        self.form = []

    def add_form(self, form):
        '''
        Insert form character to list.
        '''
        self.form.append(form)

    def get_form(self):
        '''
        Return complete list of form strings.
        '''
        return self.form

    def get_form_for_length(self, length):
        '''
        Return form list for given required length.
        '''
        return self.form[-length:]

    def get_form_string_for_length(self, length):
        '''
        Return form listing in string form.
        '''
        return "".join(self.get_form_for_length(length))
