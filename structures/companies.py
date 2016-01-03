#!/usr/bin/env python3

import random

import data


class Companies:
    def __init__(self):
        self.companies = []

        self.populate_data()

    def get_random_company(self):
        '''
        Return a random company from the list of companies.
        '''
        return random.choice(self.companies)

    def get_companies(self):
        '''
        Return a complete list of company names.
        '''
        return self.companies

    def populate_data(self):
        data.database.cursor.execute("SELECT * FROM company")

        companies = data.database.cursor.fetchall()

        self.companies = [item[0] for item in companies]

