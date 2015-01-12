#!/usr/bin/env python3

from gi.repository import Gtk


# Used when the player requests resetting of the filtering options
player_filter = (True, 0, (0, 20000000), (16, 50), 0, (0, 99), (0, 99), (0, 99), (0, 99), (0, 99), (0, 99), (0, 99), (0, 99), (0, 99))
squad_filter = (0, False)

# Populated by content of appropriate XML files and database tables
news = {}
evaluation = []
buildings = []
merchandise = []
catering = []
injuries = {}
suspensions = {}

formations = (("4-4-2", ("GK", "DL", "DR", "DC", "DC", "ML", "MR", "MC", "MC", "AS", "AS")),
              ("3-5-2", ("GK", "DC", "DC", "DC", "ML", "MR", "MC", "MC", "MC", "AS", "AS")),
              ("3-4-3", ("GK", "DC", "DC", "DC", "ML", "MR", "MC", "MC", "AS", "AS", "AS")),
              ("4-5-1", ("GK", "DL", "DR", "DC", "DC", "ML", "MR", "MC", "MC", "MC", "AS")),
              ("4-3-3", ("GK", "DL", "DR", "DC", "DC", "MC", "MC", "MC", "AS", "AS", "AS")),
              ("5-4-1", ("GK", "DL", "DR", "DC", "DC", "DC", "ML", "MR", "MC", "MC", "AS")),
              ("5-3-2", ("GK", "DL", "DR", "DC", "DC", "DC", "MC", "MC", "MC", "AS", "AS")),
              )

dates = (1, 4, 7), (9, 11, 14), (16, 19, 21), (23, 25, 27), (30, 1, 4), (6, 9, 11), (13, 16, 18), (20, 22, 25), (27, 30, 1), (4, 6, 9), (11, 14, 16), (18, 21, 23), (25, 27, 30), (1, 4, 6), (8, 10, 13), (15, 17, 20), (22, 25, 27), (29, 2, 4), (6, 9, 11), (13, 16, 18), (20, 22, 24), (26, 28, 1), (3, 6, 8), (10, 12, 15), (17, 19, 22), (24, 27, 29), (31, 2, 5), (7, 10, 12), (14, 16, 19), (21, 24, 26), (28, 3, 5), (7, 9, 12), (14, 17, 19), (21, 23, 26), (28, 31, 2), (4, 6, 9), (11, 13, 16), (18, 21, 23), (25, 28, 30), (2, 4, 7), (9, 12, 14), (16, 19, 22), (24, 26, 29), (31, 2, 4), (6, 10, 12), (14, 16, 18), (20, 22, 25), (27, 30, 3),

events = ("16/8"), ("23/8"), ("30/8"), ("13/9"), ("20/9"), ("27/9"), ("4/10"), ("18/10"), ("25/10"), ("1/11"), ("8/11"), ("22/11"), ("29/11"), ("2/12"), ("6/12"), ("13/12"), ("20/12"), ("26/12"), ("28/12"), ("1/1"), ("10/1"), ("17/1"), ("31/1"), ("7/2"), ("10/2"), ("21/2"), ("28/2"), ("3/3"), ("14/3"), ("21/3"), ("4/4"), ("11/4"), ("18/4"), ("25/4"), ("2/5"), ("9/5"), ("16/5"), ("24/5"),

skill = ("Keeping", "Tackling", "Passing", "Shooting", "Heading", "Pace", "Stamina", "Ball Control", "Set Pieces")

category = {1: "Announcements",
            2: "Chairman",
            3: "Assistant",
            4: "Transfers",
            5: "Finances",
            6: "Competitions",
            7: "Injury",
            8: "Business",
            9: "Awards",
            10: "Contracts",
            11: "Stadium",
            }

transfer_status = {0: "Awaiting response to your enquiry",
                   1: "Enquiry rejected by club",
                   2: "Enquiry accepted by club",
                   3: "Awaiting response to your offer",
                   4: "Offer rejected by club",
                   5: "Offer accepted by club",
                   6: "Awaiting reponse to your contract offer",
                   7: "Offer rejected by player",
                   8: "Offer accepted by player",
                   }

money = {0: (20000000, "Grandmother"),
         1: (10000000, "Very Easy"),
         2: (5000000, "Easy"),
         3: (2500000, "Average"),
         4: (1000000, "Hard"),
         5: (0, "Very Hard"),
         }

currency = {0: ("£", 1), 1: ("$", 1.6), 2: ("€", 1.25),}

intensity = {0: "Low", 1: "Medium", 2: "High",}

errors = {1: ("The club needs a minimum of 16 players in the squad", "Transfer Error", Gtk.MessageType.ERROR),
          2: ("The club is restricted to a maximum of 30 players in the squad", "Transfer Error", Gtk.MessageType.ERROR),
          3: ("There are no players specified for comparison.", "Comparison Error", Gtk.MessageType.ERROR),
          4: ("The club does not have enough money\nto complete this transaction.", "Not Enough Money", Gtk.MessageType.ERROR),
          5: ("Only one player has been selected for comparison.", "Comparison Error", Gtk.MessageType.ERROR),
          6: ("The current team selection contains an injured player.", "Injured Player", Gtk.MessageType.ERROR),
          7: ("A suspended player is currently listed in the team.", "Suspended Player", Gtk.MessageType.ERROR),
          8: ("The player currently does not wish to renew his contract.", "Renew Contract", Gtk.MessageType.INFO),
          9: ("Negotiations for this player are already in progress.", "Negotiation Error", Gtk.MessageType.ERROR),
          10: ("Scouting recommendations not available as there are no scouts on staff.", "Scouting Error", Gtk.MessageType.ERROR),
          11: ("The club do not wish to extend the loan at this time.", "Loan Extension", Gtk.MessageType.ERROR),
          12: ("There is currently no training schedule setup. The training camp can still be booked, however the players will not achieve the most out of the session.", "Training Camp", Gtk.MessageType.WARNING),
          13: ("There is not a full selection of first team and substitute players selected. The training camp can still be booked for the listed players at the cost of all sixteen.", "Training Camp", Gtk.MessageType.WARNING),
          }

team_training = ("No Training", "Individual", ("Attacking",
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
                                               "Throw-Ins",
                                               ))

morale = ("Miserable",
          "Very Unhappy",
          "Unhappy",
          "Displeased",
          "Content",
          "Pleased",
          "Happy",
          "Very Happy",
          "Delighted")
