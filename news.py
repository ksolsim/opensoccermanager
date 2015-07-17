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
import random

import club
import constants
import display
import game
import widgets


class News:
    class Article:
        def __init__(self, newsid, kwargs):
            item = random.choice(game.news.news[newsid])

            self.date = game.date.get_string_date()
            self.title = item[0]
            self.message = item[1]
            self.category = int(item[2])
            self.unread = True

            keys = {"_CLUB_": club.clubitem.clubs[game.teamid].name,
                    "_USER_": club.clubitem.clubs[game.teamid].manager,
                    "_CHAIRMAN_": club.clubitem.clubs[game.teamid].chairman,
                    "_SEASON_": game.date.get_season(),
                    "_FIXTURE1_": kwargs.get("fixture1"),
                    "_FIXTURE2_": kwargs.get("fixture2"),
                    "_FIXTURE3_": kwargs.get("fixture3"),
                    "_WEEKS_": kwargs.get("weeks"),
                    "_PLAYER_": kwargs.get("player"),
                    "_TEAM_": kwargs.get("team"),
                    "_INJURY_": kwargs.get("injury"),
                    "_COACH_": kwargs.get("coach"),
                    "_SCOUT_": kwargs.get("scout"),
                    "_PERIOD_": kwargs.get("period"),
                    "_RESULT_": kwargs.get("result"),
                    "_AMOUNT_": kwargs.get("amount"),
                    "_POSITION_": kwargs.get("position"),
                    "_SUSPENSION_": kwargs.get("suspension"),
                    "_CARDS_": kwargs.get("cards"),
                   }

            for key, value in keys.items():
                if value:
                    value = str(value)
                    self.title = self.title.replace(key, value)
                    self.message = self.message.replace(key, value)

    def __init__(self):
        self.news = {}

        self.articles = {}
        self.newsid = 1

        self.populate_news()

    def publish(self, newsid, **kwargs):
        '''
        Publish news article based on passed news identifier.
        '''
        article = self.Article(newsid, kwargs)
        article.newsid = self.newsid

        self.articles[self.newsid] = article

        widgets.news.show()

        self.newsid += 1

    def set_manager_name(self, previous):
        '''
        Update manager name in all news articles.
        '''
        new = club.clubitem.clubs[game.teamid].manager

        for article in self.articles.values():
            article.title = article.title.replace(previous, new)
            article.message = article.message.replace(previous, new)

    def get_unread_count(self):
        '''
        Return the number of items which are set to an unread status.
        '''
        count = 0

        for article in self.articles.values():
            if article.unread:
                count += 1

        return count

    def populate_news(self):
        '''
        Load the news articles from file.
        '''
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

            if newsid in self.news.keys():
                self.news[newsid].append([title, message, category])
            else:
                self.news[newsid] = [[title, message, category]]
