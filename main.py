import pygame as pg
from pygame._sdl2 import Window
from data import *
from Buttons import Button
import time
from Logger import Logger
from buildings import buildings
from utils import adapt_size_height, adapt_size_width, load_image, get_number_font, get_text_font, get_timeline_font, resource_path, save_data, get_data, crop_value, format_timeUnits, format_time_no_convertion, buy_buildings, can_buy_buildings
import os
from pprint import pprint
import inspect
from datetime import datetime

LOGGER: Logger = Logger()
pg.init()
pg.font.init()
clock:  pg.time.Clock = pg.time.Clock()

appdata_path = os.path.join(os.getenv('LOCALAPPDATA'), 'TimeClicker')
src_dir = resource_path("src")

os.makedirs(appdata_path, exist_ok=True)

screen: pg.Surface = pg.display.set_mode((1024, 576), pg.RESIZABLE)
icon: pg.Surface = pg.image.load(os.path.join(src_dir, "icon.png"))
pg.display.set_icon(icon)
Window.from_display_module().maximize()
pg.display.set_caption('Time Clicker')

def main():
    # define game values
    timeUnits, tps, timeline, clicker_amount, bought_buildings, max_timeUnits, last_saved_time = get_data(appdata_path)
    max_timeUnits = int(float(max_timeUnits))
    timeUnits = 1000000000000000
    clicker_amount = 10000000
    LOGGER.DEBUG(f"{timeUnits}({type(timeUnits)}), {tps}({type(tps)}), {timeline}({type(timeline)}), {clicker_amount}({type(clicker_amount)}), {bought_buildings}({type(bought_buildings)}), {max_timeUnits}({type(max_timeUnits)}).")
    

    if last_saved_time:
        elapsed_time = (datetime.now() - datetime.strptime(last_saved_time, " %Y-%m-%d %H:%M:%S")).total_seconds()
        timeUnits += tps * (elapsed_time )  # Add production for the elapsed time
        LOGGER.INFO(f"Elapsed time: {elapsed_time} seconds, added {tps * (elapsed_time )} timeUnits, tps: {tps}")




    current_frame: int = 0
    framerate: int = 10
    
    w = h = "n"
    
    era: int = 1
    
    available_buildings: list = []

    can_scroll_up = True
    
    LOGGER.INFO(timeUnits)
    
    def increment_timeUnits(amount):
        nonlocal timeUnits, clicker_amount
        timeUnits += amount    

    def buy_building_wrapper(b):
        nonlocal bought_buildings, timeUnits
        bought_buildings, timeUnits = buy_buildings(bought_buildings, b, 1, timeUnits)
        
    LOGGER.DEBUG("Initializing screen size")
    wi, he = pg.display.get_surface().get_size()
    timeUnits_text: pg.Surface = get_number_font(65, he).render(f"{format_timeUnits(timeUnits, 9)}", True, RED)
    tps_text: pg.Surface = get_number_font(50, he).render(f"{format_timeUnits(tps, 9)}", True, RED)
    
    timeline_text: pg.Surface = get_timeline_font(124, he).render(f"{format_time_no_convertion(timeline,3)}", True, YELLOW_GREEN)
    
    clicker_button: Button = Button(
        (adapt_size_width(705, wi), adapt_size_height(304, he), adapt_size_width(403, wi), adapt_size_height(400, he)), (wi, he)
        , f"{src_dir}/img/hourglass.png", lambda: increment_timeUnits(clicker_amount), 250, False, 0.4, 10, True)
    
    timeline_image: pg.surface = load_image(f"{src_dir}/img/timeline.png", wi, he)
    upgrade_image: pg.surface = load_image(f"{src_dir}/img/upgrade.png", wi, he)
    temporal_matrix_image: pg.surface = load_image(f"{src_dir}/img/temporal matrix.png", wi, he)
    human_skill_and_boost: pg.surface = load_image(f"{src_dir}/img/human_skill+boost.png", wi, he)
    shop_fond_image: pg.surface = load_image(f"{src_dir}/img/shop_fond.png", wi, he)
    shop_bord_image: pg.surface = load_image(f"{src_dir}/img/shop_bord.png", wi, he)    
    red_cable_image: pg.surface = load_image(f"{src_dir}/img/red_cable_on.png", wi, he)
    blue_cable_image: pg.surface = load_image(f"{src_dir}/img/blue_cable_on.png", wi, he)

    if buildings[0]["name"] not in bought_buildings["short_list"]:
        bought_buildings["short_list"].append(buildings[0]["name"])
        bought_buildings["long_list"].append({"name": buildings[0]["name"], "amount": 5})
    pprint(bought_buildings)

    scroll_y = 0
    scroll_speed = 20
    max_scroll_y = 0  # Define the maximum bottom scroll limit
    scroll_area_rect = pg.Rect(adapt_size_width(1525, wi), adapt_size_height(80, he), adapt_size_width(300, wi), adapt_size_height(700, he))
    scrollbar_rect = pg.Rect(adapt_size_width(1830, wi), adapt_size_height(160, he), adapt_size_width(20, wi), adapt_size_height(600, he))

    running: bool = True
    while running:
        # LOGGER.DEBUG(f"Testing screen => {(w, h)} | {pg.display.get_surface().get_size()}")
        if w != pg.display.get_surface().get_width() or h != pg.display.get_surface().get_height():
            LOGGER.DEBUG("Updating screen size")
            w, h = pg.display.get_surface().get_size()
            
            timeline_text: pg.Surface = get_timeline_font(124, h).render(f"{format_time_no_convertion(timeline,3)}", True, YELLOW_GREEN)
            
            clicker_button: Button = Button(
                (adapt_size_width(705, w, True), adapt_size_height(304, h, True), adapt_size_width(403, w, True), adapt_size_height(400, h, True)), (w, h)
                , f"{src_dir}/img/hourglass.png", lambda: increment_timeUnits(clicker_amount), 250, False, 0.4, 10, True)
            
            timeline_image: pg.surface = load_image(f"{src_dir}/img/timeline.png", w, h)
            upgrade_image: pg.surface = load_image(f"{src_dir}/img/upgrade.png", w, h)
            temporal_matrix_image: pg.surface = load_image(f"{src_dir}/img/temporal matrix.png", w, h)
            human_skill_and_boost: pg.surface = load_image(f"{src_dir}/img/human_skill+boost.png", w, h)
            shop_fond_image: pg.surface = load_image(f"{src_dir}/img/shop_fond.png", w, h)
            shop_bord_image: pg.surface = load_image(f"{src_dir}/img/shop_bord.png", w, h)
            red_cable_image: pg.surface = load_image(f"{src_dir}/img/red_cable_on.png", w, h)
            blue_cable_image: pg.surface = load_image(f"{src_dir}/img/blue_cable_on.png", w, h)
        
        timeUnits_text: pg.Surface = get_number_font(65, h).render(f"{format_timeUnits(timeUnits, 9)}", True, RED)
        tps_text: pg.Surface = get_number_font(50, h).render(f"{format_timeUnits(tps, 9)} TU/s", True, RED)
        
        for i in range(len(buildings)):
            build = buildings[i]
            previous_build = buildings[i-1] if i > 0 else None
            if build["name"] in bought_buildings["short_list"] or i == 0:
                if not build in available_buildings: available_buildings.append(build)
            elif previous_build["name"] in bought_buildings["short_list"] and (next((b['amount'] for b in bought_buildings["long_list"] if b['name'] == previous_build["name"]), None) >= 1):
                if not build in available_buildings: available_buildings.append(build)
        
        clock.tick_busy_loop(framerate)
        current_frame: int = (current_frame + 1) % framerate
        
        timeUnits += tps / framerate
        max_timeUnits = max(max_timeUnits, timeUnits)
        
        buildings_buttons: list = []
        tps: int = 0
        for i in range(len(available_buildings)):
            build = available_buildings[i]
            build_name = build["name"]
            tps += build["tps_boost"] * next((b['amount'] for b in bought_buildings["long_list"] if b['name'] == build["name"]), 0)
            img = load_image("src/img/buildings/" + build["name"].lower() + ".png", w, h)
            buildings_buttons.append(Button(
                (adapt_size_width(1525, w), adapt_size_height(45, w) + (adapt_size_height(53, w)*i) + adapt_size_height((scroll_y * 0), h), adapt_size_width(300, w), adapt_size_height(45, w)),
                (w, h), background="src/img/buildings/" + build_name.lower() + ".png", border_radius=20,
                command=lambda b=build_name: buy_building_wrapper(b), identifier=build["name"]
            ))

        

        pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                print("exiting...")
                save_data(appdata_path, timeUnits, tps, timeline, clicker_amount, bought_buildings, max_timeUnits )
                running = False
            elif event.type == pg.MOUSEWHEEL and len(available_buildings) > 6:
                print(event.y)
                if can_scroll_up or event.y > 0:
                    scroll_y += event.y * scroll_speed
                    scroll_y = min(scroll_y, 0)  # Ensure scroll_y does not go below 0
            
            clicker_button.get_event(event)
            for build_button in buildings_buttons:
                button_rect = build_button.rect.move(0, scroll_y)
                if scroll_area_rect.colliderect(button_rect) and button_rect.top >= scroll_area_rect.top:
                    build_button.get_event(event)

        mouse_pos = pg.mouse.get_pos()
        for build_button in buildings_buttons:
            button_rect = build_button.rect.move(0, scroll_y)
            if scroll_area_rect.colliderect(button_rect) and button_rect.top >= scroll_area_rect.top:
                build_button.update_hover_state(mouse_pos)

        
        screen.blit(shop_fond_image, (adapt_size_width(1475, w), adapt_size_height(45, h)))
        
        for i in range(len(buildings_buttons)):
            build_button = buildings_buttons[i]
            build = next((b for b in bought_buildings["long_list"] if b["name"] == build_button.identifier), None)
            if build is None:
                amount = 0
                cost = next((b["cost"](1) for b in buildings if b["name"] == build_button.identifier), None)
            else:
                amount = build["amount"]
                cost = next((b["cost"](amount + 1) - b["cost"](amount) for b in buildings if b["name"] == build_button.identifier), None)
            
            match era:
                case 1:
                    base = load_image("src/img/buildings/base_1.png", w, h)
                case 2:
                    base = load_image("src/img/buildings/base_2.png", w, h)
                case 3:
                    base = load_image("src/img/buildings/base_3.png", w, h)
                case 4:
                    base = load_image("src/img/buildings/base_4.png", w, h)
                case 5:
                    base = load_image("src/img/buildings/base_5.png", w, h)
            
            button_rect = build_button.rect.move(0, scroll_y)
            base_rect = base.get_rect(topleft=(adapt_size_width(1525, w), adapt_size_height(85 + 105 * i, h))).move(0, scroll_y)
            # build_button.rect = button_rect
            if not can_buy_buildings(bought_buildings, build_button.identifier, 1, timeUnits):
                base.fill((100, 100, 100), special_flags=pg.BLEND_MULT)
                screen.blit(base, base_rect.topleft)
                build_button.render(screen, darker=True)
                screen.blit(get_text_font(25, h).render(f"{format_timeUnits(round(cost))}", True, DARK_BROWN), (adapt_size_width(1592, w), adapt_size_height(132 + 104.5 * i, h) + scroll_y))
                screen.blit(get_text_font(19, h).render(f"{format_time_no_convertion(amount)}", True, GREY), (adapt_size_width(1780, w), adapt_size_height(107 + 104.5 * i, h) + scroll_y))
            else:
                screen.blit(base, base_rect.topleft)
                build_button.render(screen)
                screen.blit(get_text_font(25, h).render(f"{format_timeUnits(round(cost))}", True, BROWN), (adapt_size_width(1592, w), adapt_size_height(132 + 104.5 * i, h) + scroll_y))
                screen.blit(get_text_font(19, h).render(f"{format_time_no_convertion(amount, 6)}", True, WHITE), (adapt_size_width(1750, w), adapt_size_height(107 + 104.5 * i, h) + scroll_y))
            if scroll_area_rect.colliderect(button_rect) and button_rect.top >= scroll_area_rect.top:
                if i == len(buildings_buttons) - 1:
                    LOGGER.DEBUG("stopping scrolling")
                    can_scroll_up = False
                else:
                    LOGGER.DEBUG("starting scrolling")
                    can_scroll_up = True
                    
                    
        screen.blit(load_image("src/img/background.png", w, h), (0, 0))
        screen.blit(timeline_image, (adapt_size_width(45, w), adapt_size_height(45, h)))
        screen.blit(upgrade_image, (adapt_size_width(45, w), adapt_size_height(245, h)))
        screen.blit(temporal_matrix_image, (adapt_size_width(605, w), adapt_size_height(45, h)))
        screen.blit(human_skill_and_boost, (adapt_size_width(1265, w), adapt_size_height(45, h)))
        screen.blit(shop_bord_image, (adapt_size_width(1475, w), adapt_size_height(45, h)))
        screen.blit(red_cable_image, (adapt_size_width(1285, w), adapt_size_height(860, h)))
        screen.blit(blue_cable_image, (adapt_size_width(1285, w), adapt_size_height(935, h)))
        
        screen.blit(timeUnits_text, (adapt_size_width(700, w), adapt_size_height(835, h)))
        screen.blit(tps_text, (adapt_size_width(715, w), adapt_size_height(190, h)))
        screen.blit(timeline_text, (adapt_size_width(90, w), adapt_size_height(87, h)))
        
        clicker_button.render(screen)
        
            
            

        # Render the scrollbar
        total_height = len(buildings_buttons) * adapt_size_height(105, h)
        visible_ratio = scroll_area_rect.height / total_height
        scrollbar_height = max(scroll_area_rect.height * visible_ratio, 20)
        scrollbar_y = scroll_area_rect.y - scroll_y * visible_ratio
        pg.draw.rect(screen, (200, 200, 200), (scrollbar_rect.x, scrollbar_y, scrollbar_rect.width, scrollbar_height))

        pg.display.update()
        pg.display.flip()
        elapsed_time = clock.get_time() / 1000.0  # Get elapsed time in seconds
        loop_number = int(elapsed_time // (1 / framerate))
        # print("-" * 50 + f" loop {loop_number} tick {current_frame}/{framerate}")

if __name__ == "__main__":
    main()