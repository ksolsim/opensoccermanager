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


import random

import transfer


class Negotiation:
    def __init__(self):
        self.playerid = 0

    def enquiry_initialise(self):
        '''
        Initiate the enquiry from the buying club.
        '''

    def enquiry_response(self):
        '''
        Determine the response whether the selling club is willing to part with
        the player.
        '''

    def offer_initialise(self):
        '''
        Set the offer details for the transfer.
        '''

    def offer_response(self):
        '''
        Selling club response to the offer for the player.
        '''

    def contract_initialise(self):
        '''
        Offer a contract to the player (transfer or free transfer only).
        '''

    def contract_response(self):
        '''
        Player response to the contract offer.
        '''

    def complete_transfer(self):
        '''
        Finialise the transfer move.
        '''

    def cancel_transfer(self):
        '''
        End the transfer negotiations and cleanup details.
        '''

    def update(self):
        '''
        Update the transfer status for negotiation.
        '''
