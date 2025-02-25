import ctypes
import os
from re import S
from Buttons import Button
from config import *
import pygame as pg
from pygame._sdl2 import Window
from data import *

from buildings import buildings
from upgrade import UPGRADES, treshold
from utils import adapt_size_width as adaptw, adapt_size_height as adapth, can_buy_buildings, can_buy_upgrade, format_time_no_convertion, format_timeUnits, get_number_font, get_text_font, get_timeline_font, load_image

class PaintStrategy:
    def __init__(self, engine, screen, src_dir):
        self.engine = engine
        self.screen = screen
        self.src_dir = src_dir
        
        self.width = self.height = "Null"
        
        self.can_scroll = True
        
        self.is_building_clickable = False
        self.is_upgrading_clickable = False
        
        self.scroll_speed = 20
        
        self.scroll_value = 0
        
        self.is_init = False
        
        
    
    def update_elements(self):
        self.engine.LOGGER.DEBUG("Initializing screen...")
        width, height = pg.display.get_surface().get_size()
        
        # Screen components
        self.timeUnits_text: pg.Surface = get_number_font(65, height).render(f"{format_timeUnits(self.engine.timeUnits, 0)}", True, RED_OCHRE)
        self.timeUnits_text_logo: pg.Surface = load_image(f"{self.engine.src_dir}/img/timeUnits.png", width, height)
        
        self.engine.LOGGER.WARNING(f"TPS: {self.engine.tps}")
        self.tps_text: pg.Surface = get_number_font(50, height).render(f"{format_timeUnits(self.engine.tps, 0)}", True, RED_OCHRE)
        self.tps_text_logo: pg.Surface = load_image(f"{self.engine.src_dir}/img/tps.png", width, height)
        
        self.timeline_text: pg.Surface = get_timeline_font(124, height).render(f"{format_time_no_convertion(self.engine.timeline,3)}", True, YELLOW_GREEN)
        
        if self.has_window_been_resized():
            self.clicker_button: Button = Button(
                rect=(adaptw(705, width),adapth(304, height),adaptw(403, width),adapth(400, height)),
                screen_size=(width, height),
                background=f"{self.engine.src_dir}/img/hourglass.png",
                command=lambda: self.engine.increment_timeUnits(self.engine.clicker_amount),
                border_radius=250,
                image_scale=0.4,
                image_rotation=10,
                bump_on_click=True,
                identifier="clicker",
            )
            
            # Screen images
            self.timeline_image: pg.surface = load_image(f"{self.engine.src_dir}/img/timeline.png", width, height)
            
            self.upgrade_fond_image: pg.surface = load_image(f"{self.engine.src_dir}/img/upgrade_fond.png", width, height)
            self.upgrade_bord_image: pg.surface = load_image(f"{self.engine.src_dir}/img/upgrade_bord.png", width, height)
            
            self.temporal_matrix_image: pg.surface = load_image(f"{self.engine.src_dir}/img/temporal_matrix.png", width, height)
            
            self.human_skill_and_boost: pg.surface = load_image(f"{self.engine.src_dir}/img/human_skill+boost.png", width, height)
            
            self.shop_fond_image: pg.surface = load_image(f"{self.engine.src_dir}/img/shop_fond.png", width, height)
            self.shop_bord_image: pg.surface = load_image(f"{self.engine.src_dir}/img/shop_bord.png", width, height)
            
            self.red_cable_image: pg.surface = load_image(f"{self.engine.src_dir}/img/red_cable_on.png", width, height)
            
            self.blue_cable_image: pg.surface = load_image(f"{self.engine.src_dir}/img/blue_cable_on.png", width, height)
            self.blue_cable_button: Button = Button(
                rect=(adaptw(1285, width),adapth(935, height),adaptw(600, width),adapth(75, height)),
                screen_size=(width, height),
                background=BLUE,
                command=lambda: self.engine.buy_upgrade_wrapper("blue_cable"),
                border_radius=0,
            )
            
            
            
            self.building_scroll_area_rect = pg.Rect(adaptw(1525, width),adapth(70, height),adaptw(300, width),adapth(750, height),)
            
            self.upgrade_scroll_area_rect = pg.Rect(adaptw(67.5, width),adapth(267.5, height),adaptw(460, width),adapth(750, height),)
            
            
        self.width = width
        self.height = height
    
    def has_window_been_resized(self):
        return self.width != pg.display.get_surface().get_width()or self.height != pg.display.get_surface().get_height()
    
    def create_buildings_buttons(self):
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

            infos = f"The building '{build_name}' has {build_amount} units,\nproducing {format_timeUnits(build_tps * build_amount * build_augment)} time units per second,\nwith a boost multiplier of {build_augment}x."

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
        y = 180
        x = 82.5
        for i in range(len(self.engine.available_upgrades)):
            upgrade = self.engine.available_upgrades[i]
            upgrade_name = upgrade["name"]
            upgrade_cost = upgrade["cost"]
            upgrade_effect_value = upgrade["effect_value"]
            upgrade_building_name = upgrade["building_name"]
            upgrade_level = next(
                (
                    u["level"]
                    for u in self.engine.bought_upgrades["long_list"]
                    if u["name"] == upgrade["name"]
                ),
                0,
            )

            if (i - 4) % 4 == 0:
                x = 82.5
                y += 117.5
            else:
                x += 112.5

            infos = f"The upgrade '{upgrade_name}' costs {format_timeUnits(upgrade_cost)} time units, \nis affecting the building '{upgrade_building_name}'. \nCurrent level: {upgrade_level} \n Effect value: {upgrade_effect_value ** upgrade_level}"

            self.engine.upgrades_buttons.append(
                Button(
                    (
                        adaptw(x, self.width),
                        adapth(y, self.height),
                        adaptw(90, self.width),
                        adapth(90, self.height),
                    ),
                    (self.width, self.height),
                    background=BLUE,
                    transparent=True,
                    border_radius=250,
                    command=lambda b=upgrade_name: self.engine.buy_upgrade_wrapper(b),
                    identifier=upgrade["name"],
                    infos=infos,
                )
            )

    def handle_event(self):
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
            elif keys[pg.K_F11]:
                if self.is_maximized:
                    self.window.restore()
                    self.is_maximized = False
                else:
                    self.window.maximize()
                    self.is_maximized = True

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

            self.clicker_button.get_event(event)

    def check_mouse_hover(self):
        pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)
        
        mouse_pos = pg.mouse.get_pos()
        for build_button in self.engine.buildings_buttons:
            button_rect = build_button.rect
            if self.building_scroll_area_rect.colliderect(button_rect) and self.is_building_clickable:
                build_button.update_hover_state(mouse_pos)

        for upgrade_button in self.engine.upgrades_buttons:
            button_rect = upgrade_button.rect
            if self.upgrade_scroll_area_rect.colliderect(button_rect) and self.is_upgrading_clickable:
                upgrade_button.update_hover_state(mouse_pos)

    def display_back_images(self):
        self.screen.blit(self.shop_fond_image, (adaptw(1475, self.width), adapth(45, self.height)))
        self.screen.blit(self.upgrade_fond_image, (adaptw(45, self.width), adapth(245, self.height)))
        
    def display_buildings(self):
        match self.engine.era:
            case 1:
                base = f"{self.engine.src_dir}/img/buildings/base_1.png"
            case 2:
                base = f"{self.engine.src_dir}/img/buildings/base_2.png"
            case 3:
                base = f"{self.engine.src_dir}/img/buildings/base_3.png"
            case 4:
                base = f"{self.engine.src_dir}/img/buildings/base_4.png"
            case 5:
                base = f"{self.engine.src_dir}/img/buildings/base_5.png"
        for i in range(len(self.engine.buildings_buttons)):
            build_button = self.engine.buildings_buttons[i]
            build = next(
                (
                    b
                    for b in self.engine.bought_buildings["long_list"]
                    if b["name"] == build_button.identifier
                ),
                None,
            )
            if build is None:
                amount = 0
            else:
                amount = build["amount"]

            cost = next(
                (
                    b["cost"](amount)
                    for b in buildings
                    if b["name"] == build_button.identifier
                ),
                None,
            )

            building_image = load_image(f"{self.engine.src_dir}/img/buildings/{build_button.identifier.lower().replace(' ', '_')}.png",self.width,self.height,)
            base_image = load_image(base, self.width, self.height)

            # print(f"scroll_y: {scroll_y}({abs(adapth((scroll_y * 1), h))})")
            button_rect = build_button.rect.move(
                0, build_button.rect.height + adapth(7.5, self.height)
            )
            building_rect = building_image.get_rect(
                topleft=(adaptw(1525, self.width), adapth(85 + 105 * i, self.height))
            ).move(0, adapth((self.scroll_value * 1), self.height))
            base_rect = base_image.get_rect(
                topleft=(adaptw(1525, self.width), adapth(85 + 105 * i, self.height))
            ).move(0, adapth((self.scroll_value * 1), self.height))
            # build_button.rect = button_rect
            if not can_buy_buildings(
                self.engine.bought_buildings, build_button.identifier, 1, self.engine.timeUnits
            ):
                base_image.fill((100, 100, 100), special_flags=pg.BLEND_MULT)
                self.screen.blit(base_image, base_rect.topleft)

                building_image.fill((100, 100, 100), special_flags=pg.BLEND_MULT)
                self.screen.blit(building_image, building_rect.topleft)

                self.screen.blit(
                    get_text_font(25, self.height).render(f"{format_timeUnits(round(cost))}", True, DARK_BROWN),
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
                    get_text_font(25, self.height).render(f"{format_timeUnits(round(cost))}", True, BROWN),
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

    def display_upgrades(self):
        y = 210
        x = 127.5
        for i in range(len(self.engine.upgrades_buttons)):
            upgrade_button = self.engine.upgrades_buttons[i]
            upgrade = next(
                (b for b in UPGRADES if b["name"] == upgrade_button.identifier), None
            )
            upgrade_level = next(
                (
                    u["level"]
                    for u in self.engine.bought_upgrades["long_list"]
                    if u["name"] == upgrade_button.identifier
                ),
                0,
            )
            max_bought_level = next(
                (
                    u["level"]
                    for u in self.engine.bought_upgrades["long_list"]
                    if u["name"] == upgrade["name"]
                ),
                0,
            )
            if not upgrade_level == len(treshold):
                xth_build_price = next(
                    (
                        b["cost"](treshold[max_bought_level])
                        for b in buildings
                        if b["name"] == upgrade["building_name"]
                    ),
                    0,
                )
            else:
                xth_build_price = "FULL"

            if upgrade is None:
                cost = 0
            else:
                cost = xth_build_price * 3

            if upgrade_level == len(treshold):
                cost = "FULL"


            upgrade_image = load_image(f"{self.engine.src_dir}/img/upgrades/{upgrade_button.identifier.lower().replace(' ', '_')}.png",self.width,self.height,scale=0.75,)
            level_image = load_image(f"{self.engine.src_dir}/img/upgrades/niv{upgrade_level}.png", self.width, self.height, 0.9)
            
            if (i - 4) % 4 == 0:
                x = 127.5
                y += 117.5
            else:
                x += 112.5


            upgrade_rect = upgrade_image.get_rect(center=(adaptw(x, self.width), adapth(y, self.height)))

            level_rect = level_image.get_rect(center=upgrade_rect.center).move(adaptw(0, self.width), adapth(15, self.height))

            if not can_buy_upgrade(self.engine.bought_upgrades, upgrade_button.identifier, self.engine.timeUnits, self.engine.bought_buildings):
                upgrade_image.fill((100, 100, 100), special_flags=pg.BLEND_MULT)
                self.screen.blit(upgrade_image, upgrade_rect.topleft)

                level_image.fill((100, 100, 100), special_flags=pg.BLEND_MULT)
                self.screen.blit(level_image, level_rect.topleft)

                self.screen.blit(
                    get_text_font(17.5, self.height).render(
                        f"{format_timeUnits(round(cost))}", True, GREY
                    ),
                    get_text_font(17.5, self.height)
                    .render(f"{format_timeUnits(round(cost))}", True, GREY)
                    .get_rect(
                        center=(adaptw(x, self.width), adapth(y + 32.5, self.height))
                    ),
                )

                upgrade_button.render(self.screen, True, self.width, self.height)
            else:
                self.screen.blit(upgrade_image, upgrade_rect.topleft)

                # screen.blit(get_text_font(25, self.height).render(f"{format_timeUnits(round(cost))}", True, BROWN), (adaptw(1592, w), adapth(132 + 104.5 * i, self.height) + adapth((scroll_y_bis * 1), self.height)))

                self.screen.blit(level_image, level_rect.topleft)
                if not upgrade_level == len(treshold):
                    self.screen.blit(
                        get_text_font(17.5, self.height).render(
                            f"{format_timeUnits(round(cost))}", True, WHITE
                        ),
                        get_text_font(17.5, self.height)
                        .render(f"{format_timeUnits(round(cost))}", True, GREY)
                        .get_rect(
                            center=(
                                adaptw(x, self.width),
                                adapth(y + 32.5, self.height),
                            )
                        ),
                    )
                else:
                    self.screen.blit(
                        get_text_font(17.5, self.height).render(f"{cost}", True, WHITE),
                        get_text_font(17.5, self.height)
                        .render(f"{cost}", True, GREY)
                        .get_rect(
                            center=(
                                adaptw(x, self.width),
                                adapth(y + 32.5, self.height),
                            )
                        ),
                    )

                upgrade_button.render(self.screen, w=self.width, h=self.height)

    def display_front_elements(self):
        self.screen.blit(load_image(f"{self.engine.src_dir}/img/background.png", self.width, self.height), (0, 0))
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

        self.screen.blit(self.timeline_text, (adaptw(90, self.width), adapth(87, self.height)))
        self.blue_cable_button.render(self.screen, w=self.width, h=self.height)

        # pg.draw.rect(screen, (0, 0, 255), scroll_area_rect_bis, 2)

        self.clicker_button.render(self.screen, w=self.width, h=self.height)
        
    def display_info_box(self):
        for button in self.engine.buildings_buttons:
            button.render_infos(self.screen, w=self.width, h=self.height)

        for button in self.engine.upgrades_buttons:
            button.render_infos(self.screen, w=self.width, h=self.height)
            
    def update_screen(self):
        pg.display.flip()
        
    def init_screen(self):
        if not self.is_init:
            self.engine.LOGGER.DEBUG("Initializing screen...")
            width, height = pg.display.get_surface().get_size()
            
            # Screen components
            self.timeUnits_text: pg.Surface = get_number_font(65, height).render(f"{format_timeUnits(self.engine.timeUnits, 0)}", True, RED_OCHRE)
            self.timeUnits_text_logo: pg.Surface = load_image(f"{self.engine.src_dir}/img/timeUnits.png", width, height)
            
            self.engine.LOGGER.WARNING(f"TPS: {self.engine.tps}")
            self.tps_text: pg.Surface = get_number_font(50, height).render(f"{format_timeUnits(self.engine.tps, 0)}", True, RED_OCHRE)
            self.tps_text_logo: pg.Surface = load_image(f"{self.engine.src_dir}/img/tps.png", width, height)
            
            self.timeline_text: pg.Surface = get_timeline_font(124, height).render(f"{format_time_no_convertion(self.engine.timeline,3)}", True, YELLOW_GREEN)
            
        
            self.clicker_button: Button = Button(
                rect=(adaptw(705, width),adapth(304, height),adaptw(403, width),adapth(400, height)),
                screen_size=(width, height),
                background=f"{self.engine.src_dir}/img/hourglass.png",
                command=lambda: self.engine.increment_timeUnits(self.engine.clicker_amount),
                border_radius=250,
                image_scale=0.4,
                image_rotation=10,
                bump_on_click=True,
                identifier="clicker",
            )
            
            # Screen images
            self.timeline_image: pg.surface = load_image(f"{self.engine.src_dir}/img/timeline.png", width, height)
            
            self.upgrade_fond_image: pg.surface = load_image(f"{self.engine.src_dir}/img/upgrade_fond.png", width, height)
            self.upgrade_bord_image: pg.surface = load_image(f"{self.engine.src_dir}/img/upgrade_bord.png", width, height)
            
            self.temporal_matrix_image: pg.surface = load_image(f"{self.engine.src_dir}/img/temporal_matrix.png", width, height)
            
            self.human_skill_and_boost: pg.surface = load_image(f"{self.engine.src_dir}/img/human_skill+boost.png", width, height)
            
            self.shop_fond_image: pg.surface = load_image(f"{self.engine.src_dir}/img/shop_fond.png", width, height)
            self.shop_bord_image: pg.surface = load_image(f"{self.engine.src_dir}/img/shop_bord.png", width, height)
            
            self.red_cable_image: pg.surface = load_image(f"{self.engine.src_dir}/img/red_cable_on.png", width, height)
            
            self.blue_cable_image: pg.surface = load_image(f"{self.engine.src_dir}/img/blue_cable_on.png", width, height)
            self.blue_cable_button: Button = Button(
                rect=(adaptw(1285, width),adapth(935, height),adaptw(600, width),adapth(75, height)),
                screen_size=(width, height),
                background=BLUE,
                command=lambda: self.engine.buy_upgrade_wrapper("blue_cable"),
                border_radius=0,
            )
            
            
            
            self.building_scroll_area_rect = pg.Rect(adaptw(1525, width),adapth(70, height),adaptw(300, width),adapth(750, height),)
            
            self.upgrade_scroll_area_rect = pg.Rect(adaptw(67.5, width),adapth(267.5, height),adaptw(460, width),adapth(750, height),)
            
            self.width = width
            self.height = height
            
            self.is_init = True
            
          