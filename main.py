import pygame as pg
from pygame._sdl2 import Window
from data import *
from Buttons import Button
import time
from Logger import Logger
# import buildings
from utils import adapt_size_height, adapt_size_width, load_image, get_number_font, get_text_font, get_timeline_font, resource_path
import os
from base64 import b64decode, b64encode

# Get the path to the AppData/Local directory
appdata_path = os.path.join(os.getenv('LOCALAPPDATA'), 'TimeClicker')
src_dir = resource_path("src")

# Check if the directory exists, if not, create it
if not os.path.exists(appdata_path):
    os.makedirs(appdata_path)
    
    
def save_data(timeUnits, tps, timeline, clicker_amount, buildings):            
    with open(os.path.join(appdata_path, 'data'), 'w') as f:
        data = f"{timeUnits}\n{tps}\n{timeline}\n{clicker_amount}\n{buildings}"
        data = b64encode(data.encode())
        data = data.decode().replace("=", "").replace("=", "")
        data = data[::-1]
        f.write(data)


def get_data():
    if not os.path.exists(os.path.join(appdata_path, 'data')):
        save_data(0, 0, 0, 1, "buildings")
    with open(os.path.join(appdata_path, 'data'), 'r') as f:
        data = f.read()
        data = data[::-1]
        data = data + "=="
        data = b64decode(data.encode()).decode()
        data = data.split('\n')
        timeUnits = float(data[0])
        tps = float(data[1])
        timeline = float(data[2])
        clicker_amount = int(data[3])
        buildings = data[4]
        return timeUnits, tps, timeline, clicker_amount, buildings
        

# initializing
LOGGER: Logger = Logger()
pg.init()
pg.font.init()
clock:  pg.time.Clock = pg.time.Clock()




#initialize window
screen: pg.Surface = pg.display.set_mode((720, 480), pg.RESIZABLE)
icon: pg.Surface = pg.image.load(os.path.join(src_dir, "icon.ico"))
pygame.display.set_icon(icon)
Window.from_display_module().maximize()
pg.display.set_caption('Time Clicker')
screen.fill(BACKGROUND_COLOR)
pg.display.flip()


# LOGGER.INFO('Screen width: {} Screen height: {}'.format(w, h))





def crop_value(value: float):
    if value == 0.0:
        return 0
    if value >= 10:
        return int(value)
    return round(value, 3)

    
# def format_timeUnits(timeUnits: float):
#     timeUnits = crop_value(timeUnits)
#     timeUnits =  ".".join([str(timeUnits)[::-1][i:i+3] for i in range(0, len(str(timeUnits)), 3)])[::-1]
#     if int(timeUnits.replace(".", "")) >= 10 and len(timeUnits.replace(".", "")) < 9:
#         timeUnits = "".join([" " for _ in range(9 - len(timeUnits.replace(".", "")))]) + timeUnits
#     return timeUnits

def format_timeUnits(timeUnits: float, n):
    timeUnits = crop_value(timeUnits)
    if timeUnits < 1000:
        return "".join([" " for _ in range(n+2 - len(str(timeUnits)))]) + str(timeUnits)
    for unit, factor in zip(['k', 'M', 'B', 'T', 'Qa', 'Qi', 'Sx', 'Sp', 'Oc', 'No', 'Dc', 'Ud',  'Dd', 'Td'], [10**i for i in range(3, (14 * 3)+1, 3)]):
        if timeUnits < factor * 1000:
            timeUnits = f"{timeUnits / factor:.1f}{unit}".rstrip('.0')
            return "".join([" " for _ in range(n - len(timeUnits.replace(".", "").replace(unit, "")))]) + timeUnits
    return f"{timeUnits:.0f}"

def format_time_no_convertion(value: int, n: int):
    return "".join([" " for _ in range(n+2 - len(str(value)))]) + str(value)    



def main():
    # define game values
    timeUnits, tps, timeline, clicker_amount, buildings = get_data()
    # timeUnits: float = 1
    # tps: float = 0
    
    # clicker_amount: float = 1
    # timeline: int = 0
    
    current_frame: int = 0
    framerate: int =10
    w, h = pg.display.get_surface().get_size()
    
    

    LOGGER.INFO(timeUnits)
    
    def increment_timeUnits(amount):
        nonlocal timeUnits, clicker_amount
        timeUnits += amount    

        



    running: bool = True
    while running:
        
        # clicker = Button((adapt_size_width(717.5, w), adapt_size_height(307.5, h), adapt_size_width(375, w), adapt_size_width(375, w)), BLUE, lambda: increment_timeUnits(clicker_amount), 300)
        
        
        
        # TIMELINE_FONT: pygame.font = pygame.font.Font('src/fonts/LetterGothicStd-Bold.ttf', int(adapt_size_height(124, h)))
        # NUMBER_FONT: pygame.font = pygame.font.Font('src/fonts/LetterGothicStd-Bold.ttf', int(adapt_size_height(65, h)))
        # TEXT_FONT: pygame.font = pygame.font.Font('src/fonts/FranklinGothicHeavyRegular.ttf', 33)
        
        
        
        
        timeUnits_text: pg.Surface = get_number_font(65, h).render(f"{format_timeUnits(timeUnits, 9)}", True, RED)
        tps_text: pg.Surface = get_number_font(50, h).render(f"{format_timeUnits(tps, 9)}", True, RED)
        
        timeline_text: pg.Surface = get_timeline_font(124, h).render(f"{format_time_no_convertion(timeline,3)}", True, YELLOW_GREEN)
        # timeline_text: pg.Surface = get_timeline_font(124, h).render(f"{timeline}", True, YELLOW_GREEN)
        
        clicker_button: Button = Button(
            (adapt_size_width(705, w), adapt_size_height(304, h), adapt_size_width(403, w), adapt_size_height(400, h)), (w, h)
            , f"{src_dir}/img/hourglass.png", lambda: increment_timeUnits(clicker_amount), 250, False, 0.4, 10, True)
        


        
        
        
        # manage game loop time
        clock.tick_busy_loop(framerate)
        current_frame: int = (current_frame + 1) % framerate
        
        timeUnits += tps/framerate
        


        
        for event in pg.event.get():
        
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                save_data(timeUnits, tps, timeline, clicker_amount, buildings)
                running = False
            
            clicker_button.get_event(event)



            

        screen.fill(BACKGROUND_COLOR)
        
        
        timeline_image: pg.surface = load_image(f"{src_dir}/img/timeline.png", w, h)
        screen.blit(timeline_image, (adapt_size_width(45, w), adapt_size_height(45, h)))
        
        upgrade_image: pg.surface = load_image(f"{src_dir}/img/upgrade.png", w, h)
        screen.blit(upgrade_image, (adapt_size_width(45, w), adapt_size_height(245, h)))
        
        temporal_matrix_image: pg.surface = load_image(f"{src_dir}/img/temporal matrix.png", w, h)
        screen.blit(temporal_matrix_image, (adapt_size_width(605, w), adapt_size_height(45, h)))
        
        human_skill_and_boost: pg.surface = load_image(f"{src_dir}/img/human_skill+boost.png", w, h)
        screen.blit(human_skill_and_boost, (adapt_size_width(1265, w), adapt_size_height(45, h)))
        
        shop_image: pg.surface = load_image(f"{src_dir}/img/shop.png", w, h)
        screen.blit(shop_image, (adapt_size_width(1475, w), adapt_size_height(45, h)))
        
        red_cable_image: pg.surface = load_image(f"{src_dir}/img/red_cable_on.png", w, h)
        screen.blit(red_cable_image, (adapt_size_width(1285, w), adapt_size_height(860, h)))
        
        blue_cable_image: pg.surface = load_image(f"{src_dir}/img/blue_cable_on.png", w, h)
        screen.blit(blue_cable_image, (adapt_size_width(1285, w), adapt_size_height(935, h)))
                
        
        
        # fill screen with shapes
        # pg.draw.rect(screen, DARK_GREY, (adapt_size_width(45, w), adapt_size_height(45, h), adapt_size_width(500, w), adapt_size_height(180, h)), border_radius=20)
        # pg.draw.rect(screen, DARK_GREY, (adapt_size_width(45, w), adapt_size_height(245, h), adapt_size_width(500, w), adapt_size_height(790, h)), border_radius=20)
        # pg.draw.rect(screen, DARK_GREY, (adapt_size_width(605, w), adapt_size_height(45, h), adapt_size_width(600, w), adapt_size_height(990, h)), border_radius=20)
        # pg.draw.rect(screen, DARK_GREY, (adapt_size_width(1475, w), adapt_size_height(45, h), adapt_size_width(400, w), adapt_size_height(800, h)), border_radius=20)
        
        # pg.draw.rect(screen, LIGHT_DARK, (adapt_size_width(75, w), adapt_size_height(75, h), adapt_size_width(440, w), adapt_size_height(120, h)))
        # pg.draw.rect(screen, LIGHT_DARK, (adapt_size_width(75, w), adapt_size_height(275, h), adapt_size_width(440, w), adapt_size_height(730, h)))
        # pg.draw.rect(screen, LIGHT_DARK, (adapt_size_width(635, w), adapt_size_height(75, h), adapt_size_width(540, w), adapt_size_height(930, h)))
        # pg.draw.rect(screen, LIGHT_DARK, (adapt_size_width(1505, w), adapt_size_height(75, h), adapt_size_width(340, w), adapt_size_height(740, h)))
        
        
        
        # draw text
        screen.blit(timeUnits_text, (adapt_size_width(700, w), adapt_size_height(840, h)))
        screen.blit(tps_text, (adapt_size_width(700, w), adapt_size_height(177, h)))
        
        screen.blit(timeline_text, (adapt_size_width(90, w), adapt_size_height(87, h)))
        
        clicker_button.render(screen)

                
                
        
        pg.display.update()


if __name__ == "__main__":
    main()