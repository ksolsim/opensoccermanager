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


from configparser import ConfigParser
import os

import game


class Preferences(ConfigParser):
    def __init__(self):
        ConfigParser.__init__(self)

        self.home = os.path.expanduser("~")
        data = os.path.join(self.home, ".config", "opensoccermanager")
        save = os.path.join(data, "saves")

        self.filename = os.path.join(data, "preferences.ini")

        self["AUDIO"] = {"PlayMusic": False}
        self["INTERFACE"] = {"Currency": 0,
                             "StartScreen": 1,
                             "Maximized": False,
                             "Width": 780,
                             "Height": 480,
                            }
        self["DATABASE"] = {"Database": "databases/opensoccermaanger.db"}
        self["SAVE"] = {"Data": data, "Saves": save}

    def writefile(self):
        with open(self.filename, "w") as configfile:
            self.write(configfile)

    def readfile(self):
        self.read(self.filename)

        game.currency = int(self["INTERFACE"]["Currency"])
        game.start_screen = int(self["INTERFACE"]["StartScreen"])

        maximized = self["INTERFACE"].getboolean("Maximized")

        if maximized:
            game.window.maximize()

        width = int(self["INTERFACE"]["Width"])
        height = int(self["INTERFACE"]["Height"])
        game.window.set_default_size(width, height)

        game.music = self["AUDIO"].getboolean("PlayMusic")
        game.data_location = self["SAVE"]["Data"]
        game.save_location = self["SAVE"]["Saves"]
        game.database_filename = self["DATABASE"]["Database"]

        if game.data_location is "":
            game.data_location = os.path.join(self.home, ".config", "opensoccermanager")
            self["SAVE"]["Data"] = game.data_location

            self.writefile()

        if game.save_location is "":
            game.save_location = os.path.join(game.data_location, "saves")
            self["SAVE"]["Saves"] = game.save_location

            self.writefile()

