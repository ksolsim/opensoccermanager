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


import data


class Tickets:
    def __init__(self):
        self.tickets = None
        self.school_tickets = 0
        self.season_tickets = 0
        self.season_tickets_available = True

    def set_initial_school_tickets(self):
        '''
        Set initial number of school tickets to be made available.
        '''
        club = data.clubs.get_club_by_id(data.user.team)
        self.school_tickets = 100 * (int((20 - club.reputation) * 0.5) + 1)

    def set_initial_season_tickets(self):
        '''
        Return percentage capacity allocted to season tickets.
        '''
        club = data.clubs.get_club_by_id(data.user.team)
        self.season_tickets = 40 + club.reputation
