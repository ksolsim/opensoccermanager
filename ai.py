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
import random

import calculator
import constants
import evaluation
import game
import news
import structures


class Result:
    def __init__(self, clubid1, clubid2):
        self.clubid1 = clubid1
        self.clubid2 = clubid2

        self.final_score = [0, 0]

        self.select_team()

    def calculate_skills(self):
        '''
        Calculate the scores from the player skills based on the team
        selection.
        '''
        self.weights = [0, 0]

        for count, team in enumerate((game.clubs[self.clubid1].team,
                                      game.clubs[self.clubid2].team)):
            for playerid in team.values():
                if playerid != 0:
                    player = game.players[playerid]

                    skills = player.get_skills()
                    self.weights[count] = sum(skills)


        self.total = sum(self.weights)

        self.calculate_percentages()

    def home_advantage(self):
        '''
        Calculate home advantage score based on form and fan morale.
        '''
        club = game.clubs[self.clubid1]

        points = 0

        for item in club.form[-6:]:
            if item is "W":
                points += 3
            elif item is "D":
                points += 1

        return points

    def calculate_percentages(self):
        '''
        Determine the percentage chance of a win for each team, based on
        club reputation and home advantage.
        '''
        advantage = self.home_advantage()

        percent1 = ((self.weights[0] / self.total) + advantage) * 100
        percent1 = (percent1 * 0.05) * game.clubs[self.clubid1].reputation
        self.percent1 = round(percent1)

        percent2 = (self.weights[1] / self.total) * 100
        percent2 = (percent2 * 0.05) * game.clubs[self.clubid2].reputation
        self.percent2 = round(percent2)

        self.determine_result()

    def determine_result(self):
        if self.percent1 > self.percent2:
            draw = self.percent1 - self.percent2
        elif self.percent1 < self.percent2:
            draw = self.percent2 - self.percent1
        else:
            draw = 0

        ranges = [[], [], []]
        ranges[0] = [0, self.percent1]
        ranges[1] = [ranges[0][1], self.percent1 + draw]
        ranges[2] = [ranges[1][1], ranges[1][1] + self.percent2]

        [list(map(int, item)) for item in ranges]

        choice = random.randrange(0, int(ranges[2][1]))

        if choice < ranges[0][1]:
            score = self.generate_goals()
        elif choice < ranges[1][1]:
            score = self.generate_goals()
            score = score[0], score[0]
        elif choice < ranges[2][1]:
            score = self.generate_goals()
            score = score[1], score[0]

        self.final_score = score

        self.goalscorers()
        self.cards()
        self.injury()
        self.ratings()

    def generate_goals(self):
        score1 = 1

        if game.clubs[game.teamid].tactics[5] == 0:
            start = 35
        elif game.clubs[game.teamid].tactics[5] == 1:
            start = 50
        elif game.clubs[game.teamid].tactics[5] == 2:
            start = 65

        for x in range(2, 9):
            if random.randint(0, 100) < start:
                score1 += 1
                start = int(start * 0.5)

                if start < 1:
                    start = 1

        score2 = random.randint(0, score1 - 1)

        return score1, score2

    def select_team(self):
        self.selection1 = [[], []]
        subs = []

        for key, playerid in game.clubs[self.clubid1].team.items():
            if playerid != 0 and key < 11:
                self.selection1[0].append(playerid)

            if playerid != 0 and key >= 11:
                subs.append(playerid)

        for count in range(1, 4):
            if len(subs) > 0:
                choice = random.choice(subs)
                self.selection1[1].append(choice)
                subs.remove(choice)

        self.selection2 = [[], []]
        subs = []

        for key, playerid in game.clubs[self.clubid2].team.items():
            if playerid != 0 and key < 11:
                self.selection2[0].append(playerid)

            if playerid != 0 and key >= 11:
                subs.append(playerid)

        for count in range(1, 4):
            if len(subs) > 0:
                choice = random.choice(subs)
                self.selection2[1].append(choice)
                subs.remove(choice)

        self.increment_appearances(self.selection1, self.clubid1)
        self.increment_appearances(self.selection2, self.clubid2)

        self.calculate_skills()

    def increment_appearances(self, selection, clubid):
        players = []

        for playerid in selection[0]:
            player = game.players[playerid]
            player.appearances += 1

        for playerid in selection[1]:
            player = game.players[playerid]
            player.substitute += 1

        team = operator.concat(selection[0], selection[1])

        for playerid in game.clubs[clubid].squad:
            if playerid not in team:
                player = game.players[playerid]
                player.missed += 1
                evaluation.morale(playerid, 3)

    def goalscorers(self):
        '''
        Determines the goalscorers for each club when passed both club
        team IDs and the score for both teams.
        '''
        def maximum_calculator(player):
            maximum = 0

            if player.position == "GK":
                maximum = 1
            elif player.position in ("DL", "DR", "DC", "D"):
                maximum = player.tackling
            elif player.position in ("ML", "MR", "MC", "M"):
                maximum = player.passing * 3
            elif player.position in ("AS", "AF"):
                maximum = player.shooting * 5

            return maximum

        players = [[], []]
        scorers = [[], []]

        for playerid in self.selection1[0]:
            if playerid != 0:
                player = game.players[playerid]

                maximum = maximum_calculator(player)

                for x in range(0, maximum):
                    players[0].append(playerid)

        for playerid in self.selection1[1]:
            if playerid != 0:
                player = game.players[playerid]

                maximum = maximum_calculator(player)

                for x in range(0, maximum):
                    players[0].append(playerid)

        for playerid in self.selection2[0]:
            if playerid != 0:
                player = game.players[playerid]

                maximum = maximum_calculator(player)

                for x in range(0, maximum):
                    players[1].append(playerid)

        for playerid in self.selection2[1]:
            if playerid != 0:
                player = game.players[playerid]

                maximum = maximum_calculator(player)

                for x in range(0, maximum):
                    players[1].append(playerid)

        random.shuffle(players[0])
        random.shuffle(players[1])

        for count in range(0, self.final_score[0]):
            choice = random.choice(players[0])

            scorers[0].append(choice)

        for count in range(0, self.final_score[1]):
            choice = random.choice(players[1])

            scorers[1].append(choice)

        if self.clubid1 == game.teamid:
            self.pay_goal_bonus(scorers, 0)
        elif self.clubid2 == game.teamid:
            self.pay_goal_bonus(scorers, 1)

        self.scorers = scorers

        self.assists()

    def assists(self):#, result, selection1, selection2, scorers):
        players = [[], []]

        for playerid in self.selection1[0]:
            if playerid != 0:
                players[0].append(playerid)

        for playerid in self.selection2[0]:
            if playerid != 0:
                players[1].append(playerid)

        for playerid in self.selection1[1]:
            if playerid != 0:
                players[0].append(playerid)

        for playerid in self.selection2[1]:
            if playerid != 0:
                players[1].append(playerid)

        assisters = []
        assists = [[], []]

        for playerid in self.scorers[0]:
            for count in range(0, self.final_score[0]):
                for playerid in players[0]:
                    player = game.players[playerid]

                    maximum = 0

                    if player.position == "GK":
                        maximum = 2
                    elif player.position in ("DL", "DR", "DC", "D"):
                        maximum = player.shooting * 0.2
                    elif player.position in ("ML", "MR", "MC", "M"):
                        maximum = player.shooting
                    elif player.position in ("AS", "AF"):
                        maximum = player.shooting * 0.25

                    for x in range(0, int(maximum)):
                        assisters.append(playerid)

            if self.final_score[0] > 0:
                choice = random.choice(assisters)
                assists[0].append(choice)

        assisters = []

        for playerid in self.scorers[1]:
            for count in range(0, self.final_score[1]):
                for playerid in players[1]:
                    player = game.players[playerid]

                    maximum = 0

                    if player.position == "GK":
                        maximum = 2
                    elif player.position in ("DL", "DR", "DC", "D"):
                        maximum = player.shooting * 0.2
                    elif player.position in ("ML", "MR", "MC", "M"):
                        maximum = player.shooting
                    elif player.position in ("AS", "AF"):
                        maximum = player.shooting * 0.25

                    for x in range(0, int(maximum)):
                        assisters.append(playerid)

            if self.final_score[1] > 0:
                choice = random.choice(assisters)
                assists[1].append(choice)

        self.assists = assists

    def cards(self):
        '''
        Generate cards for each match based on tackling style. There is some
        randomness however, and in theory the likeliness of a card being
        issued diminishes as more cards are given.

        If a player receives a red, or two yellows, a suspension is also
        generated.
        '''
        def generate(clubid):
            match_cards = [{}, {}]

            multiplier = game.clubs[clubid].tactics[6] + 1

            fouls = random.randint(0, multiplier * 6) * 10
            yellow = random.randint(0, int(fouls * 0.5))
            red = random.randint(0, int(fouls / 8))

            count = 0

            while count < int(yellow):
                choice = random.randint(0, (100 * (10 - len(match_cards[0]))))

                if choice < int(yellow) and len(players[0]) > 0:
                    playerid = random.choice(players[0])
                    player = game.players[playerid]

                    if playerid in match_cards[0]:
                        match_cards[0][playerid] += 1
                        match_cards[1][playerid] = 1
                        player.yellow_cards += 1
                        player.red_cards += 1

                        player.suspension_period = 1
                        player.suspension_type = 1

                        players[0].remove(playerid)
                        players[1].remove(playerid)

                        if player.club == game.teamid:
                            name = player.get_name(mode=1)
                            game.news.publish("SU01", player=name, period="1")
                    else:
                        match_cards[0][playerid] = 1
                        player.yellow_cards += 1

                    # Ban player for one match if five/ten/etc yellows
                    if player.yellow_cards * 0.2 >= 1 and player.yellow_cards % 5 == 0:
                        player.suspension_period = 1
                        player.suspension_type = 9

                        if player.club == game.teamid:
                            name = player.get_name(mode=1)
                            game.news.publish("SU03", player=name, period="1", cards=player.yellow_cards)

                count += 1

            count = 0

            while count < int(red):
                choice = random.randint(0, (100 * (10 - len(match_cards[0]))))

                if choice < int(red):
                    playerid = random.choice(players[1])
                    player = game.players[playerid]
                    player.red_cards += 1

                    suspensionid = random.choice(list(constants.suspensions.keys())[2:8])
                    suspension = constants.suspensions[suspensionid]
                    player.suspension_type = suspensionid
                    player.suspension_period = random.randint(suspension[1], suspension[2])

                    players[0].remove(playerid)
                    players[1].remove(playerid)

                    if player.club == game.teamid:
                        name = player.get_name(mode=1)
                        game.news.publish("SU02", player=name, period=player.suspension_period, suspension=suspension[0])

                count += 1

            # Process cards and add to chart
            for playerid, amount in match_cards[0].items():
                if playerid not in game.cards.keys():
                    cards = structures.Cards()
                    game.cards[playerid] = cards
                else:
                    cards = game.cards[playerid]

                cards.yellow_cards += amount
                cards.points += amount * 1

            for playerid, amount in match_cards[1].items():
                if playerid not in game.cards.keys():
                    cards = structures.Cards()
                    game.cards[playerid] = cards
                else:
                    cards = game.cards[playerid]

                cards.red_cards += amount
                cards.points += 3

            return len(match_cards[0]), len(match_cards[1])

        players = [[], []]

        for playerid in game.clubs[self.clubid1].team.values():
            if playerid != 0:
                players[0].append(playerid)
                players[1].append(playerid)

        total1 = generate(self.clubid1)

        for playerid in game.clubs[self.clubid2].team.values():
            if playerid != 0:
                players[0].append(playerid)
                players[1].append(playerid)

        total2 = generate(self.clubid2)

        self.yellows = total1[0] + total2[0]
        self.reds = total1[1] + total2[1]

    def injury(self):
        for teamid in (self.clubid1, self.clubid2):
            team = game.clubs[teamid].team

            selection = []

            for playerid in team.values():
                if playerid != 0:
                    player = game.players[playerid]

                    if player.fitness == 100:
                        selection.append(playerid)
                    else:
                        value = 100 - player.fitness
                        count = round(value % 4)

                        number = 0

                        while number < count:
                            selection.append(playerid)
                            number += 1

            random.shuffle(selection)

            if random.randint(0, 100) < 25:
                name = player.get_name(mode=1)

                injuryid = random.choice(list(constants.injuries.keys()))
                injury = constants.injuries[injuryid]

                weighting = []

                ranges = list(range(injury[4], injury[3] - 1, -1))
                count = 0

                for value in ranges:
                    for x in range(0, count):
                        weighting.append(value)

                    count += 1

                random.shuffle(weighting)

                period = random.choice(weighting)

                player.injury_type = injuryid
                player.injury_period = period
                player.fitness -= random.randint(10, 30)

                if teamid == game.teamid:
                    game.news.publish("IN02", player=name, weeks=period, injury=injury[0])

    def ratings(self):
        ratings = [{}, {}]
        ratings[0] = self.rating(self.selection1)
        ratings[1] = self.rating(self.selection2)

        self.ratings = dict(ratings[0].items() | ratings[1].items())

        self.man_of_the_match()

    def rating(self, selection):
        '''
        Calculate player ratings for both teams at end of each match.
        '''
        ratings = {}

        for playerid in selection[0]:
            player = game.players[playerid]

            rating = random.randint(1, 10)
            player.rating.append(rating)

            ratings[playerid] = rating

        for playerid in selection[1]:
            player = game.players[playerid]

            rating = random.randint(1, 10)
            player.rating.append(rating)

            ratings[playerid] = rating

        return ratings

    def man_of_the_match(self):
        '''
        Determine the man of the match winner based on performance rating for
        the match.
        '''
        motm = []
        value = 0

        for playerid, rating in self.ratings.items():
            if rating > value:
                motm.append(playerid)
                value = rating

        self.man_of_the_match_id = random.choice(motm)

    def attendance(self, team1, team2):
        '''
        Calculate the attendance for the match taking into account ticket price,
        form, player transfers, etc.
        '''
        club = game.clubs[team1.teamid]
        stadium = game.stadiums[club.stadium]

        minimum = int(club.base_attendance * -0.1)
        maximum = int(club.base_attendance * 0.1)
        attendance = club.base_attendance + random.randrange(minimum, maximum)

        # Ensure attendance can't be higher than capacity
        if attendance > stadium.capacity:
            attendance = stadium.capacity

        return attendance

    def pay_goal_bonus(self, scorers, index):
        '''
        Iterate through each goalscorer and pay their contracted bonus amount.
        '''
        club = game.clubs[game.teamid]

        for playerid in scorers[index]:
            amount = game.players[playerid].bonus[3]
            club.accounts.withdraw(amount, "playerwage")


def team_training():
    '''
    Generate team training schedules for all teams. Sets mix of training
    for two hours in the morning, and also an individual session except
    on Sunday.
    '''
    for clubid, club in game.clubs.items():
        if clubid != game.teamid:
            values = [count for count in range(2, 17)]
            random.shuffle(values)

            for count in range(0, 6):
                club.team_training[count * 6] = values[count * 2]
                club.team_training[count * 6 + 1] = values[count * 2 + 1]
                club.team_training[count * 6 + 2] = 1
                club.team_training[count * 6 + 3] = 0
                club.team_training[count * 6 + 4] = 0
                club.team_training[count * 6 + 5] = 0


def renew_contract():
    '''
    Renew player contracts, and announce big name players who have
    agreed to renew their contract for other clubs.
    '''
    for playerid, player in game.players.items():
        if player.club != game.teamid:
            if 0 < player.contract < 24:
                value = random.randint(0, 100)

                if value < 20:
                    wage = calculator.wage(playerid)
                    player.wage = calculator.wage_rounder(wage)

                    age = player.get_age()

                    if age < 33:
                        contract = random.randint(2, 4)
                    else:
                        contract = random.randint(1, 3)

                    player.contract = contract * 52

                    announce = random.choice((True, False))

                    # Announce big name player contract renewals
                    if player.value > 5000000 and announce:
                        name = player.get_name(mode=1)
                        club = game.clubs[player.club].name

                        game.news.publish("RC01",
                                     player=name,
                                     team=club,
                                     period=contract)

                    if playerid in game.clubs[game.teamid].shortlist:
                        name = player.get_name(mode=1)
                        club = game.clubs[player.club].name

                        game.news.publish("RC02",
                                          player=name,
                                          team=club,
                                          period=contract)


def transfer_list():
    '''
    Identify which players should be added to the transfer list.
    '''
    for clubid, club in game.clubs.items():
        if clubid != game.teamid:
            score = {}
            average = 0

            for count, playerid in enumerate(club.squad, start=1):
                player = game.players[playerid]

                skills = player.get_skills()
                score[playerid] = sum(skills) * random.randint(1, 3)

                average += score[playerid] / count

            for playerid in score:
                player = game.players[playerid]

                choice = random.choice((False, True))

                if score[playerid] < average * 0.125 and choice:
                    player.transfer[0] = True


def loan_list():
    '''
    Determine which players should be placed on the loan list.
    '''
    for clubid, club in game.clubs.items():
        if clubid != game.teamid:
            score = {}
            average = 0

            for count, playerid in enumerate(club.squad, start=1):
                player = game.players[playerid]

                skills = player.get_skills()
                score[playerid] = sum(skills) * random.randint(1, 3)

                age = player.get_age()

                if age < 24:
                    score[playerid] += 24 - age * age

                average += score[playerid] / count

            for playerid in score:
                player = game.players[playerid]

                choice = random.choice((False, True))

                if score[playerid] < average * 0.125 and choice:
                    player.transfer[1] = True


def generate_team(clubid):
    '''
    Determine players in squad for all other clubs.
    '''
    formationid = random.randint(0, 6)
    game.clubs[clubid].tactics[0] = formationid
    formation = constants.formations[formationid]

    squad = game.clubs[clubid].squad
    team = game.clubs[clubid].team

    selection = []
    substitutes = []

    for position in formation[1]:
        scores = {}

        for playerid in squad:
            if playerid not in selection:
                player = game.players[playerid]

                skills = player.get_skills()
                score = sum(skills)

                if position == player.position:
                    if position in ("GK"):
                        score = player.keeping * 2.5
                    elif position in ("DL", "DR", "DC", "D"):
                        score = player.tackling * 2.5
                    elif position in ("ML", "MR", "MC", "M"):
                        score = player.passing * 2.5
                    elif position in ("AS", "AF"):
                        score = player.shooting * 2.5
                else:
                    score *= 0.1

                scores[playerid] = score

        sorted_scores = sorted(scores, key=lambda x: scores[x], reverse=True)

        selection.append(sorted_scores[0])

    for count in range(0, 5):
        scores = {}

        for playerid in squad:
            if playerid not in (selection, substitutes):
                player = game.players[playerid]
                skills = player.get_skills()
                score = sum(skills)

                if position == player.position:
                    if position in ("GK"):
                        score = player.keeping * 2.5
                    elif position in ("DL", "DR", "DC", "D"):
                        score = player.tackling * 2.5
                    elif position in ("ML", "MR", "MC", "M"):
                        score = player.passing * 2.5
                    elif position in ("AS", "AF"):
                        score = player.shooting * 2.5
                else:
                    score *= 0.1

                scores[playerid] = score

        sorted_scores = sorted(scores, key=lambda x: scores[x], reverse=True)
        substitutes.append(sorted_scores[0])

    for count, player in enumerate(selection):
        team[count] = player

    for count, player in enumerate(substitutes, start=11):
        team[count] = player


def advertising():
    '''
    Allow assistant manager to handle advertising by adding adverts to
    hoardings and programmes on each turn when there is space for them
    to be added.
    '''
    if game.advertising_assistant:
        club = game.clubs[game.teamid]

        # Programmes
        current_quantity = 0

        for item in club.hoardings[1]:
            current_quantity += item[1]

        position = 0

        for item in club.hoardings[0]:
            if current_quantity + item[1] <= club.hoardings[2]:
                club.hoardings[1].append(item[0:4])
                current_quantity += item[1]
                del club.hoardings[0][position]

                club.accounts.deposit(amount=item[3], category=advertising)

            position += 1

        # Hoardings
        current_quantity = 0

        for item in club.programmes[1]:
            current_quantity += item[1]

        position = 0

        for item in club.programmes[0]:
            if current_quantity + item[1] <= club.programmes[2]:
                club.programmes[1].append(item[0:4])
                current_quantity += item[1]
                del club.programmes[0][position]

                club.accounts.deposit(amount=item[3], category=advertising)

            position += 1
