#!/usr/bin/env python

from gi.repository import Gst
import os
import sys

import game


Gst.init(sys.argv)

music_file = os.path.join("resources", "usmtheme.wav")
music_uri = Gst.filename_to_uri(music_file)


class Player(Gst.Pipeline):
    def __init__(self):
        Gst.Pipeline.__init__(self)

        self.playbin = Gst.ElementFactory.make("playbin")
        self.playbin.set_property("uri", music_uri)
        self.playbin.set_state(Gst.State.NULL)
        self.playbin.connect("about-to-finish", self.on_about_to_finish)
        self.add(self.playbin)

    def play(self):
        game.music = True
        self.set_state(Gst.State.PLAYING)

    def stop(self):
        game.music = False
        self.set_state(Gst.State.NULL)

    def on_about_to_finish(self, playbin):
        self.playbin.set_property("uri", music_uri)
