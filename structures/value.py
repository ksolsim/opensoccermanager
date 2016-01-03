#!/usr/bin/env python3


class Value:
    def __init__(self):
        pass

    def get_value_as_string(self):
        pass

    def value_rounder(self):
        if value >= 1000000:
            divisor = 100000
        elif value >= 10000:
            divisor = 1000

        value = value - (value % divisor)
        value = int(value)

        return value
