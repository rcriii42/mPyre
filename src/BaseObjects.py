"""BaseObjects - Define some basic objects

Space - the meta object for all objects that can be on a map
Map - a dictionary holding all the spaces on a map
"""
import os
import pygame
from GraphicUtils import colors

class Unit(object):
    """Space - meta object"""

    def __init__(self, coords=(0,0)):
        self.coords = coords
        self.image_file = os.path.join('graphics', 'city_tile_32x32.png')
        self.move_speed = 0

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


class Map(object):
    """Map - meta object"""

    def __init__(self, name='The Map', dims=(10,10)):
        self.name = name
        self.dims = dims

    def __getitem__(self, item):
        'only accept spaces or lists of spaces'
        if type(item)==list:
            pass


