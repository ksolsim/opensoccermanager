#!/usr/bin/env python

import random

import game
import widgets
import constants
import display


def publish(newsid, **kwargs):
    keys = {"_CLUB_": game.clubs[game.teamid].name,
            "_USER_": game.clubs[game.teamid].manager,
            "_CHAIRMAN_": game.clubs[game.teamid].chairman,
            "_SEASON_": display.season(),
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

    item = random.choice(constants.news[newsid])

    date = "%i/%i/%i" % (game.year, game.month, game.date)
    title = item[0]
    message = item[1]
    category = int(item[2])

    for key, value in keys.items():
        if value is not None:
            value = str(value)
            title = title.replace(key, value)
            message = message.replace(key, value)

    article = [date, title, message, category, True]

    # Add news item to club message list
    game.news.insert(0, article)

    # Set unread news flag to display notification
    game.unreadnews = True

    widgets.news.show()
