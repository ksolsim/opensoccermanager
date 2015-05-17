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
import statistics

import accounts
import calculator
import constants
import game


class Player:
    def __init__(self):
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
        self.history = []

    def skills(self):
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
        if not self.common_name:
            self.common_name = ""

        if self.common_name is not "":
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
        age = game.year - int(year)

        if (game.month, game.date) < (int(month), int(day)):
            age -= 1

        return age

    def get_club(self):
        '''
        Return the club name, or none if uncontracted.
        '''
        if self.club == 0:
            club = ""
        else:
            club = game.clubs[self.club].name

        return club

    def get_nationality(self):
        '''
        Return the player nationality.
        '''
        nation = game.nations[self.nationality].name

        return nation

    def get_value(self):
        '''
        Retrieve the player value formatted with currency.
        '''
        value = calculator.value_rounder(self.value)
        currency, exchange = constants.currency[game.currency]

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
        currency, exchange = constants.currency[game.currency]

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

    def get_injury(self):
        if self.injury_period == 1:
            injury = "%i Week" % (self.injury_period)
        else:
            injury = "%i Weeks" % (self.injury_period)

        return injury

    def get_suspension(self):
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


class Club:
    def __init__(self):
        self.squad = []
        self.team = {}
        self.tactics = [0, 0, 0, 0, 0, 1, 1, 0, 0]
        self.coaches_available = {}
        self.coaches_hired = {}
        self.scouts_available = {}
        self.scouts_hired = {}
        self.team_training = [0] * 42
        self.individual_training = {}
        self.tickets = [0] * 15
        self.season_tickets = 40
        self.school_tickets = 0
        self.accounts = accounts.Accounts()
        self.finances = [0, 0, 0, 0, 0, 0, 0, 0]
        self.sponsor_status = 0
        self.sponsor_offer = ()
        self.hoardings = [[], [], 0]
        self.programmes = [[], [], 0]
        self.shortlist = set()
        self.merchandise = []
        self.catering = []
        self.sales = [[], []]
        self.evaluation = [0, 0, 0, 0, 0]
        self.statistics = [0] * 3
        self.form = []
        self.attendances = []

    def get_stadium_name(self):
        '''
        Return the stadium name.
        '''
        stadium = game.stadiums[self.stadium].name

        return stadium


class Nation:
    pass


class Flotation:
    pass


class Overdraft:
    pass


class BankLoan:
    pass


class Grant:
    pass


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

        if game.eventindex > 0:
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
        self.teamid = 0
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

        self.win = (0, ())
        self.loss = (0, ())


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

    def calculate_player(self):
        quality = (self.quality * 550) * self.quality
        location = (self.location * 425) * self.location
        purpose = self.purpose * 350

        cost = (quality + location + purpose) * self.days

        return cost

    def calculate_total(self):
        player = self.calculate_player()

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
        self.days = 1
        self.quality = 1
        self.location = 1
        self.purpose = 1
        self.squad = 0

    def retrieve_options(self):
        options = self.days, self.quality, self.location, self.purpose, self.squad

        return options
