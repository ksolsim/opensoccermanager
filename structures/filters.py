#!/usr/bin/env python3

import collections


class Squad:
    attributes = {"availableonly": False,
                  "position": 0}

    def __init__(self):
        self.options = {}

        self.reset_filter()

    def reset_filter(self):
        '''
        Restore default filtering attributes.
        '''
        for key, value in self.attributes.items():
            self.options[key] = value

    def get_filter_active(self):
        '''
        Return whether a filter is currently applied.
        '''
        return self.attributes != self.options


class Player:
    defaults = (("own_players", True),
                ("position", 0),
                ("value", [0, 20000000]),
                ("age", [16, 50]),
                ("status", 0),
                ("keeping", [0, 99]),
                ("tackling", [0, 99]),
                ("passing", [0, 99]),
                ("shooting", [0, 99]),
                ("heading", [0, 99]),
                ("pace", [0, 99]),
                ("stamina", [0, 99]),
                ("ball_control", [0, 99]),
                ("set_pieces", [0, 99]))
    defaults = collections.OrderedDict(defaults)

    def __init__(self):
        self.options = {}

        self.reset_filter()

    def reset_filter(self):
        '''
        Restore default filtering attributes.
        '''
        self.options = collections.OrderedDict(self.defaults)

    def get_filter_active(self):
        '''
        Return whether a filter is currently applied.
        '''
        return self.options != self.defaults
