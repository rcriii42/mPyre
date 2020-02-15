#!/usr/bin/python3

#     This is the startup script for mPyre, a python implementation of the game Empire
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

import Controller
from GameWindow import GameWindow
import pygame


if __name__ == "__main__":
    image_size = 32
    size = (image_size*30, image_size*30)
    pygame.init()
    pygame.display.set_mode(size)
    W = Controller.World(size, image_size)
    GW = GameWindow(W)

    GW.mainloop()
    GW.quit()