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


import configparser
import os

import data


class Preferences:
    def __init__(self):
        home = os.path.expanduser("~")
        self.data_path = os.path.join(home, ".config", "opensoccermanager")
        self.save_path = os.path.join(self.data_path, "saves")
        self.preferences_path = os.path.join(self.data_path, "preferences.ini")
        self.database_path = os.path.join("databases", "opensoccermanager.db")

        self.start_screen = "squad"
        self.currency = 0
        self.confirm_quit = False

        self.play_music = False

        self.window_size = [800, 480]
        self.window_position = [0, 0]
        self.window_maximized = False

        self.confighandler = configparser.ConfigParser()

        if not os.path.exists(self.data_path):
            os.mkdir(self.data_path)

        if not os.path.exists(self.save_path):
            os.mkdir(self.save_path)

        if not os.path.exists(self.preferences_path):
            self.create_initial_config()

    def create_initial_config(self):
        '''
        Create the initial config when it doesn't exist.
        '''
        self.confighandler["AUDIO"] = {"PlayMusic": False}
        self.confighandler["INTERFACE"] = {"Currency": 0,
                                           "StartScreen": "squad",
                                           "Maximized": False,
                                           "ConfirmQuit": False,
                                           "Width": 780,
                                           "Height": 480,
                                           "XPosition": 0,
                                           "YPosition": 0}
        self.confighandler["DATABASE"] = {"Database": self.database_path}
        self.confighandler["SAVE"] = {"Data": self.data_path}

        with open(self.preferences_path, "w") as config:
            self.confighandler.write(config)

    def read_from_config(self):
        '''
        Read preference settings from file.
        '''
        self.confighandler.read(self.preferences_path, encoding='utf-8')

        self.play_music = self.confighandler["AUDIO"].getboolean("PlayMusic")
        self.start_screen = self.confighandler["INTERFACE"]["StartScreen"]
        self.currency = int(self.confighandler["INTERFACE"]["Currency"])
        self.confirm_quit = self.confighandler["INTERFACE"].getboolean("ConfirmQuit")

        width = int(self.confighandler["INTERFACE"]["Width"])
        height = int(self.confighandler["INTERFACE"]["Height"])
        self.window_size = [width, height]

        self.window_maximized = self.confighandler["INTERFACE"].getboolean("Maximized")
        xposition = int(self.confighandler["INTERFACE"]["XPosition"])
        yposition = int(self.confighandler["INTERFACE"]["YPosition"])
        self.window_position = [xposition, yposition]

        self.database_path = self.confighandler["DATABASE"]["Database"]
        self.data_path = self.confighandler["SAVE"]["Data"]
        self.save_path = os.path.join(self.data_path, "saves")

    def write_to_config(self):
        '''
        Write preference settings to file.
        '''
        self.confighandler["AUDIO"]["PlayMusic"] = str(self.play_music)
        self.confighandler["INTERFACE"]["StartScreen"] = self.start_screen
        self.confighandler["INTERFACE"]["Currency"] = str(self.currency)
        self.confighandler["INTERFACE"]["ConfirmQuit"] = str(self.confirm_quit)
        self.confighandler["INTERFACE"]["Maximized"] = str(data.window.is_maximized())

        width, height = data.window.get_size()
        self.confighandler["INTERFACE"]["Width"] = str(width)
        self.confighandler["INTERFACE"]["Height"] = str(height)

        xposition, yposition = data.window.get_position()
        self.confighandler["INTERFACE"]["XPosition"] = str(xposition)
        self.confighandler["INTERFACE"]["YPosition"] = str(yposition)

        self.confighandler["DATABASE"]["Database"] = self.database_path
        self.confighandler["SAVE"]["Data"] = self.data_path

        with open(self.preferences_path, "w") as config:
            self.confighandler.write(config)
