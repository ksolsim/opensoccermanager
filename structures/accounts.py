#!/usr/bin/env python3

import collections


class Accounts:
    class Item:
        def __init__(self):
            self.week = 0
            self.season = 0

    def __init__(self):
        incomes = (("prize", self.Item()),
                   ("sponsorship", self.Item()),
                   ("advertising", self.Item()),
                   ("merchandise", self.Item()),
                   ("catering", self.Item()),
                   ("tickets", self.Item()),
                   ("transfers", self.Item()),
                   ("loan", self.Item()),
                   ("grant", self.Item()),
                   ("television", self.Item()),
                  )

        self.incomes = collections.OrderedDict(incomes)

        expenditures = (("fines", self.Item()),
                        ("stadium", self.Item()),
                        ("staffwage", self.Item()),
                        ("playerwage", self.Item()),
                        ("transfers", self.Item()),
                        ("merchandise", self.Item()),
                        ("catering", self.Item()),
                        ("loan", self.Item()),
                        ("overdraft", self.Item()),
                        ("training", self.Item()),
                       )

        self.expenditures = collections.OrderedDict(expenditures)

        self.income = 0
        self.expenditure = 0
        self.balance = 0

    def request(self, amount):
        '''
        Verify whether the passed amount will overdraw the account.
        '''
        overdrawn = self.balance - amount <= 0

        return overdrawn

    def withdraw(self, amount, category):
        '''
        Withdraw the passed amount and set on appropriate category.
        '''
        self.expenditures[category].week += amount
        self.expenditures[category].season += amount

        self.expenditure += amount
        self.balance -= amount

    def deposit(self, amount, category):
        '''
        Deposit the passed amount and set on appropriate category.
        '''
        self.incomes[category].week += amount
        self.incomes[category].season += amount

        self.income += amount
        self.balance += amount
