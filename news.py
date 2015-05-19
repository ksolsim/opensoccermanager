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

import constants
import display
import game
import widgets


class News:
    class Article:
        def __init__(self, newsid, kwargs):
            item = random.choice(constants.news[newsid])

            self.date = game.date.get_string_date()
            self.title = item[0]
            self.message = item[1]
            self.category = int(item[2])
            self.unread = True

            keys = {"_CLUB_": game.clubs[game.teamid].name,
                    "_USER_": game.clubs[game.teamid].manager,
                    "_CHAIRMAN_": game.clubs[game.teamid].chairman,
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
        self.articles = {}
        self.newsid = 1

    def publish(self, newsid, **kwargs):
        article = self.Article(newsid, kwargs)
        article.newsid = self.newsid

        self.articles[self.newsid] = article

        widgets.news.show()

        self.newsid += 1

    def set_manager_name(self, previous):
        new = game.clubs[game.teamid].manager

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
