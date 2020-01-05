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
        self.cities.append(city)
        city.owner = self
        city.set_image(self.color)

    def assign_unit(self, unit):
        """assign a unit to the player"""
        self.units.append(unit)
        unit.owner = self
        unit.set_image(self.color)

    def turn_step(self, G):
        """Adjust the player to reflect moving forward in time.

           game is the game I am part of."""
        ts_messages = ["{} turn {}".format(self.name, G.turn)]
        for u in self.units:
            ts_messages.extend(u.turn_step(G))

        return ts_messages
