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


import math
import random

import calculator
import dialogs
import game
import news


def deposit(amount, category=None):
    '''
    Increases the amount of money in the bank account.
    '''
    club = game.clubs[game.teamid]

    if category:
        club.accounts[category][0] += amount
        club.accounts[category][1] += amount

        club.income = 0

        for item in club.accounts[0:7]:
            club.income += item[1]

    club.balance += amount


def withdraw(amount, category):
    '''
    Decreases the amount of money in the bank account.
    '''
    club = game.clubs[game.teamid]
    club.accounts[category][0] += amount
    club.accounts[category][1] += amount

    club.expenditure = 0

    for item in club.accounts[8:19]:
        club.expenditure += item[1]

    club.balance -= amount


def pay_wages():
    '''
    Pay wages for both players and staff.
    '''
    total = 0

    club = game.clubs[game.teamid]

    for playerid in club.squad:
        total += game.players[playerid].wage

    withdraw(total, 12)

    total = 0

    for staffid in club.coaches_hired:
        total += club.coaches_hired[staffid].wage

    for staffid in club.scouts_hired:
        total += club.scouts_hired[staffid].wage

    withdraw(total, 11)


def pay_bonus():
    '''
    Calculate the user-specified win bonus on the tactics screen.
    '''
    if game.clubs[game.teamid].tactics[8] != 0:
        total = 0

        for playerid in game.clubs[game.teamid].team:
            if playerid != 0:
                total += game.players[playerid].wage

        bonus = total * (game.clubs[game.teamid].tactics[8] * 0.1)
        withdraw(bonus, 12)

        game.clubs[game.teamid].tactics[8] = 0


def pay_win_bonus():
    '''
    Pay the win bonus amount defined within the players contract.
    '''
    for playerid in game.clubs[game.teamid].team.values():
        if playerid != 0:
            amount = game.players[playerid].bonus[2]
            withdraw(amount, 12)


def request(amount):
    '''
    Requests amount to withdraw and return whether transaction is valid.
    '''
    state = True

    if amount > game.clubs[game.teamid].balance + game.overdraft.amount:
        dialogs.error(4)
        state = False

    return state


def prize_money(position):
    '''
    Handed out at end of season based on position, plus bonus for a
    first or second place finish.
    '''
    amount = 250000 * (21 - position)

    if position == 1:
        amount += 2500000
    elif position == 2:
        amount += 500000

    return amount


def calculate_loan():
    '''
    Calculate maximum amount club is allowed to borrow as part of loan.
    '''
    club = game.clubs[game.teamid]
    amount = 10000 * (club.reputation ** 2)
    amount = calculator.value_rounder(amount)
    game.bankloan.maximum = amount


def calculate_loan_repayment(amount, weeks):
    repayment = amount * (game.bankloan.rate * 0.01 + 1) / weeks
    repayment = math.ceil(repayment)

    return repayment


def pay_loan():
    if game.bankloan.amount > 0:
        if game.bankloan.repayment > game.bankloan.amount:
            game.bankloan.repayment = game.bankloan.amount

        game.bankloan.amount -= game.bankloan.repayment

        withdraw(game.bankloan.repayment, 16)


def calculate_overdraft():
    club = game.clubs[game.teamid]
    amount = ((club.balance * 0.5) * 0.05) * club.reputation
    amount = calculator.value_rounder(amount)
    game.overdraft.maximum = amount


def pay_overdraft():
    if game.overdraft.amount > 0:
        charge = game.overdraft.amount * 0.01
        interest = 0

        if game.clubs[game.teamid].balance < 0:
            interest = game.overdraft.amount * game.overdraft.rate

        amount = charge + interest

        if amount > 0:
            withdraw(amount, 17)

    if game.overdraft.timeout > 0:
        game.overdraft.timeout -= 1

        if game.overdraft.timeout == 0:
            calculate_overdraft()

            game.overdraft.timeout = random.randint(4, 16)
            game.overdraft.rate = random.randint(4, 15)


def calculate_grant():
    '''
    Check that the club reputation is less than 13, that the balance of
    the club is not too high, and that the stadium capacity is less than
    the determined amount for the club reputation.
    '''
    club = game.clubs[game.teamid]
    reputation = club.reputation
    balance = club.balance

    state = False
    amount = 0

    if reputation < 13:
        state = True

    if not state:
        if balance <= (150000 * reputation):
            state = True
        else:
            state = False

    # Determine stadium capacity
    if not state:
        capacity = game.stadiums[club.stadium].capacity

        if capacity < (1500 * reputation + (reputation * 0.5)):
            state = True
        else:
            state = False

    # Calculate amount available for grant
    if state:
        amount = reputation * reputation * 10000
        diff = amount * 0.1
        amount += random.randint(-diff, diff)
        state = True

    if state:
        game.grant.maximum = calculator.value_rounder(amount)
        game.grant.status = state


def process_grant():
    if game.grant.timeout > 0:
        game.grant.timeout -= 1

        if game.grant.timeout == 0:
            deposit(game.grant.amount, 0)  ## Change category
            news.publish("SG01", amount=game.grant.amount)


def flotation():
    '''
    Calculate estimated flotation amount for club.
    '''
    club = game.clubs[game.teamid]

    amount = club.reputation ** 2 * 100000

    form_affected = amount * 0.25
    amount -= form_affected

    points = 0
    form_length = len(club.form)

    if form_length > 12:
        form_length = 12

    for count in range(0, form_length):
        if club.form[count] == "W":
            points += 3
        elif club.form[count] == "D":
            points += 1

    if form_length >= 6:
        amount += (form_affected / form_length) * ((form_length * 3) - points)

    game.flotation.amount = amount


def float_club():
    '''
    Complete floating of club once timeout has been reached.
    '''
    if game.flotation.timeout > 0 and game.flotation.status == 1:
        game.flotation.timeout -= 1

        if game.flotation.timeout == 0:
            deposit(game.flotation.amount)
            news.publish("FL01")
