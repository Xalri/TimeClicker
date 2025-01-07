import pygame as pg
from pygame._sdl2 import Window
from data import *
from Buttons import Button
import time
from Logger import Logger
import buildings
from utils import adapt_size_height, adapt_size_width

# initializing
LOGGER: Logger = Logger()
pg.init()
pg.font.init()
clock:  pg.time.Clock = pg.time.Clock()




#initialize window
screen: pg.Surface = pg.display.set_mode((720, 480), pg.RESIZABLE)
Window.from_display_module().maximize()
pg.display.set_caption('Time Clicker')
screen.fill(BACKGROUND_COLOR)
pg.display.flip()


# LOGGER.INFO('Screen width: {} Screen height: {}'.format(w, h))




def crop_value(value: float):
    if value >= 10:
        return int(value)
    return round(value, 3)






def main():
    # define game values
    timeUnits: float = 0
    tps: float =10000
    timeline: int = 0
    current_frame: int = 0
    framerate: int =32
    w, h = pg.display.get_surface().get_size()

    LOGGER.INFO(timeUnits)




    running: bool = True
    while running:
        
        
        
        
        TIMELINE_FONT: pygame.font = pygame.font.Font('src/fonts/LetterGothicStd-Bold.ttf', int(adapt_size_height(124, h)))
        NUMBER_FONT: pygame.font = pygame.font.Font('src/fonts/LetterGothicStd-Bold.ttf', 52)
        TEXT_FONT: pygame.font = pygame.font.Font('src/fonts/FranklinGothicHeavyRegular.ttf', 33)
        
        
        
        
        timeline_text: pg.Surface = TIMELINE_FONT.render(f"{crop_value(timeUnits)}", True, YELLOW_GREEN)


        
        
        
        # manage game loop time
        clock.tick_busy_loop(framerate)
        current_frame: int = (current_frame + 1) % framerate
        
        
        timeUnits += tps/framerate
        
        # LOGGER.INFO(timeUnits)
        
        for event in pg.event.get():
        
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                running = False
                

            

        screen.fill(BACKGROUND_COLOR)
                
        
        
        # fill screen with shapes
        pg.draw.rect(screen, DARK_GREY, (adapt_size_width(45, w), adapt_size_height(45, h), adapt_size_width(500, w), adapt_size_height(180, h)), border_radius=20)
        pg.draw.rect(screen, DARK_GREY, (adapt_size_width(45, w), adapt_size_height(245, h), adapt_size_width(500, w), adapt_size_height(790, h)), border_radius=20)
        pg.draw.rect(screen, DARK_GREY, (adapt_size_width(605, w), adapt_size_height(45, h), adapt_size_width(600, w), adapt_size_height(990, h)), border_radius=20)
        pg.draw.rect(screen, DARK_GREY, (adapt_size_width(1475, w), adapt_size_height(45, h), adapt_size_width(400, w), adapt_size_height(800, h)), border_radius=20)
        
        pg.draw.rect(screen, LIGHT_DARK, (adapt_size_width(75, w), adapt_size_height(75, h), adapt_size_width(440, w), adapt_size_height(120, h)))
        pg.draw.rect(screen, LIGHT_DARK, (adapt_size_width(75, w), adapt_size_height(275, h), adapt_size_width(440, w), adapt_size_height(730, h)))
        pg.draw.rect(screen, LIGHT_DARK, (adapt_size_width(635, w), adapt_size_height(75, h), adapt_size_width(540, w), adapt_size_height(930, h)))
        pg.draw.rect(screen, LIGHT_DARK, (adapt_size_width(1505, w), adapt_size_height(75, h), adapt_size_width(340, w), adapt_size_height(740, h)))
        
        
        
        # draw text
        screen.blit(timeline_text, (adapt_size_width(95, w), adapt_size_height(90, h)))

                
                
        
        pg.display.update()


if __name__ == "__main__":
    main()