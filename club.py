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


import accounts
import advertising
import calculator
import catering
import coach
import evaluation
import game
import individualtraining
import league
import merchandise
import scout
import shortlist
import tactics
import teamtraining
import tickets


clubs = {}


class Club:
    def __init__(self):
        self.reputation = 0
        self.squad = []
        self.team = {}
        self.tactics = tactics.Tactics()
        self.scouts = scout.Scouts()
        self.coaches = coach.Coaches()
        self.shortlist = shortlist.Shortlist()
        self.team_training = teamtraining.TeamTraining()
        self.individual_training = individualtraining.IndividualTraining()
        self.tickets = tickets.Tickets()
        self.accounts = accounts.Accounts()
        self.sponsorship = advertising.Sponsorship()
        self.hoardings = advertising.Advertising()
        self.programmes = advertising.Advertising()
        self.merchandise = merchandise.Merchandise()
        self.catering = catering.Catering()
        self.evaluation = evaluation.Evaluation()
        self.form = []
        self.attendances = []

    def get_stadium_name(self):
        '''
        Return the stadium name.
        '''
        stadium = game.stadiums[self.stadium].name

        return stadium

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
        self.tickets.school_tickets = 100 * (int((20 - self.reputation) * 0.5) + 1)

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

    def pay_bonus(self):
        '''
        Calculate the user-specified win bonus on the tactics screen.
        '''
        if self.tactics.win_bonus != 0:
            total = 0

            for playerid in self.team.values():
                if playerid:
                    total += game.players[player.wage]

            bonus = total * (self.tactics.win_bonus * 0.1)
            self.accounts.withdraw(amount=bonus, category="playerwage")

            self.tactics.win_bonus = 0

    def generate_scouts(self):
        self.scouts.generate_initial_scouts()

    def generate_coaches(self):
        self.coaches.generate_initial_coaches()


def populate_data():
    '''
    Populate club data.
    '''
    game.database.cursor.execute("SELECT * FROM club JOIN clubattr ON club.id = clubattr.club WHERE year = ?", (game.date.year,))
    data = game.database.cursor.fetchall()

    for item in data:
        club = Club()
        clubid = item[0]
        clubs[clubid] = club

        club.name = item[1]
        club.nickname = item[2]
        club.league = item[6]
        club.manager = item[7]
        club.chairman = item[8]
        club.stadium = item[9]
        club.reputation = item[10]

        # Initialise playerid in team to 0
        for count in range(0, 16):
            club.team[count] = 0

        club.base_attendance = (74000 / (40 - club.reputation)) * club.reputation
        club.base_attendance = int(club.base_attendance * 0.9)

        league.leagueitem.leagues[club.league].add_club(clubid)

        club.set_advertising_spaces()

        club.set_ticket_prices()
        club.set_season_ticket_percentage()
        club.set_school_tickets()

        club.generate_coaches()
        club.generate_scouts()


def get_club(clubid):
    return clubs[clubid]
