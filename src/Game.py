"""Game.py - Contains the Game object that holds all objects in the game - players, cities, 
   dredges, and the game Map."""

import random
#from City import City
#from Player import Player

Demo = True


def comprehension_flatten(iter_lst):
    return list(item for iter_ in iter_lst for item in iter_)


class Game(object):
    """Holds the various game objects"""

    def __init__(self):
        self.turn = 1

        # possible_cities = [City(self.date, "Boston", (530, 10)),
        #                    City(self.date, "New York", (390, 120)),
        #                    City(self.date, "Norfolk", (280, 360)),
        #                    City(self.date, "Jacksonville", (15, 750)),
        #                    ]
        # self.cities = random.sample(possible_cities, 3)
        #
        # self.players = [Player()]

    # @property
    # def units(self):
    #     """return a list of all dredges"""
    #     return comprehension_flatten([p.units for p in self.players])  # this returns a flat list of all units

