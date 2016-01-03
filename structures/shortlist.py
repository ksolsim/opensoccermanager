#!/usr/bin/env python3


class Shortlist:
    '''
    Class handling shortlisted players via user add or transfer negotiation.
    '''
    def __init__(self):
        self.shortlist = set()

    def get_shortlist(self):
        '''
        Return complete list of shortlisted players.
        '''
        return self.shortlist

    def get_player_in_shortlist(self, playerid):
        '''
        Return whether given player id is already in the shortlist.
        '''
        return playerid in self.shortlist

    def add_to_shortlist(self, playerid):
        '''
        Add specified player id to the shortlist.
        '''
        self.shortlist.add(playerid)

    def remove_from_shortlist(self, playerid):
        '''
        Remove specified player id from shortlist.
        '''
        if playerid in self.shortlist:
            self.shortlist.remove(playerid)
