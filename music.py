#!/usr/bin/env python3

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
