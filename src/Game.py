"""Game.py - Contains the Game object that holds all objects in the game - players, cities, 
   dredges, and the game world."""
# Model 
import datetime
import random
from City import City
from Player import Player

Demo = True
days_to_hours = 24.


def comprehension_flatten(iter_lst):
    return list(item for iter_ in iter_lst for item in iter_)


class Game(object):
    """Holds the various game objects"""

    def __init__(self):
        self.date = datetime.datetime(1920, 1, 1)

        possible_cities = [City(self.date, "Boston", (530, 10)),
                           City(self.date, "New York", (390, 120)),
                           City(self.date, "Norfolk", (280, 360)),
                           City(self.date, "Jacksonville", (15, 750)),
                           ]
        self.cities = random.sample(possible_cities, 3)

        self.players = [Player()]
        self.date = datetime.datetime(1920, 1, 1)

    @property
    def dredges(self):
        """return a list of all dredges"""
        return comprehension_flatten([p.dredges for p in self.players])  # this returns a flat list of all dredges

    @property
    def projects(self):
        """return a list of projects"""
        return comprehension_flatten([c.projects for c in self.cities])  # this returns a flat list of projects underway
