"""GraphicUtils - pygame utility functions"""

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


import pygame , random , sys , math , time , pickle, os
from pygame.locals import *

colors = {'green': (51, 255, 0),
          'blue':( 0, 0, 255),
          'red': (204, 0, 0 ),
          'white':(255, 255, 255)}

def tile_texture(output, img, rect=None):
    """tile_texture - fill a surface with a tile"""
    cr = output.get_clip()
    if rect:
        output.set_clip(rect)
    else:
        rect=cr
    try:
        img_r = img.get_rect()
        img = [img]
    except:
        #assume img is a list of images
        img_r = img[0].get_rect()
    for x in range(0, rect.width, img_r.width):
        for y in range(0, rect.height, img_r.height):
            i=random.choice(img)
            output.blit(i, (x + rect.left, y + rect.top))

    output.set_clip(cr)
    return output.copy()
    
def draw_text(output, text, size=10, color=(255,255,255), loc=(0,0), font=None):
    """draw_text - draw the given line of text to an output window"""
    x, y = loc
    if not font:
        font = pygame.font.SysFont(None, size)
    txt = font.render(text, True, color)
    return output.blit(txt, (x,y))  #return a rect of the message
 
def show_fonts(output, loc=(10,10)):
    """list the system fonts on the given window"""
    x, y = loc
    list = pygame.font.get_fonts()
    print(list)
#    for f in list:
#        for size in (16, 8, 4):
#            font = pygame.font.SysFont(f, size)
#            draw_text(output,
#                      text="%s: %d"%(f, size),
#                      size = size,
#                      loc=(x, y),
#                      font=font)
#            y += size