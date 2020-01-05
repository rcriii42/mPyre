"""Player.py - Contains the Player object"""


class Player(object):
    """Player with units"""

    def __init__(self, name="First Player", color = 'green'):
        self.name = name
        self.cities = []
        self.units = []
        self.color = color

    def assign_city(self, city):
        """assign a city to the player"""
        city.owner = self
        city.set_image(self.color)

    def turn_step(self, G):
        """Adjust the player to reflect moving forward in time.

           game is the game I am part of."""
        ts_messages = ["{} turn {}".format(self.name, G.turn)]

        return ts_messages
