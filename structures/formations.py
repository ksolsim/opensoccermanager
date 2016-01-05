#!/usr/bin/env python3


class Formations:
    def __init__(self):
        self.formations = (("4-4-2", ("GK", "DL", "DR", "DC", "DC", "ML", "MR", "MC", "MC", "AS", "AS")),
                           ("3-5-2", ("GK", "DC", "DC", "DC", "ML", "MR", "MC", "MC", "MC", "AS", "AS")),
                           ("3-4-3", ("GK", "DC", "DC", "DC", "ML", "MR", "MC", "MC", "AS", "AS", "AS")),
                           ("4-5-1", ("GK", "DL", "DR", "DC", "DC", "ML", "MR", "MC", "MC", "MC", "AS")),
                           ("4-3-3", ("GK", "DL", "DR", "DC", "DC", "MC", "MC", "MC", "AS", "AS", "AS")),
                           ("5-4-1", ("GK", "DL", "DR", "DC", "DC", "DC", "ML", "MR", "MC", "MC", "AS")),
                           ("5-3-2", ("GK", "DL", "DR", "DC", "DC", "DC", "MC", "MC", "MC", "AS", "AS")),
                          )

    def get_formation_names(self):
        '''
        Return list of formation names.
        '''
        names = [name[0] for name in self.formations]

        return names

    def get_formations(self):
        '''
        Return full tuple of formation information.
        '''
        return self.formations

    def get_name(self, formationid):
        '''
        Get name of formation in use for given formation id.
        '''
        return self.formations[formationid][0]

    def get_positions(self, formationid):
        '''
        Get tuple of formation positions for given formation id.
        '''
        return self.formations[formationid][1]