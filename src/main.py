#!/usr/bin/python3
# this is a placeholder file
# Viewer
import Controller
from GameWindow import GameWindow
import pygame
from pygame.locals import NOEVENT, QUIT

if __name__ == "__main__":
    GW = GameWindow()
    W = Controller.World()
    GW.mainloop(W)
    print (W.G.__dict__)
    GW.quit()