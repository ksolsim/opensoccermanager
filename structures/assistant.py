#!/usr/bin/env python3

import data


class Assistant:
    def __init__(self):
        self.advertising = False

    def set_handle_advertising(self, state):
        '''
        Update whether assistant manager will handle advertising.
        '''
        self.advertising = state

    def get_handle_advertising(self):
        '''
        Return whether advertising is handled by assistant manager.
        '''
        return self.advertising
