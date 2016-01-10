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


class Training:
    def __init__(self):
        self.training = ("Attacking",
                         "Ball Skills",
                         "Corner Kicks",
                         "Crossing",
                         "Defending",
                         "Five-A-Side",
                         "Free Kicks",
                         "Gym",
                         "Long Ball",
                         "Moves",
                         "Offside Trap",
                         "Passing",
                         "Penalties",
                         "Set Pieces",
                         "Solo Runs",
                         "Throw-Ins")

    def get_training(self):
        '''
        Return full tuple of training names.
        '''
        return self.training
