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


from gi.repository import Gtk
from gi.repository import Gdk
import random
import re
import statistics

import constants
import dialogs
import display
import evaluation
import game
import league
import widgets


class Evaluation(Gtk.Grid):
    __name__ = "evaluation"

    def __init__(self):
        Gtk.Grid.__init__(self)
        self.set_row_spacing(5)
        self.set_column_spacing(5)

        for count, text in enumerate(("Chairman", "Fans", "Finances", "Players", "Staff", "Overall")):
            label = widgets.AlignedLabel("<b>%s</b>" % (text))
            self.attach(label, 0, count * 2, 1, 1)

        label = Gtk.Label()
        self.attach(label, 0, 1, 1, 1)

        self.labelChairman = Gtk.Label()
        self.labelChairman.set_hexpand(True)
        self.labelChairman.set_alignment(0, 0.5)
        self.attach(self.labelChairman, 1, 1, 1, 1)
        self.labelChairmanPercent = Gtk.Label()
        self.attach(self.labelChairmanPercent, 2, 1, 1, 1)

        self.labelFans = Gtk.Label()
        self.labelFans.set_hexpand(True)
        self.labelFans.set_alignment(0, 0.5)
        self.attach(self.labelFans, 1, 3, 1, 1)
        self.labelFansPercent = Gtk.Label()
        self.attach(self.labelFansPercent, 2, 3, 1, 1)

        self.labelFinances = Gtk.Label()
        self.labelFinances.set_hexpand(True)
        self.labelFinances.set_alignment(0, 0.5)
        self.attach(self.labelFinances, 1, 5, 1, 1)
        self.labelFinancesPercent = Gtk.Label()
        self.attach(self.labelFinancesPercent, 2, 5, 1, 1)

        self.labelPlayers = Gtk.Label()
        self.labelPlayers.set_hexpand(True)
        self.labelPlayers.set_alignment(0, 0.5)
        self.attach(self.labelPlayers, 1, 7, 1, 1)
        self.labelPlayersPercent = Gtk.Label()
        self.attach(self.labelPlayersPercent, 2, 7, 1, 1)

        self.labelStaff = Gtk.Label()
        self.labelStaff.set_hexpand(True)
        self.labelStaff.set_alignment(0, 0.5)
        self.attach(self.labelStaff, 1, 9, 1, 1)
        self.labelStaffPercent = Gtk.Label()
        self.attach(self.labelStaffPercent, 2, 9, 1, 1)

        self.labelOverallPercent = Gtk.Label()
        self.attach(self.labelOverallPercent, 2, 11, 1, 1)

    def run(self):
        evaluation.update()

        club = game.clubs[game.teamid]

        # Chairman
        value = evaluation.indexer(club.evaluation[0])
        self.labelChairman.set_label('"%s"' % (random.choice(game.evaluation.statements[0][value])))
        self.labelChairmanPercent.set_markup("<b>%i%%</b>" % (club.evaluation[0]))

        # Fans
        value = evaluation.indexer(club.evaluation[1])
        self.labelFans.set_label('"%s"' % (random.choice(game.evaluation.statements[1][value])))
        self.labelFansPercent.set_markup("<b>%i%%</b>" % (club.evaluation[1]))

        # Finances
        value = evaluation.indexer(club.evaluation[2])
        self.labelFinances.set_label('"%s"' % (random.choice(game.evaluation.statements[2][value])))
        self.labelFinancesPercent.set_markup("<b>%i%%</b>" % (club.evaluation[2]))

        # Players
        value = evaluation.indexer(club.evaluation[3])
        self.labelPlayers.set_label('"%s"' % (random.choice(game.evaluation.statements[3][value])))
        self.labelPlayersPercent.set_markup("<b>%i%%</b>" % (club.evaluation[3]))

        # Staff
        if len(club.scouts_hired) + len(club.coaches_hired) > 0:
            value = evaluation.indexer(club.evaluation[4])
            self.labelStaff.set_label('"%s"' % (random.choice(game.evaluation.statements[4][value])))
            self.labelStaffPercent.set_markup("<b>%i%%</b>" % (club.evaluation[4]))
        else:
            self.labelStaff.set_label('"There are no scouts or coaches on staff."')
            self.labelStaffPercent.set_label("")

        overall = evaluation.calculate_overall()
        self.labelOverallPercent.set_markup("<b>%i%%</b>" % (overall))

        self.show_all()
