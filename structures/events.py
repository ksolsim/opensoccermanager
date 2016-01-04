#!/usr/bin/env python3

import data


class Events:
    def __init__(self):
        self.club = data.clubs.get_club_by_id(data.user.team)

    def process_daily_events(self):
        self.club.sponsorship.update_sponsorship()
        data.injury.generate_injuries()
        data.injury.increment_fitness()
        data.advertising.assistant_handled()

    def process_weekly_events(self):
        self.club.finances.loan.update_interest_rate()
        self.club.finances.overdraft.update_interest_rate()
        data.players.update_contracts()
        self.club.pay_players()
        self.club.pay_staff()
        self.club.coaches.update_contracts()
        self.club.scouts.update_contracts()
        data.advertising.decrement_advertising()
        data.advertising.refresh_advertising()

    def process_monthly_events(self):
        print("Monthly events")

    def process_end_of_season_events(self):
        pass
