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
    def __init__(self):
        pass

    def publish_expectation(self):
        '''
        Return expectation for the club.
        '''
        keys = [clubid for clubid in data.clubs.keys()]

        positions = ([], [], [])

        print(keys)
