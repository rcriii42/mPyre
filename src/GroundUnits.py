"""GroundUnits.py - The land units, defined as units that cannot go over water or stack."""
import os
from BaseObjects import Unit
from GraphicUtils import colors
from pygame.locals import K_UP, K_DOWN, K_LEFT, K_RIGHT
import random

class unit_namer:
    """class to manage unit names"""
    def __init__(self):
        self.unit_num = 1

    def name_unit(self):
        if self.unit_num in [1]:
            suffix = "st"
        elif self.unit_num in [2]:
            suffix = "nd"
        elif self.unit_num in [3]:
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
        if direction == K_UP:
            move_vector = 0, -self.image_size[1]
        elif direction == K_DOWN:
            move_vector = 0, self.image_size[1]
        elif direction == K_RIGHT:
            move_vector = self.image_size[1], 0
        elif direction == K_LEFT:
            move_vector = -self.image_size[1], 0
        else:
            return None
        new_coords = (self.coords[0]+ move_vector[0],
                      self.coords[1] + move_vector[1])
        self.moved += 1
        u = self.check_collision(new_coords, G)
        if not u:
            self.coords = new_coords
            self.plane.rect.move_ip(move_vector)
            return None
        else:
            return u

    def turn_step(self, G):
        turn_messages = ["{} turn {} moved {}".format(self.name, G.turn, self.moved)]
        self.moved = 0
        return turn_messages