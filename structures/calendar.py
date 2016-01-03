#!/usr/bin/env python3

import data


class Calendar:
    def __init__(self):
        self.calendar = {1: 31, 2: 28, 3: 31, 4: 30,
                         5: 31, 6: 30, 7: 31, 8: 31,
                         9: 30, 10: 31, 11: 30, 12: 31}

        self.event = 0

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

    def get_other_fixtures(self):
        '''
        Return fixtures for all other teams.
        '''

    def get_user_fixture(self):
        '''
        Return fixture for user operated club.
        '''
        club = data.clubs.get_club_by_id(data.user.team)
        league = data.leagues.get_league_by_id(club.league)

        fixtures = league.fixtures.get_fixtures_for_week(self.event)

        if data.date.get_date_for_event() == league.fixtures.events[self.event]:
            for fixture in fixtures.values():
                if data.user.team in (fixture.home, fixture.away):
                    club1 = data.clubs.get_club_by_id(fixture.home)
                    club2 = data.clubs.get_club_by_id(fixture.away)

                    data.window.mainscreen.information.set_show_next_match(club1.name, club2.name)

        return club1, club2

    def get_user_opposition(self):
        '''
        Return club id of opposition team.
        '''
        club1, club2 = self.get_user_fixture()

        if club1 is data.clubs.get_club_by_id(data.user.team):
            club = club2
        else:
            club = club1

        return club
