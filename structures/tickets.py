#!/usr/bin/env python3

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
