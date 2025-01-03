import pygame as pg
from pygame._sdl2 import Window
from data import *
from Buttons import Button
import time
from Logger import Logger

LOGGER = Logger()
pg.init()
clock=pg.time.Clock()




#initialize window
screen = pg.display.set_mode((720, 480), pg.RESIZABLE)
Window.from_display_module().maximize()
pg.display.set_caption('Time Clicker')
screen.fill(BACKGROUND_COLOR)
pg.display.flip()

timeUnits = 0

def main():

    global timeUnits

    def addTimeUnits(number=1):
        global timeUnits
        timeUnits += number
        LOGGER.INFO(timeUnits)
        

    clicker = Button((10, 10, 150, 50), addTimeUnits)


    LOGGER.INFO(timeUnits)


    running = True
    while running:
        
        clock.tick(60)
        
        for event in pg.event.get():
        
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                running = False
                
            clicker.get_event(event)

                
        clicker.render(screen)
                
                
        
        pg.display.update()

if __name__ == "__main__":
    main()