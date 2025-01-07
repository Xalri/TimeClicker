import pygame as pg
from pygame._sdl2 import Window
from data import *
from Buttons import Button
import time
from Logger import Logger
import buildings

LOGGER: Logger = Logger()
pg.init()
clock:  pg.time.Clock = pg.time.Clock()




#initialize window
screen: pg.Surface = pg.display.set_mode((720, 480), pg.RESIZABLE)
Window.from_display_module().maximize()
pg.display.set_caption('Time Clicker')
screen.fill(BACKGROUND_COLOR)
pg.display.flip()

timeUnits: float = 0
tps: float = 1


text_test: pg.Surface = TEXT_FONT.render('1547', True, WHITE)




def main():

    global timeUnits
        



    LOGGER.INFO(timeUnits)


    # BOUCLE DU JEU
    running: bool = True
    current_frame: int = 0
    while running:
        
        
        framerate: int =32
        if current_frame != framerate:
            current_frame += 1
        else:
            current_frame = 0
                
        
        clock.tick_busy_loop(framerate)
        
        timeUnits += tps/framerate
        
        # LOGGER.INFO(timeUnits)
        
        for event in pg.event.get():
        
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                running = False
                

            

        screen.fill(BACKGROUND_COLOR)
                
        
        screen.blit(text_test, (500, 500))

                
                
        
        pg.display.update()


if __name__ == "__main__":
    main()