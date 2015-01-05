#!/usr/bin/env python

import os
import lxml.etree as ET

import constants


def import_news():
    xmlpath = os.path.join("resources", "news.xml")
    tree = ET.parse(xmlpath)
    root = tree.getroot()

    for value, child in enumerate(root):
        newsid = root[value].attrib["id"]
        title = root[value][0].text
        message = root[value][1].text
        category = root[value][2].text

        if newsid in constants.news.keys():
            constants.news[newsid].append([title, message, category])
        else:
            constants.news[newsid] = [[title, message, category]]


def import_evaluation():
    xmlpath = os.path.join("resources", "evaluation.xml")
    tree = ET.parse(xmlpath)
    root = tree.getroot()

    for count in range(0, 5):
        constants.evaluation.append({})

        for value, child in enumerate(root[count]):
            evaluationid = root[count][value].attrib["id"]
            evaluationid = int(evaluationid)
            message = root[count][value].text

            if evaluationid in constants.evaluation[count].keys():
                constants.evaluation[count][evaluationid].append(message)
            else:
                constants.evaluation[count][evaluationid] = [message]
