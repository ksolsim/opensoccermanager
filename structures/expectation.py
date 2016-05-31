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


import xml.dom.minidom
import os

import data


class Evaluation:
    def __init__(self):
        self.evaluations = []

        self.populate_evaluations()

    def populate_evaluations(self):
        filepath = os.path.join("resources", "evaluation.xml")
        evaluation = xml.dom.minidom.parse(filepath)

        count = 0

        for item in evaluation.firstChild.childNodes:
            if item.nodeType == item.ELEMENT_NODE:
                self.statements.append({})

                messages = item.getElementsByTagName("message")

                for text in messages:
                    evaluationid = text.getAttribute("id")
                    evaluationid = int(evaluationid)
                    message = text.firstChild.data

                    if evaluationid in self.statements[count].keys():
                        self.evaluations[count][evaluationid].append(message)
                    else:
                        self.evaluations[count][evaluationid] = [message]

                count += 1


class Expectation:
    '''
    Initial season expectation generator.
    '''
    def __init__(self):
        self.positions = [[], [], []]

    def generate_expectation(self):
        '''
        Return expectation for the club.
        '''
        keys = [club for clubid, club in data.clubs.get_clubs()]

        high_value = 0
        high_club = 0
        low_value = 20
        low_club = 0

        for clubid, club in data.clubs.get_clubs():
            if club.reputation > high_value:
                high_value = club.reputation
                high_club = club
                self.positions[0] = [clubid]
            elif club.reputation < low_value:
                low_value = club.reputation
                low_club = club
                self.positions[2] = [clubid]

        midpoint = 20 - ((high_value - low_value) * 0.5)

        keys.remove(high_club)
        keys.remove(low_club)

        for club in keys:
            if club.reputation == midpoint:
                self.positions[1].append(club)
            elif club.reputation > midpoint:
                if club.reputation > high_value - (high_value - midpoint) * 0.5:
                    self.positions[0].append(club)
                else:
                    self.positions[1].append(club)
            elif club.reputation < midpoint:
                if club.reputation < midpoint - (midpoint - low_value) * 0.5:
                    self.positions[2].append(club)
                else:
                    self.positions[1].append(club)

    def publish_expectation(self):
        '''
        Publish season expectation for club.
        '''
        for count, position in enumerate(self.positions):
            for club in position:
                if club == data.user.club:
                    if count == 0:
                        data.user.club.news.publish("EX01")
                    elif count == 1:
                        data.user.club.news.publish("EX02")
                    elif count == 2:
                        data.user.club.news.publish("EX03")
