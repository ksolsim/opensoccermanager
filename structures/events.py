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
    def process_daily_events(self):
        '''
        Events processed each day.
        '''
        data.user.club.tickets.check_season_ticket_availability()
        data.user.club.sponsorship.update_sponsorship()
        data.injury.increment_fitness()
        data.injury.generate_injuries()
        data.advertising.assistant_handled()
        data.negotiations.update_negotiations()

    def process_weekly_events(self):
        '''
        Events processed at the end of each week.
        '''
        data.user.club.accounts.reset_weekly()
        data.user.club.finances.loan.update_interest_rate()
        data.user.club.finances.overdraft.update_interest_rate()
        data.user.club.pay_players()
        data.user.club.pay_staff()
        data.user.club.coaches.update_contracts()
        data.user.club.scouts.update_contracts()
        data.user.club.team_training.update_schedule()
        data.user.club.individual_training.individual_training_event()
        data.user.club.stadium.update_condition()
        data.players.update_contracts()
        data.injury.injury_recovery()
        data.advertising.decrement_advertising()
        data.advertising.refresh_advertising()
        data.purchase_list.refresh_list()
        data.loan_list.refresh_list()

    def process_monthly_events(self):
        '''
        Events processed at the end of each month.
        '''

    def process_end_of_season_events(self):
        '''
        Events processed at the end of each season.
        '''
        data.user.club.tickets.toggle_season_ticket_availability()

        data.date.set_end_of_season()

    def process_end_of_match_events(self, fixture):
        '''
        Events processed at the end of a match.
        '''
        if fixture.result[0] > fixture.result[1]:
            fixture.home.club.tactics.pay_bonus()
        elif fixture.result[0] < fixture.result[1]:
            fixture.away.club.tactics.pay_bonus()

        fixture.referee.increment_statistics(fixture)

        fixture.store_team_selection()
        fixture.pay_televised_money()

        fixture.played = True
