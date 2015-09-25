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
import string

import constants
import game
import news
import user


def check_morale():
    '''
    Check workload of other coaches and decrease morale if overworked.
    '''
    counts = {}

    club = user.get_user_club()

    for playerid, training in club.individual_training.individual_training.items():
        if training.coachid in counts:
            counts[training.coachid] += 1
        else:
            counts[training.coachid] = 1

    average = 0

    for value in counts.values():
        average += value

    if len(counts) > 1:
        average = average / len(counts)
    else:
        for coachid, count in counts.items():
            if count > 9:
                coach = club.coaches_hired[coachid]
                news.publish("IT01", coach=coach.name)
                coach.morale -= 1


def refresh_staff():
    '''
    Regenerate the list of scouts and coaches available every 8-12 weeks.
    '''
    if game.staff_timeout > 0:
        game.staff_timeout -= 1
    else:
        club = user.get_user_club()

        club.coaches.generate_initial_coaches()
        club.scouts.generate_initial_scouts()

        game.staff_timeout = random.randint(8, 12)
