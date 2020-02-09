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

    def set_image(self, color=None):
        """Set the image and color"""
        image = pygame.image.load(self.image_file).convert()
        self.image_size = (32, 32)
        self.image = pygame.transform.scale(image, self.image_size)
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
                print("check_collision: collided with {}".format(c.name))
                return c
        for u in G.units:
            if u.coords == coords:
                "check_collision: collided with {}".format(u.name)
                return u
        print("check_collision: No collision {}".format(coords))
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



