#!/usr/bin/env python3

from gi.repository import Gtk

import game
import widgets


class Menu(Gtk.MenuBar):
    def __init__(self):
        Gtk.MenuBar.__init__(self)

        menuitem = widgets.MenuItem("_File")
        self.append(menuitem)
        menu = Gtk.Menu()
        menuitem.set_submenu(menu)
        self.menuitemNew = widgets.MenuItem("_New Game")
        key, mod = Gtk.accelerator_parse("<CONTROL>N")
        self.menuitemNew.add_accelerator("activate",
                                         game.accelgroup,
                                         key,
                                         mod,
                                         Gtk.AccelFlags.VISIBLE)
        menu.append(self.menuitemNew)
        self.menuitemLoad = widgets.MenuItem("_Load Game")
        key, mod = Gtk.accelerator_parse("<CONTROL>O")
        self.menuitemLoad.add_accelerator("activate",
                                          game.accelgroup,
                                          key,
                                          mod,
                                          Gtk.AccelFlags.VISIBLE)
        menu.append(self.menuitemLoad)
        self.menuitemSave = widgets.MenuItem("_Save Game")
        key, mod = Gtk.accelerator_parse("<CONTROL>S")
        self.menuitemSave.add_accelerator("activate",
                                          game.accelgroup,
                                          key,
                                          mod,
                                          Gtk.AccelFlags.VISIBLE)
        menu.append(self.menuitemSave)
        self.menuitemDelete = widgets.MenuItem("_Delete Game")
        menu.append(self.menuitemDelete)
        separator = Gtk.SeparatorMenuItem()
        menu.append(separator)
        self.menuitemQuit = widgets.MenuItem("_Quit")
        key, mod = Gtk.accelerator_parse("<CONTROL>Q")
        self.menuitemQuit.add_accelerator("activate",
                                          game.accelgroup,
                                          key,
                                          mod,
                                          Gtk.AccelFlags.VISIBLE)
        menu.append(self.menuitemQuit)

        menuitem = widgets.MenuItem("_Edit")
        self.append(menuitem)
        menu = Gtk.Menu()
        menuitem.set_submenu(menu)
        self.menuitemManager = widgets.MenuItem("_Manager Name")
        menu.append(self.menuitemManager)
        self.menuitemPreferences = widgets.MenuItem("_Preferences")
        menu.append(self.menuitemPreferences)

        menuitem = widgets.MenuItem("_View")
        self.append(menuitem)
        menu = Gtk.Menu()
        menuitem.set_submenu(menu)
        self.menuitemPlayers = widgets.MenuItem("_Players")
        menu.append(self.menuitemPlayers)
        self.menuitemComparison = widgets.MenuItem("C_omparison")
        menu.append(self.menuitemComparison)
        separator = Gtk.SeparatorMenuItem()
        menu.append(separator)
        self.menuitemNews = widgets.MenuItem("_News")
        menu.append(self.menuitemNews)
        self.menuitemFixtures = widgets.MenuItem("_Fixtures")
        menu.append(self.menuitemFixtures)
        self.menuitemResults = widgets.MenuItem("_Results")
        menu.append(self.menuitemResults)
        self.menuitemStandings = widgets.MenuItem("_Standings")
        menu.append(self.menuitemStandings)
        self.menuitemCharts = widgets.MenuItem("_Charts")
        menu.append(self.menuitemCharts)
        self.menuitemEvaluation = widgets.MenuItem("_Evaluation")
        menu.append(self.menuitemEvaluation)
        separator = Gtk.SeparatorMenuItem()
        menu.append(separator)
        self.menuitemNegotiations = widgets.MenuItem("Ne_gotiations")
        menu.append(self.menuitemNegotiations)
        self.menuitemShortlist = widgets.MenuItem("Short_list")
        menu.append(self.menuitemShortlist)
        separator = Gtk.SeparatorMenuItem()
        menu.append(separator)
        self.menuitemStatistics = widgets.MenuItem("_Statistics")
        menu.append(self.menuitemStatistics)

        menuitem = widgets.MenuItem("_Business")
        self.append(menuitem)
        menu = Gtk.Menu()
        menuitem.set_submenu(menu)
        self.menuitemStadium = widgets.MenuItem("_Stadium")
        menu.append(self.menuitemStadium)
        self.menuitemBuildings = widgets.MenuItem("_Buildings")
        menu.append(self.menuitemBuildings)
        separator = Gtk.SeparatorMenuItem()
        menu.append(separator)
        self.menuitemTickets = widgets.MenuItem("_Tickets")
        menu.append(self.menuitemTickets)
        self.menuitemSponsorship = widgets.MenuItem("S_ponsorship")
        menu.append(self.menuitemSponsorship)
        self.menuitemAdvertising = widgets.MenuItem("_Advertising")
        menu.append(self.menuitemAdvertising)
        self.menuitemMerchandise = widgets.MenuItem("_Merchandise")
        menu.append(self.menuitemMerchandise)
        self.menuitemCatering = widgets.MenuItem("_Catering")
        menu.append(self.menuitemCatering)
        separator = Gtk.SeparatorMenuItem()
        menu.append(separator)
        self.menuitemFinances = widgets.MenuItem("_Finances")
        menu.append(self.menuitemFinances)
        self.menuitemAccounts = widgets.MenuItem("A_ccounts")
        menu.append(self.menuitemAccounts)

        menuitem = widgets.MenuItem("_Team")
        self.append(menuitem)
        menu = Gtk.Menu()
        menuitem.set_submenu(menu)
        self.menuitemSquad = widgets.MenuItem("_Squad")
        menu.append(self.menuitemSquad)
        self.menuitemTactics = widgets.MenuItem("_Tactics")
        menu.append(self.menuitemTactics)
        menuitem = widgets.MenuItem("T_raining")
        menu.append(menuitem)
        menuTraining = Gtk.Menu()
        menuitem.set_submenu(menuTraining)
        self.menuitemTeamTraining = widgets.MenuItem("_Team Training")
        menuTraining.append(self.menuitemTeamTraining)
        self.menuitemIndTraining = widgets.MenuItem("_Individual Training")
        menuTraining.append(self.menuitemIndTraining)
        self.menuitemTrainingCamp = widgets.MenuItem("Training _Camp")
        menuTraining.append(self.menuitemTrainingCamp)
        self.menuitemInjSus = widgets.MenuItem("Injuries & _Suspensions")
        menu.append(self.menuitemInjSus)
        separator = Gtk.SeparatorMenuItem()
        menu.append(separator)
        self.menuitemStaff = widgets.MenuItem("_Staff")
        menu.append(self.menuitemStaff)

        menuitem = widgets.MenuItem("_Help")
        self.append(menuitem)
        menu = Gtk.Menu()
        menuitem.set_submenu(menu)
        self.menuitemContents = widgets.MenuItem("_Contents")
        key, mod = Gtk.accelerator_parse("F1")
        self.menuitemContents.add_accelerator("activate",
                                              game.accelgroup,
                                              key,
                                              mod,
                                              Gtk.AccelFlags.VISIBLE)
        menu.append(self.menuitemContents)
        self.menuitemInformation = widgets.MenuItem("_Information")
        menu.append(self.menuitemInformation)
        self.menuitemAbout = widgets.MenuItem("_About")
        menu.append(self.menuitemAbout)
