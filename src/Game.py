"""Game.py - Contains the Game object that holds all objects in the game - players, cities, 
   dredges, and the game Map."""

import random
from Cities import City
from Player import Player
from GroundUnits import Infantry
from GraphicUtils import colors

Demo = True


def comprehension_flatten(iter_lst):
    return list(item for iter_ in iter_lst for item in iter_)


class Game(object):
    """Holds the various game objects"""

    def __init__(self):
        self.turn = 1

        possible_cities = [City("Boston", (530, 10)),
                           City("New York", (390, 120)),
                           City("Norfolk", (280, 360)),
                           City("Jacksonville", (15, 750)),
                           ]
        self.cities = random.sample(possible_cities, 3)

        self.players = [Player()]
        self.players[0].assign_city(self.cities[0])
        self.players[0].assign_unit(Infantry(coords=(320,320)))

    @property
    def units(self):
        """return a list of all units"""
        return comprehension_flatten([p.units for p in self.players])  # this returns a flat list of all units

