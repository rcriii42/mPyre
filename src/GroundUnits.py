"""GroundUnits.py - The land units, defined as units that cannot go over water or stack."""

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
from BaseObjects import Unit
from pygame.locals import K_UP, K_DOWN, K_LEFT, K_RIGHT
from pygame.locals import K_KP1, K_KP2, K_KP3, K_KP4, K_KP6, K_KP7, K_KP8, K_KP9
import random
import Cities

class unit_namer:
    """class to manage unit names"""
    def __init__(self):
        self.unit_num = 1

    def name_unit(self):
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
                                random.choice(["Infantry",
                                               "Grenadiers",
                                               "Halbardiers",
                                               "Guards",
                                               "Marines"]))
        self.unit_num += 1
        return name

namer = unit_namer()

class Infantry(Unit):
    """The basic ground unit"""

    def __init__(self, name=None, coords=(0, 0)):
        self.coords = coords
        if name:
            self.name = name
        else:
            self.name = namer.name_unit()
        self.owner = None
        self.image_file = os.path.join('graphics', 'inf_icon_32x32.png')
        self.set_image()
        self.plane = None

        self.moved = 0
        self.move_speed = 1
        self.connot_enter = ['edge', 'water']

        self.max_strength = 1
        self.current_strength = 1  # How much damage the unit can take
        self.attack = 1  # Attack Strength and damage dealt
        self.defense = 1  # Defense strength, successful defense always does 1 damage

        self.build_time = 2

    def move(self, direction, G):
        "Move one step in the given direction"

        if self.moved >= self.move_speed:
            print("{} not moving {}, moved {}".format(self.name, self.move_speed, self.moved))
            print("{}".format((self.moved < self.move_speed)))
            return None
        print("{} moving {}, moved {}".format(self.name, self.move_speed, self.moved))
        if direction in [K_UP, K_KP8]:
            move_vector = 0, -self.image_size[1]
        elif direction in [K_KP9]:
            move_vector = self.image_size[0], -self.image_size[1]
        elif direction in [K_RIGHT, K_KP6]:
            move_vector = self.image_size[0], 0
        elif direction in [K_KP3]:
            move_vector = self.image_size[0], self.image_size[1]
        elif direction in [K_DOWN, K_KP2]:
            move_vector = 0, self.image_size[1]
        elif direction in [K_KP1]:
            move_vector = -self.image_size[0], self.image_size[1]
        elif direction in [K_LEFT, K_KP4]:
            move_vector = -self.image_size[0], 0
        elif direction in [K_KP7]:
            move_vector = -self.image_size[0], -self.image_size[1]
        else:
            return None
        new_coords = (self.coords[0]+ move_vector[0],
                      self.coords[1] + move_vector[1])
        if G.map[new_coords] in self.connot_enter :
            print("{} cannot move into {}".format(self.name, G.map[new_coords]))
            return None
        u = self.check_collision(new_coords, G)
        if not u:
            self.coords = new_coords
            self.plane.rect.move_ip(move_vector)
            self.moved += 1
            return None
        elif u.owner is not self.owner:
            return u
        elif isinstance(u, Cities.City):
            self.coords = new_coords
            self.plane.rect.move_ip(move_vector)
            self.moved += 1
            return None
        else:
            return None

    def turn_step(self, G):
        if self.plane:
            if self.coords != (self.plane.rect.left, self.plane.rect.top):
                print("{} Coordinate mismatch {} != {}".format(self.name, self.coords, (self.plane.rect.left, self.plane.rect.top)))
        turn_messages = ["{} turn {} moved {}".format(self.name, G.turn, self.moved)]
        self.moved = 0
        return turn_messages