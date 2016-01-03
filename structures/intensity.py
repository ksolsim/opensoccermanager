#!/usr/bin/env python3


class Intensity:
    def __init__(self):
        self.intensity = ["Low", "Medium", "High"]

    def get_intensity_by_index(self, index):
        '''
        Get intensity name for given index.
        '''
        return self.intensity[index]
