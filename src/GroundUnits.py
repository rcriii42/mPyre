"""GroundUnits.py - The land units, defined as units that cannot go over water or stack."""
import os
from BaseObjects import Unit
from GraphicUtils import colors
from pygame.locals import K_UP, K_DOWN, K_LEFT, K_RIGHT

class Infantry(Unit):
    """The basic ground unit"""

    def __init__(self, name="1st Infantry", coords=(0, 0)):
        self.coords = coords
        self.name = name
        self.owner = None
        self.image_file = os.path.join('graphics', 'inf_icon_32x32.png')
        self.set_image()
        self.plane = None

        self.moved = 0
        self.move_speed = 1

    def move(self, direction, G):
        "Move one step in the given direction"

        if self.moved >= self.move_speed:
            print("{} not moving {}, moved {}".format(self.name, self.move_speed, self.moved))
            print("{}".format((self.moved < self.move_speed)))
            return False
        print("{} moving {}, moved {}".format(self.name, self.move_speed, self.moved))
        if direction == K_UP:
            move_vector = 0, -self.image_size[1]
        elif direction == K_DOWN:
            move_vector = 0, self.image_size[1]
        elif direction == K_RIGHT:
            move_vector = self.image_size[1], 0
        elif direction == K_LEFT:
            move_vector = -self.image_size[1], 0
        new_coords = (self.coords[0]+ move_vector[0],
                      self.coords[1] + move_vector[1])
        if not self.check_collision(new_coords, G):
            self.coords = new_coords
            self.plane.rect.move_ip(move_vector)
            self.moved += 1
        return True

    def turn_step(self, G):
        turn_messages = ["{} turn {} moved {}".format(self.name, G.turn, self.moved)]
        self.moved = 0
        return turn_messages