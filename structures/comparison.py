#!/usr/bin/env python3

import uigtk.comparison


class Comparison:
    def __init__(self):
        self.comparison = []

    def add_to_comparison(self, playerid):
        '''
        Add player to comparison list.
        '''
        if playerid not in self.comparison:
            self.comparison.insert(0, playerid)

            del self.comparison[2:]

    def get_comparison(self):
        '''
        Return list of two players for comparison.
        '''
        return self.comparison

    def get_comparison_valid(self):
        '''
        Return True if comparison contains two players.
        '''
        return len(self.comparison) == 2

    def get_comparison_count(self):
        '''
        Return number of players stored for comparison.
        '''
        return len(self.comparison)

    def set_show_comparison(self):
        '''
        Show comparison of two players, or error if unable.
        '''
        if self.get_comparison_valid():
            uigtk.comparison.ComparisonDialog()
        else:
            uigtk.comparison.ComparisonError()
