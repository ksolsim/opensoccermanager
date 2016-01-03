#!/usr/bin/env python3

import data
import uigtk.continuedialog


class Date:
    def __init__(self, year):
        self.day = 1
        self.month = 8
        self.year = int(year)
        self.week = 1

        self.week_count = 0

    def increment_date(self):
        '''
        Increment date and week, and update display for user.
        '''
        maximum = data.calendar.get_maximum_days(self.month)

        self.week_count += 1

        if self.week_count == 7:
            self.week += 1
            self.week_count = 0

            data.events.process_weekly_events()

        if self.day == maximum:
            self.month += 1
            self.day = 1
        else:
            self.day += 1

            data.events.process_daily_events()

        if self.month == 12:
            self.year += 1
            self.month = 1

        dialog = uigtk.continuedialog.ContinueDialog()
        dialog.show()

    def set_end_of_year(self):
        '''
        Increment year and reset day and month values.
        '''
        self.year += 1
        self.month = 1
        self.day = 1

    def set_end_of_season(self):
        '''
        Set day and month for start of new season.
        '''
        self.month = 8
        self.day = 1
        self.week = 1

    def get_season(self):
        '''
        Return the current season string.
        '''
        season = "%i/%i" % (self.year, self.year + 1)

        return season

    def get_date_as_string(self):
        '''
        Return the date string for display.
        '''
        if self.day < 10:
            day = "0%i" % (self.day)
        else:
            day = str(self.day)

        if self.month < 10:
            month = "0%i" % (self.month)
        else:
            month = str(self.month)

        date = "%i/%s/%s" % (self.year, month, day)

        return date

    def get_date_as_tuple(self):
        '''
        Return the date in tuple format.
        '''
        return self.year, self.month, self.day

    def get_date_for_event(self):
        '''
        Return day and month combo for use with event.
        '''
        return self.day, self.month
