#!/usr/bin/env python

from configparser import ConfigParser
import os

import game


class Preferences(ConfigParser):
    def __init__(self):
        ConfigParser.__init__(self)

        home = os.path.expanduser("~")

        data = os.path.join(home, ".config", "opensoccermanager")
        save = os.path.join(home, ".config", "opensoccermanager", "saves")

        self["AUDIO"] = {"PlayMusic": False}
        self["INTERFACE"] = {"Currency": 0, "StartScreen": 1}
        self["DATABASE"] = {"Database": "osm1415.db"}
        self["SAVE"] = {"Data": data, "Saves": save}

        self.filename = os.path.join(data, "preferences.ini")

    def writefile(self):
        with open(self.filename, "w") as configfile:
            self.write(configfile)

    def readfile(self):
        self.read(self.filename)

        game.currency = int(self["INTERFACE"]["Currency"])
        game.start_screen = int(self["INTERFACE"]["StartScreen"])
        game.music = self["AUDIO"].getboolean("PlayMusic")
        game.save_location = self["SAVE"]["Saves"]
        game.data_location = self["SAVE"]["Data"]
        game.database_filename = self["DATABASE"]["Database"]

        if game.save_location is "":
            home = os.path.expanduser("~")
            game.save_location = os.path.join(home, ".config", "opensoccermanager", "saves")
            self["SAVE"]["Saves"] = game.save_location

            self.writefile()

        if game.data_location is "":
            home = os.path.expanduser("~")
            game.data_location = os.path.join(home, ".config", "opensoccermanager")
            self["SAVE"]["Data"] = game.data_location

            self.writefile()
