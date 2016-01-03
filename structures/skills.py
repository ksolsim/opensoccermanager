#!/usr/bin/env python3


class Skills:
    def __init__(self):
        self.skills = (("KP", "Keeping"),
                       ("TK", "Tackling"),
                       ("PS", "Passing"),
                       ("SH", "Shooting"),
                       ("HD", "Heading"),
                       ("PC", "Pace"),
                       ("ST", "Stamina"),
                       ("BC", "Ball Control"),
                       ("SP", "Set Pieces"))

    def get_skills(self):
        '''
        Return complete tuple of skill names and short names.
        '''
        return self.skills

    def get_skill_by_index(self, index):
        '''
        Return skill name and short name for given index.
        '''
        return self.skills[index]

    def get_skill_name(self, index):
        '''
        Return skill name for given index.
        '''
        return self.skills[index][1]

    def get_names(self):
        '''
        Return tuple of full skill names.
        '''
        names = [item[1] for item in self.skills]

        return names

    def get_short_names(self):
        '''
        Return tuple of shortened skill names.
        '''
        names = [item[0] for item in self.skills]

        return names
