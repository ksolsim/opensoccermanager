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


class Speciality:
    def __init__(self):
        self.speciality = {0: "Goalkeeping",
                           1: "Defensive",
                           2: "Midfield",
                           3: "Attacking",
                           4: "Fitness",
                           5: "All"}

    def get_specialities(self):
        '''
        Return full set of specialities.
        '''
        return self.speciality

    def get_speciality_for_id(self, specialityid):
        '''
        Return speciality for given id value.
        '''
        return self.speciality[specialityid]


class Categories:
    def __init__(self):
        self.speciality = {0: ("Keeping",),
                           1: ("Tackling", "Stamina"),
                           2: ("Passing", "Ball Control"),
                           3: ("Shooting",),
                           4: ("Fitness", "Pace", "Stamina"),
                           5: ("All",)}

    def get_category_label(self, index):
        '''
        Get category labels for display in individual training dialog.
        '''
        categories = self.speciality[index]

        if len(categories) > 1:
            return ", ".join(item for item in categories)
        else:
            return categories[0]
