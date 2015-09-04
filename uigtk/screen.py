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

import uigtk.dialogs
from uigtk import interface
from uigtk import printing
from uigtk import sponsorship
import game
import menu
import user
import widgets


class ScreenGame(Gtk.Grid):
    def __init__(self):
        Gtk.Grid.__init__(self)

        game.menu = menu.Menu()
        self.attach(game.menu, 0, 0, 1, 1)

        game.menu.menuitemNew.connect("activate", self.new_game_clicked)
        game.menu.menuitemLoad.connect("activate", self.load_game_clicked)
        game.menu.menuitemSave.connect("activate", self.save_game_clicked)
        game.menu.menuitemDelete.connect("activate", self.delete_game_clicked)
        game.menu.menuitemPrint.connect("activate", self.print_clicked)
        game.menu.menuitemQuit.connect("activate", game.window.exit_game)

        game.menu.menuitemManager.connect("activate", self.name_change)
        game.menu.menuitemPreferences.connect("activate", self.preferences_dialog_clicked)

        game.menu.menuitemPlayers.connect("activate", lambda i: game.window.screen_loader(20))
        game.menu.menuitemComparison.connect("activate", self.player_comparison)
        game.menu.menuitemNews.connect("activate", lambda i: game.window.screen_loader(3))
        game.menu.menuitemFixtures.connect("activate", lambda i: game.window.screen_loader(2))
        game.menu.menuitemResults.connect("activate", lambda i: game.window.screen_loader(6))
        game.menu.menuitemStandings.connect("activate", lambda i: game.window.screen_loader(5))
        game.menu.menuitemCharts.connect("activate", lambda i: game.window.screen_loader(30))
        game.menu.menuitemEvaluation.connect("activate", lambda i: game.window.screen_loader(25))
        game.menu.menuitemOpposition.connect("activate", self.view_opposition)
        game.menu.menuitemNegotiations.connect("activate", lambda i: game.window.screen_loader(21))
        game.menu.menuitemShortlist.connect("activate", lambda i: game.window.screen_loader(22))
        game.menu.menuitemStatistics.connect("activate", lambda i: game.window.screen_loader(29))

        game.menu.menuitemStadium.connect("activate", lambda i: game.window.screen_loader(10))
        game.menu.menuitemBuildings.connect("activate", lambda i: game.window.screen_loader(14))
        game.menu.menuitemTickets.connect("activate", lambda i: game.window.screen_loader(19))
        game.menu.menuitemSponsorship.connect("activate", self.sponsorship_clicked)
        game.menu.menuitemAdvertising.connect("activate", lambda i: game.window.screen_loader(16))
        game.menu.menuitemMerchandise.connect("activate", lambda i: game.window.screen_loader(17))
        game.menu.menuitemCatering.connect("activate", lambda i: game.window.screen_loader(18))
        game.menu.menuitemFinances.connect("activate", lambda i: game.window.screen_loader(11))
        game.menu.menuitemAccounts.connect("activate", lambda i: game.window.screen_loader(12))

        game.menu.menuitemSquad.connect("activate", lambda i: game.window.screen_loader(1))
        game.menu.menuitemTactics.connect("activate", lambda i: game.window.screen_loader(4))
        game.menu.menuitemTeamTraining.connect("activate", lambda i: game.window.screen_loader(7))
        game.menu.menuitemIndTraining.connect("activate", lambda i: game.window.screen_loader(9))
        game.menu.menuitemTrainingCamp.connect("activate", lambda i: game.window.screen_loader(8))
        game.menu.menuitemInjSus.connect("activate", lambda i: game.window.screen_loader(24))
        game.menu.menuitemStaff.connect("activate", lambda i: game.window.screen_loader(23))

        game.menu.menuitemContents.connect("activate", self.help_content_clicked)
        game.menu.menuitemInformation.connect("activate", self.info_dialog_clicked)
        game.menu.menuitemAbout.connect("activate", self.aboutdialog_clicked)

        grid = Gtk.Grid()
        grid.set_border_width(1)
        grid.set_column_spacing(5)
        self.attach(grid, 0, 2, 1, 1)

        widgets.date = widgets.Date()
        grid.attach(widgets.date, 0, 0, 1, 1)

        widgets.news = widgets.News()
        widgets.news.connect("clicked", self.news_activated)
        grid.attach(widgets.news, 1, 0, 1, 1)

        label = Gtk.Label()  # Intentional blank label
        label.set_hexpand(True)
        grid.attach(label, 2, 0, 1, 1)

        widgets.nextmatch = widgets.NextMatch()
        grid.attach(widgets.nextmatch, 3, 0, 1, 1)

        widgets.continuegame = widgets.Button("_Continue Game")
        widgets.continuegame.connect("clicked", self.on_continue_game_clicked)
        grid.attach(widgets.continuegame, 4, 0, 1, 1)

    def run(self):
        self.show_all()

    def name_change(self, menuitem):
        club = user.get_user_club()
        previous = club.manager

        name_change = interface.NameChange()

        if name_change.display():
            game.news.set_manager_name(previous)

            game.window.screen_loader(game.active_screen_id)

    def news_activated(self, button):
        game.window.screen_loader(3)

        game.window.screenNews.select_oldest_item()

    def player_comparison(self, menuitem):
        if dialogs.comparison.comparison == [None, None]:
            dialogs.error(3)
        elif not dialogs.comparison.comparison[0] or not dialogs.comparison.comparison[1]:
            dialogs.error(5)
        else:
            dialogs.comparison.display()

    def view_opposition(self, menuitem):
        dialog = uigtk.dialogs.Opposition()
        dialog.display()

    def sponsorship_clicked(self, menuitem):
        dialog = sponsorship.Sponsorship()
        dialog.display()

    def new_game_clicked(self, menuitem):
        exit_dialog = interface.ExitDialog()

        if not exit_dialog.display(leave=True):
            game.window.remove(game.window.screenGame)
            game.window.add(game.window.screenMain)

            # Reset teamid to zero to prevent having to confirm quit
            game.teamid = None

    def load_game_clicked(self, menuitem):
        open_dialog = interface.OpenDialog()

        if open_dialog.display():
            game.window.screen_loader(game.active_screen_id)

    def save_game_clicked(self, menuitem):
        save_dialog = interface.SaveDialog()
        save_dialog.display()
        save_dialog.destroy()

    def delete_game_clicked(self, menuitem):
        delete_dialog = interface.DeleteDialog()
        delete_dialog.display()

    def print_clicked(self, menuitem):
        print_dialog = printing.PrintType()
        print_dialog.display()

    def preferences_dialog_clicked(self, menuitem):
        preferences_dialog = interface.PreferencesDialog()
        preferences_dialog.display()

        game.window.screen_loader(game.active_screen_id)

    def aboutdialog_clicked(self, menuitem):
        about_dialog = interface.AboutDialog()
        about_dialog.display()

    def help_content_clicked(self, menuitem):
        help_dialog = interface.HelpDialog()
        help_dialog.display()

    def info_dialog_clicked(self, menuitem):
        info_dialog = interface.InfoDialog()
        info_dialog.display()

    def on_continue_game_clicked(self, button):
        game.continuegame.continue_game()

        game.window.screen_loader(game.active_screen_id)
