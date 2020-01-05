"""
Cities - Contain s the code for City objects
"""
import os
import pygame
from BaseObjects import Unit
from GraphicUtils import colors


city_tile_path = os.path.join('graphics', 'city_tile_32x32.png')


class City(Unit):
    """
    Builds units and must be conquered to win the game.
    """

    def __init__(self, name="anytown", coords=(0, 0)):
        self.coords = coords
        self.name = name
        self.image_file = os.path.join('graphics', 'city_tile_32x32.png')
        self.set_image()
        self.plane = None


