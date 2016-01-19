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


class Events:
    def __init__(self):
        self.club = data.clubs.get_club_by_id(data.user.team)

    def process_daily_events(self):
        '''
        Events processed each day.
        '''
        self.club.sponsorship.update_sponsorship()
        data.injury.increment_fitness()
        data.injury.generate_injuries()
        data.advertising.assistant_handled()
        self.club.tickets.check_season_ticket_availability()

    def process_weekly_events(self):
        '''
        Events processed at the end of each week.
        '''
        self.club.accounts.reset_weekly()
        self.club.finances.loan.update_interest_rate()
        self.club.finances.overdraft.update_interest_rate()
        data.players.update_contracts()
        self.club.pay_players()
        self.club.pay_staff()
        self.club.coaches.update_contracts()
        self.club.scouts.update_contracts()
        data.advertising.decrement_advertising()
        data.advertising.refresh_advertising()

    def process_monthly_events(self):
        '''
        Events processed at the end of each month.
        '''
        print("Monthly events")

    def process_end_of_season_events(self):
        '''
        Events processed at the end of each season.
        '''
        self.club.tickets.toggle_season_ticket_availability()
