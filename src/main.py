#!/usr/bin/python3
# this is a placeholder file
import Controller
from GameWindow import GameWindow


if __name__ == "__main__":
    GW = GameWindow()
    W = Controller.World()
    GW.mainloop(W)
    GW.quit()