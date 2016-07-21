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

import data
import uigtk.aboutdialog
import uigtk.comparison
import uigtk.filedialog
import uigtk.managername
import uigtk.playersearch
import uigtk.printdialog
import uigtk.quitdialog
import uigtk.screen
import uigtk.version
import uigtk.widgets


class Menu(Gtk.MenuBar):
    def __init__(self):
        Gtk.MenuBar.__init__(self)
        self.set_hexpand(True)

        menuitem = uigtk.widgets.MenuItem("_File")
        self.add(menuitem)
        menu = Gtk.Menu()
        menuitem.set_submenu(menu)
        menuitemNew = uigtk.widgets.MenuItem("_New Game...")
        key, modifier = Gtk.accelerator_parse("<Control>N")
        menuitemNew.add_accelerator("activate",
                                    data.window.accelgroup,
                                    key,
                                    modifier,
                                    Gtk.AccelFlags.VISIBLE)
        menuitemNew.connect("activate", self.on_new_clicked)
        menu.append(menuitemNew)
        menuitemLoad = uigtk.widgets.MenuItem("_Load Game...")
        key, modifier = Gtk.accelerator_parse("<Control>L")
        menuitemLoad.add_accelerator("activate",
                                     data.window.accelgroup,
                                     key,
                                     modifier,
                                     Gtk.AccelFlags.VISIBLE)
        menuitemLoad.connect("activate", uigtk.filedialog.LoadDialog)
        menu.append(menuitemLoad)
        menuitemSave = uigtk.widgets.MenuItem("_Save Game...")
        key, modifier = Gtk.accelerator_parse("<Control>S")
        menuitemSave.add_accelerator("activate",
                                     data.window.accelgroup,
                                     key,
                                     modifier,
                                     Gtk.AccelFlags.VISIBLE)
        menuitemSave.connect("activate", self.on_save_clicked)
        menu.append(menuitemSave)
        menuitemDelete = uigtk.widgets.MenuItem("_Delete Game...")
        menuitemDelete.connect("activate", uigtk.deletedialog.DeleteDialog)
        menu.append(menuitemDelete)
        separator = Gtk.SeparatorMenuItem()
        menu.append(separator)
        menuitemPrint = uigtk.widgets.MenuItem("_Print...")
        key, modifier = Gtk.accelerator_parse("<Control>P")
        menuitemPrint.add_accelerator("activate",
                                      data.window.accelgroup,
                                      key,
                                      modifier,
                                      Gtk.AccelFlags.VISIBLE)
        menuitemPrint.connect("activate", self.on_print_clicked)
        menu.append(menuitemPrint)
        separator = Gtk.SeparatorMenuItem()
        menu.append(separator)
        menuitemQuit = uigtk.widgets.MenuItem("_Quit Game")
        key, modifier = Gtk.accelerator_parse("<Control>Q")
        menuitemQuit.add_accelerator("activate",
                                     data.window.accelgroup,
                                     key,
                                     modifier,
                                     Gtk.AccelFlags.VISIBLE)
        menuitemQuit.connect("activate", self.on_quit_clicked)
        menu.append(menuitemQuit)

        menuitem = uigtk.widgets.MenuItem("_Edit")
        self.add(menuitem)
        menu = Gtk.Menu()
        menuitem.set_submenu(menu)
        menuitemSetManagerName = uigtk.widgets.MenuItem("_Set Manager Name...")
        menuitemSetManagerName.connect("activate", uigtk.managername.ManagerName)
        menu.append(menuitemSetManagerName)
        separator = Gtk.SeparatorMenuItem()
        menu.append(separator)
        menuitemPreferences = uigtk.widgets.MenuItem("_Preferences")
        menuitemPreferences.connect("activate", uigtk.preferences.Dialog)
        menu.append(menuitemPreferences)

        menuitem = uigtk.widgets.MenuItem("_Screen")
        self.add(menuitem)
        menu = Gtk.Menu()
        menuitem.set_submenu(menu)
        menuitemBack = uigtk.widgets.MenuItem("_Back")
        key, modifier = Gtk.accelerator_parse("<Alt>Left")
        menuitemBack.add_accelerator("activate",
                                     data.window.accelgroup,
                                     key,
                                     modifier,
                                     Gtk.AccelFlags.VISIBLE)
        menuitemBack.connect("activate", self.on_back_clicked)
        menu.append(menuitemBack)

        menuitem = uigtk.widgets.MenuItem("_View")
        self.add(menuitem)
        menu = Gtk.Menu()
        menuitem.set_submenu(menu)
        menuitem = uigtk.widgets.MenuItem("_Search")
        menu.append(menuitem)
        menuSearch = Gtk.Menu()
        menuitem.set_submenu(menuSearch)
        menuitemPlayerSearch = uigtk.widgets.MenuItem("_Players")
        menuitemPlayerSearch.name = "playersearch"
        key, modifier = Gtk.accelerator_parse("<Control>1")
        menuitemPlayerSearch.add_accelerator("activate",
                                             data.window.accelgroup,
                                             key,
                                             modifier,
                                             Gtk.AccelFlags.VISIBLE)
        menuitemPlayerSearch.connect("activate", self.on_screen_clicked)
        menuSearch.append(menuitemPlayerSearch)
        menuitemClubSearch = uigtk.widgets.MenuItem("_Clubs")
        menuitemClubSearch.name = "clubsearch"
        key, modifier = Gtk.accelerator_parse("<Control>2")
        menuitemClubSearch.add_accelerator("activate",
                                           data.window.accelgroup,
                                           key,
                                           modifier,
                                           Gtk.AccelFlags.VISIBLE)
        menuitemClubSearch.connect("activate", self.on_screen_clicked)
        menuSearch.append(menuitemClubSearch)
        menuitemNationSearch = uigtk.widgets.MenuItem("_Nations")
        menuitemNationSearch.name = "nationsearch"
        key, modifier = Gtk.accelerator_parse("<Control>3")
        menuitemNationSearch.add_accelerator("activate",
                                             data.window.accelgroup,
                                             key,
                                             modifier,
                                             Gtk.AccelFlags.VISIBLE)
        menuitemNationSearch.connect("activate", self.on_screen_clicked)
        menuSearch.append(menuitemNationSearch)
        separator = Gtk.SeparatorMenuItem()
        menu.append(separator)
        menuitemNews = uigtk.widgets.MenuItem("_News")
        menuitemNews.name = "news"
        menuitemNews.connect("activate", self.on_screen_clicked)
        menu.append(menuitemNews)
        menuitemShortlist = uigtk.widgets.MenuItem("_Shortlist")
        menuitemShortlist.name = "shortlist"
        menuitemShortlist.connect("activate", self.on_screen_clicked)
        menu.append(menuitemShortlist)
        menuitemNegotiations = uigtk.widgets.MenuItem("_Negotiations")
        menuitemNegotiations.name = "negotiations"
        menuitemNegotiations.connect("activate", self.on_screen_clicked)
        menu.append(menuitemNegotiations)
        menuitemFixtures = uigtk.widgets.MenuItem("_Fixtures")
        menuitemFixtures.name = "fixtures"
        menuitemFixtures.connect("activate", self.on_screen_clicked)
        menu.append(menuitemFixtures)
        menuitemStandings = uigtk.widgets.MenuItem("_Standings")
        menuitemStandings.name = "standings"
        menuitemStandings.connect("activate", self.on_screen_clicked)
        menu.append(menuitemStandings)
        separator = Gtk.SeparatorMenuItem()
        menu.append(separator)
        menuitemCharts = uigtk.widgets.MenuItem("_Charts")
        menuitemCharts.name = "charts"
        menuitemCharts.connect("activate", self.on_screen_clicked)
        menu.append(menuitemCharts)
        menuitemEvaluation = uigtk.widgets.MenuItem("_Evaluation")
        menuitemEvaluation.name = "evaluation"
        menuitemEvaluation.connect("activate", self.on_screen_clicked)
        menu.append(menuitemEvaluation)
        separator = Gtk.SeparatorMenuItem()
        menu.append(separator)
        menuitemComparison = uigtk.widgets.MenuItem("_Comparison")
        menuitemComparison.connect("activate", self.on_comparison_clicked)
        menu.append(menuitemComparison)

        menuitem = uigtk.widgets.MenuItem("_Business")
        self.add(menuitem)
        menu = Gtk.Menu()
        menuitem.set_submenu(menu)
        menuitemStadium = uigtk.widgets.MenuItem("_Stadium")
        menuitemStadium.name = "stadium"
        menuitemStadium.connect("activate", self.on_screen_clicked)
        menu.append(menuitemStadium)
        menuitemBuildings = uigtk.widgets.MenuItem("_Buildings")
        menuitemBuildings.name = "buildings"
        menuitemBuildings.connect("activate", self.on_screen_clicked)
        menu.append(menuitemBuildings)
        separator = Gtk.SeparatorMenuItem()
        menu.append(separator)
        menuitemTickets = uigtk.widgets.MenuItem("_Tickets")
        menuitemTickets.name = "tickets"
        menuitemTickets.connect("activate", self.on_screen_clicked)
        menu.append(menuitemTickets)
        menuitemSponsorship = uigtk.widgets.MenuItem("_Sponsorship")
        menuitemSponsorship.connect("activate", self.on_sponsorship_clicked)
        menu.append(menuitemSponsorship)
        menuitemAdvertising = uigtk.widgets.MenuItem("_Advertising")
        menuitemAdvertising.name = "advertising"
        menuitemAdvertising.connect("activate", self.on_screen_clicked)
        menu.append(menuitemAdvertising)
        menuitemMerchandise = uigtk.widgets.MenuItem("_Merchandise")
        menuitemMerchandise.name = "merchandise"
        menuitemMerchandise.connect("activate", self.on_screen_clicked)
        menu.append(menuitemMerchandise)
        menuitemCatering = uigtk.widgets.MenuItem("_Catering")
        menuitemCatering.name = "catering"
        menuitemCatering.connect("activate", self.on_screen_clicked)
        menu.append(menuitemCatering)
        separator = Gtk.SeparatorMenuItem()
        menu.append(separator)
        menuitemAccounts = uigtk.widgets.MenuItem("_Accounts")
        menuitemAccounts.name = "accounts"
        menuitemAccounts.connect("activate", self.on_screen_clicked)
        menu.append(menuitemAccounts)
        menuitemFinances = uigtk.widgets.MenuItem("_Finances")
        menuitemFinances.name = "finances"
        menuitemFinances.connect("activate", self.on_screen_clicked)
        menu.append(menuitemFinances)

        menuitem = uigtk.widgets.MenuItem("_Team")
        self.add(menuitem)
        menu = Gtk.Menu()
        menuitem.set_submenu(menu)
        menuitemSquad = uigtk.widgets.MenuItem("_Squad")
        menuitemSquad.name = "squad"
        menuitemSquad.connect("activate", self.on_screen_clicked)
        menu.append(menuitemSquad)
        menuitemTactics = uigtk.widgets.MenuItem("_Tactics")
        menuitemTactics.name = "tactics"
        menuitemTactics.connect("activate", self.on_screen_clicked)
        menu.append(menuitemTactics)
        menuitemTraining = uigtk.widgets.MenuItem("_Training")
        menu.append(menuitemTraining)
        menuTraining = Gtk.Menu()
        menuitemTraining.set_submenu(menuTraining)
        menuitemTeamTraining = uigtk.widgets.MenuItem("_Team Training")
        menuitemTeamTraining.name = "teamtraining"
        menuitemTeamTraining.connect("activate", self.on_screen_clicked)
        menuTraining.append(menuitemTeamTraining)
        menuitemIndividualTraining = uigtk.widgets.MenuItem("_Individual Training")
        menuitemIndividualTraining.name = "individualtraining"
        menuitemIndividualTraining.connect("activate", self.on_screen_clicked)
        menuTraining.append(menuitemIndividualTraining)
        menuitemTrainingCamp = uigtk.widgets.MenuItem("Training _Camp")
        menuitemTrainingCamp.name = "trainingcamp"
        menuitemTrainingCamp.connect("activate", self.on_screen_clicked)
        menuTraining.append(menuitemTrainingCamp)
        menuitemStaff = uigtk.widgets.MenuItem("_Staff")
        menuitemStaff.name = "staff"
        menuitemStaff.connect("activate", self.on_screen_clicked)
        menu.append(menuitemStaff)
        separator = Gtk.SeparatorMenuItem()
        menu.append(separator)
        menuitemUnavailable = uigtk.widgets.MenuItem("_Unavailable")
        menuitemUnavailable.name = "unavailable"
        menuitemUnavailable.connect("activate", self.on_screen_clicked)
        menu.append(menuitemUnavailable)

        menuitem = uigtk.widgets.MenuItem("_Help")
        self.add(menuitem)
        menu = Gtk.Menu()
        menuitem.set_submenu(menu)
        menuitemContents = uigtk.widgets.MenuItem("_Contents")
        key, modifier = Gtk.accelerator_parse("F1")
        menuitemContents.add_accelerator("activate",
                                         data.window.accelgroup,
                                         key,
                                         modifier,
                                         Gtk.AccelFlags.VISIBLE)
        menuitemContents.connect("activate", self.on_help_clicked)
        menu.append(menuitemContents)
        menuitemVersions = uigtk.widgets.MenuItem("_Versions")
        menuitemVersions.connect("activate", uigtk.version.VersionDialog)
        menu.append(menuitemVersions)
        separator = Gtk.SeparatorMenuItem()
        menu.append(separator)
        menuitemAbout = uigtk.widgets.MenuItem("_About")
        menuitemAbout.connect("activate", uigtk.aboutdialog.AboutDialog)
        menu.append(menuitemAbout)

    def on_new_clicked(self, *args):
        '''
        Ask user to save or instantly go the main menu screen.
        '''
        dialog = uigtk.quitdialog.UnsavedDialog()
        response = dialog.run()

        if response == Gtk.ResponseType.REJECT:
            data.window.welcome.set_show_welcome_screen()
        elif response == Gtk.ResponseType.ACCEPT:
            data.window.welcome.set_show_welcome_screen()

        dialog.destroy()

    def on_save_clicked(self, *args):
        '''
        Display save file dialog.
        '''
        dialog = uigtk.filedialog.SaveDialog()
        dialog.run()
        dialog.destroy()

    def on_print_clicked(self, *args):
        '''
        Display print dialog allowing user to select print output.
        '''
        dialog = uigtk.printdialog.PrintDialog()
        dialog.show()

    def on_back_clicked(self, *args):
        '''
        Move back to previously visible screen.
        '''
        data.window.screen.return_previous_screen()

    def on_sponsorship_clicked(self, *args):
        '''
        Display sponsorship dialog for current sponsor status.
        '''
        data.user.club.sponsorship.display_sponsorship_dialog()

    def on_comparison_clicked(self, *args):
        '''
        View comparison data for chosen players.
        '''
        data.comparison.set_show_comparison()

    def on_screen_clicked(self, menuitem):
        '''
        Load appropriate screen for item activated.
        '''
        data.window.screen.change_visible_screen(menuitem.name)

    def on_help_clicked(self, *args):
        '''
        Display help dialog window for current screen.
        '''
        data.window.help_dialog.show()

    def on_quit_clicked(self, *args):
        '''
        Handle quitting of game when clicked from menu.
        '''
        data.window.on_quit_game()
