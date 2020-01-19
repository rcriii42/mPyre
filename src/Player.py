"""Player.py - Contains the Player object"""

#     This part of mPyre, a python implementation of the game Empire
#     Copyright (C) 2019  Robert C. Ramsdell III <rcriii42@gmail.com>
#
#     mPyre is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     mPyre is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with mPyre.  If not, see <https://www.gnu.org/licenses/>.
#
#     Work started on 19 December, 2019



class Player(object):
    """Player with units"""

    def __init__(self, name="First Player", color = 'green'):
        self.name = name
        self.cities = []
        self.units = []
        self.color = color

    def assign_city(self, city, build_unit=True):
        """assign a city to the player"""
        self.cities.append(city)
        city.owner = self
        city.set_image(self.color)
        if build_unit:
            city.start_building()

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

    def next_to_move(self, u=None):
        if not u:
            if self.units:
                u = self.units[0]
            if u.moved < u.move_speed:
                return u
        if u in self.units:
            i = self.units.index(u)
            after = [a for a in self.units[i:]]
            for a in after:
                if a is not u and a.moved < a.move_speed:
                    return a
            before = [b for b in self.units[:i]]
            for b in before:
                if b.moved < b.move_speed:
                    return b
        return None


