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


import data


class Referees:
    class Referee:
        def __init__(self):
            self.name = ""
            self.league = None

            self.games = 0
            self.yellow_cards = 0
            self.red_cards = 0

        def increment_statistics(self, fixture):
            '''
            Increment referee statistics for played fixture.
            '''
            self.games += 1
            self.yellow_cards += len(fixture.home.yellow_cards) + len(fixture.away.yellow_cards)
            self.red_cards += len(fixture.home.red_cards) + len(fixture.away.red_cards)

        def get_points(self):
            '''
            Calculate points for cards issued by referee.
            '''
            return (self.yellow_cards * 1) + (self.red_cards * 3)

    def __init__(self, season):
        self.referees = {}
        self.season = season

        self.populate_data()

    def get_referees(self):
        '''
        Return dictionary items for all referees.
        '''
        return self.referees.items()

    def get_referee_by_id(self, refereeid):
        '''
        Fetch referee for given referee id.
        '''
        return self.referees[refereeid]

    def get_referee_data(self):
        '''
        Return sorted list of referee data.
        '''
        if data.calendar.event == 0:
            referees = sorted(self.referees.items(),
                              key=lambda item: item[1].name)
        else:
            referees = sorted(self.referees.items(),
                              key=lambda item: (item[1].get_points(),
                                                item[1].red_cards,
                                                item[1].yellow_cards,
                                                item[1].games))

        return referees

    def populate_data(self):
        data.database.cursor.execute("SELECT * FROM referee \
                                     JOIN refereeattr \
                                     ON referee.id = refereeattr.referee \
                                     WHERE refereeattr.year = ?",
                                     (self.season,))

        for item in data.database.cursor.fetchall():
            referee = self.Referee()
            referee.refereeid = item[0]
            referee.name = item[1]
            referee.league = data.leagues.get_league_by_id(item[5])
            self.referees[referee.refereeid] = referee

            referee.league.add_referee_to_league(referee)
