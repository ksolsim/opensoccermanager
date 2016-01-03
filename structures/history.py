#!/usr/bin/env python3

import data


class History:
    def __init__(self):
        self.history = []

    def add_season(self):
        '''
        Add season to history list.
        '''
        self.history.append([])

    def get_history(self):
        '''
        Return history in descending order by season.
        '''
        return sorted(self.history, reverse=True)
