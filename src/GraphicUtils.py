"""GraphicUtils - pygame utility functions"""

import pygame , random , sys , math , time , pickle, os
from pygame.locals import *

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