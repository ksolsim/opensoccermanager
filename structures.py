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


import operator

import accounts
import advertising
import ai
import aitransfer
import calculator
import catering
import club
import constants
import display
import evaluation
import events
import fixtures
import game
import merchandise
import nation
import player
import preferences
import shortlist
import standings
import tactics
import teamtraining
import tickets
import transfer
import widgets


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


class Player:
    def __init__(self):
        self.common_name = None
        self.fitness = 100
        self.training_points = 0
        self.morale = 20
        self.injury_type = 0
        self.injury_period = 0
        self.suspension_points = 0
        self.suspension_type = 0
        self.suspension_period = 0
        self.yellow_cards = 0
        self.red_cards = 0
        self.transfer = [False, False]
        self.not_for_sale = False
        self.appearances = 0
        self.substitute = 0
        self.missed = 0
        self.goals = 0
        self.assists = 0
        self.man_of_the_match = 0
        self.rating = []
        self.history = player.History()

    def get_skills(self):
        '''
        Return tuple of skill attributes for the player.
        '''
        values = (self.keeping,
                  self.tackling,
                  self.passing,
                  self.shooting,
                  self.heading,
                  self.pace,
                  self.stamina,
                  self.ball_control,
                  self.set_pieces,
                 )

        return values

    def get_name(self, mode=0):
        '''
        Return the player name in the requested format.
        '''
        if self.common_name:
            name = self.common_name
        else:
            if mode == 0:
                name = "%s, %s" % (self.second_name, self.first_name)
            elif mode == 1:
                name = "%s %s" % (self.first_name, self.second_name)

        return name

    def get_age(self):
        '''
        Determine the player age relative to current in-game date.
        '''
        year, month, day = self.date_of_birth.split("-")
        age = game.date.year - int(year)

        if (game.date.month, game.date.day) < (int(month), int(day)):
            age -= 1

        return age

    def get_club(self):
        '''
        Return the club name, or none if player is without a contract.
        '''
        if self.club:
            name = club.clubitem.clubs[self.club].name
        else:
            name = ""

        return name

    def get_nationality(self):
        '''
        Return the player nationality.
        '''
        name = nation.get_nation(self.nationality)

        return name

    def get_value(self):
        '''
        Retrieve the player value formatted with currency.
        '''
        value = calculator.value_rounder(self.value)
        currency, exchange = constants.currency[preferences.preferences.currency]

        if value >= 1000000:
            amount = (value / 1000000) * exchange
            value = "%s%.1fM" % (currency, amount)
        elif value >= 1000:
            amount = (value / 1000) * exchange
            value = "%s%iK" % (currency, amount)

        return value

    def get_wage(self):
        '''
        Fetch the player wage and return with appropriate currency.
        '''
        wage = calculator.wage_rounder(self.wage)
        currency, exchange = constants.currency[preferences.preferences.currency]

        if wage >= 1000:
            amount = (wage / 1000) * exchange
            wage = "%s%.1fK" % (currency, amount)
        elif wage >= 100:
            amount = wage * exchange
            wage = "%s%i" % (currency, amount)

        return wage

    def get_contract(self):
        '''
        Format the number of weeks on the contract remaining and return.
        '''
        if self.contract > 1:
            contract = "%i Weeks" % (self.contract)
        elif self.contract == 1:
            contract = "%i Week" % (self.contract)
        elif self.contract == 0:
            contract = "Out of Contract"

        return contract

    def set_morale(self, amount):
        '''
        Set the morale of the player between -100 and 100.
        '''
        self.morale += amount

        if self.morale > 100:
            self.morale = 100
        elif self.morale < -100:
            self.morale = -100

    def get_morale(self):
        '''
        Return the string indicating the players morale value.
        '''
        status = ""

        if self.morale >= 85:
            status = constants.morale[8]
        elif self.morale >= 70:
            status = constants.morale[7]
        elif self.morale >= 45:
            status = constants.morale[6]
        elif self.morale >= 20:
            status = constants.morale[5]
        elif self.morale >= 0:
            status = constants.morale[4]
        elif self.morale >= -25:
            status = constants.morale[3]
        elif self.morale >= -50:
            status = constants.morale[2]
        elif self.morale >= -75:
            status = constants.morale[1]
        elif self.morale >= -100:
            status = constants.morale[0]

        return status

    def get_appearances(self):
        '''
        Get number of appearances and substitute appearances.
        '''
        appearances = "%i (%i)" % (self.appearances, self.substitute)

        return appearances

    def get_cards(self):
        '''
        Get number of yellow and red cards.
        '''
        cards = "%i/%i" % (self.yellow_cards, self.red_cards)

        return cards

    def get_injury(self):
        '''
        Return number of weeks out injured.
        '''
        if self.injury_period == 1:
            injury = "%i Week" % (self.injury_period)
        else:
            injury = "%i Weeks" % (self.injury_period)

        return injury

    def get_suspension(self):
        '''
        Return number of matches out suspended.
        '''
        if self.suspension_period == 1:
            suspension = "%i Match" % (self.suspension_period)
        else:
            suspension = "%i Matches" % (self.suspension_period)

        return suspension

    def get_rating(self):
        '''
        Display the average player rating.
        '''
        if self.rating != []:
            average = sum(self.rating) / float(len(self.rating))
            rating = "%.1f" % (average)
        else:
            rating = "0.0"

        return rating

    def renew_contract(self):
        '''
        Determine whether player will agree on a contract renewal.
        '''
        points = self.morale

        overall = evaluation.calculate_overall()
        points += overall - 25

        state = points >= 0

        return state


class Stand:
    def __init__(self):
        self.capacity = 0
        self.seating = False
        self.roof = False


class Team:
    def __init__(self):
        self.teamid = None
        self.name = ""
        self.team = {}
        self.substitutes = {}
        self.shots_on_target = 0
        self.shots_off_target = 0
        self.throw_ins = 0
        self.corner_kicks = 0
        self.free_kicks = 0
        self.penalty_kicks = 0
        self.fouls = 0
        self.yellow_cards = 0
        self.red_cards = 0
        self.possession = 0


class Cards:
    def __init__(self):
        self.yellow_cards = 0
        self.red_cards = 0
        self.points = 0


class Statistics:
    def __init__(self):
        self.yellows = 0
        self.reds = 0

        self.win = (None, ())
        self.loss = (None, ())

        self.record = []

    def update(self, result):
        '''
        Update statistical information with result.
        '''
        score = result.final_score

        if result.clubid1 == game.teamid:
            if score[0] > score[1]:
                if score > self.win[1]:
                    self.win = (result.clubid2, score)
            elif score[1] > score[0]:
                if score > self.loss[1]:
                    self.loss = (result.clubid2, score)
        elif result.clubid2 == game.teamid:
            if score[0] < score[1]:
                if score > self.win[1]:
                    self.win = (result.clubid1, score)
            elif score[1] < score[0]:
                if score > self.loss[1]:
                    self.loss = (result.clubid1, score)

        self.yellows += result.yellows
        self.reds += result.reds

    def reset_statistics(self):
        '''
        Save current statistics and reset to default for new season.
        '''
        position = game.standings.find_position(game.teamid)
        position = display.format_position(position)
        season = game.date.get_season()

        details = game.standings.clubs[game.teamid]

        record = (season,
                  details.played,
                  details.wins,
                  details.draws,
                  details.losses,
                  details.goals_for,
                  details.goals_against,
                  details.goal_difference,
                  details.points,
                  position
                 )

        self.record.insert(0, record)

        self.yellows = 0
        self.reds = 0

        self.win = (None, ())
        self.loss = (None, ())
