"""GroundUnits.py - The land units, defined as units that cannot go over water or stack."""
import os
from BaseObjects import Unit
from GraphicUtils import colors


class Infantry(Unit):
    """The basic ground unit"""

    def __init__(self, name="1st Infantry", coords=(0, 0)):
        self.coords = coords
        self.name = name
        self.owner = None
        self.image_file = os.path.join('graphics', 'inf_icon_32x32.png')
        self.set_image()
        self.plane = None

    def turn_step(self, G):
        turn_messages = ["{} turn {}".format(self.name, G.turn)]
        return turn_messages