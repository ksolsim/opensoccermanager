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

import data
import structures.skills
import uigtk.playersearch
import uigtk.squad
import uigtk.widgets


class PlayerInformation(uigtk.widgets.Grid):
    __name__ = "playerinformation"

    playerid = None

    def __init__(self):
        uigtk.widgets.Grid.__init__(self)

        self.labelName = uigtk.widgets.Label()
        self.labelName.set_hexpand(True)
        self.attach(self.labelName, 0, 0, 3, 1)

        buttonbox = uigtk.widgets.ButtonBox()
        buttonbox.set_layout(Gtk.ButtonBoxStyle.END)
        self.attach(buttonbox, 2, 0, 3, 1)
        buttonBack = uigtk.widgets.Button("_Back")
        buttonBack.set_tooltip_text("Return to previously visible screen.")
        buttonBack.connect("clicked", self.on_back_clicked)
        buttonbox.add(buttonBack)
        self.buttonActions = Gtk.MenuButton("_Actions")
        self.buttonActions.set_use_underline(True)
        self.buttonActions.set_tooltip_text("Perform actions on current player.")
        buttonbox.add(self.buttonActions)

        # Personal bar
        self.personal = Personal()
        self.attach(self.personal, 0, 1, 3, 1)

        grid = uigtk.widgets.Grid()
        self.attach(grid, 0, 2, 3, 1)

        # Skills
        box = Gtk.Box()
        box.set_orientation(Gtk.Orientation.VERTICAL)
        grid.attach(box, 0, 0, 1, 2)

        self.skills = Skills()
        box.pack_start(self.skills, False, False, 0)

        self.morale = Morale()
        box.pack_start(self.morale, False, False, 0)

        self.transfer = Transfer()
        box.pack_start(self.transfer, True, True, 0)

        # History
        self.history = History()
        grid.attach(self.history, 1, 0, 2, 1)

        # Contract
        self.contract = Contract()
        grid.attach(self.contract, 1, 1, 1, 1)

        # Injuries / suspensions / training
        box = Gtk.Box()
        box.set_orientation(Gtk.Orientation.VERTICAL)
        grid.attach(box, 2, 1, 1, 1)

        self.injuries = Injuries()
        box.pack_start(self.injuries, False, False, 0)

        self.suspensions = Suspensions()
        box.pack_start(self.suspensions, False, False, 0)

        self.training = Training()
        box.pack_start(self.training, False, False, 0)

    def on_back_clicked(self, *args):
        '''
        Return to previous screen when back button is clicked.
        '''
        data.window.screen.return_previous_screen()

    def set_visible_player(self, playerid):
        '''
        Update the display with the visible player for given id.
        '''
        PlayerInformation.playerid = playerid
        player = data.players.get_player_by_id(playerid)

        self.personal.club = player.club.clubid
        self.personal.nation = player.nationality

        self.labelName.set_label("<span size='24000'><b>%s</b></span>" % (player.get_name(mode=1)))

        self.personal.labelDateOfBirth.set_label("Date of Birth: %s (%i)" % (player.get_date_of_birth(), player.get_age()))
        self.personal.labelClub.set_markup("Club: <a href='club'>%s</a>" % (player.get_club_name()))
        self.personal.labelNationality.set_markup("Nation: <a href='nation'>%s</a>" % (player.get_nationality_name()))
        self.personal.labelPosition.set_label("Position: %s" % (player.position))

        for count, skill in enumerate(player.get_skills()):
            self.skills.labelAttributes[count].set_label("%s" % (skill))

        self.transfer.labelValue.set_label(player.value.get_value_as_string())
        self.transfer.set_purchase_status()
        self.transfer.set_loan_status()

        self.contract.labelWage.set_label(player.wage.get_wage_as_string())
        self.contract.labelLeagueChampBonus.set_label(player.contract.get_bonus(0))
        self.contract.labelLeagueRunnerUpBonus.set_label(player.contract.get_bonus(1))
        self.contract.labelWinBonus.set_label(player.contract.get_bonus(2))
        self.contract.labelGoalBonus.set_label(player.contract.get_bonus(3))
        self.contract.labelContract.set_label(player.contract.get_contract())

        self.history.update_history()

        self.morale.set_morale()

        self.training.set_fitness_value(player.injury.fitness)
        self.training.set_training_status()

        self.injuries.set_injury_status()
        self.suspensions.set_suspension_status()

        if player.club.clubid == data.user.clubid:
            actionmenu = ContextMenu1()
        else:
            actionmenu = ContextMenu2()

        actionmenu.playerid = playerid
        self.buttonActions.set_popup(actionmenu)
        actionmenu.show()

    def run(self):
        self.show_all()

        if PlayerInformation.playerid:
            self.set_visible_player(PlayerInformation.playerid)


class Personal(uigtk.widgets.Grid):
    def __init__(self):
        uigtk.widgets.Grid.__init__(self)
        self.set_column_homogeneous(True)

        self.labelDateOfBirth = Gtk.Label()
        self.attach(self.labelDateOfBirth, 0, 0, 1, 1)

        self.labelClub = Gtk.Label()
        self.labelClub.connect("activate-link", self.on_club_activated)
        self.attach(self.labelClub, 1, 0, 1, 1)

        self.labelNationality = Gtk.Label()
        self.labelNationality.connect("activate-link", self.on_nation_activated)
        self.attach(self.labelNationality, 2, 0, 1, 1)

        self.labelPosition = Gtk.Label()
        self.attach(self.labelPosition, 3, 0, 1, 1)

    def on_club_activated(self, *args):
        '''
        Load club information screen.
        '''
        data.window.screen.change_visible_screen("clubinformation")
        data.window.screen.active.set_visible_club(data.user.club)

        return True

    def on_nation_activated(self, label, uri):
        '''
        Load nation information screen.
        '''
        data.window.screen.change_visible_screen("nationsearch")
        data.window.screen.active.set_visible_nation(self.nation)

        return True


class Skills(uigtk.widgets.CommonFrame):
    def __init__(self):
        uigtk.widgets.CommonFrame.__init__(self, "Skills")

        skills = structures.skills.Skills()
        self.labelAttributes = []

        for count, skill in enumerate(skills.get_skills()):
            label = uigtk.widgets.Label("%s" % skill[1], leftalign=True)
            self.grid.attach(label, 0, count, 1, 1)
            label = uigtk.widgets.Label()
            label.set_hexpand(True)
            self.grid.attach(label, 1, count, 1, 1)
            self.labelAttributes.append(label)


class Transfer(uigtk.widgets.CommonFrame):
    def __init__(self):
        uigtk.widgets.CommonFrame.__init__(self, "Transfer")

        label = uigtk.widgets.Label("Value", leftalign=True)
        self.grid.attach(label, 0, 0, 1, 1)
        self.labelValue = uigtk.widgets.Label(leftalign=True)
        self.grid.attach(self.labelValue, 1, 0, 1, 1)

        self.labelPurchaseList = uigtk.widgets.Label(leftalign=True)
        self.grid.attach(self.labelPurchaseList, 0, 1, 2, 1)
        self.labelLoanList = uigtk.widgets.Label(leftalign=True)
        self.grid.attach(self.labelLoanList, 0, 2, 2, 1)

    def set_purchase_status(self):
        '''
        Set message for purchase listed status.
        '''
        player = data.players.get_player_by_id(PlayerInformation.playerid)

        if player.transfer[0]:
            self.labelPurchaseList.set_label("Currently added to purchase list.")
        else:
            self.labelPurchaseList.set_label("Not listed as available for purchase.")

    def set_loan_status(self):
        '''
        Set message for loan listed status.
        '''
        player = data.players.get_player_by_id(PlayerInformation.playerid)

        if player.transfer[1]:
            self.labelLoanList.set_label("Currently added to loan list.")
        else:
            self.labelLoanList.set_label("Not listed as available for loan.")


class Contract(uigtk.widgets.CommonFrame):
    def __init__(self):
        uigtk.widgets.CommonFrame.__init__(self, "Contract")

        label = uigtk.widgets.Label("Wage", leftalign=True)
        self.grid.attach(label, 0, 0, 1, 1)
        self.labelWage = uigtk.widgets.Label(leftalign=True)
        self.grid.attach(self.labelWage, 1, 0, 1, 1)
        label = uigtk.widgets.Label("Contract", leftalign=True)
        self.grid.attach(label, 0, 1, 1, 1)
        self.labelContract = uigtk.widgets.Label(leftalign=True)
        self.grid.attach(self.labelContract, 1, 1, 1, 1)

        label = uigtk.widgets.Label("League Champions Bonus", leftalign=True)
        self.grid.attach(label, 0, 2, 1, 1)
        self.labelLeagueChampBonus = uigtk.widgets.Label(leftalign=True)
        self.grid.attach(self.labelLeagueChampBonus, 1, 2, 1, 1)
        label = uigtk.widgets.Label("League Runner Up Bonus", leftalign=True)
        self.grid.attach(label, 0, 3, 1, 1)
        self.labelLeagueRunnerUpBonus = uigtk.widgets.Label(leftalign=True)
        self.grid.attach(self.labelLeagueRunnerUpBonus, 1, 3, 1, 1)
        label = uigtk.widgets.Label("Win Bonus", leftalign=True)
        self.grid.attach(label, 0, 4, 1, 1)
        self.labelWinBonus = uigtk.widgets.Label(leftalign=True)
        self.grid.attach(self.labelWinBonus, 1, 4, 1, 1)
        label = uigtk.widgets.Label("Goal Bonus", leftalign=True)
        self.grid.attach(label, 0, 5, 1, 1)
        self.labelGoalBonus = uigtk.widgets.Label(leftalign=True)
        self.grid.attach(self.labelGoalBonus, 1, 5, 1, 1)


class Injuries(uigtk.widgets.CommonFrame):
    def __init__(self):
        uigtk.widgets.CommonFrame.__init__(self, "Injuries")

        self.labelInjuries = uigtk.widgets.Label(leftalign=True)
        self.labelInjuries.set_line_wrap(True)
        self.grid.attach(self.labelInjuries, 0, 0, 1, 1)

    def set_injury_status(self):
        '''
        Set message for current injury status.
        '''
        player = data.players.get_player_by_id(PlayerInformation.playerid)

        if not player.injury.get_injured():
            message = "Not currently injured."
        else:
            message = "Out for %s with a %s." % (player.injury.get_injury_period(), player.injury.get_injury_name())

        self.labelInjuries.set_label(message)


class Suspensions(uigtk.widgets.CommonFrame):
    def __init__(self):
        uigtk.widgets.CommonFrame.__init__(self, "Suspensions")

        self.labelSuspensions = uigtk.widgets.Label(leftalign=True)
        self.labelSuspensions.set_line_wrap(True)
        self.grid.attach(self.labelSuspensions, 0, 0, 1, 1)

    def set_suspension_status(self):
        '''
        Set message for current injury status.
        '''
        player = data.players.get_player_by_id(PlayerInformation.playerid)

        if not player.suspension.get_suspended():
            message = "Not currently suspended."
        else:
            message = "Out for %s due to a %s." % (player.suspension.get_suspension_period(), player.suspension.get_suspension_name())

        self.labelSuspensions.set_label(message)


class Training(uigtk.widgets.CommonFrame):
    def __init__(self):
        uigtk.widgets.CommonFrame.__init__(self, "Training")

        label = uigtk.widgets.Label("Fitness", leftalign=True)
        self.grid.attach(label, 0, 0, 1, 1)
        self.labelFitness = uigtk.widgets.Label(leftalign=True)
        self.grid.attach(self.labelFitness, 1, 0, 1, 1)

        self.labelTraining = uigtk.widgets.Label(leftalign=True)
        self.labelTraining.set_line_wrap(True)
        self.grid.attach(self.labelTraining, 0, 1, 2, 1)

        self.skills = structures.skills.Skills()

    def set_fitness_value(self, value):
        '''
        Set the fitness value.
        '''
        self.labelFitness.set_label("%i%%" % (value))

    def set_training_status(self):
        '''
        Set the training status string.
        '''
        player = data.players.get_player_by_id(PlayerInformation.playerid)

        if player.club:
            if player.club.individual_training.get_player_in_training(PlayerInformation.playerid):
                item = player.club.individual_training.get_individual_training_by_playerid(PlayerInformation.playerid)

                coach = player.club.coaches.get_coach_by_id(item.coachid)
                skill = self.skills.get_skill_name(item.skill)

                message = "Currently working on %s with coach %s." % (skill, coach.name)
            else:
                message = "Not currently participating in individual training."

            self.labelTraining.set_label(message)


class History(uigtk.widgets.CommonFrame):
    def __init__(self):
        uigtk.widgets.CommonFrame.__init__(self, "History")

        scrolledwindow = uigtk.widgets.ScrolledWindow()
        self.grid.attach(scrolledwindow, 0, 0, 1, 1)

        self.liststore = Gtk.ListStore(str, str, str, int, int, int, str, int)

        treeview = uigtk.widgets.TreeView()
        treeview.set_hexpand(True)
        treeview.set_vexpand(True)
        treeview.set_model(self.liststore)
        scrolledwindow.add(treeview)

        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Season", column=0)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Club", column=1)
        treeviewcolumn.set_expand(True)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Transfer", column=2)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Appearances", column=3)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Goals", column=4)
        treeviewcolumn.set_fixed_width(50)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Assists", column=5)
        treeviewcolumn.set_fixed_width(50)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="Cards", column=6)
        treeviewcolumn.set_fixed_width(50)
        treeview.append_column(treeviewcolumn)
        treeviewcolumn = uigtk.widgets.TreeViewColumn(title="MOTM",
                                                      tooltip="Man of the Match",
                                                      column=7)
        treeviewcolumn.set_fixed_width(50)
        treeview.append_column(treeviewcolumn)

    def update_history(self):
        '''
        Update history treeview with current and previous seasons.
        '''
        player = data.players.get_player_by_id(PlayerInformation.playerid)

        self.liststore.clear()

        self.liststore.append(player.history.get_current_season())


class Morale(uigtk.widgets.CommonFrame):
    def __init__(self):
        uigtk.widgets.CommonFrame.__init__(self, "Morale")

        label = uigtk.widgets.Label("Morale", leftalign=True)
        self.grid.attach(label, 0, 0, 1, 1)
        self.labelMorale = uigtk.widgets.Label(leftalign=True)
        self.grid.attach(self.labelMorale, 1, 0, 1, 1)

        label = uigtk.widgets.Label("Actions", leftalign=True)
        label.set_yalign(0)
        self.grid.attach(label, 0, 1, 1, 1)
        self.labelActions = uigtk.widgets.Label(leftalign=True)
        self.labelActions.set_line_wrap(True)
        self.grid.attach(self.labelActions, 1, 1, 1, 1)

        self.morale = structures.morale.PlayerMorale()

    def set_morale(self):
        '''
        Display morale string for player.
        '''
        player = data.players.get_player_by_id(PlayerInformation.playerid)
        morale = self.morale.get_morale(player.morale)

        self.labelMorale.set_label(morale)


class ContextMenu1(Gtk.Menu):
    '''
    Context menu displayed for players belonging to user club.
    '''
    def __init__(self):
        Gtk.Menu.__init__(self)

        self.menuitemAddPurchase = uigtk.widgets.MenuItem("_Add To Purchase List")
        self.menuitemAddPurchase.connect("activate", self.on_purchase_list_clicked)
        self.append(self.menuitemAddPurchase)
        self.menuitemRemovePurchase = uigtk.widgets.MenuItem("_Remove From Purchase List")
        self.menuitemRemovePurchase.connect("activate", self.on_purchase_list_clicked)
        self.append(self.menuitemRemovePurchase)
        self.menuitemAddLoan = uigtk.widgets.MenuItem("_Add To Loan List")
        self.menuitemAddLoan.connect("activate", self.on_loan_list_clicked)
        self.append(self.menuitemAddLoan)
        self.menuitemRemoveLoan = uigtk.widgets.MenuItem("_Remove From Loan List")
        self.menuitemRemoveLoan.connect("activate", self.on_loan_list_clicked)
        self.append(self.menuitemRemoveLoan)
        menuitem = uigtk.widgets.MenuItem("_Renew Contract")
        menuitem.connect("activate", self.on_renew_contract_clicked)
        self.append(menuitem)
        menuitem = uigtk.widgets.MenuItem("_Terminate Contract")
        menuitem.connect("activate", self.on_terminate_contract_clicked)
        self.append(menuitem)
        self.menuitemNotForSale = uigtk.widgets.CheckMenuItem("_Not for Sale")
        self.menuitemNotForSale.connect("toggled", self.on_not_for_sale_clicked)
        self.append(self.menuitemNotForSale)

        separator = Gtk.SeparatorMenuItem()
        self.append(separator)

        menuitem = uigtk.widgets.MenuItem("Add To _Comparison")
        menuitem.connect("activate", self.on_comparison_clicked)
        self.append(menuitem)

    def on_purchase_list_clicked(self, *args):
        '''
        Add player to the transfer list for sale.
        '''
        self.player.transfer[0] = not self.player.transfer[0]
        self.update_sensitivity()

        data.window.screen.refresh_visible_screen()

    def on_loan_list_clicked(self, *args):
        '''
        Add player to the transfer list for loan.
        '''
        self.player.transfer[1] = not self.player.transfer[1]
        self.update_sensitivity()

        data.window.screen.refresh_visible_screen()

    def on_renew_contract_clicked(self, *args):
        '''
        Query user to renew contract of selected player.
        '''
        dialog = uigtk.squad.RenewContract(self.playerid)

        if dialog.show():
            data.window.screen.refresh_visible_screen()

    def on_terminate_contract_clicked(self, *args):
        '''
        Query user to terminate contract of selected player.
        '''
        dialog = uigtk.squad.TerminateContract(self.playerid)

        if dialog.show():
            self.player.contract.terminate_contract()
            data.window.screen.refresh_visible_screen()

    def on_not_for_sale_clicked(self, checkmenuitem):
        '''
        Toggle not for sale flag on player object.
        '''
        self.player.not_for_sale = checkmenuitem.get_active()

    def on_comparison_clicked(self, *args):
        '''
        Add player to stack for comparison.
        '''
        data.comparison.add_to_comparison(self.playerid)

    def update_sensitivity(self):
        '''
        Update menu item sensitivity for available options.
        '''
        self.menuitemAddPurchase.set_sensitive(not self.player.transfer[0])
        self.menuitemRemovePurchase.set_sensitive(self.player.transfer[0])
        self.menuitemAddLoan.set_sensitive(not self.player.transfer[1])
        self.menuitemRemoveLoan.set_sensitive(self.player.transfer[1])
        self.menuitemNotForSale.set_active(self.player.not_for_sale)

    def show(self):
        self.player = data.players.get_player_by_id(self.playerid)

        self.update_sensitivity()
        self.show_all()


class ContextMenu2(Gtk.Menu):
    def __init__(self):
        Gtk.Menu.__init__(self)

        self.menuitemPurchase = uigtk.widgets.MenuItem("Make Offer To _Purchase")
        self.menuitemPurchase.connect("activate", self.on_purchase_offer_clicked)
        self.append(self.menuitemPurchase)
        self.menuitemLoan = uigtk.widgets.MenuItem("Make Offer To _Loan")
        self.menuitemLoan.connect("activate", self.on_loan_offer_clicked)
        self.append(self.menuitemLoan)
        self.menuitemAddShortlist = uigtk.widgets.MenuItem("_Add To Shortlist")
        self.menuitemAddShortlist.connect("activate", self.on_add_to_shortlist_clicked)
        self.append(self.menuitemAddShortlist)
        self.menuitemRemoveShortlist = uigtk.widgets.MenuItem("_Remove From Shortlist")
        self.menuitemRemoveShortlist.connect("activate", self.on_remove_from_shortlist_clicked)
        self.append(self.menuitemRemoveShortlist)
        separator = Gtk.SeparatorMenuItem()
        self.append(separator)
        menuitem = uigtk.widgets.MenuItem("Add To _Comparison")
        menuitem.connect("activate", self.on_comparison_clicked)
        self.append(menuitem)

    def on_purchase_offer_clicked(self, *args):
        '''
        Initiate purchase offer of selected player.
        '''
        data.negotiations.initialise_purchase(self.playerid)

    def on_loan_offer_clicked(self, *args):
        '''
        Initiate loan offer of selected player.
        '''
        data.negotiations.initialise_loan(self.playerid)

    def on_add_to_shortlist_clicked(self, *args):
        '''
        Add player to shortlist.
        '''
        data.user.club.shortlist.add_to_shortlist(self.playerid)
        self.update_sensitivity()

    def on_remove_from_shortlist_clicked(self, *args):
        '''
        Remove player from shortlist.
        '''
        dialog = uigtk.shortlist.RemoveShortlist()

        if dialog.show(self.playerid):
            data.user.club.shortlist.remove_from_shortlist(self.playerid)
            self.update_sensitivity()

    def on_comparison_clicked(self, *args):
        '''
        Add player to stack for comparison.
        '''
        data.comparison.add_to_comparison(self.playerid)

    def update_sensitivity(self):
        '''
        Update menu item sensitivity for available options.
        '''
        sensitive = data.user.club.shortlist.get_player_in_shortlist(self.playerid)
        self.menuitemAddShortlist.set_sensitive(not sensitive)
        self.menuitemRemoveShortlist.set_sensitive(sensitive)

        if self.player.club:
            self.menuitemPurchase.set_label("Make Offer to _Purchase")
            self.menuitemLoan.set_sensitive(True)
        else:
            self.menuitemPurchase.set_label("Make Offer to _Sign")
            self.menuitemLoan.set_sensitive(False)

    def show(self):
        self.player = data.players.get_player_by_id(self.playerid)

        self.update_sensitivity()
        self.show_all()
