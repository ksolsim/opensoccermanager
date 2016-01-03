#!/usr/bin/env python3


class Training:
    def __init__(self):
        self.training = ("Attacking",
                         "Ball Skills",
                         "Corner Kicks",
                         "Crossing",
                         "Defending",
                         "Five-A-Side",
                         "Free Kicks",
                         "Gym",
                         "Long Ball",
                         "Moves",
                         "Offside Trap",
                         "Passing",
                         "Penalties",
                         "Set Pieces",
                         "Solo Runs",
                         "Throw-Ins")

    def get_training(self):
        '''
        Return full tuple of training names.
        '''
        return self.training
