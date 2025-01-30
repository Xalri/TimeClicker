import pygame as pg
from pygame._sdl2 import Window
from data import *
from Buttons import Button
import time
from Logger import Logger
from buildings import buildings
from utils import adapt_size_height, adapt_size_width, load_image, get_number_font, get_text_font, get_timeline_font, resource_path, save_data, get_data, crop_value, format_timeUnits, format_time_no_convertion
import os
from pprint import pprint

LOGGER: Logger = Logger()
pg.init()
pg.font.init()
clock:  pg.time.Clock = pg.time.Clock()


appdata_path = os.path.join(os.getenv('LOCALAPPDATA'), 'TimeClicker')
src_dir = resource_path("src")

os.makedirs(appdata_path, exist_ok=True)
    
    
        


screen: pg.Surface = pg.display.set_mode((1024, 576), pg.RESIZABLE)
icon: pg.Surface = pg.image.load(os.path.join(src_dir, "icon.png"))
pygame.display.set_icon(icon)
Window.from_display_module().maximize()
pg.display.set_caption('Time Clicker')







 



def main():
    # define game values
    save_data(appdata_path, 0)
    timeUnits, tps, timeline, clicker_amount, bought_buildings, max_timeUnits = get_data(appdata_path)
    max_timeUnits = int(float(max_timeUnits))
    LOGGER.DEBUG(f"{timeUnits}({type(timeUnits)}), {tps}({type(tps)}), {timeline}({type(timeline)}), {clicker_amount}({type(clicker_amount)}), {bought_buildings}({type(bought_buildings)}), {max_timeUnits}({type(max_timeUnits)}).")
    
    current_frame: int = 0
    framerate: int =10
    
    w = h = "n"
    
    era: int = 1
    
    available_buildings: list = []
    
    

    LOGGER.INFO(timeUnits)
    
    def increment_timeUnits(amount):
        nonlocal timeUnits, clicker_amount
        timeUnits += amount    
        
        
        
    LOGGER.DEBUG("Initializing screen size")
    wi, he = pg.display.get_surface().get_size()
    timeUnits_text: pg.Surface = get_number_font(65, he).render(f"{format_timeUnits(timeUnits, 9)}", True, RED)
    tps_text: pg.Surface = get_number_font(50, he).render(f"{format_timeUnits(tps, 9)}", True, RED)
    
    timeline_text: pg.Surface = get_timeline_font(124, he).render(f"{format_time_no_convertion(timeline,3)}", True, YELLOW_GREEN)
    # timeline_text: pg.Surface = get_timeline_font(124, he).render(f"{timeline}", True, YELLOW_GREEN)
    
    clicker_button: Button = Button(
        (adapt_size_width(705, wi), adapt_size_height(304, he), adapt_size_width(403, wi), adapt_size_height(400, he)), (wi, he)
        , f"{src_dir}/img/hourglass.png", lambda: increment_timeUnits(clicker_amount), 250, False, 0.4, 10, True)
    
    # clicker_button: Button = Button((adapt_size_width(705, wi, True), adapt_size_height(304, he, True), adapt_size_width(403, wi, True), adapt_size_height(400, he, True)), (wi, he))    
    
    timeline_image: pg.surface = load_image(f"{src_dir}/img/timeline.png", wi, he)
    upgrade_image: pg.surface = load_image(f"{src_dir}/img/upgrade.png", wi, he)
    temporal_matrix_image: pg.surface = load_image(f"{src_dir}/img/temporal matrix.png", wi, he)
    human_skill_and_boost: pg.surface = load_image(f"{src_dir}/img/human_skill+boost.png", wi, he)
    shop_image: pg.surface = load_image(f"{src_dir}/img/shop.png", wi, he)
    red_cable_image: pg.surface = load_image(f"{src_dir}/img/red_cable_on.png", wi, he)
    blue_cable_image: pg.surface = load_image(f"{src_dir}/img/blue_cable_on.png", wi, he)

    if buildings[0]["name"] not in bought_buildings["short_list"]:
        bought_buildings["short_list"].append(buildings[0]["name"])
        bought_buildings["long_list"].append({"name": buildings[0]["name"], "amount": 5})
    pprint(bought_buildings)



    running: bool = True
    while running:
        
        # w, h = pg.display.get_surface().get_size()

        # clicker = Button((adapt_size_width(717.5, w), adapt_size_height(307.5, h), adapt_size_width(375, w), adapt_size_width(375, w)), BLUE, lambda: increment_timeUnits(clicker_amount), 300)
        
        
        
        # TIMELINE_FONT: pygame.font = pygame.font.Font('src/fonts/LetterGothicStd-Bold.ttf', int(adapt_size_height(124, h)))
        # NUMBER_FONT: pygame.font = pygame.font.Font('src/fonts/LetterGothicStd-Bold.ttf', int(adapt_size_height(65, h)))
        # TEXT_FONT: pygame.font = pygame.font.Font('src/fonts/FranklinGothicHeavyRegular.ttf', 33)
        
        
        LOGGER.DEBUG(f"Testing screen => {(w, h)} | {pg.display.get_surface().get_size()}")
        if w != pg.display.get_surface().get_width() or h != pg.display.get_surface().get_height():
            LOGGER.DEBUG("Updating screen size")
            w, h = pg.display.get_surface().get_size()
            
            timeline_text: pg.Surface = get_timeline_font(124, h).render(f"{format_time_no_convertion(timeline,3)}", True, YELLOW_GREEN)
            # timeline_text: pg.Surface = get_timeline_font(124, h).render(f"{timeline}", True, YELLOW_GREEN)
            
            clicker_button: Button = Button(
                (adapt_size_width(705, w, True), adapt_size_height(304, h, True), adapt_size_width(403, w, True), adapt_size_height(400, h, True)), (w, h)
                , f"{src_dir}/img/hourglass.png", lambda: increment_timeUnits(clicker_amount), 250, False, 0.4, 10, True)
            
            
            timeline_image: pg.surface = load_image(f"{src_dir}/img/timeline.png", w, h)
            upgrade_image: pg.surface = load_image(f"{src_dir}/img/upgrade.png", w, h)
            temporal_matrix_image: pg.surface = load_image(f"{src_dir}/img/temporal matrix.png", w, h)
            human_skill_and_boost: pg.surface = load_image(f"{src_dir}/img/human_skill+boost.png", w, h)
            shop_image: pg.surface = load_image(f"{src_dir}/img/shop.png", w, h)
            red_cable_image: pg.surface = load_image(f"{src_dir}/img/red_cable_on.png", w, h)
            blue_cable_image: pg.surface = load_image(f"{src_dir}/img/blue_cable_on.png", w, h)
        
        timeUnits_text: pg.Surface = get_number_font(65, h).render(f"{format_timeUnits(timeUnits, 9)}", True, RED)
        tps_text: pg.Surface = get_number_font(50, h).render(f"{format_timeUnits(tps, 9)}", True, RED)
        
        
        

        
        for i in range(len(buildings)):
            build = buildings[i]
            previous_build = buildings[i-1] if i > 0 else None
            if build["name"] in bought_buildings["short_list"] or i == 0:
                if not build in available_buildings: available_buildings.append(build)
            elif max_timeUnits > build["cost"](1)/2     and     previous_build["name"] in bought_buildings["short_list"]     and     (next((b['amount'] for b in bought_buildings["long_list"] if b['name'] == previous_build["name"]), None) >= 5):
                if not build in available_buildings: available_buildings.append(build)
                
                
        
        
        LOGGER.DEBUG(f"Available buildings:")
        pprint([build["name"] for build in available_buildings])
        
        
        
        
        
        
        
        
        
        # manage game loop time
        clock.tick_busy_loop(framerate)
        current_frame: int = (current_frame + 1) % framerate
        
        timeUnits += tps/framerate
        
        max_timeUnits = max(max_timeUnits, timeUnits)
        

        
        for event in pg.event.get():
        
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                print("exiting...")
                save_data(appdata_path, timeUnits, tps, timeline, clicker_amount, bought_buildings, max_timeUnits)
                running = False
            
            clicker_button.get_event(event)



            





        screen.fill(BACKGROUND_COLOR)
        
        
        screen.blit(timeline_image, (adapt_size_width(45, w), adapt_size_height(45, h)))
        screen.blit(upgrade_image, (adapt_size_width(45, w), adapt_size_height(245, h)))
        screen.blit(temporal_matrix_image, (adapt_size_width(605, w), adapt_size_height(45, h)))
        screen.blit(human_skill_and_boost, (adapt_size_width(1265, w), adapt_size_height(45, h)))
        screen.blit(shop_image, (adapt_size_width(1475, w), adapt_size_height(45, h)))
        screen.blit(red_cable_image, (adapt_size_width(1285, w), adapt_size_height(860, h)))
        screen.blit(blue_cable_image, (adapt_size_width(1285, w), adapt_size_height(935, h)))
                
        
        tps = 0
        for build in available_buildings:
            
            tps += build["tps_boost"]*next((b['amount'] for b in bought_buildings["long_list"] if b['name'] == build["name"]), 0)
            
        
        
        
        # draw text
        screen.blit(timeUnits_text, (adapt_size_width(700, w), adapt_size_height(835, h)))
        screen.blit(tps_text, (adapt_size_width(715, w), adapt_size_height(190, h)))
        screen.blit(timeline_text, (adapt_size_width(90, w), adapt_size_height(87, h)))
        
        clicker_button.render(screen)

                
        
        
        
        pg.display.update()
        pg.display.flip()
        elapsed_time = clock.get_time() / 1000.0  # Get elapsed time in seconds
        loop_number = int(elapsed_time // (1 / framerate))
        print("-" * 50 + f" loop {loop_number} tick {current_frame}/{framerate}")


if __name__ == "__main__":
    main()