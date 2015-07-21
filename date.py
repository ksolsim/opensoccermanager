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


import ai
import constants
import evaluation
import events
import game
import staff
import transfer


class Date:
    def __init__(self):
        self.year = 2014
        self.month = 8
        self.day = 1

        self.week = 1

        self.fixturesindex = 0  # Index number of which fixture the game is on
        self.eventindex = 0     # Position in relation to events
        self.dateindex = 1      # Position in relation to dates
        self.dateprev = 0

    def get_string_date(self):
        '''
        Return the current date as a YY/MM/DD string.
        '''
        date = "%i/%i/%i" % (self.year, self.month, self.day)

        return date

    def get_date(self):
        '''
        Return the current date as a tuple.
        '''
        date = self.year, self.month, self.day

        return date

    def end_of_season(self):
        '''
        Set the current date to the first day of a season.
        '''
        self.month = 8
        self.day = 1

    def end_of_year(self):
        '''
        Update the date for the start of a new year.
        '''
        self.year += 1
        self.month = 1
        self.day = 1

    def get_season(self):
        '''
        Return the season as a string.
        '''
        season = "%i/%i" % (self.year, self.year + 1)

        return season

    def increment_date(self):
        '''
        Move to the next date.
        '''
        self.day = constants.dates[game.date.week - 1][self.dateindex]

        if game.date.dateprev > self.day:
            self.dateprev = 0

            if self.month == 12:
                self.end_of_year()
            else:
                self.month += 1

        if len(constants.dates[self.week - 1]) - 1 > self.dateindex:
            self.dateindex += 1
        else:
            self.weekly_events()
            self.dateprev = self.day
            self.dateindex = 0
            self.week += 1

        self.daily_events()

        widgets.date.update()
        widgets.nextmatch.update()

    def daily_events(self):
        '''
        Process events on each continue game operation.
        '''
        transfer.transfer()
        events.injury_generation()
        ai.advertising()
        evaluation.update()
        aitransfer.identify()
        staff.check_morale()
        ai.transfer_list()
        ai.loan_list()

        # Initiate sponsorship generation if needed
        if (game.date.day, game.date.month) == (4, 8):
            club = game.clubs[game.teamid]

            if club.sponsorship.status == 0:
                club.sponsorship.generate()

        # Stop sale of season tickets and deposit earnings
        if (game.date.day, game.date.month) == (16, 8):
            for club in game.clubs.values():
                club.set_season_tickets_unavailable()

            game.clubs[game.teamid].tickets.calculate_season_tickets()

        # Player value adjustments
        for playerid, player in game.players.items():
            player.value = calculator.value(playerid)

    def weekly_events(self):
        '''
        Process events once the end of the week is reached.
        '''
        club = game.clubs[game.teamid]

        club.accounts.reset_weekly()
        club.team_training.update()
        events.update_contracts()
        events.update_advertising()
        club.sponsorship.update()
        events.refresh_staff()
        events.individual_training()
        ai.renew_contract()
        events.injury_period()
        events.update_condition()
        club.perform_maintenance()
        game.flotation.complete_float()
        game.bankloan.repay_loan()
        game.bankloan.update_interest_rate()
        game.overdraft.pay_overdraft()
        game.overdraft.update_interest_rate()
        game.grant.update_grant()

        for club in game.clubs.values():
            club.pay_wages()
