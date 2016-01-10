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

import random

import data


class Companies:
    def __init__(self):
        self.companies = []

        self.populate_data()

    def get_random_company(self):
        '''
        Return a random company from the list of companies.
        '''
        return random.choice(self.companies)

    def get_companies(self):
        '''
        Return a complete list of company names.
        '''
        return self.companies

    def populate_data(self):
        data.database.cursor.execute("SELECT * FROM company")

        companies = data.database.cursor.fetchall()

        self.companies = [item[0] for item in companies]

