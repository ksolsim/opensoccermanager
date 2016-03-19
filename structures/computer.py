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
    def generate_injuries(self):
        '''
        Generate injuries with weighting for players with lower fitness.
        '''
        for clubid, club in data.clubs.get_clubs():
            for playerid, player in club.squad.get_squad():
                number = random.randint(0, 256)

                if number < 1:
                    injury = data.injuries.get_random_injury()
                    player.injury.set_injured(injury)

    def increment_fitness(self):
        '''
        Improve fitness for players with less than 100 fitness.
        '''
        for playerid, player in data.players.get_players():
            if player.injury.fitness < 100:
                player.injury.fitness += random.randint(0, 5)

                if player.injury.fitness > 100:
                    player.injury.fitness = 100


class AdvertHandler:
    def __init__(self):
        self.update_timeout()

    def update_timeout(self):
        '''
        Refresh timeout
        '''
        self.timeout = random.randint(12, 20)

    def decrement_advertising(self):
        '''
        Decrement weeks remaining on purchased adverts.
        '''
        for item in (data.user.club.hoardings, data.user.club.programmes):
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
            self.update_timeout()

            data.user.club.hoardings.available = {}
            data.user.club.hoardings.generate_adverts(36)

            data.user.club.programmes.available = {}
            data.user.club.programmes.generate_adverts(24)

    def assistant_handled(self):
        '''
        Have assistant manager populate free advertisement spacings.
        '''
        if data.user.club.assistant.get_handle_advertising():
            for item in (data.user.club.hoardings, data.user.club.programmes):
                delete = []

                for advertid, advert in item.available.items():
                    if item.get_advert_count() + advert.quantity <= item.maximum:
                        item.current[advertid] = advert
                        delete.append(advertid)

                for advertid in delete:
                    del item.available[advertid]
