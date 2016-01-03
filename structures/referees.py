#!/usr/bin/env python3

import data


class Referees:
    class Referee:
        def __init__(self):
            self.name = ""
            self.league = None

    def __init__(self, season):
        self.referees = {}
        self.season = season

        self.populate_data()

    def get_referees(self):
        '''
        Return dictionary items for all referees.
        '''
        return self.referees.items()

    def populate_data(self):
        data.database.cursor.execute("SELECT * FROM referee \
                                     JOIN refereeattr \
                                     ON referee.id = refereeattr.referee \
                                     WHERE refereeattr.year = ?",
                                     (self.season,))

        for item in data.database.cursor.fetchall():
            referee = self.Referee()
            refereeid = item[0]
            self.referees[refereeid] = referee

            referee.name = item[1]
            referee.league = item[5]

            league = data.leagues.get_league_by_id(referee.league)
            league.add_referee(refereeid)
