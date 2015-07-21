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


class Statistics:
    def __init__(self):
        self.yellows = 0
        self.reds = 0

        self.win = (None, ())
        self.loss = (None, ())

        self.record = []

    def update(self, result):
        '''
        Update statistical information with result.
        '''
        score = result.final_score

        if result.clubid1 == game.teamid:
            if score[0] > score[1]:
                if score > self.win[1]:
                    self.win = (result.clubid2, score)
            elif score[1] > score[0]:
                if score > self.loss[1]:
                    self.loss = (result.clubid2, score)
        elif result.clubid2 == game.teamid:
            if score[0] < score[1]:
                if score > self.win[1]:
                    self.win = (result.clubid1, score)
            elif score[1] < score[0]:
                if score > self.loss[1]:
                    self.loss = (result.clubid1, score)

        self.yellows += result.yellows
        self.reds += result.reds

    def reset_statistics(self):
        '''
        Save current statistics and reset to default for new season.
        '''
        position = game.standings.find_position(game.teamid)
        position = display.format_position(position)
        season = game.date.get_season()

        details = game.standings.clubs[game.teamid]

        record = (season,
                  details.played,
                  details.wins,
                  details.draws,
                  details.losses,
                  details.goals_for,
                  details.goals_against,
                  details.goal_difference,
                  details.points,
                  position
                 )

        self.record.insert(0, record)

        self.yellows = 0
        self.reds = 0

        self.win = (None, ())
        self.loss = (None, ())
