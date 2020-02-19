"""BaseObjects - Define some basic objects

Unit - the meta object for all objects that can be on a map
Map - a dictionary holding all the spaces on a map
"""

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


import os
import pygame
from GraphicUtils import colors
import random

infantry_list = ["Infantry",
                 "Grenadiers",
                 "Halbardiers",
                 "Guards",
                 "Marines"]

class Namer:
    """class to manage unit names"""
    def __init__(self, name_list=None, number_names=True):
        self.unit_num = 1
        if not name_list:
            self.original_name_list = infantry_list.copy()
            self.name_list = infantry_list.copy()
        else:
            self.original_name_list = name_list.copy()
            self.name_list = name_list.copy()
            random.shuffle(self.name_list)
        if number_names:
            self.name_unit = self.name_numbered_unit
        else:
            self.name_unit = self.name_unnumbered_unit


    def name_unnumbered_unit(self):
        """Name units in the case they are unnumbered

        selects from the name_list without replacement"""
        if len(self.name_list) > 0:
            return self.name_list.pop()
        else:
            print("Out of names!")
            self.name_list = self.original_name_list
            self.name_unit = self.name_numbered_unit
            return self.name_unit()


    def name_numbered_unit(self):
        suffixed = [1] + [x for x in range(21, 101, 10)]
        for c in range(100, 10000, 100):
            suffixed += [x for x in range(c + 21, c + 101, 10)]
        if self.unit_num in suffixed:
            suffix = "st"
        elif self.unit_num in [x + 1 for x in suffixed]:
            suffix = "nd"
        elif self.unit_num in [x + 2 for x in suffixed]:
            suffix = "rd"
        else:
            suffix = "th"
        name = "{}{} {}".format(self.unit_num,
                                suffix,
                                random.choice(self.name_list))
        self.unit_num += 1
        return name


class Unit(object):
    """Space - meta object"""

    def __init__(self, coords=(0,0)):
        self.coords = coords
        self.image_file = os.path.join('graphics', 'city_tile_32x32.png')

        self.is_container = False

        self.move_speed = 0
        self.moved = 0

        self.max_strength = 1
        self.current_strength = 1 #How much damage the unit can take
        self.attack = 0 #Attack Strength and damage dealt
        self.defense = 1 #Defense strength, successful defense always does 1 damage

    def set_image(self, size, color=None):
        """Set the image and color"""
        image = pygame.image.load(self.image_file).convert()

        self.image = pygame.transform.scale(image, size)
        if color:
            new_pixels = pygame.transform.threshold(self.image,
                                                    self.image,
                                                    colors['white'],
                                                    threshold=(50,50,50,50),
                                                    set_color=colors[color],
                                                    inverse_set=True)
            #print("City.set_image: {}".format(new_pixels))

    def check_collision(self, coords, G):
        """Check to see if the unit will collide with any units or cities in the game
        G is the game object
        should be called with the new coords before moving!"""
        if not coords:
            coords = self.coords
        for c in G.cities:
            if c.coords == coords:
                #print("check_collision: collided with {}".format(c.name))
                return c
        for u in G.units:
            if u.coords == coords:
                "check_collision: collided with {}".format(u.name)
                return u
        #print("check_collision: No collision {}".format(coords))
        return None

    def distance_to(self, unit):
        """Calculate the distance to the given unit"""
        return max(abs(self.coords[0] - unit.coords[0]),
                   abs(self.coords[1] - unit.coords[1]))

    def direction_to(self, unit):
        """return the unit vector to the given unit"""
        if unit.coords[0] == self.coords[0]:
            x_dir = 0
        else:
            x_dir = (unit.coords[0] - self.coords[0]) / abs(unit.coords[0] - self.coords[0])
        if unit.coords[1] == self.coords[1]:
            y_dir = 0
        else:
            y_dir = (unit.coords[1] - self.coords[1]) / abs(unit.coords[1] - self.coords[1])
        return x_dir, y_dir


class Map(dict):
    """Map - meta object"""

    def __init__(self, name='The Map', dims=(10,10)):
        self.name = name
        self.dims = dims


    def __getitem__(self, key):
        if type(key) is not type(self.dims):
            raise TypeError("Invalid type for map coords: {}".format(key))
        if key[0] > self.dims[0] or key[1] > self.dims[1]:
            raise KeyError("Coordinates out of bounds: {}".format(key))
        if key[0] < 0 or key[1] < 0:
            raise KeyError("Coordinates out of bounds: {}".format(key))
        if key[0] in (0, self.dims[0]) or key[1] in (0, self.dims[1]):
            return "edge"
        return self.get(key, "plains")

    def __setitem__(self, key, value):
        if type(key) is not type(self.dims):
            raise TypeError("Invalid type for map coords: {}".format(key))
        if key[0] > self.dims[0] or key[1] > self.dims[1]:
            raise KeyError("Coordinates out of bounds: {}".format(key))
        if key[0] < 0 or key[1] < 0:
            raise KeyError("Coordinates out of bounds: {}".format(key))
        super(Map, self).__setitem__(key, value)

    def neighbors(self, xy):
        """Return a list of coordinates of the neighbors of the given square"""
        ne_list = []
        for x in [-1, 0, 1]:
            for y in [-1, 0, 1]:
                if (x, y) != (0, 0) and \
                   (0 <= xy[0] + x <= self.dims[0]) and \
                   (0 <= xy[1] + y <= self.dims[1]):
                    ne_list.append((xy[0] + x,
                                    xy[1] + y))
        return ne_list

# function reconstruct_path(cameFrom, current)
#     total_path := {current}
#     while current in cameFrom.Keys:
#         current := cameFrom[current]
#         total_path.prepend(current)
#     return total_path
#
#
# def A_Star(start, goal, map, impassible):
#     """// A* finds a path from start to goal.
#
#     map is the map object with terrain.
#     impassible is a list of impassible terrain
#
#     from the wiki page: https://en.wikipedia.org/wiki/A*_search_algorithm"""
#
#     # The set of discovered nodes that may need to be (re-)expanded.
#     # Initially, only the start node is known.
#     open_set = set([start])
#
#     # For node n, cameFrom[n] is the node immediately preceding it on the cheapest path from start to n currently known.
#     cameFrom := an empty map
#
#     // For node n, gScore[n] is the cost of the cheapest path from start to n currently known.
#     gScore := map with default value of Infinity
#     gScore[start] := 0
#
#     // For node n, fScore[n] := gScore[n] + h(n).
#     fScore := map with default value of Infinity
#     fScore[start] := h(start)
#
#     while openSet is not empty
#         current := the node in openSet having the lowest fScore[] value
#         if current = goal
#             return reconstruct_path(cameFrom, current)
#
#         openSet.Remove(current)
#         for each neighbor of current
#             // d(current,neighbor) is the weight of the edge from current to neighbor
#             // tentative_gScore is the distance from start to the neighbor through current
#             tentative_gScore := gScore[current] + d(current, neighbor)
#             if tentative_gScore < gScore[neighbor]
#                 // This path to neighbor is better than any previous one. Record it!
#                 cameFrom[neighbor] := current
#                 gScore[neighbor] := tentative_gScore
#                 fScore[neighbor] := gScore[neighbor] + h(neighbor)
#                 if neighbor not in openSet
#                     openSet.add(neighbor)
#
#     // Open set is empty but goal was never reached
#     return failure

