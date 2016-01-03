#!/usr/bin/env python3


class Morale:
    morale = ["Annoyed",
              "Miserable",
              "Very Unhappy",
              "Unhappy",
              "Displeased",
              "Content",
              "Pleased",
              "Happy",
              "Very Happy",
              "Delighted"]


class PlayerMorale(Morale):
    '''
    Morale object used by players.
    '''
    def get_morale(self, value):
        '''
        Get player morale status for given value.
        '''
        if value >= 85:
            morale = self.morale[8]
        elif value >= 70:
            morale = self.morale[7]
        elif value >= 45:
            morale = self.morale[6]
        elif value >= 20:
            morale = self.morale[5]
        elif value >= 0:
            morale = self.morale[4]
        elif value >=-25:
            morale = self.morale[3]
        elif value >= -50:
            morale = self.morale[2]
        elif value >= -75:
            morale = self.morale[1]
        elif self.morale >= -100:
            morale = self.morale[0]

        return morale


class StaffMorale(Morale):
    '''
    Morale object used by coach and scout staff.
    '''
    def get_morale(self, value):
        '''
        Get staff morale status for given value.
        '''
        return self.morale[value]
