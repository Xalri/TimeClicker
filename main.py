import os
import sys
import time
import ctypes
import inspect
from pprint import pprint
from datetime import datetime

import pygame as pg
from pygame._sdl2 import Window
from pygame.locals import *

from data import *
from Buttons import Button
from Logger import Logger
from buildings import buildings
from utils import (
    adapt_size_height, adapt_size_width, load_image, get_number_font,
    get_text_font, get_timeline_font, resource_path, save_data, get_data,
    crop_value, format_timeUnits, format_time_no_convertion, buy_buildings,
    can_buy_buildings
)

LOGGER: Logger = Logger()
pg.init()
pg.font.init()
clock:  pg.time.Clock = pg.time.Clock()


if len(sys.argv) > 1:
    if sys.argv[1] == "--debug":
        LOGGER.set_level(4)
        
appdata_path = os.path.join(os.getenv('LOCALAPPDATA'), 'TimeClicker')
src_dir = resource_path("src")

os.makedirs(appdata_path, exist_ok=True)

ctypes.windll.user32.SetProcessDPIAware()
monitor_info = ctypes.windll.user32.MonitorFromWindow(None, 2)
monitor_rect = ctypes.wintypes.RECT()
ctypes.windll.user32.GetMonitorInfoW(monitor_info, ctypes.byref(monitor_rect))
monitor_x = monitor_rect.left
monitor_y = monitor_rect.top
os.environ['SDL_VIDEO_WINDOW_POS'] = f"{monitor_x},{monitor_y}"


screen: pg.Surface = pg.display.set_mode((1024, 576), pg.RESIZABLE)
icon: pg.Surface = pg.image.load(os.path.join(src_dir, "icon.png"))
pg.display.set_icon(icon)
Window.from_display_module().maximize()
pg.display.set_caption('Time Clicker')

def main():
    # define game values
    # save_data(appdata_path)
    timeUnits, tps, timeline, clicker_amount, bought_buildings, max_timeUnits, last_saved_time = get_data(appdata_path)
    max_timeUnits = int(float(max_timeUnits))
    timeUnits = 1000000000000000
    # clicker_amount = 10000000
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
    
    is_clickable = False
    
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
        bought_buildings["long_list"].append({"name": buildings[0]["name"], "amount": 0})
    LOGGER.DEBUG(bought_buildings)

    scroll_y = 0
    scroll_speed = 20
    max_scroll_y = 0  # Define the maximum bottom scroll limit
    scroll_area_rect = pg.Rect(adapt_size_width(1525, wi), adapt_size_height(70, he), adapt_size_width(300, wi), adapt_size_height(750, he))
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
        
        timeUnits_text: pg.Surface = get_number_font(65, h).render(f"{format_timeUnits(timeUnits, 6)}", True, RED)
        tps_text: pg.Surface = get_number_font(50, h).render(f"{format_timeUnits(tps, 6)} TU/s", True, RED)
        
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
        
        
        
        match era:
            case 1:
                base = "src/img/buildings/base_1.png"
            case 2:
                base = "src/img/buildings/base_2.png"
            case 3:
                base = "src/img/buildings/base_3.png"
            case 4:
                base = "src/img/buildings/base_4.png"
            case 5:
                base = "src/img/buildings/base_5.png"
        for i in range(len(available_buildings)):
            build = available_buildings[i]
            build_name = build["name"]
            tps += build["tps_boost"] * next((b['amount'] for b in bought_buildings["long_list"] if b['name'] == build["name"]), 0)
            # img = load_image("src/img/buildings/" + build["name"].lower() + ".png", w, h)
            buildings_buttons.append(Button(
                (adapt_size_width(1525, w), adapt_size_height(85, h) + (adapt_size_height(105, h)*i) + adapt_size_height((scroll_y * 1), h), adapt_size_width(300, w), adapt_size_height(45, w)),
                (w, h), background=base, border_radius=20,
                command=lambda b=build_name: buy_building_wrapper(b), identifier=build["name"]
            ))
            # buildings_buttons.append(Button(
            #     (adapt_size_width(1525, w), adapt_size_height(85, h) + (adapt_size_height(105, h)*i) + adapt_size_height((scroll_y * 1), h), adapt_size_width(300, w), adapt_size_height(45, w)),
            #     (w, h), background=BLUE, border_radius=20,
            #     command=lambda b=build_name: buy_building_wrapper(b), identifier=build["name"]
            # ))

        
        pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                print("exiting...")
                save_data(appdata_path, timeUnits, tps, timeline, clicker_amount, bought_buildings, max_timeUnits )
                running = False
            elif event.type == pg.KEYDOWN and event.key == pg.K_F7:
                if LOGGER.get_level() == 4:
                    LOGGER.INFO("Setting log level to WARNING")
                    LOGGER.set_level(3)
                else:
                    LOGGER.INFO("Setting log level to DEBUG")
                    LOGGER.set_level(4)
            elif event.type == pg.MOUSEWHEEL and len(available_buildings) > 6:
                LOGGER.DEBUG(f"scroll offset: {event.y}")
                if can_scroll_up or event.y > 0:
                    scroll_y += event.y * scroll_speed
                    scroll_y = min(scroll_y, 0)  # Ensure scroll_y does not go below 0
            
            if event.type == pg.MOUSEMOTION:
                is_clickable = False
                clicker_button.get_event(event)
                for build_button in buildings_buttons:
                    rel_x, rel_y = event.pos[0] - scroll_area_rect.x, event.pos[1] - scroll_area_rect.y
                    if 0 <= rel_x < scroll_area_rect.width and 0 <= rel_y < scroll_area_rect.height:
                        is_clickable = True
                        
            for build_button in buildings_buttons:
                build_button.get_event(event)
                
            clicker_button.get_event(event)

        mouse_pos = pg.mouse.get_pos()
        for build_button in buildings_buttons:
            button_rect = build_button.rect
            if scroll_area_rect.colliderect(button_rect) and is_clickable:
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
            
            building_image = load_image(f"src/img/buildings/{build_button.identifier.lower()}.png", w, h)
            
            # print(f"scroll_y: {scroll_y}({abs(adapt_size_height((scroll_y * 1), h))})")
            button_rect = build_button.rect.move(0, build_button.rect.height + adapt_size_height(7.5, h))
            building_rect = building_image.get_rect(topleft=(adapt_size_width(1525, w), adapt_size_height(85 + 105 * i, h))).move(0, adapt_size_height((scroll_y * 1), h))
            # build_button.rect = button_rect
            if not can_buy_buildings(bought_buildings, build_button.identifier, 1, timeUnits):
                build_button.render(screen, darker=True)
                building_image.fill((100, 100, 100), special_flags=pg.BLEND_MULT)
                screen.blit(building_image, building_rect.topleft)
                screen.blit(get_text_font(25, h).render(f"{format_timeUnits(round(cost))}", True, DARK_BROWN), (adapt_size_width(1592, w), adapt_size_height(132 + 104.5 * i, h) + adapt_size_height((scroll_y * 1), h)))
                screen.blit(get_text_font(19, h).render(f"{format_time_no_convertion(amount)}", True, GREY), (adapt_size_width(1780, w), adapt_size_height(112.5 + 104.5 * i, h) + adapt_size_height((scroll_y * 1), h)))
            else:
                build_button.render(screen)
                screen.blit(building_image, building_rect.topleft)
                screen.blit(get_text_font(25, h).render(f"{format_timeUnits(round(cost))}", True, BROWN), (adapt_size_width(1592, w), adapt_size_height(132 + 104.5 * i, h) + adapt_size_height((scroll_y * 1), h)))
                screen.blit(get_text_font(19, h).render(f"{format_time_no_convertion(amount, 6)}", True, WHITE), (adapt_size_width(1750, w), adapt_size_height(132.5 + 104.5 * i, h) + adapt_size_height((scroll_y * 1), h)))
            if scroll_area_rect.colliderect(button_rect) and button_rect.top >= scroll_area_rect.top:
                if i == len(buildings_buttons) - 1:
                    if  can_scroll_up:
                        LOGGER.DEBUG("stopping scrolling")
                        can_scroll_up = False
                else:
                    if not can_scroll_up:
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
        screen.blit(tps_text, (adapt_size_width(710, w), adapt_size_height(187.5, h)))
        screen.blit(timeline_text, (adapt_size_width(90, w), adapt_size_height(87, h)))
        
        # pg.draw.rect(screen, (0, 0, 255), scroll_area_rect, 2)
        
        clicker_button.render(screen)
        
            
            

        # Render the scrollbar
        total_height = len(buildings_buttons) * adapt_size_height(105, h)
        visible_ratio = scroll_area_rect.height / total_height
        scrollbar_height = max(scroll_area_rect.height * visible_ratio, 20)
        scrollbar_y = scroll_area_rect.y - scroll_y * visible_ratio
        pg.draw.rect(screen, (200, 200, 200), (scrollbar_rect.x, scrollbar_y, scrollbar_rect.width, scrollbar_height))

        pg.display.flip()
        elapsed_time = clock.get_time() / 1000.0  # Get elapsed time in seconds
        loop_number = int(elapsed_time // (1 / framerate))
        # print("-" * 50 + f" loop {loop_number} tick {current_frame}/{framerate}")

if __name__ == "__main__":
    main()