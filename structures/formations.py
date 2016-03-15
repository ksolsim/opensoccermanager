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


class Formations:
    def __init__(self):
        self.formations = (("4-4-2", ("GK", "DL", "DR", "DC", "DC", "ML", "MR", "MC", "MC", "AS", "AS")),
                           ("3-5-2", ("GK", "DC", "DC", "DC", "ML", "MR", "MC", "MC", "MC", "AS", "AS")),
                           ("3-4-3", ("GK", "DC", "DC", "DC", "ML", "MR", "MC", "MC", "AS", "AS", "AS")),
                           ("4-5-1", ("GK", "DL", "DR", "DC", "DC", "ML", "MR", "MC", "MC", "MC", "AS")),
                           ("4-3-3", ("GK", "DL", "DR", "DC", "DC", "MC", "MC", "MC", "AS", "AS", "AS")),
                           ("5-4-1", ("GK", "DL", "DR", "DC", "DC", "DC", "ML", "MR", "MC", "MC", "AS")),
                           ("5-3-2", ("GK", "DL", "DR", "DC", "DC", "DC", "MC", "MC", "MC", "AS", "AS")),
                          )

    def get_formation_names(self):
        '''
        Return list of formation names.
        '''
        return [name[0] for name in self.formations]

    def get_formations(self):
        '''
        Return full tuple of formation information.
        '''
        return self.formations

    def get_formation_by_index(self, index):
        '''
        Return formation tuple of name and positions for given index.
        '''
        return self.formations[index]

    def get_name(self, formationid):
        '''
        Get name of formation in use for given formation id.
        '''
        return self.formations[formationid][0]

    def get_positions(self, formationid):
        '''
        Get tuple of formation positions for given formation id.
        '''
        return self.formations[formationid][1]
