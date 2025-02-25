import os
from random import randint
import sys
import time
import ctypes
from pprint import pprint
from datetime import datetime
import threading

import pygame as pg
from pygame._sdl2 import Window
from pygame.locals import *

from data import *
from Buttons import Button
from Logger import Logger
from buildings import buildings
from upgrade import UPGRADES, treshold

from utils import (
    adapt_size_height,
    adapt_size_width,
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
)

LOGGER: Logger = Logger()
pg.init()
pg.font.init()
clock: pg.time.Clock = pg.time.Clock()


if len(sys.argv) > 1:
    if sys.argv[1] == "--debug":
        LOGGER.set_level(4)

appdata_path = os.path.join(os.getenv("LOCALAPPDATA"), "TimeClicker")
src_dir = resource_path("src")
# show_message("src path: " + str(src_dir))

os.makedirs(appdata_path, exist_ok=True)

ctypes.windll.user32.SetProcessDPIAware()
monitor_info = ctypes.windll.user32.MonitorFromWindow(None, 2)
monitor_rect = ctypes.wintypes.RECT()
ctypes.windll.user32.GetMonitorInfoW(monitor_info, ctypes.byref(monitor_rect))
os.environ["SDL_VIDEO_WINDOW_POS"] = f"{500},{300}"


screen: pg.Surface = pg.display.set_mode((1024, 576), pg.RESIZABLE)
icon: pg.Surface = pg.image.load(os.path.join(src_dir, "icon.png"))
pg.display.set_icon(icon)
window = Window.from_display_module()
window.maximize()
is_maximized = True
pg.display.set_caption("Time Clicker")


def main():
    is_maximized = True
    # define game values
    # save_data(appdata_path)
    (
        timeUnits,
        tps,
        timeline,
        clicker_amount,
        bought_buildings,
        max_timeUnits,
        bought_upgrades,
        last_saved_time,
    ) = get_data(appdata_path)
    # bought_upgrades = {"short_list": [], "long_list": []}
    pprint(bought_buildings)
    # bought_buildings["long_list"][0]["amount"] = 1
    max_timeUnits = int(float(max_timeUnits))
    # timeUnits = 1000000000000000
    # clicker_amount = 100000000000000000000000**2
    LOGGER.DEBUG(
        f"{timeUnits}({type(timeUnits)}), {tps}({type(tps)}), {timeline}({type(timeline)}), {clicker_amount}({type(clicker_amount)}), {bought_buildings}({type(bought_buildings)}), {max_timeUnits}({type(max_timeUnits)})."
    )

    if last_saved_time:
        elapsed_time = (
            datetime.now() - datetime.strptime(last_saved_time, " %Y-%m-%d %H:%M:%S")
        ).total_seconds()
        timeUnits += tps * (elapsed_time)  # Add production for the elapsed time
        LOGGER.INFO(
            f"Elapsed time: {elapsed_time} seconds, added {tps * (elapsed_time )} timeUnits, tps: {tps}"
        )

    current_frame: int = 0
    framerate: int = 10

    w = h = "n"

    era: int = 1

    available_buildings: list = []

    available_upgrades: list = []

    can_scroll_up = True
    can_scroll_up_bis = True

    is_clickable = False
    is_clickable_bis = False

    save_count = 0

    blue_cable_count = 0
    blue_cable_timer = randint(60, 350)
    # is_blue_cable_off

    LOGGER.INFO(timeUnits)

    def increment_timeUnits(amount):
        nonlocal timeUnits, clicker_amount
        timeUnits += amount

    def buy_building_wrapper(b):
        nonlocal bought_buildings, timeUnits
        bought_buildings, timeUnits = buy_buildings(bought_buildings, b, 1, timeUnits)

    def buy_upgrade_wrapper(u):
        nonlocal bought_upgrades, timeUnits, bought_buildings
        bought_upgrades, timeUnits, bought_buildings = buy_upgrades(
            bought_upgrades, u, timeUnits, bought_buildings
        )
        # pprint(bought_upgrades)
        # pprint(bought_buildings)

    def buy_blue_cable():
        nonlocal blue_cable_count, blue_cable_timer, blue_cable_image, blue_cable_button

    LOGGER.DEBUG("Initializing screen size")
    wi, he = pg.display.get_surface().get_size()
    timeUnits_text: pg.Surface = get_number_font(65, he).render(
        f"{format_timeUnits(timeUnits, 9)}", True, RED_OCHRE
    )
    timeUnits_text_logo: pg.Surface = load_image(f"{src_dir}/img/timeUnits.png", wi, he)
    tps_text: pg.Surface = get_number_font(50, he).render(
        f"{format_timeUnits(tps, 9)}", True, RED_OCHRE
    )

    timeline_text: pg.Surface = get_timeline_font(124, he).render(
        f"{format_time_no_convertion(timeline,3)}", True, YELLOW_GREEN
    )

    clicker_button: Button = Button(
        (
            adapt_size_width(705, wi),
            adapt_size_height(304, he),
            adapt_size_width(403, wi),
            adapt_size_height(400, he),
        ),
        (wi, he),
        f"{src_dir}/img/hourglass.png",
        lambda: increment_timeUnits(clicker_amount),
        250,
        False,
        0.4,
        10,
        True,
        identifier="clicker",
    )

    timeline_image: pg.surface = load_image(f"{src_dir}/img/timeline.png", wi, he)
    upgrade_fond_image: pg.surface = load_image(
        f"{src_dir}/img/upgrade_fond.png", wi, he
    )
    upgrade_bord_image: pg.surface = load_image(
        f"{src_dir}/img/upgrade_bord.png", wi, he
    )
    temporal_matrix_image: pg.surface = load_image(
        f"{src_dir}/img/temporal_matrix.png", wi, he
    )
    human_skill_and_boost: pg.surface = load_image(
        f"{src_dir}/img/human_skill+boost.png", wi, he
    )
    shop_fond_image: pg.surface = load_image(f"{src_dir}/img/shop_fond.png", wi, he)
    shop_bord_image: pg.surface = load_image(f"{src_dir}/img/shop_bord.png", wi, he)
    red_cable_image: pg.surface = load_image(f"{src_dir}/img/red_cable_on.png", wi, he)
    blue_cable_image: pg.surface = load_image(
        f"{src_dir}/img/blue_cable_on.png", wi, he
    )
    blue_cable_button: Button = Button(
        rect=(
            adapt_size_width(1285, wi),
            adapt_size_height(935, he),
            adapt_size_width(600, wi),
            adapt_size_height(75, he),
        ),
        screen_size=(wi, he),
        background=BLUE,
        command=lambda: buy_upgrade_wrapper("blue_cable"),
        border_radius=0,
        transparent=False,
        image_scale=1,
    )

    if buildings[0]["name"] not in bought_buildings["short_list"]:
        bought_buildings["short_list"].append(buildings[0]["name"])
        bought_buildings["long_list"].append(
            {"name": buildings[0]["name"], "amount": 0}
        )
    LOGGER.DEBUG(bought_buildings)
    LOGGER.DEBUG(bought_upgrades)

    scroll_speed = 20

    scroll_y = 0
    scroll_area_rect = pg.Rect(
        adapt_size_width(1525, wi),
        adapt_size_height(70, he),
        adapt_size_width(300, wi),
        adapt_size_height(750, he),
    )
    scrollbar_rect = pg.Rect(
        adapt_size_width(1830, wi),
        adapt_size_height(160, he),
        adapt_size_width(20, wi),
        adapt_size_height(600, he),
    )

    scroll_y_bis = 0
    scroll_area_rect_bis = pg.Rect(
        adapt_size_width(67.5, wi),
        adapt_size_height(267.5, he),
        adapt_size_width(460, wi),
        adapt_size_height(750, he),
    )
    scrollbar_rect_bis = pg.Rect(
        adapt_size_width(1830, wi),
        adapt_size_height(160, he),
        adapt_size_width(20, wi),
        adapt_size_height(600, he),
    )

    running: bool = True
    while running:
        available_upgrades = []
        # LOGGER.DEBUG(f"Testing screen => {(w, h)} | {pg.display.get_surface().get_size()}")
        if (
            w != pg.display.get_surface().get_width()
            or h != pg.display.get_surface().get_height()
        ):
            LOGGER.DEBUG("Updating screen size")
            w, h = pg.display.get_surface().get_size()

            timeline_text: pg.Surface = get_timeline_font(124, h).render(
                f"{format_time_no_convertion(timeline,3)}", True, YELLOW_GREEN
            )

            clicker_button: Button = Button(
                (
                    adapt_size_width(705, w, True),
                    adapt_size_height(304, h, True),
                    adapt_size_width(403, w, True),
                    adapt_size_height(400, h, True),
                ),
                (w, h),
                f"{src_dir}/img/hourglass.png",
                lambda: increment_timeUnits(clicker_amount),
                250,
                False,
                0.4,
                10,
                True,
                identifier="clicker",
            )

            timeline_image: pg.surface = load_image(f"{src_dir}/img/timeline.png", w, h)
            upgrade_fond_image: pg.surface = load_image(
                f"{src_dir}/img/upgrade_fond.png", w, h
            )
            upgrade_bord_image: pg.surface = load_image(
                f"{src_dir}/img/upgrade_bord.png", w, h
            )
            temporal_matrix_image: pg.surface = load_image(
                f"{src_dir}/img/temporal_matrix.png", w, h
            )
            human_skill_and_boost: pg.surface = load_image(
                f"{src_dir}/img/human_skill+boost.png", w, h
            )
            shop_fond_image: pg.surface = load_image(
                f"{src_dir}/img/shop_fond.png", w, h
            )
            shop_bord_image: pg.surface = load_image(
                f"{src_dir}/img/shop_bord.png", w, h
            )
            red_cable_image: pg.surface = load_image(
                f"{src_dir}/img/red_cable_on.png", w, h
            )
            blue_cable_image: pg.surface = load_image(
                f"{src_dir}/img/blue_cable_on.png", w, h
            )

        if blue_cable_count == framerate * blue_cable_timer:
            is_blue_cable_off = True

        timeUnits_text: pg.Surface = get_number_font(65, h).render(
            f"{format_timeUnits(timeUnits, 6)}", True, RED_OCHRE
        )
        timeUnits_text_logo: pg.Surface = load_image(
            f"{src_dir}/img/timeUnits.png", w, h, scale=0.12
        )
        tps_text: pg.Surface = get_number_font(50, h).render(
            f"{format_timeUnits(tps, 6)} TU/s", True, RED_OCHRE
        )

        for i in range(len(buildings)):
            build = buildings[i]
            previous_build = buildings[i - 1] if i > 0 else None
            if build["name"] in bought_buildings["short_list"] or i == 0:
                if not build in available_buildings:
                    available_buildings.append(build)
            elif previous_build["name"] in bought_buildings["short_list"] and (
                next(
                    (
                        b["amount"]
                        for b in bought_buildings["long_list"]
                        if b["name"] == previous_build["name"]
                    ),
                    None,
                )
                >= 1
            ):
                if not build in available_buildings:
                    available_buildings.append(build)

        for i in range(len(UPGRADES)):
            upgrade = UPGRADES[i]
            build_amount = next(
                (
                    b["amount"]
                    for b in bought_buildings["long_list"]
                    if b["name"] == upgrade["building_name"]
                ),
                None,
            )

            if not build_amount is None:

                max_bought_level = next(
                    (
                        u["level"]
                        for u in bought_upgrades["long_list"]
                        if u["name"] == upgrade["name"]
                    ),
                    0,
                )

                if build_amount >= treshold[0]:

                    if max_bought_level == 0:
                        if not upgrade in available_upgrades:
                            available_upgrades.append(upgrade)

                    elif max_bought_level != 0:
                        if not upgrade in available_upgrades:
                            available_upgrades.append(upgrade)

            # print(f"upgrade : {upgrade['name']} | max_bought_upgrade : {max_bought_upgrade['name'] if max_bought_upgrade is not None else 'None'}")
            # if ((max_bought_upgrade is None and upgrade["id"] == 1)or (max_bought_upgrade is not None and upgrade["id"] == max_bought_upgrade["id"] + 1) or upgrade["id"] == 4) and upgrade["building_name"] in bought_buildings["short_list"]:
            #     if not upgrade in available_upgrades: available_upgrades.append(upgrade)
            # if max_bought_upgrade is None:
            # if upgrade["name"] == "campfire":
            #     print(upgrade["building_name"] in bought_buildings["short_list"])
            #     print("(next((int(b['amount']) for b in bought_buildings['long_list'] if b['name'].lower() == upgrade['building_name']), None) :", next((int(b['amount']) for b in bought_buildings["long_list"] if b['name'].lower() == upgrade["building_name"]), None))
            #     print("upgrade['unlock'] :", upgrade["unlock"])
            #     print()
            # if not upgrade["name"] in bought_upgrades["short_list"] and upgrade["building_name"] in bought_buildings["short_list"] and (next((int(b['amount']) for b in bought_buildings["long_list"] if b['name'].lower() == upgrade["building_name"].lower()), None) >= upgrade["unlock"]):
            #     if not upgrade in available_upgrades: available_upgrades.append(upgrade)

            # elif upgrade["id"] == max_bought_upgrade["id"] + 1:
            #     if not upgrade in available_upgrades: available_upgrades.append(upgrade)

        # LOGGER.DEBUG([u["name"] for u in available_upgrades])

        clock.tick_busy_loop(framerate)
        current_frame: int = (current_frame + 1) % framerate

        timeUnits += tps / framerate
        max_timeUnits = max(max_timeUnits, timeUnits)

        buildings_buttons: list = []
        upgrades_buttons: list = []
        tps: int = 0

        for build in bought_buildings["long_list"]:
            try:
                temp = build["upgrade_boost"]
            except KeyError:
                build["upgrade_boost"] = 1

        for i in range(len(available_buildings)):
            build = available_buildings[i]

            build_name = build["name"]
            build_tps = build["tps_boost"]
            build_amount = next(
                (
                    b["amount"]
                    for b in bought_buildings["long_list"]
                    if b["name"] == build["name"]
                ),
                0,
            )
            build_augment = next(
                (
                    b["upgrade_boost"]
                    for b in bought_buildings["long_list"]
                    if b["name"] == build["name"]
                ),
                1,
            )
            tps += build_tps * build_amount * build_augment

            infos = f"The building '{build_name}' has {build_amount} units,\nproducing {format_timeUnits(build_tps * build_amount * build_augment)} time units per second,\nwith a boost multiplier of {build_augment}x."

            buildings_buttons.append(
                Button(
                    (
                        adapt_size_width(1525, w),
                        adapt_size_height(85, h)
                        + (adapt_size_height(105, h) * i)
                        + adapt_size_height((scroll_y * 1), h),
                        adapt_size_width(300, w),
                        adapt_size_height(45, w),
                    ),
                    (w, h),
                    background=BLUE,
                    transparent=True,
                    border_radius=20,
                    command=lambda b=build_name: buy_building_wrapper(b),
                    identifier=build["name"],
                    infos=infos,
                )
            )
            # buildings_buttons.append(Button(
            #     (adapt_size_width(1525, w), adapt_size_height(85, h) + (adapt_size_height(105, h)*i) + adapt_size_height((scroll_y * 1), h), adapt_size_width(300, w), adapt_size_height(45, w)),
            #     (w, h), background=BLUE, border_radius=20,
            #     command=lambda b=build_name: buy_building_wrapper(b), identifier=build["name"]
            # ))

        y = 210
        x = 81
        for i in range(len(available_upgrades)):
            upgrade = available_upgrades[i]
            upgrade_name = upgrade["name"]
            upgrade_cost = upgrade["cost"]
            upgrade_effect_value = upgrade["effect_value"]
            upgrade_building_name = upgrade["building_name"]
            upgrade_level = next(
                (
                    u["level"]
                    for u in bought_upgrades["long_list"]
                    if u["name"] == upgrade["name"]
                ),
                0,
            )

            if (i - 4) % 4 == 0:
                x = 81
                y += 117.5
            else:
                x += 112.5

            infos = f"The upgrade '{upgrade_name}' costs {format_timeUnits(upgrade_cost)} time units, \nis affecting the building '{upgrade_building_name}'. \nCurrent level: {upgrade_level} \n Effect value: {upgrade_effect_value ** upgrade_level}"

            upgrades_buttons.append(
                Button(
                    (
                        adapt_size_width(x, w),
                        adapt_size_height(y, h)
                        + adapt_size_height((scroll_y_bis * 1), h),
                        adapt_size_width(90, w),
                        adapt_size_height(90, h),
                    ),
                    (w, h),
                    background=BLUE,
                    transparent=True,
                    border_radius=250,
                    command=lambda b=upgrade_name: buy_upgrade_wrapper(b),
                    identifier=upgrade["name"],
                    infos=infos,
                )
            )

            # buildings_buttons.append(Button(
            #     (adapt_size_width(1525, w), adapt_size_height(85, h) + (adapt_size_height(105, h)*i) + adapt_size_height((scroll_y * 1), h), adapt_size_width(300, w), adapt_size_height(45, w)),
            #     (w, h), background=BLUE, border_radius=20,
            #     command=lambda b=build_name: buy_building_wrapper(b), identifier=build["name"]
            # ))

        pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)
        for event in pg.event.get():
            if event.type == pg.QUIT or (
                event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE
            ):
                print("exiting...")
                save_data(
                    appdata_path,
                    timeUnits,
                    tps,
                    timeline,
                    clicker_amount,
                    bought_buildings,
                    max_timeUnits,
                    bought_upgrades,
                )
                running = False
            elif event.type == pg.KEYDOWN and event.key == pg.K_F7:
                if LOGGER.get_level() == 4:
                    LOGGER.INFO("Setting log level to WARNING")
                    LOGGER.set_level(3)
                else:
                    LOGGER.INFO("Setting log level to DEBUG")
                    LOGGER.set_level(4)
            elif event.type == pg.KEYDOWN and event.key == pg.K_F11:
                if is_maximized:
                    window.restore()
                    is_maximized = False
                else:
                    window.maximize()
                    is_maximized = True

            elif event.type == pg.MOUSEWHEEL and len(available_buildings) > 6:
                LOGGER.DEBUG(f"scroll offset: {event.y}")
                if can_scroll_up or event.y > 0:
                    scroll_y += event.y * scroll_speed
                    scroll_y = min(scroll_y, 0)

            elif event.type == pg.MOUSEWHEEL and len(available_upgrades) > 20:
                if can_scroll_up_bis or event.y > 0:
                    scroll_y_bis += event.y * scroll_speed
                    scroll_y_bis = min(scroll_y_bis, 0)

            if event.type == pg.MOUSEMOTION:
                clicker_button.get_event(event)

                is_clickable = False
                for build_button in buildings_buttons:
                    rel_x, rel_y = (
                        event.pos[0] - scroll_area_rect.x,
                        event.pos[1] - scroll_area_rect.y,
                    )
                    if (
                        0 <= rel_x < scroll_area_rect.width
                        and 0 <= rel_y < scroll_area_rect.height
                    ):
                        is_clickable = True

                is_clickable_bis = False
                for upgrade_button in upgrades_buttons:
                    rel_x, rel_y = (
                        event.pos[0] - scroll_area_rect_bis.x,
                        event.pos[1] - scroll_area_rect_bis.y,
                    )
                    if (
                        0 <= rel_x < scroll_area_rect_bis.width
                        and 0 <= rel_y < scroll_area_rect_bis.height
                    ):
                        is_clickable_bis = True

            for build_button in buildings_buttons:
                build_button.get_event(event)

            for upgrade_button in upgrades_buttons:
                upgrade_button.get_event(event)

            clicker_button.get_event(event)

        mouse_pos = pg.mouse.get_pos()
        for build_button in buildings_buttons:
            button_rect = build_button.rect
            if scroll_area_rect.colliderect(button_rect) and is_clickable:
                build_button.update_hover_state(mouse_pos)

        for upgrade_button in upgrades_buttons:
            button_rect = upgrade_button.rect
            if scroll_area_rect_bis.colliderect(button_rect) and is_clickable_bis:
                upgrade_button.update_hover_state(mouse_pos)

        screen.blit(
            shop_fond_image, (adapt_size_width(1475, w), adapt_size_height(45, h))
        )
        screen.blit(
            upgrade_fond_image, (adapt_size_width(45, w), adapt_size_height(245, h))
        )

        match era:
            case 1:
                base = f"{src_dir}/img/buildings/base_1.png"
            case 2:
                base = f"{src_dir}/img/buildings/base_2.png"
            case 3:
                base = f"{src_dir}/img/buildings/base_3.png"
            case 4:
                base = f"{src_dir}/img/buildings/base_4.png"
            case 5:
                base = f"{src_dir}/img/buildings/base_5.png"
        for i in range(len(buildings_buttons)):
            build_button = buildings_buttons[i]
            build = next(
                (
                    b
                    for b in bought_buildings["long_list"]
                    if b["name"] == build_button.identifier
                ),
                None,
            )
            if build is None:
                amount = 0
                cost = next(
                    (
                        b["cost"](1)
                        for b in buildings
                        if b["name"] == build_button.identifier
                    ),
                    None,
                )
            else:
                amount = build["amount"]
                cost = next(
                    (
                        b["cost"](amount + 1) - b["cost"](amount)
                        for b in buildings
                        if b["name"] == build_button.identifier
                    ),
                    None,
                )

            building_image = load_image(
                f"{src_dir}/img/buildings/{build_button.identifier.lower().replace(' ', '_')}.png",
                w,
                h,
            )
            base_image = load_image(base, w, h)

            # print(f"scroll_y: {scroll_y}({abs(adapt_size_height((scroll_y * 1), h))})")
            button_rect = build_button.rect.move(
                0, build_button.rect.height + adapt_size_height(7.5, h)
            )
            building_rect = building_image.get_rect(
                topleft=(adapt_size_width(1525, w), adapt_size_height(85 + 105 * i, h))
            ).move(0, adapt_size_height((scroll_y * 1), h))
            base_rect = base_image.get_rect(
                topleft=(adapt_size_width(1525, w), adapt_size_height(85 + 105 * i, h))
            ).move(0, adapt_size_height((scroll_y * 1), h))
            # build_button.rect = button_rect
            if not can_buy_buildings(
                bought_buildings, build_button.identifier, 1, timeUnits
            ):
                base_image.fill((100, 100, 100), special_flags=pg.BLEND_MULT)
                screen.blit(base_image, base_rect.topleft)

                building_image.fill((100, 100, 100), special_flags=pg.BLEND_MULT)
                screen.blit(building_image, building_rect.topleft)

                screen.blit(
                    get_text_font(25, h).render(
                        f"{format_timeUnits(round(cost))}", True, DARK_BROWN
                    ),
                    (
                        adapt_size_width(1592, w),
                        adapt_size_height(132 + 104.5 * i, h)
                        + adapt_size_height((scroll_y * 1), h),
                    ),
                )
                screen.blit(
                    get_text_font(19, h).render(
                        f"{format_time_no_convertion(amount)}", True, GREY
                    ),
                    (
                        adapt_size_width(1780, w),
                        adapt_size_height(132.5 + 104.5 * i, h)
                        + adapt_size_height((scroll_y * 1), h),
                    ),
                )

                build_button.render(screen, True, w, h)
            else:
                screen.blit(base_image, base_rect.topleft)

                screen.blit(building_image, building_rect.topleft)

                screen.blit(
                    get_text_font(25, h).render(
                        f"{format_timeUnits(round(cost))}", True, BROWN
                    ),
                    (
                        adapt_size_width(1592, w),
                        adapt_size_height(132 + 104.5 * i, h)
                        + adapt_size_height((scroll_y * 1), h),
                    ),
                )
                screen.blit(
                    get_text_font(19, h).render(
                        f"{format_time_no_convertion(amount, 6)}", True, WHITE
                    ),
                    (
                        adapt_size_width(1750, w),
                        adapt_size_height(132.5 + 104.5 * i, h)
                        + adapt_size_height((scroll_y * 1), h),
                    ),
                )

                build_button.render(screen, w=w, h=h)
            if scroll_area_rect.colliderect(
                button_rect
            ) and button_rect.top >= scroll_area_rect.top + adapt_size_height(50, h):
                if i == len(buildings_buttons) - 1:
                    if can_scroll_up:
                        can_scroll_up = False
                else:
                    if not can_scroll_up:
                        can_scroll_up = True

        y = 220
        x = 100
        for i in range(len(upgrades_buttons)):
            upgrade_button = upgrades_buttons[i]
            upgrade = next(
                (b for b in UPGRADES if b["name"] == upgrade_button.identifier), None
            )
            upgrade_level = next(
                (
                    u["level"]
                    for u in bought_upgrades["long_list"]
                    if u["name"] == upgrade_button.identifier
                ),
                0,
            )
            max_bought_level = next(
                (
                    u["level"]
                    for u in bought_upgrades["long_list"]
                    if u["name"] == upgrade["name"]
                ),
                0,
            )
            xth_build_price = next(
                (
                    b["cost"](treshold[max_bought_level])
                    for b in buildings
                    if b["name"] == upgrade["building_name"]
                ),
                0,
            ) - next(
                (
                    b["cost"](treshold[max_bought_level] - 1)
                    for b in buildings
                    if b["name"] == upgrade["building_name"]
                ),
                0,
            )

            if upgrade is None:
                cost = 0
            else:
                cost = xth_build_price * 3

            # print(f"{upgrade_button.identifier} ({i}) : ", end='')

            upgrade_image = load_image(
                f"{src_dir}/img/upgrades/{upgrade_button.identifier.lower().replace(' ', '_')}.png",
                w,
                h,
            )
            level_image = load_image(
                f"{src_dir}/img/upgrades/niv{upgrade_level}.png", w, h, 0.9
            )
            # y = 220
            if (i - 4) % 4 == 0:
                x = 100
                y += 117.5
                # print(f"x -> 1")
            else:
                x += 112.5
                # print(f"x -> 4")

            upgrade_button_rect = upgrade_button.rect.move(
                0, upgrade_button.rect.height + adapt_size_height(7.5, h)
            )
            upgrade_rect = upgrade_image.get_rect(
                topleft=(adapt_size_width(x, w), adapt_size_height(y, h))
            ).move(0, adapt_size_height((scroll_y_bis * 1), h))

            level_rect = level_image.get_rect(center=upgrade_rect.center).move(
                0, adapt_size_height(7, h)
            )

            if not can_buy_upgrade(
                bought_upgrades, upgrade_button.identifier, timeUnits, bought_buildings
            ):
                upgrade_image.fill((100, 100, 100), special_flags=pg.BLEND_MULT)
                screen.blit(upgrade_image, upgrade_rect.topleft)

                level_image.fill((100, 100, 100), special_flags=pg.BLEND_MULT)
                screen.blit(level_image, level_rect.topleft)

                screen.blit(
                    get_text_font(25, h).render(
                        f"{format_timeUnits(round(cost))}", True, GREY
                    ),
                    (adapt_size_width(x, w), adapt_size_height(y + 40, h)),
                )

                upgrade_button.render(screen, True, w, h)
            else:
                screen.blit(upgrade_image, upgrade_rect.topleft)

                # screen.blit(get_text_font(25, h).render(f"{format_timeUnits(round(cost))}", True, BROWN), (adapt_size_width(1592, w), adapt_size_height(132 + 104.5 * i, h) + adapt_size_height((scroll_y_bis * 1), h)))

                screen.blit(level_image, level_rect.topleft)
                if not upgrade_level == len(treshold):
                    screen.blit(
                        get_text_font(25, h).render(
                            f"{format_timeUnits(round(cost))}", True, WHITE
                        ),
                        (adapt_size_width(x, w), adapt_size_height(y + 40, h)),
                    )

                upgrade_button.render(screen, w=w, h=h)

            if scroll_area_rect_bis.colliderect(
                upgrade_button_rect
            ) and upgrade_button_rect.top >= scroll_area_rect_bis.top + adapt_size_height(
                50, h
            ):
                if i == len(upgrades_buttons) - 1:
                    if can_scroll_up_bis:
                        can_scroll_up_bis = False
                else:
                    if not can_scroll_up_bis:
                        can_scroll_up_bis = True

        screen.blit(load_image(f"{src_dir}/img/background.png", w, h), (0, 0))
        screen.blit(timeline_image, (adapt_size_width(45, w), adapt_size_height(45, h)))
        screen.blit(
            upgrade_bord_image, (adapt_size_width(45, w), adapt_size_height(245, h))
        )
        screen.blit(
            temporal_matrix_image, (adapt_size_width(605, w), adapt_size_height(45, h))
        )
        screen.blit(
            human_skill_and_boost, (adapt_size_width(1265, w), adapt_size_height(45, h))
        )
        screen.blit(
            shop_bord_image, (adapt_size_width(1475, w), adapt_size_height(45, h))
        )
        screen.blit(
            red_cable_image, (adapt_size_width(1285, w), adapt_size_height(860, h))
        )
        screen.blit(
            blue_cable_image, (adapt_size_width(1285, w), adapt_size_height(935, h))
        )

        screen.blit(
            timeUnits_text,
            timeUnits_text.get_rect(
                center=(adapt_size_width(870, w), adapt_size_height(865, h))
            ),
        )
        screen.blit(
            timeUnits_text_logo,
            timeUnits_text_logo.get_rect(
                midleft=timeUnits_text.get_rect(
                    center=(adapt_size_width(870, w), adapt_size_height(865, h))
                )
                .move(0, adapt_size_height(-5, h))
                .midright
            ),
        )
        screen.blit(
            tps_text,
            tps_text.get_rect(
                center=(adapt_size_width(882.5, w), adapt_size_height(212.5, h))
            ),
        )
        screen.blit(timeline_text, (adapt_size_width(90, w), adapt_size_height(87, h)))
        blue_cable_button.render(screen, w=w, h=h)

        # pg.draw.rect(screen, (0, 0, 255), scroll_area_rect_bis, 2)

        clicker_button.render(screen, w=w, h=h)

        for button in buildings_buttons:
            button.render_infos(screen, w=w, h=h)

        for button in upgrades_buttons:
            button.render_infos(screen, w=w, h=h)

        # # Render the scrollbar
        # total_height = len(buildings_buttons) * adapt_size_height(105, h)
        # visible_ratio = scroll_area_rect.height / total_height
        # scrollbar_height = max(scroll_area_rect.height * visible_ratio, 20)
        # scrollbar_y = scroll_area_rect.y - scroll_y * visible_ratio
        # pg.draw.rect(
        #     screen,
        #     (200, 200, 200),
        #     (scrollbar_rect.x, scrollbar_y, scrollbar_rect.width, scrollbar_height),
        # )

        pg.display.flip()
        elapsed_time = clock.get_time() / 1000.0  # Get elapsed time in seconds
        loop_number = int(elapsed_time // (1 / framerate))
        # print("-" * 50 + f" loop {loop_number} tick {current_frame}/{framerate}")
        save_count += 1
        # print(count)
        if save_count == framerate * 60:
            save_data(
                appdata_path,
                timeUnits,
                tps,
                timeline,
                clicker_amount,
                bought_buildings,
                max_timeUnits,
                bought_upgrades,
            )
            # cancel_save_timer()
            count = 0
            LOGGER.INFO("Data saved")


if __name__ == "__main__":
    main()
