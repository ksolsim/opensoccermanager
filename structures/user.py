#!/usr/bin/env python3

import os

import data


class User:
    '''
    User handling object storing selected club object.
    '''
    def __init__(self):
        self.team = None


class Names:
    def __init__(self):
        self.names = []

        self.names_path = "/home/andrew/.config/opensoccermanager/users.txt"

        if not os.path.exists(self.names_path):
            open(self.names_path, "w").close()

        self.populate_names()

    def get_names(self):
        '''
        Return list of stored names.
        '''
        return self.names

    def get_first_name(self):
        '''
        Return first name from list to display to user.
        '''
        return self.names[0]

    def add_name(self, name):
        '''
        Add name to list of names if it does not already exist.
        '''
        if name in self.names:
            self.names.remove(name)

        self.names.insert(0, name)

        self.save_names()

    def set_name(self, name):
        '''
        Retrieve chosen name and update in-game references.
        '''
        self.add_name(name)

        club = data.clubs.get_club_by_id(data.user.team)

        for article in club.news.articles.values():
            article.title = article.title.replace(club.manager, name)
            article.message = article.message.replace(club.manager, name)

        club.manager = name

    def save_names(self):
        '''
        Update names file with latest names.
        '''
        with open(self.names_path, "w") as fp:
            for name in self.names:
                fp.write("%s\n" % (name))

    def clear_names(self):
        '''
        Empty loaded names list.
        '''
        self.names = []

    def populate_names(self):
        with open(self.names_path, "r") as fp:
            names = fp.readlines()

            for name in names:
                self.names.append(name.rstrip("\n"))
