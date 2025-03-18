import ctypes
from json import load
import os
from re import S
import time
from turtle import width
import math

from engine.Buttons import Button
from config import *
import pygame as pg
from data.data import *

from data.buildings import buildings
from data.upgrade import TIMELINE_UPGRADE, UPGRADES, treshold
from engine.utils import adapt_size_width as adaptw, adapt_size_height as adapth, can_buy_buildings, can_buy_timeline, can_buy_upgrade, format_time_no_convertion, format_timeUnits, get_clock_font, get_number_font, get_text_font, get_timeline_font, load_image, can_buy_human_skill

class PaintStrategy:
    def __init__(self, engine, screen, src_dir):
        """
        Initialize the PaintStrategy object.

        :param Engine engine: The game engine.
        :param pygame.Surface screen: The pygame screen to draw on.
        :param str src_dir: The directory containing the images and fonts.
        :raises AssertionError: If the src_dir does not exist.
        """
        self.engine = engine
        self.screen = screen
        self.src_dir = src_dir
        assert os.path.exists(self.src_dir), f"Folder {self.src_dir} does not exist"
        
        self.width = self.height = "Null"
        
        self.can_scroll = True
        
        self.is_building_clickable = False
        self.is_upgrading_clickable = False
        
        self.scroll_speed = 20
        
        self.scroll_value = 0
        
        self.is_init = False
        
        self.is_maximized = True
        
        
    
    def update_elements(self):
        """
        Update the screen elements' size and position according to the window's size.
        """
        
        width, height = pg.display.get_surface().get_size()
        
        if self.engine.reset_scroll:
            self.scroll_value = 0
            self.engine.reset_scroll = False
        
        # Screen components
        self.timeUnits_text: pg.Surface = get_number_font(65, height).render(f"{format_timeUnits(self.engine.timeUnits, 0)}", True, RED_OCHRE)
        self.timeUnits_text_logo: pg.Surface = load_image(f"{self.src_dir}/img/timeUnits.png", width, height)
        
        self.tps_text: pg.Surface = get_number_font(50, height).render(f"{format_timeUnits(self.engine.tps, 0)}", True, RED_OCHRE)
        self.tps_text_logo: pg.Surface = load_image(f"{self.src_dir}/img/tps.png", width, height)
        
        match self.engine.era:
            case 1:
                era_name = "Prehistory"
            case 2:
                era_name = "Antiquity"
            case 3:
                era_name = "Middle Ages"
            case 4:
                era_name = "Modern Times"
            case 5:
                era_name = "Contemporary"
            case 6:
                era_name = "Future"
            
        self.era_text: pg.surface = get_timeline_font(35, height).render(f"{era_name}", True, YELLOW_GREEN)
        
        if self.engine.timeline < 0:
            timeline = "Null"
            size = 100
        elif self.engine.timeline >= 2500:
            timeline = "Out Of Time"
            size = 50
        else:
            timeline = format_time_no_convertion(self.engine.timeline)
            size = 100
        self.timeline_text: pg.Surface = get_timeline_font(size, height).render(f"{timeline}", True, YELLOW_GREEN)
        
        self.blue_cable_image: pg.surface = load_image(f"{self.src_dir}/img/blue_cable_on.png", width, height)
        if self.engine.is_blue_cable_cut:
            self.blue_cable_image = load_image(f"{self.src_dir}/img/blue_cable_off.png", width, height)
            self.blue_cable_button: Button = Button(
                rect=(adaptw(1285, width),adapth(935, height),adaptw(600, width),adapth(75, height)),
                screen_size=(width, height),
                background=BLUE,
                transparent=True,
                command=lambda: self.engine.buy_blue_cable_wrapper(),
                border_radius=0,
            )
            
        self.red_cable_image: pg.surface = load_image(f"{self.src_dir}/img/red_cable_on.png", width, height)
        if self.engine.is_red_cable_cut:
            self.red_cable_image = load_image(f"{self.src_dir}/img/red_cable_off.png", width, height)
            self.red_cable_button: Button = Button(
                rect=(adaptw(1285, width),adapth(860, height),adaptw(600, width),adapth(75, height)),
                screen_size=(width, height),
                background=BLUE,
                transparent=True,
                command=lambda: self.engine.buy_red_cable_wrapper(),
                border_radius=0,
            )
            
            
        
        if self.has_window_been_resized():
            self.clicker_button: Button = Button(
                rect=(adaptw(705, width),adapth(304, height),adaptw(403, width),adapth(400, height)),
                screen_size=(width, height),
                background=f"{self.src_dir}/img/hourglass.png",
                command=lambda: self.engine.increment_timeUnits(self.engine.clicker_amount),
                border_radius=250,
                image_scale=0.4,
                image_rotation=10,
                bump_on_click=True,
                circle_on_click=True,
                identifier="clicker",
            )
            
            # Screen images
            self.timeline_image: pg.surface = load_image(f"{self.src_dir}/img/timeline.png", width, height)
            
            self.upgrade_fond_image: pg.surface = load_image(f"{self.src_dir}/img/upgrade_fond.png", width, height)
            self.upgrade_bord_image: pg.surface = load_image(f"{self.src_dir}/img/upgrade_bord.png", width, height)
            
            self.temporal_matrix_image: pg.surface = load_image(f"{self.src_dir}/img/temporal_matrix.png", width, height)
            
            self.human_skill_and_boost: pg.surface = load_image(f"{self.src_dir}/img/human_skill+boost.png", width, height)
            
            self.shop_fond_image: pg.surface = load_image(f"{self.src_dir}/img/shop_fond.png", width, height)
            self.shop_bord_image: pg.surface = load_image(f"{self.src_dir}/img/shop_bord.png", width, height)
            
            self.red_cable_image: pg.surface = load_image(f"{self.src_dir}/img/red_cable_on.png", width, height)
            
            
            
            
            
            self.building_scroll_area_rect = pg.Rect(adaptw(1525, width),adapth(70, height),adaptw(300, width),adapth(750, height),)
            
            self.upgrade_scroll_area_rect = pg.Rect(adaptw(67.5, width),adapth(267.5, height),adaptw(460, width),adapth(750, height),)
            
            
        self.width = width
        self.height = height
    
    
    def has_window_been_resized(self):
        """
        Check if the window has been resized since the last frame.

        :return bool: If the window size has changed since the last frame.
        """
        return self.width != pg.display.get_surface().get_width()or self.height != pg.display.get_surface().get_height()
    
    
    def create_buildings_buttons(self):
        """
        Create the buttons for the buildings available to buy.
        """

        for i in range(len(self.engine.available_buildings)):
            build = self.engine.available_buildings[i]

            build_name = build["name"]
            build_tps = build["tps_boost"]
            build_amount = next(
                (
                    b["amount"]
                    for b in self.engine.bought_buildings["long_list"]
                    if b["name"] == build["name"]
                ),
                0,
            )
            build_augment = next(
                (
                    b["upgrade_boost"]
                    for b in self.engine.bought_buildings["long_list"]
                    if b["name"] == build["name"]
                ),
                1,
            )
            self.engine.tps += build_tps * build_amount * build_augment

            infos = f"The building '{build_name}' has {build_amount} instances,\nproducing {format_timeUnits(build_tps * build_amount * build_augment * self.engine.prestige_boost)} time units per second,\nwith a boost multiplier of: \n- {build_augment}x from upgrade \n- {self.engine.era_boost}x from era \n- +{self.engine.prestige}% from prestige.\nEach building is producing {format_timeUnits(build_tps * build_augment*self.engine.prestige_boost)} time units per second."

            self.engine.buildings_buttons.append(
                Button(
                    (
                        adaptw(1525, self.width),
                        adapth(85, self.height)
                        + (adapth(105, self.height) * i)
                        + adapth((self.scroll_value * 1), self.height),
                        adaptw(300, self.width),
                        adapth(45, self.width),
                    ),
                    (self.width, self.height),
                    background=BLUE,
                    transparent=True,
                    border_radius=20,
                    command=lambda b=build_name: self.engine.buy_building_wrapper(b),
                    identifier=build["name"],
                    infos=infos,
                )
            )


    def create_upgrades_buttons(self):
        """
        Create and position upgrade buttons for each available upgrade.
        """

        y = 180
        x = 82.5
        for i in range(len(self.engine.available_upgrades)):
            upgrade = self.engine.available_upgrades[i]
            upgrade_name = upgrade["name"]
            upgrade_level = next((u["level"] for u in self.engine.bought_upgrades["long_list"] if u["name"] == upgrade["name"]), 0)
            
            if upgrade["effect_type"] == "building":
                upgrade_effect_value = upgrade["effect_value"]
                upgrade_building_name = upgrade["building_name"]
                if not upgrade_level == len(treshold):
                    xth_build_price = next((b["cost"](treshold[upgrade_level]) for b in buildings if b["name"] == upgrade["building_name"]), 0)
                else:
                    xth_build_price = "FULL"

                if upgrade is None:
                    cost = 0
                else:
                    cost = xth_build_price * 3

                infos = f"The upgrade '{upgrade_name}' costs {format_timeUnits(cost)} time units, \nis affecting the building '{upgrade_building_name}'. \nCurrent level: {upgrade_level} \n Effect value: {upgrade_effect_value}"
                cmd = lambda b=upgrade_name: self.engine.buy_upgrade_wrapper(b)
            elif upgrade["effect_type"] == "timeline":
                cost = upgrade["cost"](self.engine.timeline)
                if self.engine.era == 1:
                    cost = TIMELINE_UPGRADE_PRICE
                if self.engine.timeline >= 2500:
                    cmd = lambda: self.engine.buy_reset_wrapper(next((b["amount"] for b in self.engine.bought_buildings["long_list"] if b["name"].lower() == "Time Machine".lower()), 0))
                    infos = f"The upgrade 'Timeline' will prestige your game. \nYour time units, buildings, upgrades, timeline and human skills will be reset. \nYou will gain prestige based on the amount of  Time Machines you have. \n1 prestige = 1% production boost."
                else:
                    cmd = lambda: self.engine.buy_timeline_wrapper()
                    infos = f"The special upgrade '{upgrade_name}' costs {format_timeUnits(cost)} time units. \nIt adds 1 to the timeline."

            if (i - 4) % 4 == 0:
                x = 82.5
                y += 117.5
            else:
                x += 112.5
                
            
            

            self.engine.upgrades_buttons.append(
                Button(
                    (adaptw(x, self.width), adapth(y, self.height), adaptw(90, self.width), adapth(90, self.height)),
                    (self.width, self.height),
                    background=BLUE,
                    transparent=True,
                    border_radius=250,
                    command=cmd,
                    identifier=upgrade["name"],
                    infos=infos,
                )
            )


    def create_human_skills_buttons(self):
        """
        Create and position human skills buttons for each available human skill.
        """
        self.engine.human_skills_buttons.append(
            Button(
                rect=(adaptw(1280.5, self.width), adapth(748.5, self.height), adaptw(27.5, self.width), adapth(27.5, self.height)),
                screen_size=(self.width, self.height),
                background=RED_OCHRE,
                command=lambda :self.engine.buy_human_skills_wrapper("strength"),
                border_radius=250,
                identifier="strength",
                infos=f"The Strength skill allow you to produce more Time Units per click. \nCurrent Time Units/click is {format_timeUnits(self.engine.clicker_amount)} TU. \nthe cost of the next level is {format_timeUnits(200 * (2**self.engine.human_skills['strength']))} TU."
            )
        )
        self.engine.human_skills_buttons.append(
            Button(
                rect=(adaptw(1325, self.width), adapth(748.5, self.height), adaptw(27.5, self.width), adapth(27.5, self.height)),
                screen_size=(self.width, self.height),
                background=CABLE_BLUE,
                command=lambda :self.engine.buy_human_skills_wrapper("agility"),
                border_radius=250,
                identifier="agility",
                infos=f"The Agility skill increase the duration of the boost from the blue cable. \nCurrent duration is {time.strftime('%M:%S', time.gmtime(60 + self.engine.boost_duration))}. \nthe cost of the next level is {format_timeUnits(200 * (2**self.engine.human_skills['agility']))} TU."
            )
        )
        self.engine.human_skills_buttons.append(
            Button(
                rect=(adaptw(1370.5, self.width), adapth(748.5, self.height), adaptw(27.5, self.width), adapth(27.5, self.height)),
                screen_size=(self.width, self.height),
                background=YELLOW,
                command=lambda :self.engine.buy_human_skills_wrapper("intelligence"),
                border_radius=250,
                identifier="intelligence",
                infos=f"The Intelligence skill decrease the price of buildings and upgrades. \nCurrent reduction is {(self.engine.human_skills['intelligence']/2)}%. \nthe cost of the next level is {format_timeUnits(200 * (2**self.engine.human_skills['intelligence']))} TU."
            )
        )


    def handle_event(self):
        """
        Handle game events to control the game.
        """
        
        keys = pygame.key.get_pressed()
        # print(keys[pg.K_LCTRL] in keys, keys[pg.K_RCTRL] in keys, keys[K_F1] in keys)
        for event in pg.event.get():
            if event.type == pg.QUIT or (keys[pg.K_ESCAPE]):
                self.engine.exit()
            elif keys[pg.K_F7]:
                if self.engine.LOGGER.get_level() == 4:
                    self.engine.LOGGER.INFO("Setting log level to WARNING")
                    self.engine.LOGGER.set_level(3)
                else:
                    self.engine.LOGGER.INFO("Setting log level to DEBUG")
                    self.engine.LOGGER.set_level(4)
            elif event.type == pg.KEYDOWN and event.key == pg.K_F11:
                # if self.is_maximized:
                #     self.engine.window.restore()
                #     self.is_maximized = False
                # else:
                #     self.engine.window.maximize()
                #     self.is_maximized = True
                pg.display.toggle_fullscreen()

            elif (keys[pg.K_LCTRL] or keys[pg.K_RCTRL]) and keys[pg.K_F1]:
                self.engine.reset()

            elif event.type == pg.MOUSEWHEEL and len(self.engine.available_buildings) > 6:
                self.engine.LOGGER.DEBUG(f"scroll offset: {event.y}")
                if self.can_scroll or event.y > 0:
                    self.scroll_value += event.y * self.scroll_speed
                    self.scroll_value = min(self.scroll_value, 0)


            if event.type == pg.MOUSEMOTION:
                self.clicker_button.get_event(event)

                self.is_building_clickable = False
                for build_button in self.engine.buildings_buttons:
                    rel_x, rel_y = (
                        event.pos[0] - self.building_scroll_area_rect.x,
                        event.pos[1] - self.building_scroll_area_rect.y,
                    )
                    if (
                        0 <= rel_x < self.building_scroll_area_rect.width
                        and 0 <= rel_y < self.building_scroll_area_rect.height
                    ):
                        self.is_building_clickable = True

                self.is_upgrading_clickable = False
                for upgrade_button in self.engine.upgrades_buttons:
                    rel_x, rel_y = (
                        event.pos[0] - self.upgrade_scroll_area_rect.x,
                        event.pos[1] - self.upgrade_scroll_area_rect.y,
                    )
                    if (
                        0 <= rel_x < self.upgrade_scroll_area_rect.width
                        and 0 <= rel_y < self.upgrade_scroll_area_rect.height
                    ):
                        self.is_upgrading_clickable = True

            for build_button in self.engine.buildings_buttons:
                build_button.get_event(event)

            for upgrade_button in self.engine.upgrades_buttons:
                upgrade_button.get_event(event)

            for human_skill_button in self.engine.human_skills_buttons:
                human_skill_button.get_event(event)
                
            if self.engine.is_blue_cable_cut:
                self.blue_cable_button.get_event(event)
                
            if self.engine.is_red_cable_cut:
                self.red_cable_button.get_event(event)

            self.clicker_button.get_event(event)


    def check_mouse_hover(self):
        """
        Check if the mouse is hovering over any interactive elements.
        """
        pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)
        
        mouse_pos = pg.mouse.get_pos()
        if self.building_scroll_area_rect.collidepoint(mouse_pos):
            for build_button in self.engine.buildings_buttons:
                build_button.update_hover_state(mouse_pos)

        for upgrade_button in self.engine.upgrades_buttons:
            upgrade_button.update_hover_state(mouse_pos)

        for human_skill_button in self.engine.human_skills_buttons:
            human_skill_button.update_hover_state(mouse_pos)

        if self.engine.is_blue_cable_cut:
            self.blue_cable_button.update_hover_state(mouse_pos)
            
        if self.engine.is_red_cable_cut:
                self.red_cable_button.update_hover_state(mouse_pos)


    def display_back_images(self):
        """
        Display background images on the screen.
        """
        self.screen.blit(self.shop_fond_image, (adaptw(1475, self.width), adapth(45, self.height)))
        self.screen.blit(self.upgrade_fond_image, (adaptw(45, self.width), adapth(245, self.height)))
    
        
    def display_buildings(self):
        """
        Display the buildings on the screen.
        """
        match self.engine.era:
            case 1:
                base = f"{self.src_dir}/img/buildings/base_1.png"
                price_color = BROWN
                price_color_dark = DARK_BROWN
            case 2:
                base = f"{self.src_dir}/img/buildings/base_2.png"
                price_color = (119, 224, 219)
                price_color_dark = (50, 86, 82)
            case 3:
                base = f"{self.src_dir}/img/buildings/base_3.png"
                price_color = (255, 217, 149)
                price_color_dark = (94, 78, 54)
            case 4:
                base = f"{self.src_dir}/img/buildings/base_4.png"
                price_color = (10, 71, 0)
                price_color_dark = (4, 10, 0)
            case 5:
                base = f"{self.src_dir}/img/buildings/base_5.png"
                price_color = (0, 233, 236)
                price_color_dark = (0, 64, 64)
            case 6:
                base = f"{self.src_dir}/img/buildings/base_6.png"
                price_color = (0, 81, 255)
                price_color_dark = (7, 38, 63)
                
        for i in range(len(self.engine.buildings_buttons)):
            build_button = self.engine.buildings_buttons[i]
            build = next((b for b in self.engine.bought_buildings["long_list"] if b["name"] == build_button.identifier),None)
            if build is None:
                amount = 0
            else:
                amount = build["amount"]

            cost = next((b["cost"](amount) for b in buildings if b["name"] == build_button.identifier),None,) * self.engine.price_reduction

            building_image = load_image(f"{self.src_dir}/img/buildings/{build_button.identifier.lower().replace(' ', '_')}.png",self.width,self.height,)
            base_image = load_image(base, self.width, self.height)

            # print(f"scroll_y: {scroll_y}({abs(adapth((scroll_y * 1), h))})")
            button_rect = build_button.rect.move(0, build_button.rect.height + adapth(7.5, self.height))
            building_rect = building_image.get_rect(
                topleft=(adaptw(1525, self.width), adapth(85 + 105 * i, self.height))
            ).move(0, adapth((self.scroll_value * 1), self.height))
            base_rect = base_image.get_rect(
                topleft=(adaptw(1525, self.width), adapth(85 + 105 * i, self.height))
            ).move(0, adapth((self.scroll_value * 1), self.height))
            # build_button.rect = button_rect
            if not can_buy_buildings(
                self.engine.bought_buildings, build_button.identifier, 1, self.engine.timeUnits, self.engine.price_reduction
            ):
                base_image.fill((100, 100, 100), special_flags=pg.BLEND_MULT)
                self.screen.blit(base_image, base_rect.topleft)

                building_image.fill((100, 100, 100), special_flags=pg.BLEND_MULT)
                self.screen.blit(building_image, building_rect.topleft)

                self.screen.blit(
                    get_text_font(25, self.height).render(f"{format_timeUnits(round(cost))}", True, price_color_dark),
                    (adaptw(1592, self.width),adapth(132 + 105 * i, self.height)+ adapth((self.scroll_value * 1), self.height),)
                )
                self.screen.blit(
                    get_text_font(19, self.height).render(f"{format_time_no_convertion(amount)}", True, GREY),
                    (adaptw(1780, self.width),adapth(132.5 + 105 * i, self.height)+ adapth((self.scroll_value * 1), self.height),)
                )

                build_button.render(self.screen, True, self.width, self.height)
            else:
                self.screen.blit(base_image, base_rect.topleft)

                self.screen.blit(building_image, building_rect.topleft)

                self.screen.blit(
                    get_text_font(25, self.height).render(f"{format_timeUnits(round(cost))}", True, price_color),
                    (adaptw(1592, self.width),adapth(132 + 105 * i, self.height)+ adapth((self.scroll_value * 1), self.height),)
                )
                self.screen.blit(
                    get_text_font(19, self.height).render(f"{format_time_no_convertion(amount)}", True, WHITE),
                    (adaptw(1780, self.width),adapth(132.5 + 105 * i, self.height)+ adapth((self.scroll_value * 1), self.height),)
                )

                build_button.render(self.screen, w=self.width, h=self.height)
            if self.building_scroll_area_rect.colliderect(button_rect) and button_rect.top >= self.building_scroll_area_rect.top + adapth(50, self.height):
                if i == len(self.engine.buildings_buttons) - 1:
                    if self.can_scroll:
                        self.can_scroll = False
                else:
                    if not self.can_scroll:
                        self.can_scroll = True


        arrow_color = (255, 255, 255)
        arrow_size = 20

        if self.scroll_value < 0:
            pg.draw.polygon(
                self.screen,
                arrow_color,
                [
                    (self.building_scroll_area_rect.centerx, self.building_scroll_area_rect.top + adapth(10, self.height)),
                    (self.building_scroll_area_rect.centerx - arrow_size, self.building_scroll_area_rect.top + adapth(30, self.height)),
                    (self.building_scroll_area_rect.centerx + arrow_size, self.building_scroll_area_rect.top + adapth(30, self.height)),
                ]
            )

        if self.can_scroll:
            pg.draw.polygon(
                self.screen,
                arrow_color,
                [
                    (self.building_scroll_area_rect.centerx, self.building_scroll_area_rect.bottom - adapth(10, self.height)),
                    (self.building_scroll_area_rect.centerx - arrow_size, self.building_scroll_area_rect.bottom - adapth(30, self.height)),
                    (self.building_scroll_area_rect.centerx + arrow_size, self.building_scroll_area_rect.bottom - adapth(30, self.height)),
                ]
            )

    def display_upgrades(self):
        """
        Display the upgrades on the screen.
        """
        # LOGGER.DEBUG([b.identifier for b in self.engine.upgrades_buttons])
        y = 210
        x = 127.5
        for i in range(len(self.engine.upgrades_buttons)):
            upgrade_button = self.engine.upgrades_buttons[i]
            if upgrade_button.identifier == "Time":
                
                
                if (i - 4) % 4 == 0:
                    x = 127.5
                    y += 117.5
                else:
                    x += 112.5
                
                cost = TIMELINE_UPGRADE["cost"](self.engine.timeline)
                
                
                if self.engine.timeline >= 2500 and next((b["amount"] for b in self.engine.bought_buildings["long_list"] if b["name"] == "Time Machine"), 0) > 0:
                    is_prestige_button = True
                else:
                    is_prestige_button = False
                
                upgrade_image = load_image(f"{self.src_dir}/img/upgrades/time.png", self.width, self.height, scale=0.9)
                if self.engine.era == 1 or is_prestige_button:
                    cost = TIMELINE_UPGRADE_PRICE
                    upgrade_image = load_image(f"{self.src_dir}/img/upgrades/timeline_unlock_image.png", self.width, self.height)
                upgrade_rect = upgrade_image.get_rect(center=(adaptw(x, self.width), adapth(y, self.height)))
                
                level_image = load_image(f"{self.src_dir}/img/upgrades/base_timeline.png", self.width, self.height, scale=0.9)
                level_rect = level_image.get_rect(center=upgrade_rect.center).move(adaptw(0, self.width), adapth(15, self.height))
                
                
                
                
                
                if can_buy_timeline(self.engine.timeline, self.engine.timeUnits, self.engine.era):
                
                    self.screen.blit(upgrade_image, upgrade_rect.topleft)

                    self.screen.blit(level_image, level_rect.topleft)
                    
                    if not is_prestige_button:
                        self.screen.blit(
                            get_text_font(17.5, self.height).render(f"{format_timeUnits(round(cost))}", True, WHITE),
                            get_text_font(17.5, self.height)
                            .render(f"{format_timeUnits(round(cost))}", True, GREY)
                            .get_rect(center=(adaptw(x, self.width),adapth(y + 32.5, self.height),)),
                        )

                    upgrade_button.render(self.screen, w=self.width, h=self.height)
                else:
                    upgrade_image.fill((100, 100, 100), special_flags=pg.BLEND_MULT)
                    self.screen.blit(upgrade_image, upgrade_rect.topleft)

                    level_image.fill((100, 100, 100), special_flags=pg.BLEND_MULT)
                    self.screen.blit(level_image, level_rect.topleft)
                    
                    self.screen.blit(
                        get_text_font(17.5, self.height).render(f"{format_timeUnits(round(cost))}", True, GREY),
                        get_text_font(17.5, self.height)
                        .render(f"{format_timeUnits(round(cost))}", True, GREY)
                        .get_rect(center=(adaptw(x, self.width),adapth(y + 32.5, self.height),)),
                    )

                    upgrade_button.render(self.screen, w=self.width, h=self.height, darker=True)
                    
            else:
                upgrade = next((b for b in UPGRADES if b["name"] == upgrade_button.identifier), None)
                upgrade_level = next((u["level"]for u in self.engine.bought_upgrades["long_list"]if u["name"] == upgrade_button.identifier),0,)
                max_bought_level = next((u["level"]for u in self.engine.bought_upgrades["long_list"]if u["name"] == upgrade["name"]),0)
                if not upgrade_level == len(treshold):
                    xth_build_price = next((b["cost"](treshold[max_bought_level])for b in buildings if b["name"] == upgrade["building_name"]),0,)
                else:
                    xth_build_price = "FULL"

                if upgrade is None:
                    cost = 0
                else:
                    cost = xth_build_price * 3 * self.engine.price_reduction

                if upgrade_level == len(treshold):
                    cost = "FULL"


                upgrade_image = load_image(f"{self.src_dir}/img/upgrades/{upgrade_button.identifier.lower().replace(' ', '_')}.png",self.width,self.height,scale=0.75,)
                level_image = load_image(f"{self.src_dir}/img/upgrades/niv{upgrade_level}.png", self.width, self.height, 0.9)
                
                if (i - 4) % 4 == 0:
                    x = 127.5
                    y += 117.5
                else:
                    x += 112.5


                upgrade_rect = upgrade_image.get_rect(center=(adaptw(x, self.width), adapth(y, self.height)))

                level_rect = level_image.get_rect(center=upgrade_rect.center).move(adaptw(0, self.width), adapth(15, self.height))

                if not can_buy_upgrade(self.engine.bought_upgrades, upgrade_button.identifier, self.engine.timeUnits, self.engine.bought_buildings, self.engine.price_reduction):
                    upgrade_image.fill((100, 100, 100), special_flags=pg.BLEND_MULT)
                    self.screen.blit(upgrade_image, upgrade_rect.topleft)

                    level_image.fill((100, 100, 100), special_flags=pg.BLEND_MULT)
                    self.screen.blit(level_image, level_rect.topleft)

                    self.screen.blit(
                        get_text_font(17.5, self.height).render(f"{format_timeUnits(round(cost))}", True, GREY),
                        get_text_font(17.5, self.height)
                        .render(f"{format_timeUnits(round(cost))}", True, GREY)
                        .get_rect(center=(adaptw(x, self.width), adapth(y + 32.5, self.height))),)

                    upgrade_button.render(self.screen, True, self.width, self.height)
                else:
                    self.screen.blit(upgrade_image, upgrade_rect.topleft)

                    # screen.blit(get_text_font(25, self.height).render(f"{format_timeUnits(round(cost))}", True, BROWN), (adaptw(1592, w), adapth(132 + 104.5 * i, self.height) + adapth((scroll_y_bis * 1), self.height)))

                    self.screen.blit(level_image, level_rect.topleft)
                    if not upgrade_level == len(treshold):
                        self.screen.blit(
                            get_text_font(17.5, self.height).render(f"{format_timeUnits(round(cost))}", True, WHITE),
                            get_text_font(17.5, self.height)
                            .render(f"{format_timeUnits(round(cost))}", True, WHITE)
                            .get_rect(center=(adaptw(x, self.width),adapth(y + 32.5, self.height),)),
                        )
                    else:
                        self.screen.blit(
                            get_text_font(17.5, self.height).render(f"{cost}", True, WHITE),
                            get_text_font(17.5, self.height)
                            .render(f"{cost}", True, WHITE)
                            .get_rect(center=(adaptw(x, self.width),adapth(y + 32.5, self.height),)),
                        )

                    upgrade_button.render(self.screen, w=self.width, h=self.height)


    def display_human_skills(self):
        """
        Display the human skills on the screen.
        """
        strength_offset = (self.engine.human_skills["strength"] / 100) * 527
        pg.draw.rect(self.screen, RED_OCHRE, (adaptw(1285.5, self.width), adapth(734.5-strength_offset, self.height), adaptw(15, self.width), adapth(strength_offset, self.height)), border_radius=60)
        self.screen.blit(
            get_number_font(20, self.height).render(f"{self.engine.human_skills['strength']}", True, RED_OCHRE),
            get_number_font(20, self.height).render(f"{self.engine.human_skills['strength']}", True, RED_OCHRE).get_rect(center=(adaptw(1292.5, self.width), adapth(798.5, self.height))),
        )
        
        agility_offset = (self.engine.human_skills["agility"] / 100) * 527
        pg.draw.rect(self.screen, CABLE_BLUE, (adaptw(1331, self.width), adapth(734.5-agility_offset, self.height), adaptw(15, self.width), adapth(agility_offset, self.height)), border_radius=60)
        self.screen.blit(
            get_number_font(20, self.height).render(f"{self.engine.human_skills['agility']}", True, CABLE_BLUE),
            get_number_font(20, self.height).render(f"{self.engine.human_skills['agility']}", True, CABLE_BLUE).get_rect(center=(adaptw(1338, self.width), adapth(798.5, self.height))),
        )

        intelligence_offset = (self.engine.human_skills["intelligence"] / 100) * 527
        pg.draw.rect(self.screen, YELLOW, (adaptw(1375.5, self.width), adapth(734.5-intelligence_offset, self.height), adaptw(15, self.width), adapth(intelligence_offset, self.height)), border_radius=60)
        self.screen.blit(
            get_number_font(20, self.height).render(f"{self.engine.human_skills['intelligence']}", True, YELLOW),
            get_number_font(20, self.height).render(f"{self.engine.human_skills['intelligence']}", True, YELLOW).get_rect(center=(adaptw(1385, self.width), adapth(798.5, self.height))),
        )

        for button in self.engine.human_skills_buttons:
            if can_buy_human_skill(self.engine.human_skills, self.engine.timeUnits, button.identifier):
                button.render(self.screen)
            else:
                button.render(self.screen, darker=True)
            

    def display_front_elements(self):
        """
        Display the front elements on the screen.
        """
        self.screen.blit(load_image(f"{self.src_dir}/img/background.png", self.width, self.height), (0, 0))
        self.screen.blit(self.timeline_image, (adaptw(45, self.width), adapth(45, self.height)))
        self.screen.blit(
            self.upgrade_bord_image, (adaptw(45, self.width), adapth(245, self.height))
        )
        self.screen.blit(
            self.temporal_matrix_image, (adaptw(605, self.width), adapth(45, self.height))
        )
        self.screen.blit(
            self.human_skill_and_boost, (adaptw(1265, self.width), adapth(45, self.height))
        )
        self.screen.blit(
            self.shop_bord_image, (adaptw(1475, self.width), adapth(45, self.height))
        )
        self.screen.blit(
            self.red_cable_image, (adaptw(1285, self.width), adapth(860, self.height))
        )
        self.screen.blit(
            self.blue_cable_image, (adaptw(1285, self.width), adapth(935, self.height))
        )

        self.screen.blit(
            self.timeUnits_text,
            self.timeUnits_text.get_rect(
                center=(adaptw(870, self.width), adapth(865, self.height))
            ),
        )
        self.screen.blit(
            self.timeUnits_text_logo,
            self.timeUnits_text_logo.get_rect(
                midleft=self.timeUnits_text.get_rect(
                    center=(adaptw(870, self.width), adapth(865, self.height))
                )
                .move(0, adapth(-5, self.height))
                .midright
            ),
        )
        self.screen.blit(
            self.tps_text,
            self.tps_text.get_rect(
                center=(adaptw(860, self.width), adapth(212.5, self.height))
            ),
        )
        self.screen.blit(
            self.tps_text_logo,
            self.tps_text_logo.get_rect(
                midleft=self.tps_text.get_rect(
                    center=(adaptw(860, self.width), adapth(212.5, self.height))
                )
                .move(0, adapth(-5, self.height))
                .midright
            ),
        )

        self.screen.blit(self.timeline_text, self.timeline_text.get_rect(center=(adaptw(335, self.width), adapth(135, self.height))))
        
        
        
        self.screen.blit(self.era_text, self.era_text.get_rect(center=(adaptw(905, self.width), adapth(935, self.height))))
        
        self.screen.blit(
            get_number_font(40, self.height).render(f"{self.engine.prestige}x TimeBack", True, RED_OCHRE),
            get_number_font(40, self.height).render(f"{self.engine.prestige}x TimeBack", True, RED_OCHRE).get_rect(center=(adaptw(225, self.width), adapth(182.5, self.height))),
        )
        
        if self.engine.is_blue_cable_cut:
            self.blue_cable_button.render(self.screen, w=self.width, h=self.height)

        # pg.draw.rect(self.screen, (0, 0, 255), self.building_scroll_area_rect, 2)

        self.clicker_button.render(self.screen, w=self.width, h=self.height)
    
    

        
    def display_info_box(self):
        """
        Renders all the info boxes of the buttons in the game.
        """
        for button in self.engine.buildings_buttons:
            button.render_infos(self.screen, w=self.width, h=self.height)

        for button in self.engine.upgrades_buttons:
            button.render_infos(self.screen, w=self.width, h=self.height)
            
        for button in self.engine.human_skills_buttons:
            button.render_infos(self.screen, w=self.width, h=self.height)
    
            
    def update_screen(self):
        """
        Update the display to reflect the current game state.
        """
        pg.display.flip()
        
        # self.engine.window.maximize()
        
        
    def init_screen(self):
        """
        Initialize the screen elements if not already initialized.
        """
        if not self.is_init:
            width, height = pg.display.get_surface().get_size()
        
            # Screen components
            self.timeUnits_text: pg.Surface = get_number_font(65, height).render(f"{format_timeUnits(self.engine.timeUnits, 0)}", True, RED_OCHRE)
            self.timeUnits_text_logo: pg.Surface = load_image(f"{self.src_dir}/img/timeUnits.png", width, height)
            
            self.tps_text: pg.Surface = get_number_font(50, height).render(f"{format_timeUnits(self.engine.tps, 0)}", True, RED_OCHRE)
            self.tps_text_logo: pg.Surface = load_image(f"{self.src_dir}/img/tps.png", width, height)
            
            if self.engine.timeline < 0:
                timeline = "Null"
                size = 124
            elif self.engine.timeline >= 2500:
                timeline = "Out Of Time"
                size = 62
            else:
                timeline = format_time_no_convertion(self.engine.timeline)
                size = 124
            self.timeline_text: pg.Surface = get_timeline_font(size, height).render(f"{timeline}", True, YELLOW_GREEN)
            
            self.blue_cable_image: pg.surface = load_image(f"{self.src_dir}/img/blue_cable_on.png", width, height)
            if self.engine.is_blue_cable_cut:
                self.blue_cable_image = load_image(f"{self.src_dir}/img/blue_cable_off.png", width, height)
                self.blue_cable_button: Button = Button(
                    rect=(adaptw(1285, width),adapth(935, height),adaptw(600, width),adapth(75, height)),
                    screen_size=(width, height),
                    background=BLUE,
                    transparent=True,
                    command=lambda: self.engine.buy_blue_cable_wrapper(),
                    border_radius=0,
                )
                
            self.red_cable_image: pg.surface = load_image(f"{self.src_dir}/img/red_cable_on.png", width, height)
            if self.engine.is_red_cable_cut:
                self.red_cable_image = load_image(f"{self.src_dir}/img/red_cable_off.png", width, height)
                self.red_cable_button: Button = Button(
                    rect=(adaptw(1285, width),adapth(860, height),adaptw(600, width),adapth(75, height)),
                    screen_size=(width, height),
                    background=BLUE,
                    transparent=True,
                    command=lambda: self.engine.buy_red_cable_wrapper(),
                    border_radius=0,
                )
            
            
        
            self.clicker_button: Button = Button(
                rect=(adaptw(705, width),adapth(304, height),adaptw(403, width),adapth(400, height)),
                screen_size=(width, height),
                background=f"{self.src_dir}/img/hourglass.png",
                command=lambda: self.engine.increment_timeUnits(self.engine.clicker_amount),
                border_radius=250,
                image_scale=0.4,
                image_rotation=10,
                bump_on_click=True,
                circle_on_click=True,
                identifier="clicker",
            )
            
            match self.engine.era:
                case 1:
                    era_name = "Prehistory"
                case 2:
                    era_name = "Antiquity"
                case 3:
                    era_name = "Middle Ages"
                case 4:
                    era_name = "Modern Times"
                case 5:
                    era_name = "Contemporary"
                case 6:
                    era_name = "Future"
                
            self.era_text: pg.surface = get_text_font(35, height).render(f"{era_name}", True, YELLOW_GREEN)
            
            # Screen images
            self.timeline_image: pg.surface = load_image(f"{self.src_dir}/img/timeline.png", width, height)
            
            self.upgrade_fond_image: pg.surface = load_image(f"{self.src_dir}/img/upgrade_fond.png", width, height)
            self.upgrade_bord_image: pg.surface = load_image(f"{self.src_dir}/img/upgrade_bord.png", width, height)
            
            self.temporal_matrix_image: pg.surface = load_image(f"{self.src_dir}/img/temporal_matrix.png", width, height)
            
            self.human_skill_and_boost: pg.surface = load_image(f"{self.src_dir}/img/human_skill+boost.png", width, height)
            
            self.shop_fond_image: pg.surface = load_image(f"{self.src_dir}/img/shop_fond.png", width, height)
            self.shop_bord_image: pg.surface = load_image(f"{self.src_dir}/img/shop_bord.png", width, height)
                        
            
            
            
            
            self.building_scroll_area_rect = pg.Rect(adaptw(1525, width),adapth(70, height),adaptw(300, width),adapth(750, height),)
            
            self.upgrade_scroll_area_rect = pg.Rect(adaptw(67.5, width),adapth(267.5, height),adaptw(460, width),adapth(750, height),)
            
            
            self.width = width
            self.height = height
            
            self.is_init = True
            
    
    def display_cables(self):
        """
        Display the cable-related elements on the screen.
        """
        if self.engine.is_blue_cable_cut:
            self.blue_cable_button.render(self.screen)
            
        
        if self.engine.blue_cable_x2_timer != 0:
            # pg.draw.rect(self.screen, CABLE_BLUE, (adaptw(1265, self.width), adapth(45, self.height), adaptw(150, self.width), adapth(65, self.height)))
            
            usb_image = load_image(f"{self.src_dir}/img/usb_boost_2.png", self.width, self.height)
            self.screen.blit(usb_image, (adaptw(1265, self.width), adapth(40, self.height)))
            
            
            timer_text = time.strftime("%M:%S", time.gmtime(self.engine.blue_cable_x2_timer/self.engine.framerate))
            timer_text_surface = get_clock_font(30, self.height).render(f"{timer_text}", True, CLOCK_GREEN)
            self.screen.blit(timer_text_surface,(adaptw(1328.5, self.width), adapth(59.5, self.height)))
            
            
        if self.engine.blue_cable_x5_timer != 0:
            # pg.draw.rect(self.screen, CABLE_BLUE, (adaptw(1265, self.width), adapth(115, self.height), adaptw(150, self.width), adapth(65, self.height)))
            
            usb_image = load_image(f"{self.src_dir}/img/usb_boost_5.png", self.width, self.height)
            self.screen.blit(usb_image, (adaptw(1265, self.width), adapth(113, self.height)))
            
            
            timer_text = time.strftime("%M:%S", time.gmtime(self.engine.blue_cable_x5_timer/self.engine.framerate))
            timer_text_surface = get_clock_font(30, self.height).render(f"{timer_text}", True, CLOCK_GREEN)
            self.screen.blit(timer_text_surface,(adaptw(1328.5, self.width), adapth(132.5, self.height)))


    def display_tunings(self):
    
        bar_height = adapth(8, self.height)
        bar_spacing = adaptw(2.5, self.width)
        bar_x = adaptw(70, self.width)
        bar_y_start = adapth(70, self.height)
        
        current_time = time.time()*5
        bar_widths = [
            (math.sin(current_time * 0.3) + 1) * 37.5,  # Example dynamic width for bar 1
            (math.sin(current_time * 0.4) + 1) * 37.5,  # Example dynamic width for bar 2
            (math.sin(current_time * 0.2) + 1) * 37.5,  # Example dynamic width for bar 3
            (math.sin(current_time) + 1) * 37.5         # Example dynamic width for bar 4
        ]
        for i in range(4):
            bar_y = bar_y_start + i * (bar_height + bar_spacing)
            bar_width = adaptw(bar_widths[i], self.width)
            bar_color = YELLOW_GREEN

            pg.draw.rect(self.screen, bar_color, (bar_x, bar_y, bar_width, bar_height), border_radius=40)
            
            
            
            
            
        bar_x = adaptw(632.5, self.width)
        bar_y_start = adapth(75, self.height)
        
        current_time = time.time()*5
        bar_widths = [
            (math.sin(current_time * 0.45) + 1) * 37.5,
            (math.sin(current_time * 0.17) + 1) * 37.5,
            (math.sin(current_time * 0.7) + 1) * 37.5,
            (math.sin(current_time * 0.35) + 1) * 37.5
        ]
        for i in range(4):
            bar_y = bar_y_start + i * (bar_height + bar_spacing)
            bar_width = adaptw(bar_widths[i], self.width)
            bar_color = LIGHT_CYAN

            pg.draw.rect(self.screen, bar_color, (bar_x, bar_y, bar_width, bar_height), border_radius=40)
            
            
            
        bar_spacing = adaptw(5, self.width)
        bar_width = adapth(12.5, self.height)
        bar_y = adapth(800, self.height)
        bar_x_start = adaptw(705, self.width)
        
        current_time = time.time()*5
        bar_heights = [
            (math.sin(current_time * 0.19) + 1) * 37.5,
            (math.sin(current_time * 0.24) + 1) * 37.5,
            (math.sin(current_time * 0.7) + 1) * 37.5,
            (math.sin(current_time * 0.215) + 1) * 37.5
        ]
        for i in range(4):
            bar_x = bar_x_start + i * (bar_width + bar_spacing)
            bar_height = -adapth(bar_heights[i], self.height)
            bar_color = RED_OCHRE

            pg.draw.rect(self.screen, bar_color, (bar_x, bar_y, bar_width, bar_height), border_radius=40)
            
            
            
        point_radius = adaptw(10, self.width)
        point_spacing = adaptw(30, self.width)
        point_y = adapth(185, self.height)
        point_x_start = adaptw(442.5, self.width)

        blink_alpha_values = [
            3,
            7,
            2
        ]

        for i in range(3):
            blink_alpha_value = blink_alpha_values[i]
            blink_alpha = int((pg.time.get_ticks() % blink_alpha_value) / blink_alpha_value * 255)
            
            point_x = point_x_start + i * point_spacing
            point_surface = pg.Surface((point_radius * 2, point_radius * 2), pg.SRCALPHA)
            pg.draw.circle(point_surface, YELLOW_GREEN + (blink_alpha,), (point_radius, point_radius), point_radius)
            self.screen.blit(point_surface, (point_x - point_radius, point_y - point_radius))
            
            
            
            
        point_y = adapth(790, self.height)
        point_x_start = adaptw(1040, self.width)

        blink_alpha_values = [
            2.4,
            4.2,
            1.6
        ]

        for i in range(3):
            blink_alpha_value = blink_alpha_values[i]
            blink_alpha = int((pg.time.get_ticks() % blink_alpha_value) / blink_alpha_value * 255)
            
            point_x = point_x_start + i * point_spacing
            point_surface = pg.Surface((point_radius * 2, point_radius * 2), pg.SRCALPHA)
            pg.draw.circle(point_surface, RED_OCHRE + (blink_alpha,), (point_radius, point_radius), point_radius)
            self.screen.blit(point_surface, (point_x - point_radius, point_y - point_radius))
            
            
