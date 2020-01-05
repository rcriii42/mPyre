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
        self.set_image()
        self.plane = None

    def set_image(self, color=None):
        """Set the image and color"""
        image = pygame.image.load(os.path.join('graphics', 'city_tile_32x32.png')).convert()
        self.image_size = (32, 32)
        self.image = pygame.transform.scale(image, self.image_size)
        if color:
            self.image = pygame.transform.threshold(self.image,
                                                    self.image,
                                                    colors['white'],
                                                    threshold=(5,5,5,5),
                                                    set_color=colors[color],
                                                    inverse_set=True)
