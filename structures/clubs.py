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

import data
import structures.accounts
import structures.advertising
import structures.assistant
import structures.catering
import structures.coaches
import structures.expectation
import structures.finances
import structures.form
import structures.individualtraining
import structures.merchandise
import structures.news
import structures.scouts
import structures.sponsorship
import structures.squad
import structures.tactics
import structures.teamtraining
import structures.tickets
import structures.training


class Clubs:
    class Club:
        def __init__(self):
            self.name = ""
            self.nickname = ""
            self.manager = ""
            self.chairman = ""
            self.reputation = 0
            self.stadium = None
            self.assistant = structures.assistant.Assistant()
            self.news = structures.news.News()
            self.squad = structures.squad.Squad()
            self.tactics = structures.tactics.Tactics()
            self.coaches = structures.coaches.Coaches()
            self.scouts = structures.scouts.Scouts()
            self.tickets = structures.tickets.Tickets()
            self.team_training = structures.teamtraining.TeamTraining()
            self.individual_training = structures.individualtraining.IndividualTraining()
            self.merchandise = structures.merchandise.Merchandise()
            self.catering = structures.catering.Catering()
            self.sponsorship = structures.sponsorship.Sponsorship()
            self.hoardings = structures.advertising.Advertising()
            self.programmes = structures.advertising.Advertising()
            self.accounts = structures.accounts.Accounts()
            self.finances = structures.finances.Finances()
            self.shortlist = structures.shortlist.Shortlist()
            self.form = structures.form.Form()
            self.expectation = structures.expectation.Expectation()

        def get_total_value(self):
            '''
            Get total value of all players in squad.
            '''
            value = 0

            for playerid in self.squad.get_squad():
                player = data.players.get_player_by_id(playerid)
                value += player.get_value()

            return value

        def get_total_wage(self):
            '''
            Get total wage bill for players at the club.
            '''
            wage = 0

            for playerid in self.squad.get_squad():
                player = data.players.get_player_by_id(playerid)
                wage += player.contract.wage

            return wage

        def pay_players(self):
            '''
            Pay wages for contracted players.
            '''
            wage = self.get_total_wage()
            self.accounts.withdraw(wage, category="playerwage")

        def pay_staff(self):
            '''
            Pay wage for contracted staff members.
            '''
            wage = self.coaches.get_total_wage()
            self.accounts.withdraw(wage, category="staffwage")

            wage = self.scouts.get_total_wage()
            self.accounts.withdraw(wage, category="staffwage")

    def __init__(self, season):
        self.clubs = {}
        self.season = season

        self.populate_data()

    def get_clubs(self):
        '''
        Return complete dictionary of clubs.
        '''
        return self.clubs.items()

    def get_club_by_id(self, clubid):
        '''
        Return club for given club id.
        '''
        if clubid:
            return self.clubs[clubid]
        else:
            return None

    def get_club_keys(self):
        '''
        Get list of club id keys.
        '''
        return self.clubs.keys()

    def populate_data(self):
        data.database.cursor.execute("SELECT * FROM club \
                                     JOIN clubattr \
                                     ON club.id = clubattr.club \
                                     WHERE year = ?",
                                     (self.season,))

        for item in data.database.cursor.fetchall():
            club = self.Club()
            clubid = item[0]
            self.clubs[clubid] = club

            club.name = item[1]
            club.nickname = item[2]
            club.league = item[6]
            club.manager = item[7]
            club.chairman = item[8]
            club.stadium = item[9]
            club.reputation = item[10]

            club.squad.team = clubid

            league = data.leagues.get_league_by_id(club.league)
            league.add_club(clubid)

    def set_initial_balance(self, option):
        '''
        Set the initial bank balance based on details chosen.
        '''
        for club in self.clubs.values():
            if option == -1:
                club.accounts.balance = club.reputation ** 3 * random.randint(985, 1025) * 3
            else:
                finances = structures.finances.FinanceCategories()
                club.accounts.balance = finances.get_value_by_index(option)
