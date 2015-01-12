#!/usr/bin/env python3

import random
import string

import game


class Staff:
    pass


def generate(number, role):
    '''
    Generates names for use as scouts and coaches. Takes a number, as in
    the number of staff names to generate when run.

    On first run, the game will request five coaches and five scouts. When staff
    are hired, the game will request a five minus the current number in the
    list.

    Periodically the game will request new scouts and coaches to be generated,
    around every three months.
    '''
    def name():
        # Generate the first (name) letter
        letters = list(string.ascii_letters[26:])
        initial = random.choice(letters)

        # Random surname
        surname = random.choice(game.surnames)
        name = "%s. %s" % (initial, surname)

        return name

    def age():
        age = random.randint(43, 61)

        return age

    def skill():
        def salary(level):
            if level == "Average":
                lower = 335
                upper = 380
            elif level == "Good":
                lower = 370
                upper = 555
            elif level == "Superb":
                lower = 545
                upper = 730

            wage = random.randrange(lower, upper, 5)

            return wage

        skill = ("Average", "Good", "Superb")
        level = random.choice(skill)

        wage = salary(level)

        return level, wage

    def speciality():
        speciality = ("Goalkeeping",
                      "Defensive",
                      "Midfield",
                      "Attacking",
                      "Fitness",
                      "All")
        speciality = random.choice(speciality)

        return speciality

    def contract():
        period = random.randint(24, 260)

        return period

    members = {}

    for count in range(1, 6):
        staff = Staff()
        staff.name = name()
        staff.age = age()
        staff.skill, staff.wage = skill()
        staff.contract = contract()
        staff.retiring = False

        if role == "coach":
            staff.speciality = speciality()
            members[game.coachid] = staff
            game.coachid += 1
        else:
            members[game.scoutid] = staff
            game.scoutid += 1

    return members
