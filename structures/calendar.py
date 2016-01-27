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


class Calendar:
    def __init__(self):
        self.calendar = {1: 31, 2: 28, 3: 31, 4: 30,
                         5: 31, 6: 30, 7: 31, 8: 31,
                         9: 30, 10: 31, 11: 30, 12: 31}

        self.days = ("Monday",
                     "Tuesday",
                     "Wednesday",
                     "Thursday",
                     "Friday",
                     "Saturday",
                     "Sunday")

        self.event = 0

    def get_days(self):
        '''
        Return tuple of day names.
        '''
        return self.days

    def get_maximum_days(self, month):
        '''
        Return number of days in month for passed month value.
        '''
        return self.calendar[month]

    def get_fixture(self):
        '''
        Return whether current date has a scheduled fixture.
        '''
        state = False

        for leagueid, league in data.leagues.get_leagues():
            if data.date.get_date_for_event() == league.fixtures.events[self.event]:
                state = True

        return state

    def get_user_fixture(self):
        '''
        Return fixture for user operated club.
        '''
        club = data.clubs.get_club_by_id(data.user.team)
        league = data.leagues.get_league_by_id(club.league)

        fixtures = league.fixtures.get_fixtures_for_week(self.event)

        if data.date.get_date_for_event() == league.fixtures.events[self.event]:
            for fixtureid, fixture in fixtures.items():
                if data.user.team in (fixture.home.clubid, fixture.away.clubid):
                    club1 = fixture.get_home_name()
                    club2 = fixture.get_away_name()

                    data.window.mainscreen.information.leagueid = club.league
                    data.window.mainscreen.information.fixtureid = fixtureid
                    data.window.mainscreen.information.set_show_next_match(club1, club2)

                    data.window.mainscreen.information.set_continue_to_match()

                    return fixtureid, fixture

    def get_other_fixtures(self, leagueid):
        '''
        Return fixtures for all other teams.
        '''
        fixtures = []

        league = data.leagues.get_league_by_id(leagueid)

        for fixtureid, fixture in league.fixtures.get_fixtures_for_week(self.event).items():
            if data.user.team not in (fixture.home.clubid, fixture.away.clubid):
                fixtures.append(fixtureid)

        return fixtures

    def get_user_opposition(self):
        '''
        Return club id of opposition team.
        '''
        fixtureid, fixture = self.get_user_fixture()

        if fixture.home.clubid == data.user.team:
            club = fixture.away.clubid
        else:
            club = fixture.home.clubid

        return club

    def increment_event(self):
        '''
        Increment event index value.
        '''
        self.event += 1
