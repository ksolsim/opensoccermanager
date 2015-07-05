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


import constants
import dialogs
import widgets


teamid = None               # Team that user has selected
active_screen = None        # Track screen currently in view

staff_timeout = 1
coachid = 1
scoutid = 1
negotiationid = 1
advertising_assistant = False  # Toggle assistant handling advertising

# Data
clubs = {}
players = {}
nations = {}
stadiums = {}
referees = {}
injuries = {}
suspensions = {}
surnames = []
negotiations = {}
loans = {}

# Charts
goalscorers = {}
assists = {}
cleansheets = {}
cards = {}
transfers = []


class ContinueGame:
    continue_to_game = True
    continue_date = True

    def continue_game(self):
        current_date = "%i/%i" % (date.day, date.month)

        if date.week == len(constants.dates):
            if dateindex == len(constants.dates[date.week - 1]) - 1:
                # End of season events
                events.end_of_season()

        if date.eventindex <= len(constants.events) - 1:
            event = constants.events[date.eventindex]
        else:
            event = None

        if current_date == event:
            # Team names to be passed to proceed dialog
            leagueid = clubs[teamid].league
            fixtures = leagues[leagueid].fixtures

            for item in fixtures.fixtures[date.fixturesindex]:
                if teamid in item:
                    match = item

            if teamid == match[0]:
                opposition = clubs[match[1]].name
            else:
                opposition = clubs[match[0]].name

            error = True

            if dialogs.proceed_to_game(opposition):
                error = self.check_squad()

                if error:
                    self.continue_date = False
            else:
                self.continue_date = False

            if not error:
                window.screen_loader(99)

                self.continue_to_game = False
                self.continue_date = False
                widgets.nextmatch.clear()
                date.eventindex += 1
        else:
            if self.continue_date:
                date.increment_date()
            else:
                window.screen_loader(1)

                menu.set_sensitive(True)
                widgets.news.set_sensitive(True)
                self.continue_date = True

    def check_squad(self):
        '''
        Check whether the squad has been selected, determine the numbers
        and return whether the game can proceed or not.
        '''
        class Errors:
            team_count = 0
            injuries = []
            suspensions = []
            errored = False

        errors = Errors()

        error = False
        team_count = 0
        sub_count = 0

        for positionid, playerid in clubs[teamid].team.items():
            if playerid:
                player = players[playerid]

                if player.injury_type != 0:
                    errors.injuries.append(player)
                    errors.errored = True

                if player.suspension_type != 0:
                    errors.suspensions.append(player)
                    errors.errored = True

            if playerid != 0:
                if positionid < 11:
                    team_count += 1

                if positionid >= 11:
                    sub_count += 1

        errors.team_count = team_count

        if team_count < 11:
            errors.errored = True
        elif sub_count < 5:
            if not dialogs.not_enough_subs(sub_count):
                error = True

        if errors.errored:
            error = True

            dialog = dialogs.SquadReport()
            dialog.display(errors)

        return error
