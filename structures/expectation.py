#!/usr/bin/env python3

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
