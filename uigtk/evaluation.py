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
from matplotlib.figure import Figure
from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvas

import uigtk.widgets


class Evaluation(uigtk.widgets.Grid):
    __name__ = "evaluation"

    def __init__(self):
        uigtk.widgets.Grid.__init__(self)

        figure = Figure()
        axis = figure.add_subplot(1, 1, 1)
        axis.set_xlim(0, 46)
        axis.set_xlabel("Week")
        axis.set_ylim(0, 100)
        axis.set_ylabel("Percentage Rating")

        values = [0] * 46
        line, = axis.plot(values, label='Chairman')
        line, = axis.plot(values, label='Staff')
        line, = axis.plot(values, label='Fans')
        line, = axis.plot(values, label='Finances')
        line, = axis.plot(values, label='Media')
        axis.legend()

        figurecanvas = FigureCanvas(figure)
        figurecanvas.set_hexpand(True)
        figurecanvas.set_vexpand(True)
        self.add(figurecanvas)

    def run(self):
        self.show_all()
