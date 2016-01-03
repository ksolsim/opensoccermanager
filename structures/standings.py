#!/usr/bin/env python3

import operator

import data


class Standings:
    def __init__(self):
        self.standings = {}

    def add_club(self, clubid):
        '''
        Adds passed clubid to standing with new object.
        '''
        self.standings[clubid] = Standing()

    def get_data(self):
        '''
        Return the sorted league standings.
        '''
        standings = []

        for clubid, standing in self.standings.items():
            club = data.clubs.get_club_by_id(clubid)
            item = standing.get_standing_data()

            item.insert(0, clubid)

            standings.append(item)

        standings = sorted(standings, key=operator.itemgetter(8, 7, 5, 6), reverse=True)

        return standings

    def get_position_for_club(self, clubid):
        '''
        Return the position for the given clubid.
        '''

    def get_club_for_position(self, position):
        '''
        Return the clubid for the given position.
        '''
        standings = self.get_data()
        clubid = standings[0]

        return clubid


class Standing:
    def __init__(self):
        self.played = 0
        self.wins = 0
        self.draws = 0
        self.losses = 0
        self.goals_for = 0
        self.goals_against = 0
        self.goal_difference = 0
        self.points = 0

    def get_standing_data(self):
        '''
        Return the standing data as a list.
        '''
        data = [self.played,
                self.wins,
                self.draws,
                self.losses,
                self.goals_for,
                self.goals_against,
                self.goal_difference,
                self.points]

        return data
