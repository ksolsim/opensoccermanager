#!/usr/bin/env python3

from gi.repository import Gtk

import game
import widgets


class Menu(Gtk.MenuBar):
    '''
    Main menu structure seen once the game has been started.
    '''
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
        key, mod = Gtk.accelerator_parse("<CONTROL>2")
        self.menuitemPlayers.add_accelerator("activate",
                                          game.accelgroup,
                                          key,
                                          mod,
                                          Gtk.AccelFlags.VISIBLE)
        menu.append(self.menuitemPlayers)
        self.menuitemComparison = widgets.MenuItem("C_omparison")
        key, mod = Gtk.accelerator_parse("<CONTROL><SHIFT>U")
        self.menuitemComparison.add_accelerator("activate",
                                          game.accelgroup,
                                          key,
                                          mod,
                                          Gtk.AccelFlags.VISIBLE)
        menu.append(self.menuitemComparison)
        separator = Gtk.SeparatorMenuItem()
        menu.append(separator)
        self.menuitemNews = widgets.MenuItem("_News")
        key, mod = Gtk.accelerator_parse("<CONTROL>4")
        self.menuitemNews.add_accelerator("activate",
                                          game.accelgroup,
                                          key,
                                          mod,
                                          Gtk.AccelFlags.VISIBLE)
        menu.append(self.menuitemNews)
        self.menuitemFixtures = widgets.MenuItem("_Fixtures")
        key, mod = Gtk.accelerator_parse("<CONTROL><SHIFT>F")
        self.menuitemFixtures.add_accelerator("activate",
                                          game.accelgroup,
                                          key,
                                          mod,
                                          Gtk.AccelFlags.VISIBLE)
        menu.append(self.menuitemFixtures)
        self.menuitemResults = widgets.MenuItem("_Results")
        key, mod = Gtk.accelerator_parse("<CONTROL><SHIFT>R")
        self.menuitemResults.add_accelerator("activate",
                                          game.accelgroup,
                                          key,
                                          mod,
                                          Gtk.AccelFlags.VISIBLE)
        menu.append(self.menuitemResults)
        self.menuitemStandings = widgets.MenuItem("_Standings")
        key, mod = Gtk.accelerator_parse("<CONTROL>7")
        self.menuitemStandings.add_accelerator("activate",
                                          game.accelgroup,
                                          key,
                                          mod,
                                          Gtk.AccelFlags.VISIBLE)
        menu.append(self.menuitemStandings)
        self.menuitemCharts = widgets.MenuItem("_Charts")
        key, mod = Gtk.accelerator_parse("<CONTROL><SHIFT>C")
        self.menuitemCharts.add_accelerator("activate",
                                          game.accelgroup,
                                          key,
                                          mod,
                                          Gtk.AccelFlags.VISIBLE)
        menu.append(self.menuitemCharts)
        self.menuitemEvaluation = widgets.MenuItem("_Evaluation")
        key, mod = Gtk.accelerator_parse("<CONTROL><SHIFT>E")
        self.menuitemEvaluation.add_accelerator("activate",
                                          game.accelgroup,
                                          key,
                                          mod,
                                          Gtk.AccelFlags.VISIBLE)
        menu.append(self.menuitemEvaluation)
        self.menuitemOpposition = widgets.MenuItem("_Opposition")
        key, mod = Gtk.accelerator_parse("<CONTROL><SHIFT>O")
        self.menuitemOpposition.add_accelerator("activate",
                                          game.accelgroup,
                                          key,
                                          mod,
                                          Gtk.AccelFlags.VISIBLE)
        menu.append(self.menuitemOpposition)
        separator = Gtk.SeparatorMenuItem()
        menu.append(separator)
        self.menuitemNegotiations = widgets.MenuItem("Ne_gotiations")
        key, mod = Gtk.accelerator_parse("<CONTROL><SHIFT>G")
        self.menuitemNegotiations.add_accelerator("activate",
                                          game.accelgroup,
                                          key,
                                          mod,
                                          Gtk.AccelFlags.VISIBLE)
        menu.append(self.menuitemNegotiations)
        self.menuitemShortlist = widgets.MenuItem("Short_list")
        key, mod = Gtk.accelerator_parse("<CONTROL><SHIFT>L")
        self.menuitemShortlist.add_accelerator("activate",
                                          game.accelgroup,
                                          key,
                                          mod,
                                          Gtk.AccelFlags.VISIBLE)
        menu.append(self.menuitemShortlist)
        separator = Gtk.SeparatorMenuItem()
        menu.append(separator)
        self.menuitemStatistics = widgets.MenuItem("_Statistics")
        key, mod = Gtk.accelerator_parse("<CONTROL><SHIFT>S")
        self.menuitemStatistics.add_accelerator("activate",
                                          game.accelgroup,
                                          key,
                                          mod,
                                          Gtk.AccelFlags.VISIBLE)
        menu.append(self.menuitemStatistics)

        menuitem = widgets.MenuItem("_Business")
        self.append(menuitem)
        menu = Gtk.Menu()
        menuitem.set_submenu(menu)
        self.menuitemStadium = widgets.MenuItem("_Stadium")
        key, mod = Gtk.accelerator_parse("<CONTROL><SHIFT>Z")
        self.menuitemStadium.add_accelerator("activate",
                                          game.accelgroup,
                                          key,
                                          mod,
                                          Gtk.AccelFlags.VISIBLE)
        menu.append(self.menuitemStadium)
        self.menuitemBuildings = widgets.MenuItem("_Buildings")
        key, mod = Gtk.accelerator_parse("<CONTROL><SHIFT>X")
        self.menuitemBuildings.add_accelerator("activate",
                                          game.accelgroup,
                                          key,
                                          mod,
                                          Gtk.AccelFlags.VISIBLE)
        menu.append(self.menuitemBuildings)
        separator = Gtk.SeparatorMenuItem()
        menu.append(separator)
        self.menuitemTickets = widgets.MenuItem("_Tickets")
        key, mod = Gtk.accelerator_parse("<CONTROL><SHIFT>K")
        self.menuitemTickets.add_accelerator("activate",
                                          game.accelgroup,
                                          key,
                                          mod,
                                          Gtk.AccelFlags.VISIBLE)
        menu.append(self.menuitemTickets)
        self.menuitemSponsorship = widgets.MenuItem("S_ponsorship")
        key, mod = Gtk.accelerator_parse("<CONTROL><SHIFT>O")
        self.menuitemSponsorship.add_accelerator("activate",
                                          game.accelgroup,
                                          key,
                                          mod,
                                          Gtk.AccelFlags.VISIBLE)
        menu.append(self.menuitemSponsorship)
        self.menuitemAdvertising = widgets.MenuItem("_Advertising")
        key, mod = Gtk.accelerator_parse("<CONTROL><SHIFT>D")
        self.menuitemAdvertising.add_accelerator("activate",
                                          game.accelgroup,
                                          key,
                                          mod,
                                          Gtk.AccelFlags.VISIBLE)
        menu.append(self.menuitemAdvertising)
        self.menuitemMerchandise = widgets.MenuItem("_Merchandise")
        key, mod = Gtk.accelerator_parse("<CONTROL><SHIFT>M")
        self.menuitemMerchandise.add_accelerator("activate",
                                          game.accelgroup,
                                          key,
                                          mod,
                                          Gtk.AccelFlags.VISIBLE)
        menu.append(self.menuitemMerchandise)
        self.menuitemCatering = widgets.MenuItem("_Catering")
        key, mod = Gtk.accelerator_parse("<CONTROL><SHIFT>T")
        self.menuitemCatering.add_accelerator("activate",
                                          game.accelgroup,
                                          key,
                                          mod,
                                          Gtk.AccelFlags.VISIBLE)
        menu.append(self.menuitemCatering)
        separator = Gtk.SeparatorMenuItem()
        menu.append(separator)
        self.menuitemFinances = widgets.MenuItem("_Finances")
        key, mod = Gtk.accelerator_parse("<CONTROL><SHIFT>F")
        self.menuitemFinances.add_accelerator("activate",
                                          game.accelgroup,
                                          key,
                                          mod,
                                          Gtk.AccelFlags.VISIBLE)
        menu.append(self.menuitemFinances)
        self.menuitemAccounts = widgets.MenuItem("A_ccounts")
        key, mod = Gtk.accelerator_parse("<CONTROL>9")
        self.menuitemAccounts.add_accelerator("activate",
                                          game.accelgroup,
                                          key,
                                          mod,
                                          Gtk.AccelFlags.VISIBLE)
        menu.append(self.menuitemAccounts)

        menuitem = widgets.MenuItem("_Team")
        self.append(menuitem)
        menu = Gtk.Menu()
        menuitem.set_submenu(menu)
        self.menuitemSquad = widgets.MenuItem("_Squad")
        key, mod = Gtk.accelerator_parse("<CONTROL>1")
        self.menuitemSquad.add_accelerator("activate",
                                          game.accelgroup,
                                          key,
                                          mod,
                                          Gtk.AccelFlags.VISIBLE)
        menu.append(self.menuitemSquad)
        self.menuitemTactics = widgets.MenuItem("_Tactics")
        key, mod = Gtk.accelerator_parse("<CONTROL>3")
        self.menuitemTactics.add_accelerator("activate",
                                          game.accelgroup,
                                          key,
                                          mod,
                                          Gtk.AccelFlags.VISIBLE)
        menu.append(self.menuitemTactics)
        menuitem = widgets.MenuItem("T_raining")
        menu.append(menuitem)
        menuTraining = Gtk.Menu()
        menuitem.set_submenu(menuTraining)
        self.menuitemTeamTraining = widgets.MenuItem("_Team Training")
        key, mod = Gtk.accelerator_parse("<CONTROL>5")
        self.menuitemTeamTraining.add_accelerator("activate",
                                          game.accelgroup,
                                          key,
                                          mod,
                                          Gtk.AccelFlags.VISIBLE)
        menuTraining.append(self.menuitemTeamTraining)
        self.menuitemIndTraining = widgets.MenuItem("_Individual Training")
        key, mod = Gtk.accelerator_parse("<CONTROL>6")
        self.menuitemIndTraining.add_accelerator("activate",
                                          game.accelgroup,
                                          key,
                                          mod,
                                          Gtk.AccelFlags.VISIBLE)
        menuTraining.append(self.menuitemIndTraining)
        self.menuitemTrainingCamp = widgets.MenuItem("Training _Camp")
        key, mod = Gtk.accelerator_parse("<CONTROL><SHIFT>C")
        self.menuitemTrainingCamp.add_accelerator("activate",
                                          game.accelgroup,
                                          key,
                                          mod,
                                          Gtk.AccelFlags.VISIBLE)
        menuTraining.append(self.menuitemTrainingCamp)
        self.menuitemInjSus = widgets.MenuItem("Injuries & _Suspensions")
        key, mod = Gtk.accelerator_parse("<CONTROL>8")
        self.menuitemInjSus.add_accelerator("activate",
                                          game.accelgroup,
                                          key,
                                          mod,
                                          Gtk.AccelFlags.VISIBLE)
        menu.append(self.menuitemInjSus)
        separator = Gtk.SeparatorMenuItem()
        menu.append(separator)
        self.menuitemStaff = widgets.MenuItem("_Staff")
        key, mod = Gtk.accelerator_parse("<CONTROL><SHIFT>Q")
        self.menuitemStaff.add_accelerator("activate",
                                          game.accelgroup,
                                          key,
                                          mod,
                                          Gtk.AccelFlags.VISIBLE)
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


class PlayersContextMenu(Gtk.Menu):
    '''
    Context menu displayed for players not belonging to the users club.
    '''
    def __init__(self):
        Gtk.Menu.__init__(self)

        self.menuitemTransfer = widgets.MenuItem("Make _Transfer Offer")
        self.append(self.menuitemTransfer)
        self.menuitemLoan = widgets.MenuItem("Make _Loan Offer")
        self.append(self.menuitemLoan)

        self.separator1 = Gtk.SeparatorMenuItem()
        self.append(self.separator1)

        self.menuitemAddShortlist = widgets.MenuItem("_Add To Shortlist")
        self.append(self.menuitemAddShortlist)
        self.menuitemRemoveShortlist = widgets.MenuItem("_Remove From Shortlist")
        self.append(self.menuitemRemoveShortlist)

        self.separator2 = Gtk.SeparatorMenuItem()
        self.append(self.separator2)

        self.menuitemComparison1 = widgets.MenuItem("Add to Comparison _1")
        self.append(self.menuitemComparison1)
        self.menuitemComparison2 = widgets.MenuItem("Add to Comparison _2")
        self.append(self.menuitemComparison2)

        separator = Gtk.SeparatorMenuItem()
        self.append(separator)

        self.menuitemRecommends = Gtk.CheckMenuItem("_Scout Recommends")
        self.menuitemRecommends.set_use_underline(True)
        self.append(self.menuitemRecommends)

    def display(self, mode=0):
        self.show_all()

        if mode == 1:
            self.menuitemTransfer.set_visible(False)
            self.menuitemLoan.set_visible(False)
            self.menuitemAddShortlist.set_visible(False)
            self.menuitemRemoveShortlist.set_visible(False)
            self.separator1.set_visible(False)
            self.separator2.set_visible(False)


class SquadContextMenu(Gtk.Menu):
    def __init__(self):
        Gtk.Menu.__init__(self)

        self.menuitemAddPosition = widgets.MenuItem("_Add To Position")
        self.append(self.menuitemAddPosition)
        self.menuitemRemovePosition = widgets.MenuItem("_Remove From Position")
        self.append(self.menuitemRemovePosition)

        separator = Gtk.SeparatorMenuItem()
        self.append(separator)

        self.menuitemAddTransfer = widgets.MenuItem("_Add To Transfer List")
        self.append(self.menuitemAddTransfer)
        self.menuitemRemoveTransfer = widgets.MenuItem("_Remove From Transfer List")
        self.append(self.menuitemRemoveTransfer)
        self.menuitemAddLoan = widgets.MenuItem("Add To _Loan List")
        self.append(self.menuitemAddLoan)
        self.menuitemRemoveLoan = widgets.MenuItem("_Remove From Loan List")
        self.append(self.menuitemRemoveLoan)
        self.menuitemQuickSell = widgets.MenuItem("_Quick Sell")
        self.append(self.menuitemQuickSell)
        self.menuitemRenewContract = widgets.MenuItem("Renew _Contract")
        self.append(self.menuitemRenewContract)
        self.menuitemNotForSale = Gtk.CheckMenuItem("_Not For Sale")
        self.menuitemNotForSale.set_use_underline(True)
        self.append(self.menuitemNotForSale)

        self.menuitemExtendLoan = widgets.MenuItem("_Extend Loan")
        self.append(self.menuitemExtendLoan)
        self.menuitemCancelLoan = widgets.MenuItem("_Cancel Loan")
        self.append(self.menuitemCancelLoan)
