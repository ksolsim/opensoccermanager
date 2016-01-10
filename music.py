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

from gi.repository import Gst
import os
import sys

import data


Gst.init(sys.argv)


class Music(Gst.Pipeline):
    def __init__(self):
        Gst.Pipeline.__init__(self)

        self.music_file = os.path.join("resources", "usmtheme.wav")
        self.music_uri = Gst.filename_to_uri(self.music_file)

        self.playbin = Gst.ElementFactory.make("playbin")
        self.playbin.set_property("uri", self.music_uri)
        self.playbin.set_state(Gst.State.NULL)
        self.playbin.connect("about-to-finish", self.on_about_to_finish)
        self.add(self.playbin)

    def play(self):
        '''
        Begin playing of music and set playing state.
        '''
        data.preferences.play_music = True
        self.set_state(Gst.State.PLAYING)

    def stop(self):
        '''
        Stop playing of music and set playing state.
        '''
        data.preferences.play_music = False
        self.set_state(Gst.State.NULL)

    def on_about_to_finish(self, playbin):
        '''
        Set music to repeat.
        '''
        self.playbin.set_property("uri", self.music_uri)
