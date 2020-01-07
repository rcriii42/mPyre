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

        possible_cities = [City("Boston", (17*32, 32)),
                           City("New York", (13*32, 4*32)),
                           City("Norfolk", (9*32, 11*32)),
                           City("Jacksonville", (32, 20*32)),
                           ]
        self.cities = random.sample(possible_cities, 3)

        self.players = [Player(), Player(name="Blue", color='blue')]
        self.players[0].assign_city(self.cities[0])
        self.players[0].assign_unit(Infantry(coords=(320,320)))
        self.players[1].assign_city(self.cities[2])
        self.players[1].assign_unit(Infantry(name="42nd grenadiers", coords=(18*32, 3*32)))

    @property
    def units(self):
        """return a list of all units"""
        return comprehension_flatten([p.units for p in self.players])  # this returns a flat list of all units

