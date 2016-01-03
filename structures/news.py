#!/usr/bin/env python3

import os
import random
import xml.dom.minidom

import data


class News:
    def __init__(self):
        self.news = {}
        self.articles = {}

        self.newsid = 0

        self.populate_news()

    def publish(self, newsid, **kwargs):
        '''
        Publish news article for given id with passed dynamic values.
        '''
        article = Article(newsid, kwargs)
        article.newsid = self.get_newsid()
        self.articles[article.newsid] = article

        data.window.mainscreen.information.update_news_visible()

    def get_unread_count(self):
        '''
        Return the number of unread articles.
        '''
        count = 0

        for article in self.articles.values():
            if article.unread:
                count += 1

        return count

    def get_newsid(self):
        '''
        Increment and retrieve news id.
        '''
        self.newsid += 1

        return self.newsid

    def populate_news(self):
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


class Article:
    def __init__(self, newsid, kwargs):
        club = data.clubs.get_club_by_id(data.user.team)

        item = random.choice(club.news.news[newsid])

        self.date = data.date.get_date_as_string()
        self.title = item[0]
        self.message = item[1]
        self.category = int(item[2])
        self.unread = True

        keys = Keys(kwargs)

        for key, value in keys.get_keys():
            if value:
                value = str(value)
                self.title = self.title.replace(key, value)
                self.message = self.message.replace(key, value)


class Keys:
    '''
    Key substitution class for passed news articles.
    '''
    def __init__(self, kwargs):
        club = data.clubs.get_club_by_id(data.user.team)

        self.keys = {"_CLUB_": club.name,
                     "_USER_": club.manager,
                     "_CHAIRMAN_": club.chairman,
                     "_SEASON_": data.date.get_season(),
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
                     "_CARDS_": kwargs.get("cards")}

    def get_keys(self):
        return self.keys.items()


class Categories:
    '''
    Categories used by news screen to filter articles.
    '''
    def __init__(self):
        self.categories = {1: "Stadium",
                           2: "Transfers",
                           3: "Staff",
                           4: "Training",
                           5: "Contracts",
                           6: "Fixtures",
                           7: "Advertising",
                           8: "Awards"}

    def get_category_for_id(self, categoryid):
        return self.categories[categoryid]

    def get_categories(self):
        return self.categories.items()
