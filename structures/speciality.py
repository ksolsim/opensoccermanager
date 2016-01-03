#!/usr/bin/env python3


class Speciality:
    def __init__(self):
        self.speciality = {0: "Goalkeeping",
                           1: "Defensive",
                           2: "Midfield",
                           3: "Attacking",
                           4: "Fitness",
                           5: "All"}

    def get_specialities(self):
        '''
        Return full set of specialities.
        '''
        return self.speciality

    def get_speciality_for_id(self, specialityid):
        '''
        Return speciality for given id value.
        '''
        return self.speciality[specialityid]


class Categories:
    def __init__(self):
        self.speciality = {0: ("Keeping",),
                           1: ("Tackling", "Stamina"),
                           2: ("Passing", "Ball Control"),
                           3: ("Shooting",),
                           4: ("Fitness", "Pace", "Stamina"),
                           5: ("All",)}

    def get_category_label(self, index):
        categories = self.speciality[index]

        if len(categories) > 1:
            return ", ".join(item for item in categories)
        else:
            return categories[0]
