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


class Player:
    def __init__(self):
        self.fitness = 100
        self.training_points = 0
        self.morale = 10
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
        self.accounts = [[0, 0] for x in range(20)]
        self.income = 0
        self.expenditure = 0
        self.balance = 0
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


class Nation:
    pass


class Negotiation:
    pass


class Flotation:
    pass


class Overdraft:
    pass


class BankLoan:
    pass


class Grant:
    pass


class Staff:
    pass


class League:
    def __init__(self):
        self.played = 0
        self.wins = 0
        self.draws = 0
        self.losses = 0
        self.goals_for = 0
        self.goals_against = 0
        self.goal_difference = 0
        self.points = 0


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
