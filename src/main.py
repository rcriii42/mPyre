#!/usr/bin/python3

#     This is the startup script for Pyre, a python implementation of the game Empire
#     Copyright (C) 2019  Robert C. Ramsdell III <rcriii42@gmail.com>
#
#     Pyre is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     Pyre is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with Pyre.  If not, see <https://www.gnu.org/licenses/>.
#
#     Work started on 19 December, 2019

import Controller
from GameWindow import GameWindow


if __name__ == "__main__":
    GW = GameWindow()
    W = Controller.World()
    GW.mainloop(W)
    GW.quit()