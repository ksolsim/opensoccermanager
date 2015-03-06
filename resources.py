#!/usr/bin/env python3

import xml.dom.minidom
import os

import constants


def import_news():
    filepath = os.path.join("resources", "news.xml")
    news = xml.dom.minidom.parse(filepath)

    for item in news.getElementsByTagName("article"):
        newsid = item.getAttribute("id")

        title = item.getElementsByTagName("title")[0]
        title = title.firstChild.data
        message = item.getElementsByTagName("message")[0]
        message = message.firstChild.data
        category = item.getElementsByTagName("category")[0]
        category = category.firstChild.data

        if newsid in constants.news.keys():
            constants.news[newsid].append([title, message, category])
        else:
            constants.news[newsid] = [[title, message, category]]


def import_evaluation():
    filepath = os.path.join("resources", "evaluation.xml")
    evaluation = xml.dom.minidom.parse(filepath)

    count = 0

    for item in evaluation.firstChild.childNodes:
        if item.nodeType == item.ELEMENT_NODE:
            constants.evaluation.append({})

            messages = item.getElementsByTagName("message")

            for text in messages:
                evaluationid = text.getAttribute("id")
                evaluationid = int(evaluationid)
                message = text.firstChild.data

                if evaluationid in constants.evaluation[count].keys():
                    constants.evaluation[count][evaluationid].append(message)
                else:
                    constants.evaluation[count][evaluationid] = [message]

            count += 1
