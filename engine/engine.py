import math
import os
from random import randint
import sys
import ctypes
from pprint import pprint
from datetime import datetime
import threading

import pygame as pg
from pygame._sdl2 import Window
from pygame.locals import *

from config import FRAMERATE
from data.data import *
from other.Logger import Logger
from data.buildings import buildings
from data.upgrade import TIMELINE_UPGRADE, UPGRADES, treshold

from engine.utils import (
    adapt_size_height as adapth,
    adapt_size_width as adaptw,
    buy_human_skill,
    buy_timeline,
    load_image,
    get_number_font,
    get_text_font,
    get_timeline_font,
    resource_path,
    save_data,
    get_data,
    crop_value,
    format_timeUnits,
    format_time_no_convertion,
    buy_buildings,
    can_buy_buildings,
    buy_upgrades,
    can_buy_upgrade,
    show_message,
    unlock_timeline,
)






class Engine:
    def __init__(self):
        self.LOGGER = Logger()
        pg.init()
        pg.font.init()
        self.clock = pg.time.Clock()

        if len(sys.argv) > 1:
            if sys.argv[1] == "--debug":
                self.LOGGER.set_level(4)

        self.appdata_path = os.path.join(os.getenv("LOCALAPPDATA"), "TimeClicker")
        self.src_dir = resource_path("src")
        os.makedirs(self.appdata_path, exist_ok=True)
        
        ctypes.windll.user32.SetProcessDPIAware()
        monitor_info = ctypes.windll.user32.MonitorFromWindow(None, 2)
        monitor_rect = ctypes.wintypes.RECT()
        ctypes.windll.user32.GetMonitorInfoW(monitor_info, ctypes.byref(monitor_rect))
        os.environ["SDL_VIDEO_WINDOW_POS"] = f"{500},{300}"

        self.screen = pg.display.set_mode((1024, 576), pg.RESIZABLE)
        icon = pg.image.load(os.path.join(self.src_dir, "icon.png"))
        pg.display.set_icon(icon)
        self.window = Window.from_display_module()
        self.window.restore()
        self.window.maximize()
        pg.display.set_caption("Time Clicker")
    
    
    
        self.current_frame = 0
        self.framerate = FRAMERATE

        self.timeUnits = 0
        self.tps = 0
        self.timeline = -1
        self.clicker_amount = 1
        self.bought_buildings = {"short_list": [buildings[0]["name"]], "long_list": [{"name": buildings[0]["name"], "amount": 0}]}
        self.max_timeUnits = 0
        self.bought_upgrades = {"short_list": [], "long_list": []}
        self.human_skills = {"strength":100, "agility": 0, "intelligence": 0}
        self.last_saved_time = None
        
        self.era = 1
                
        self.available_buildings = []
        self.available_upgrades = []
        
        self.save_count = 0
        
        
        
        self.blue_cable_count = 0
        self.blue_cable_timer = randint(3, 15)
        self.is_blue_cable_cut = False
        
        self.blue_cable_x5_timer=0
        self.blue_cable_x2_timer=0
        
        self.red_cable_timer = randint(3, 15)
        self.red_cable_count = 0
        self.is_red_cable_cut = False
        self.red_cable_tps_reduction = 0
        
        self.tps_boost_from_cable = 0
        
        self.price_reduction = 0
        
        self.boost_duration = 0
        
        self.running = True
        
        
        
    def increment_timeUnits(self, amount):
        self.timeUnits += amount
        print(amount)
    def buy_building_wrapper(self, building_name):
        if building_name == "Time Machine":
            if can_buy_buildings(self.bought_buildings, building_name, 1, self.timeUnits):
                self.reset("Congratulations! You have finished the game!\n Time Units earned: " + str(format_timeUnits(self.timeUnits)) + "\n THE GAME WILL NOW RESET...")
                

        self.bought_buildings, self.timeUnits = buy_buildings(self.bought_buildings, building_name, 1, self.timeUnits, self.price_reduction)     
    def buy_upgrade_wrapper(self, upgrade_name):
        self.LOGGER.INFO("upgrade wrapper called")
        self.bought_upgrades, self.timeUnits, self.bought_buildings = buy_upgrades(self.bought_upgrades, upgrade_name, self.timeUnits, self.bought_buildings, self.price_reduction)
    def buy_timeline_wrapper(self):
        if self.era == 1:
            self.era, self.timeline, self.timeUnits = unlock_timeline(self.era, self.timeline, self.timeUnits)
        else:
            self.timeline, self.timeUnits = buy_timeline(self.timeline, self.timeUnits)
    def buy_human_skills_wrapper(self, skill_name):
        self.human_skills, self.timeUnits = buy_human_skill(self.human_skills, self.timeUnits, skill_name)
    def buy_blue_cable_wrapper(self):
        print("blue cable clicked ", end='')
        if randint(1, 2) == 1:
            print("X2")
            self.blue_cable_x2_timer = self.framerate * 60 * 1 + self.framerate * self.boost_duration
            # print("base duration :", self.framerate * 60 * 1)
            # print("additional timer :", self.framerate * 60 * self.boost_duration)
            # print("blue cable timer :", self.blue_cable_x2_timer)
            
            
            
            self.blue_cable_timer = randint(3, 15)
            
            self.is_blue_cable_cut = False
            
            if self.tps_boost_from_cable == 5 or self.tps_boost_from_cable == 0:
                self.tps_boost_from_cable += 2
        else:
            print("X5")
            self.blue_cable_x5_timer = self.framerate * 60 * 1 + self.framerate * self.boost_duration
            # print("base duration :", self.framerate * 60 * 1)
            # print("additional timer :", self.framerate * 60 * self.boost_duration)
            # print("blue cable timer :", self.blue_cable_x2_timer)
            
            
            
            self.blue_cable_timer = randint(3, 15)
            
            self.is_blue_cable_cut = False
            
            if self.tps_boost_from_cable == 2 or self.tps_boost_from_cable == 0:
                self.tps_boost_from_cable += 5
    def buy_red_cable_wrapper(self):
        self.red_cable_timer = randint(3, 15)
        self.is_red_cable_cut = False
        self.red_cable_tps_reduction = 0
            
      
      
    def load_data(self):
        (
            self.timeUnits,
            self.tps,
            self.timeline,
            self.clicker_amount,
            self.bought_buildings,
            self.max_timeUnits,
            self.bought_upgrades,
            self.human_skills,
            self.last_saved_time,
        ) = get_data(self.appdata_path)
        
        self.max_timeUnits = int(float(self.max_timeUnits))
    def save_data(self):
        save_data(
            self.appdata_path,
            self.timeUnits,
            self.tps,
            self.timeline,
            self.clicker_amount,
            self.bought_buildings,
            self.max_timeUnits,
            self.bought_upgrades,
            self.human_skills
        )
             
    def give_timeUnits_from_afk(self):
        if self.last_saved_time:
            elapsed_time = (datetime.now() - datetime.strptime(self.last_saved_time, " %Y-%m-%d %H:%M:%S")).total_seconds()
            self.timeUnits += self.tps * (elapsed_time)  # Add production for the elapsed time
            self.LOGGER.INFO(
                f"Elapsed time: {round(elapsed_time)} seconds, added {self.tps * (elapsed_time )} timeUnits, tps: {self.tps}"
            )
        
        
    def check_available_buildings(self):
        for i in range(len(buildings)):
            build = buildings[i]
            
            match self.era:
                case 1:
                    if i < 4:
                        can_be_bought = True
                    else:
                        can_be_bought = False
                case 2:
                    if i < 8:
                        can_be_bought = True
                    else:
                        can_be_bought = False
                case 3:
                    if i < 12:
                        can_be_bought = True
                    else:
                        can_be_bought = False
                case 4:
                    if i < 16:
                        can_be_bought = True
                    else:
                        can_be_bought = False
                case 5:
                    if i < 20:
                        can_be_bought = True
                    else:
                        can_be_bought = False
                case 6:
                    can_be_bought = True
                    
            
            previous_build = buildings[i - 1] if i > 0 else None
            if can_be_bought:
                if build["name"] in self.bought_buildings["short_list"] or i == 0:
                    if not build in self.available_buildings:
                        self.available_buildings.append(build)
                elif previous_build["name"] in self.bought_buildings["short_list"] and (
                    next(
                        (
                            b["amount"]
                            for b in self.bought_buildings["long_list"]
                            if b["name"] == previous_build["name"]
                        ),
                        None,
                    )
                    >= 1
                ):
                    if not build in self.available_buildings:
                        self.available_buildings.append(build)

    def check_available_upgrades(self):
        for i in range(len(UPGRADES)):
            upgrade = UPGRADES[i]
            build_amount = next(
                (
                    b["amount"]
                    for b in self.bought_buildings["long_list"]
                    if b["name"] == upgrade["building_name"]
                ),
                None,
            )

            if not build_amount is None:

                max_bought_level = next(
                    (
                        u["level"]
                        for u in self.bought_upgrades["long_list"]
                        if u["name"] == upgrade["name"]
                    ),
                    0,
                )

                if build_amount >= treshold[0]:

                    if max_bought_level == 0:
                        if not upgrade in self.available_upgrades:
                            self.available_upgrades.append(upgrade)

                    elif max_bought_level != 0:
                        if not upgrade in self.available_upgrades:
                            self.available_upgrades.append(upgrade)
                            
        if next((u for u in self.available_upgrades if u["name"] == UPGRADES[0]["name"]), None) is not None and next((u for u in self.available_upgrades if u["name"] == UPGRADES[1]["name"]), None) is not None:
            self.available_upgrades.append(TIMELINE_UPGRADE)
    
    def update(self):
        # self.timeUnits = 50000**10
        
        self.current_frame: int = (self.current_frame + 1) % self.framerate
        
        self.timeUnits += self.tps / self.framerate
        self.max_timeUnits = max(self.max_timeUnits, self.timeUnits)
        
        self.tps: int = 0


        self.available_upgrades = []
        self.buildings_buttons: list = []
        self.upgrades_buttons: list = []
        self.human_skills_buttons: list = []
        
    def exit(self):
        self.save_data()
        self.running = False    
    def reset(self, message="The game has been reseted."):
        save_data(self.appdata_path)
        self.bought_buildings = {"short_list": [], "long_list": []}
        show_message(message)
        self.load_data()
    
    def check_autosave(self):
        self.save_count += 1
        # print(count)
        if self.save_count == self.framerate * 10:
            self.save_data()
            self.save_count = 0
            self.LOGGER.INFO("Data saved")

    def handle_human_skills(self):
        # self.human_skills["intelligence"] = 0
        self.clicker_amount = 1 + (math.log10(1 + 9 * (self.human_skills["strength"] / 100)) * self.tps)
        
        self.price_reduction = 1 - ( (self.human_skills["intelligence"]/2)/100 )
        
        self.boost_duration = 17.4 * self.human_skills["agility"]
    
    def check_cables(self):
        self.blue_cable_count += 1
        self.red_cable_count += 1
        
        
        
        if self.is_red_cable_cut:
            self.red_cable_count = 0
            if self.red_cable_tps_reduction < 100:
                self.red_cable_tps_reduction += 0.1
                self.red_cable_tps_reduction = round(self.red_cable_tps_reduction, 1)
        if self.is_blue_cable_cut:
            self.blue_cable_count = 0
            
        
        if self.red_cable_count == self.framerate * 60 * self.red_cable_timer:
        # if self.red_cable_count == self.framerate * 3:
            self.is_red_cable_cut = True
            
            self.red_cable_count = 0
            
            
        
        if self.blue_cable_count == self.framerate * 60 * self.blue_cable_timer:
        # if self.blue_cable_count == self.framerate * 3:
            self.is_blue_cable_cut = True
            
            self.blue_cable_count = 0
            
        if self.blue_cable_x2_timer != 0:
            self.blue_cable_x2_timer -= 1
            
            if self.blue_cable_x2_timer == 0:
                self.tps_boost_from_cable -= 2
            
        if self.blue_cable_x5_timer != 0:
            self.blue_cable_x5_timer -= 1
            
            if self.blue_cable_x5_timer == 0:
                self.tps_boost_from_cable -= 5
            
                
    def check_era(self):
        if self.timeline >=   2500:
            self.era = 6
        elif self.timeline >=   1789:
            self.era = 5
        elif self.timeline >=   1492:
            self.era = 4
        elif self.timeline >=   476:
            self.era = 3
        elif self.timeline >=   0:
            self.era = 2
        else:
            self.era = 1
    
    
    def add_cable_boost(self):
        if self.tps_boost_from_cable != 0:
            self.tps *= self.tps_boost_from_cable
        if self.red_cable_tps_reduction != 0:
            self.tps *= (1 - self.red_cable_tps_reduction / 100)
            