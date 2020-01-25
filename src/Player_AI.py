"""Player_AI.py - Contains the AI object that can clontrol a player"""

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
#     Work on this file started on 25 January, 2020

class AI():
    """An AI to control a player"""
    def __init__(self, player, game):
        self.player = player
        self.game = game

    def next_move(self):
        """Determine my next move

        return a list with messages for the game window:
        'End_Turn': end my turn
        """
        return ["End Turn"]