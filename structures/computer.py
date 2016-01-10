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


import random

import data


class InjuryGenerator:
    '''
    Generate random injuries for players outside of a match.
    '''
    def __init__(self):
        pass

    def generate_injuries(self):
        '''
        Generate injuries with weighting for players with lower fitness.
        '''
        #for playerid, player in data.players.get_players():
        #    print(player.get_name())

    def increment_fitness(self):
        '''
        Improve fitness for players with less than 100 fitness.
        '''
        for playerid, player in data.players.get_players():
            if player.fitness < 100:
                player.fitness += random.randint(1, 5)

                if player.fitness > 100:
                    player.fitness = 100


class AdvertHandler:
    def __init__(self):
        self.club = data.clubs.get_club_by_id(data.user.team)

        self.timeout = random.randint(12, 20)

    def decrement_advertising(self):
        '''
        Decrement weeks remaining on purchased adverts.
        '''
        for item in (self.club.hoardings, self.club.programmes):
            delete = []

            for advertid, advert in item.current.items():
                advert.period -= 1

                if advert.period == 0:
                    delete.append(advertid)

            for advertid in delete:
                del item.current[advertid]

    def refresh_advertising(self):
        '''
        Refresh list of available advertisements once timeout expires.
        '''
        self.timeout -= 1

        if self.timeout == 0:
            self.timeout = random.randint(12, 20)

            self.club.hoardings.available = {}
            self.club.hoardings.generate_adverts(36)

            self.club.programmes.available = {}
            self.club.programmes.generate_adverts(24)

    def assistant_handled(self):
        '''
        Have assistant manager populate free advertisement spacings.
        '''
        if self.club.assistant.get_handle_advertising():
            for item in (self.club.hoardings, self.club.programmes):
                delete = []

                for advertid, advert in item.available.items():
                    if item.get_advert_count() + advert.quantity <= item.maximum:
                        item.current[advertid] = advert
                        delete.append(advertid)

                for advertid in delete:
                    del item.available[advertid]
