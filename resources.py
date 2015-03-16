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
