#!/usr/bin/env python3

import data
import structures.advertising
import uigtk.match


class ContinueGame:
    '''
    Class handling proceeding with the game to the next event.
    '''
    def __init__(self):
        self.continuetomatch = ContinueToMatch()
        self.continue_allowed = 0

    def on_continue_game(self):
        '''
        Determine whether game will continue, or handle if there is a match.
        '''
        if self.continue_allowed == 0:
            if not data.calendar.get_fixture():
                data.date.increment_date()
                data.window.screen.refresh_visible_screen()

            if data.calendar.get_fixture():
                data.calendar.get_user_fixture()

                data.window.mainscreen.information.set_continue_to_match()

                self.continue_allowed = 1

        if self.continue_allowed == 1:
            self.continue_allowed = 2
        elif self.continue_allowed == 2:
            opposition = data.calendar.get_user_opposition()
            self.on_continue_to_match(opposition)

    def on_continue_to_match(self, club):
        '''
        Determine whether match can continue or display error.
        '''
        if not self.continuetomatch.state:
            if self.continuetomatch.get_valid_squad():
                dialog = uigtk.match.ProceedToMatch(club.name)

                if dialog.show():
                    self.continuetomatch.get_selected_substitutes()


class ContinueToMatch:
    '''
    Class to verify whether next match is able to be played.
    '''
    def __init__(self):
        self.state = False

    def get_valid_squad(self):
        '''
        Verify eleven selected players are eligible.
        '''
        club = data.clubs.get_club_by_id(data.user.team)
        count = club.squad.teamselection.get_team_count()

        if count < 11:
            uigtk.match.NotEnoughPlayers(count)

            state = False
        else:
            state = True

        return state

    def get_selected_substitutes(self):
        '''
        Check whether the user has selected all substitutes.
        '''
        club = data.clubs.get_club_by_id(data.user.team)
        count = club.squad.teamselection.get_subs_count()

        if count < 5:
            dialog = uigtk.match.NotEnoughSubs(count)

            if dialog.show():
                data.window.screen.change_visible_screen("match")
                data.window.screen.active.update_match_details()
