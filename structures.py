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
import operator
import statistics

import accounts
import advertising
import ai
import aitransfer
import business
import calculator
import catering
import constants
import data
import database
import dialogs
import display
import evaluation
import events
import fileio
import finances
import fixtures
import game
import information
import interface
import match
import menu
import merchandise
import money
import music
import nation
import player
import preferences
import printing
import sales
import shortlist
import squad
import stadium
import staff
import structures
import tactics
import team
import training
import transfer
import version
import view
import widgets


class Date:
    def __init__(self):
        self.year = 2014
        self.month = 8
        self.day = 1
        self.season = "2014/2015"

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

    def increment_season(self):
        '''
        Adjust the season attribute for new season.
        '''
        self.season = "%i/%i" % (self.year, self.year + 1)

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
        events.injury()
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

            sales.season_tickets()

        # Player value adjustments
        for playerid, player in game.players.items():
            player.value = calculator.value(playerid)

    def weekly_events(self):
        '''
        Process events once the end of the week is reached.
        '''
        club = game.clubs[game.teamid]

        club.accounts.reset_weekly()
        events.update_contracts()
        events.update_advertising()
        club.sponsorship.update()
        events.refresh_staff()
        events.team_training()
        events.individual_training()
        ai.renew_contract()
        events.injury_period()
        events.update_condition()
        club.perform_maintenance()
        money.float_club()
        money.pay_overdraft()
        money.pay_loan()
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
        Return the club name, or none if uncontracted.
        '''
        if self.club:
            club = game.clubs[self.club].name
        else:
            club = ""

        return club

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
        if amount > 0:
            if self.morale + amount <= 100:
                self.morale += amount
            elif self.morale + amount > 100:
                self.morale = 100
        elif amount < 0:
            if self.morale + amount >= -100:
                self.morale += amount
            elif self.morale + amount < -100:
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
            rating = "%.1f" % (statistics.mean(self.rating))
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


class Club:
    def __init__(self):
        self.reputation = 0
        self.squad = []
        self.team = {}
        self.tactics = tactics.Tactics()
        self.coaches_available = {}
        self.coaches_hired = {}
        self.scouts_available = {}
        self.scouts_hired = {}
        self.shortlist = shortlist.Shortlist()
        self.team_training = TeamTraining()
        self.individual_training = {}
        self.tickets = Tickets()
        self.accounts = accounts.Accounts()
        self.sponsorship = advertising.Sponsorship()
        self.hoardings = advertising.Advertising()
        self.programmes = advertising.Advertising()
        self.merchandise = merchandise.Merchandise()
        self.catering = catering.Catering()
        self.evaluation = [0, 0, 0, 0, 0]
        self.form = []
        self.attendances = []

    def get_stadium_name(self):
        '''
        Return the stadium name.
        '''
        stadium = game.stadiums[self.stadium].name

        return stadium

    def perform_maintenance(self):
        '''
        Calculate the cost of stadium and building maintenance.
        '''
        cost = calculator.maintenance()

        self.accounts.withdraw(cost, "stadium")

    def set_advertising_spaces(self):
        '''
        Set the maximum allowed advertising spaces.
        '''
        self.hoardings.maximum = 48

        if self.reputation > 10:
            self.programmes.maximum = 36
        else:
            self.programmes.maximum = 24

    def set_ticket_prices(self):
        '''
        Set initial ticket prices.
        '''
        self.tickets.tickets[0] = 1 + self.reputation
        self.tickets.tickets[1] = 1 + self.reputation + (self.reputation * 0.25)
        self.tickets.tickets[2] = (1 + self.reputation) * 15
        self.tickets.tickets[3] = 2 + self.reputation
        self.tickets.tickets[4] = 2 + self.reputation + (self.reputation * 0.25)
        self.tickets.tickets[5] = (2 + self.reputation) * 15
        self.tickets.tickets[6] = 3 + self.reputation
        self.tickets.tickets[7] = 3 + self.reputation + (self.reputation * 0.25)
        self.tickets.tickets[8] = (3 + self.reputation) * 15
        self.tickets.tickets[9] = 4 + self.reputation
        self.tickets.tickets[10] = 4 + self.reputation + (self.reputation * 0.25)
        self.tickets.tickets[11] = (4 + self.reputation) * 15
        self.tickets.tickets[12] = 30 + self.reputation
        self.tickets.tickets[13] = 30 + self.reputation + (self.reputation * 0.25)
        self.tickets.tickets[14] = (30 + self.reputation) * 15

        self.tickets.tickets = list(map(int, self.tickets.tickets))

    def set_season_ticket_percentage(self):
        '''
        Set initial percentage of stadium available for season ticket sales.
        '''
        self.tickets.season_tickets = 40 + self.reputation

    def set_school_tickets(self):
        '''
        Set number of free school tickets to make available.
        '''
        self.tickets.school_tickets = tickets = 100 * (int((20 - self.reputation) * 0.5) + 1)

    def set_season_tickets_unavailable(self):
        '''
        Close season ticket sales prior to first game.
        '''
        self.tickets.season_tickets_available = False

    def pay_wages(self):
        '''
        Pay wages for both players and staff.
        '''
        total = 0

        for playerid in self.squad:
            total += game.players[playerid].wage

        self.accounts.withdraw(amount=total, category="playerwage")

        total = 0

        for staffid in self.coaches_hired:
            total += self.coaches_hired[staffid].wage

        for staffid in self.scouts_hired:
            total += self.scouts_hired[staffid].wage

        self.accounts.withdraw(amount=total, category="staffwage")


class League:
    def __init__(self):
        self.name = ""
        self.teams = []
        self.referees = {}

        self.fixtures = fixtures.Fixtures()
        self.results = []
        self.standings = Standings()

        self.televised = []

    def add_club(self, clubid):
        '''
        Add club to league and standings.
        '''
        self.teams.append(clubid)

        self.standings.add_item(clubid)

    def add_result(self, result):
        '''
        Update results with latest for given teams.
        '''
        self.results[game.date.fixturesindex].append(result)


class Tickets:
    def __init__(self):
        self.tickets = [0] * 15

        self.season_tickets = 0
        self.season_tickets_available = True

        self.school_tickets = 0


class Flotation:
    def __init__(self):
        self.amount = 0
        self.timeout = 0
        self.status = 0


class Overdraft:
    def __init__(self):
        self.amount = 0
        self.rate = random.randint(4, 15)
        self.timeout = random.randint(4, 16)


class BankLoan:
    def __init__(self):
        self.amount = 0
        self.rate = random.randint(4, 15)
        self.timeout = random.randint(4, 16)


class Grant:
    def __init__(self):
        self.timeout = 0
        self.status = 0
        self.amount = 0

    def get_grant_allowed(self):
        club = game.clubs[game.teamid]

        state = club.reputation < 13

        # Determine current bank balance
        if state:
            state = club.accounts.balance <= (150000 * club.reputation)

        # Determine stadium capacity
        if state:
            capacity = game.stadiums[club.stadium].capacity

            state = capacity < (1500 * club.reputation + (club.reputation * 0.5))

        return state

    def get_grant_maximum(self):
        amount = club.reputation ** 2 * 10000
        diff = amount * 0.1
        amount += random.randint(-diff, diff)

        maximum = calculator.value_rounder(amount)

        return maximum

    def get_grant_response(self):
        '''
        Determine whether the grant request is accepted or rejected.
        '''
        response = random.choice((True, False))  # Replace with AI

        return response

    def update_grant(self):
        '''
        Update grant timeout.
        '''
        if self.status == 1:
            if self.timeout > 0:
                self.timeout -= 1
            else:
                if self.get_grant_response():
                    self.status = 2

                    club = game.clubs[game.teamid]
                    club.accounts.deposit(amount=self.amount, category="grant")
                    game.news.publish("SG01", amount=self.amount)
                else:
                    self.status = 3

                    self.timeout = random.randint(26, 78)
        elif self.status == 2:
            if self.timeout > 0:
                self.timeout -= 1
            else:
                print("Grant running")
        elif self.status == 3:
            if self.timeout > 0:
                self.timeout -= 1
            else:
                self.status = 0

    def set_grant_application(self, amount):
        '''
        Apply for grant with set amount.
        '''
        self.timeout = random.randint(6, 10)
        self.status = 1
        self.amount = amount


class Standings:
    class Item:
        def __init__(self):
            self.played = 0
            self.wins = 0
            self.draws = 0
            self.losses = 0
            self.goals_for = 0
            self.goals_against = 0
            self.goal_difference = 0
            self.points = 0

        def get_data(self):
            data = [self.played,
                    self.wins,
                    self.draws,
                    self.losses,
                    self.goals_for,
                    self.goals_against,
                    self.goal_difference,
                    self.points
                   ]

            return data

        def reset_data(self):
            self.played = 0
            self.wins = 0
            self.draws = 0
            self.losses = 0
            self.goals_for = 0
            self.goals_against = 0
            self.goal_difference = 0
            self.points = 0

    def __init__(self):
        self.clubs = {}

    def add_item(self, clubid):
        '''
        Create initial data item for given club.
        '''
        self.clubs[clubid] = self.Item()

        return self.clubs[clubid]

    def update_item(self, result):
        '''
        Update information for specified club.
        '''
        team1 = result[0]
        team2 = result[3]

        self.clubs[team1].played += 1
        self.clubs[team2].played += 1

        if result[1] > result[2]:
            self.clubs[team1].wins += 1
            self.clubs[team2].losses += 1
            self.clubs[team1].goals_for += result[1]
            self.clubs[team1].goals_against += result[2]
            self.clubs[team1].goal_difference = self.clubs[team1].goals_for - self.clubs[team1].goals_against
            self.clubs[team2].goals_for += result[2]
            self.clubs[team2].goals_against += result[1]
            self.clubs[team2].goal_difference = self.clubs[team2].goals_for - self.clubs[team2].goals_against
            self.clubs[team1].points += 3

            game.clubs[team1].form.append("W")
            game.clubs[team2].form.append("L")
        elif result[2] > result[1]:
            self.clubs[team2].wins += 1
            self.clubs[team1].losses += 1
            self.clubs[team2].goals_for += result[2]
            self.clubs[team2].goals_against += result[1]
            self.clubs[team2].goal_difference = self.clubs[team2].goals_for - self.clubs[team2].goals_against
            self.clubs[team1].goals_for += result[1]
            self.clubs[team1].goals_against += result[2]
            self.clubs[team1].goal_difference = self.clubs[team1].goals_for - self.clubs[team1].goals_against
            self.clubs[team2].points += 3

            game.clubs[team1].form.append("L")
            game.clubs[team2].form.append("W")
        else:
            self.clubs[team1].draws += 1
            self.clubs[team2].draws += 1
            self.clubs[team1].goals_for += result[1]
            self.clubs[team1].goals_against += result[2]
            self.clubs[team1].goal_difference = self.clubs[team1].goals_for - self.clubs[team1].goals_against
            self.clubs[team2].goals_for += result[2]
            self.clubs[team2].goals_against += result[1]
            self.clubs[team2].goal_difference = self.clubs[team2].goals_for - self.clubs[team2].goals_against
            self.clubs[team1].points += 1
            self.clubs[team2].points += 1

            game.clubs[team1].form.append("D")
            game.clubs[team2].form.append("D")

    def reset_standings(self):
        '''
        Clear information back to defaults.
        '''
        for item in self.clubs.values():
            item.reset_data()

    def get_data(self):
        standings = []

        for key, value in self.clubs.items():
            item = []

            club = game.clubs[key]
            item = value.get_data()

            form = "".join(club.form[-6:])

            item.insert(0, key)
            item.insert(1, club.name)
            item.append(form)

            standings.append(item)

        if game.date.eventindex > 0:
            standings = sorted(standings,
                                key=operator.itemgetter(9, 8, 6, 7),
                                reverse=True)
        else:
            standings = sorted(standings,
                                key=operator.itemgetter(1))

        return standings

    def find_champion(self):
        '''
        Return club which is top of the league.
        '''
        standings = self.get_data()
        champion = standings[0]

        return champion

    def find_position(self, teamid):
        '''
        Return position for given club.
        '''
        standings = self.get_data()

        position = 0

        for count, item in enumerate(standings, start=1):
            if item[0] == teamid:
                position = count

        return position


class Stadium:
    def __init__(self):
        self.capacity = 0
        self.maintenance = 100
        self.main = []
        self.corner = []
        self.fines = 0
        self.warnings = 0


class Stand:
    def __init__(self):
        self.capacity = 0
        self.seating = False
        self.roof = False


class Referee:
    def __init__(self):
        self.name = ""
        self.matches = 0
        self.fouls = 0
        self.yellows = 0
        self.reds = 0

    def increment_appearance(self, fouls=0, yellows=0, reds=0):
        '''
        Increment referee appearances and match statistics.
        '''
        self.matches += 1
        self.fouls += fouls
        self.yellows += yellows
        self.reds += reds

    def reset_statistics(self):
        '''
        Clear statistics for referee.
        '''
        self.matches = 0
        self.fouls = 0
        self.yellows = 0
        self.reds = 0


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


class TeamTraining:
    def __init__(self):
        self.training = [0] * 42

        self.timeout = random.randint(8, 12)
        self.alert = 0

    def generate_schedule(self):
        '''
        Generate team training schedule.
        '''
        values = [count for count in range(2, 18)]
        random.shuffle(values)

        for count in range(0, 6):
            self.training[count * 6] = values[count * 2]
            self.training[count * 6 + 1] = values[count * 2 + 1]
            self.training[count * 6 + 2] = 1
            self.training[count * 6 + 3] = 0
            self.training[count * 6 + 4] = 0
            self.training[count * 6 + 5] = 0

    def get_sunday_training(self):
        '''
        Return True if team is training on Sunday.
        '''
        sunday = False

        for trainingid in self.training[36:42]:
            if trainingid != 0:
                sunday = True

        return sunday


    def get_overworked_training(self):
        '''
        Return True if the team is being overworked.
        '''
        count = 0

        for trainingid in game.clubs[game.teamid].team_training.training:
            if trainingid != 0:
                count += 1

        overwork = count > 18

        return overwork


class IndividualTraining:
    def __init__(self):
        self.playerid = 0
        self.coachid = 0
        self.skill = 0
        self.intensity = 1
        self.start_value = 0


class TrainingCamp:
    def __init__(self):
        self.days = 1
        self.quality = 1
        self.location = 1
        self.purpose = 1
        self.squad = 0

    def get_player_total(self):
        '''
        Calculate cost per player of training camp with current options.
        '''
        quality = (self.quality * 550) * self.quality
        location = (self.location * 425) * self.location
        purpose = self.purpose * 350

        cost = (quality + location + purpose) * self.days

        return cost

    def get_total(self):
        '''
        Calculate cost of training camp for current options.
        '''
        player = self.get_player_total()

        if self.squad == 0:
            squad = 16
        elif self.squad == 1:
            count = 0

            for item in game.clubs[game.teamid].squad:
                if item not in game.clubs[game.teamid].team.values():
                    count += 1

            squad = count
        elif self.squad == 2:
            squad = len(game.clubs[game.teamid].squad)

        total = player * squad

        return total

    def revert_options(self):
        '''
        Reset selected options back to defaults.
        '''
        self.days = 1
        self.quality = 1
        self.location = 1
        self.purpose = 1
        self.squad = 0

    def get_options(self):
        '''
        Return a tuple of the current options.
        '''
        options = self.days, self.quality, self.location, self.purpose, self.squad

        return options

    def apply_training(self):
        '''
        Take options provided by training camp screen and determine player changes.
        '''
        # Determine players to take on training camp
        squad = []

        if self.squad == 0:
            for playerid in game.clubs[game.teamid].team.values():
                if playerid != 0:
                    squad.append(playerid)
        elif self.squad == 1:
            for playerid in game.clubs[game.teamid].squad:
                if playerid not in game.clubs[game.teamid].team.values():
                    squad.append(playerid)
        else:
            squad = [playerid for playerid in game.clubs[game.teamid].squad]

        if self.purpose == 1:
            # Leisure
            morale = (self.quality) + (self.location) * self.days
            morale = morale * 3
            fitness = 1
        elif self.purpose == 2:
            # Schedule
            morale = (self.quality) + (self.location) * self.days
            morale = morale * 1.5
            individual_training()
            fitness = 3
        elif self.purpose == 3:
            # Intensive
            morale = (-self.quality) + (-self.location) * -self.days
            morale = -morale * 2
            fitness = 8

        for playerid in squad:
            evaluation.morale(playerid, morale)
            events.adjust_fitness(recovery=fitness)
