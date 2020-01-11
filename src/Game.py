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
                           City("Jacksonville", (32, 19*32)),
                           ]
        self.cities = random.sample(possible_cities, 3)
        print([c.name for c in self.cities])

        self.neutral = Player(name="Neutral", color = "white")
        for c in self.cities:
            self.neutral.assign_city(c)

        self.players = [Player(), Player(name="Blue", color='blue')]
        self.players[0].assign_city(self.cities[0])
        self.players[0].assign_unit(Infantry(coords=(self.cities[2].coords[0]+32,
                                                     self.cities[2].coords[1])))
        self.players[1].assign_city(self.cities[2])
        self.players[1].assign_unit(Infantry(name="42nd grenadiers",
                                             coords=(self.cities[0].coords[0]+32,
                                                     self.cities[0].coords[1])))
        self.player_turn_list = self.players.copy()

    @property
    def units(self):
        """return a list of all units"""
        return comprehension_flatten([p.units for p in self.players])  # this returns a flat list of all units

    @property
    def current_player(self):
        """The player whose turn it is"""
        return self.player_turn_list[0]\

    @property
    def next_player(self, advance="True"):
        """The next player in turn"""
        if len(self.player_turn_list) == 1:
            return None
        else:
            if advance:
                self.player_turn_list.pop(0)
                return self.player_turn_list[0]
            else:
                return self.player_turn_list[1]
