"""
Cities - Contain s the code for City objects
"""
import os
import pygame
from BaseObjects import Unit
from GraphicUtils import colors
import GroundUnits


city_tile_path = os.path.join('graphics', 'city_tile_32x32.png')


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

        self.start_building()

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