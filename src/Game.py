"""Game.py - Contains the Game object that holds all objects in the game - players, cities, 
   units, and the game Map."""

#     This part of mPyre, a python implementation of the game Empire
#     Copyright (C) 2019  Robert C. Ramsdell III <rcriii42@gmail.com>
#
#     mPyre is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     mPyre is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with mPyre.  If not, see <https://www.gnu.org/licenses/>.
#
#     Work started on 19 December, 2019


import random
from Cities import City
from Player import Player
from GroundUnits import Infantry
from Player_AI import AI
from  BaseObjects import Map

Demo = True


def comprehension_flatten(iter_lst):
    return list(item for iter_ in iter_lst for item in iter_)


class Game(object):
    """Holds the various game objects"""

    def __init__(self, size):
        self.turn = 1

        possible_cities = [City("Boston", (17*32, 32)),
                           City("New York", (13*32, 4*32)),
                           City("Norfolk", (9*32, 11*32)),
                           City("Jacksonville", (32, 19*32)),
                           ]
        self.cities = possible_cities

        self.neutral = Player(name="Neutral", color = "white")
        for c in self.cities:
            self.neutral.assign_city(c, build_unit=False)

        self.players = [Player(),
                        Player(name="Blue", color='blue'),
                        Player(name="MLBBR", color='orange')]

        self.players[0].assign_city(possible_cities[0])
        self.players[0].assign_unit(Infantry(coords=(possible_cities[0].coords[0],
                                                     possible_cities[0].coords[1])))

        self.players[1].assign_city(possible_cities[-1])
        self.players[1].assign_unit(Infantry(coords=(possible_cities[-1].coords[0],
                                                     possible_cities[-1].coords[1])))
        self.players[1].AI = AI(self.players[1],
                                self)

        c = random.sample(possible_cities[1:3], 1)[0]
        self.players[2].assign_city(c)
        self.players[2].assign_unit(Infantry(coords=(c.coords[0],
                                                     c.coords[1])))
        self.players[2].AI = AI(self.players[2],
                                self)

        self.player_turn_list = self.players.copy()

        self.lost_players = []

        self.map = Map(dims = size)
        for x in range(18*32, 24*32, 32):
            for y in range(32, 4*32, 32):
                self.map[x, y] = "water"

    @property
    def size(self):
        return self.map.dims

    @property
    def units(self):
        """return a list of all units"""
        return comprehension_flatten([p.units for p in self.players])  # this returns a flat list of all units

    @property
    def current_player(self):
        """The player whose turn it is"""
        return self.player_turn_list[0]

    @property
    def next_player(self):
        """The next player in turn"""
        if len(self.player_turn_list) <= 1:
            return None
        else:
            return self.player_turn_list[1]

    def advance_player(self):
        msgs = []
        if len(self.player_turn_list) <= 1:
            return msgs
        else:
            self.player_turn_list.pop(0)
            return ["Starting {} turn {}".format(self.current_player.name,
                                                 self.turn)]

    def advance_turn(self):
        """advance the turn and reset players"""
        self.turn += 1
        self.player_turn_list = self.players.copy()
        return ["Turn: {}".format(self.turn)]

    def player_lost(self, p):
        """The player lost, remove them from the game"""
        self.lost_players.append(p)
        self.players.remove(p)
        if p in self.player_turn_list:
            self.player_turn_list.remove(p)
        return "Player {} lost!".format(p.name)

