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
tps = 0

buildings = [
    # Préhistoire
    {"name": "Campfire", "cost": 15, "tps_boost": 0.1},
    {"name": "Farming", "cost": 100, "tps_boost": 1},
    {"name": "Painting", "cost": 1100, "tps_boost": 8},
    {"name": "Hunting", "cost": 12000, "tps_boost": 47},
    
    # Antiquité
    {"name": "Aqueduct", "cost": 130000, "tps_boost": 260},
    {"name": "Pyramid", "cost": 1400000, "tps_boost": 1400},
    {"name": "Temple", "cost": 20000000, "tps_boost": 7800},
    {"name": "Cash", "cost": 330000000, "tps_boost": 44000},
    
    # Moyen Âge
    {"name": "Printing", "cost": 5100000000, "tps_boost": 260000},
    {"name": "School", "cost": 75000000000, "tps_boost": 1600000},
    {"name": "Church", "cost": 1000000000000, "tps_boost": 10000000},
    {"name": "Castle", "cost": 14000000000000, "tps_boost": 65000000},
    
    # Temps Modernes
    {"name": "Steam Engine", "cost": 170000000000000, "tps_boost": 430000000},
    {"name": "Rail", "cost": 2100000000000000, "tps_boost": 2900000000},
    {"name": "Factory", "cost": 26000000000000000, "tps_boost": 21000000000},
    {"name": "Car", "cost": 310000000000000000, "tps_boost": 150000000000},
    
    # Époque Contemporaine
    {"name": "Electronic", "cost": 7100000000000000000, "tps_boost": 1100000000000},
    {"name": "Internet", "cost": 12000000000000000000000, "tps_boost": 8300000000000},
    {"name": "Rocket", "cost": 1900000000000000000000000, "tps_boost": 64000000000000},
    {"name": "Nuclear Central", "cost": 540000000000000000000000000, "tps_boost": 510000000000000},
    
    # Futur
    {"name": "AI", "cost": 30000000000000000000000000000, "tps_boost": 4000000000000000},
    {"name": "Antimatter Central", "cost": 4200000000000000000000000000000, "tps_boost": 31000000000000000},
    {"name": "Spaceship", "cost": 630000000000000000000000000000000, "tps_boost": 240000000000000000},
    #{"name": "Time Machine", "cost": 100000000000000000000000000000000000, "tps_boost": },
]

def main():

    global timeUnits

    def addTimeUnits(number=1):
        global timeUnits
        timeUnits += number
        LOGGER.INFO(timeUnits)
        

    clicker = Button((10, 10, 150, 50), addTimeUnits)


    LOGGER.INFO(timeUnits)


    # BOUCLE DU JEU
    running = True
    while running:
        
        clock.tick(60)
        
        for event in pg.event.get():
        
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                running = False
                
            clicker.get_event(event)

            

        screen.fill(BACKGROUND_COLOR)
                
        clicker.render(screen)
                
                
        
        pg.display.update()


if __name__ == "__main__":
    main()