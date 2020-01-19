"""
Cities - Contains the code for City objects
"""

#     This part of Pyre, a python implementation of the game Empire
#     Copyright (C) 2019  Robert C. Ramsdell III <rcriii42@gmail.com>
#
#     Pyre is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     Pyre is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with Pyre.  If not, see <https://www.gnu.org/licenses/>.
#
#     Work started on 19 December, 2019


import os
import pygame
from BaseObjects import Unit
from GraphicUtils import colors
import GroundUnits


city_tile_path = os.path.join('graphics', 'city_tile_32x32.png')

not_building = Unit()
not_building.name = "none"

class City(Unit):
    """
    Builds units and must be conquered to win the game.
    """

    def __init__(self, name="anytown", coords=(0, 0)):
        Unit.__init__(self, coords)
        self.name = name
        self.owner = None
        self.image_file = os.path.join('graphics', 'city_tile_32x32.png')
        self.set_image()
        self.plane = None

        self.building = not_building
        self.time_to_build = 0

    def turn_step(self, G):
        turn_messages=["{} turn {}".format(self.name, G.turn)]
        self.time_to_build -= 1
        if self.time_to_build == 0:
            self.owner.assign_unit(self.building)
            self.start_building()
            turn_messages.append("{} built {}".format(self.name,
                                                      self.owner.units[-1].name))
        return turn_messages

    def start_building(self):
        """Start building a unit"""
        self.building = GroundUnits.Infantry(coords=(self.coords[0],
                                                     self.coords[1]-32))
        self.time_to_build = self.building.build_time