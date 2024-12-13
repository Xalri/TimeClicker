from graphics_nsi import *
from pprint import pprint
import pygame as pg
import ctypes
import os

#define constant
SCREEN = {"width": ctypes.windll.user32.GetSystemMetrics(0), "height": ctypes.windll.user32.GetSystemMetrics(1)}
NAVIGUATION_BAR_HEIGHT = 29

# place window in position 0,0
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0, NAVIGUATION_BAR_HEIGHT)






def main():
    #test modif
    init_graphic(SCREEN["width"], SCREEN["height"] - NAVIGUATION_BAR_HEIGHT, "Binary Clicker")
    
    
    wait_escape("Appuyer sur Echap pour terminer")
if __name__ == "__main__":
    main()