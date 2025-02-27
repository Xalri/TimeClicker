from pprint import pprint
import time
import pygame
import sys
import os
from base64 import b64decode, b64encode
import Timeline
from buildings import buildings
from datetime import datetime
from config import TIMELINE_UPGRADE_PRICE
from upgrade import TIMELINE_UPGRADE, UPGRADES, treshold
import upgrade
from data import UNITS
import ctypes
import threading


def adapt_size_height(size, height, debug=False):
    if debug:
        print(int(round((size / 1080 * height))))
    return int(round(size / 1080 * height))


def adapt_size_width(size, width, debug=False):
    if debug:
        print("Size: " + str(size))
        print("Size type: " + str(type(size)))
    return int(round(float(size) / 1920 * width))


def load_image(path, width, height, scale=1, debug=False):
    image: pygame.surface = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(
        image,
        (
            adapt_size_width(image.get_width(), width, debug) * scale,
            adapt_size_height(image.get_height(), height) * scale,
        ),
    )


def resource_path(relative_path):
    """Get the absolute path to the resource, works for dev and for PyInstaller"""
    if getattr(sys, "frozen", False):
        base_path = sys._MEIPASS  # Temporary folder for PyInstaller
    else:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path).replace("\\", "/")


def get_timeline_font(size, height):
    return pygame.font.Font(
        resource_path("src") + "/fonts/LetterGothicStd-Bold.ttf",
        int(adapt_size_height(size, height)),
    )


def get_number_font(size, height):
    return pygame.font.Font(
        resource_path("src") + "/fonts/LetterGothicStd-Bold.ttf",
        int(adapt_size_height(size, height)),
    )


def get_text_font(size, height):
    return pygame.font.Font(
        resource_path("src") + "/fonts/FranklinGothicHeavyRegular.ttf",
        int(adapt_size_height(size, height)),
    )


def get_data(appdata_path):
    if not os.path.exists(os.path.join(appdata_path, "data")):
        save_data(0, 0, 0, 1, {"short_list": [], "long_list": []}, 0)

    print("path is: " + str(os.path.join(appdata_path, "data")))
    with open(os.path.join(appdata_path, "data"), "r") as f:
        data = f.read()
        print(data)
        data = data[::-1]
        data = data + "=="
        data = b64decode(data.encode()).decode()
        data = data.split("\n")
        print(data)
        if data == [""] or len(data) < 9:
            save_data(appdata_path)
            return get_data(appdata_path)
        timeUnits = float(data[0])
        tps = float(data[1])
        timeline = int(float(data[2]))
        clicker_amount = int(float(data[3]))
        buildings = eval(data[4])  # {'short_list': [], 'long_list': []}
        temp = data[5]
        upgrades = eval(data[6])
        human_skills = eval(data[7])
        last_saved = data[8]
        return (
            timeUnits,
            tps,
            timeline,
            clicker_amount,
            buildings,
            temp,
            upgrades,
            human_skills,
            last_saved,
        )


def save_data(
    appdata_path,
    timeUnits=0,
    tps=0,
    timeline=-1,
    clicker_amount=1,
    buildings={"short_list": [], "long_list": []},
    max_timeUnits=0,
    bought_upgrades={"short_list": [], "long_list": []},
    human_skills={"agility":0, "intelligence":0, "strength":0},
    last_saved_time="None",
):
    
    now = datetime.now().strftime(" %Y-%m-%d %H:%M:%S")
    if last_saved_time == "None": last_saved_time = now
    
    if max_timeUnits == 0:
        max_timeUnits = timeUnits

    print(f"Saving data to: {os.path.join(appdata_path, 'data')}")
    print(f"Time Units: {timeUnits}")
    print(f"TPS: {tps}")
    print(f"Timeline: {timeline}")
    print(f"Clicker Amount: {clicker_amount}")
    pprint(f"Buildings: {buildings}")
    print(f"Max Time Units: {max_timeUnits}")
    print(f"Bought Upgrades: {bought_upgrades}")
    print(f"Human Skills: {human_skills}")
    print(f"Last Saved Time: {last_saved_time} ({now})")


    with open(os.path.join(appdata_path, "data"), "w") as f:
        data = f"{timeUnits}\n{tps}\n{timeline}\n{clicker_amount}\n{buildings}\n{max_timeUnits}\n{bought_upgrades}\n{human_skills}\n{last_saved_time}"
        data = b64encode(data.encode())
        print("Encoded data: " + str(data))
        data = data.decode().replace("=", "").replace("=", "")
        data = data[::-1]
        f.write(data)


def crop_value(value: float):
    if value == 0.0:
        return 0
    if value >= 10:
        return int(round(value))
    return round(value, 1)


def format_timeUnits(timeUnits: float, n=0):
    timeUnits = crop_value(timeUnits)
    if timeUnits < 1000:
        return "".join([" " for _ in range(n + 2 - len(str(timeUnits)))]) + str(
            timeUnits
        )
    for unit, factor in zip(
        UNITS,
        [10**i for i in range(3, (len(UNITS) * 3) + 1, 3)],
    ):
        if timeUnits < factor * 1000:
            timeUnits = f"{timeUnits / factor:.1f}{unit}".rstrip(".0")
            return (
                "".join(
                    [
                        " "
                        for _ in range(
                            n - len(timeUnits.replace(".", "").replace(unit, ""))
                        )
                    ]
                )
                + timeUnits
            )
    return f"{timeUnits:.0f}"


def format_time_no_convertion(value: int, n: int = 0):
    return "".join([" " for _ in range(n + 2 - len(str(value)))]) + str(value)


def can_buy_buildings(bought_buildings, building_name, amount, timeUnits):
    building = next((b for b in buildings if b["name"] == building_name), None)
    if building is None:
        return False

    current_amount = next(
        (
            b["amount"]
            for b in bought_buildings["long_list"]
            if b["name"] == building_name
        ),
        0,
    )
    cost = sum(building["cost"](current_amount + i) for i in range(amount))

    return timeUnits >= cost


def buy_buildings(bought_buildings, building_name, amount, timeUnits, price_reduction):
    print(building_name)
    building = next((b for b in buildings if b["name"] == building_name), None)
    print(building)
    if building is None:
        return bought_buildings
    current_amount = next(
        (
            b["amount"]
            for b in bought_buildings["long_list"]
            if b["name"] == building_name
        ),
        0,
    )
    print(current_amount)
    # cost = round(
    #     building["cost"](current_amount + amount) - building["cost"](current_amount)
    # )
    cost = sum(building["cost"](current_amount + i) for i in range(amount)) * price_reduction
    print(cost)

    if timeUnits >= cost:
        if not building_name in bought_buildings["short_list"]:
            bought_buildings["short_list"].append(building_name)
            bought_buildings["long_list"].append(
                {"name": building_name, "amount": amount, "upgrade_boost":1}
            )
        else:
            for b in bought_buildings["long_list"]:
                if b["name"] == building_name:
                    b["amount"] += amount
                    break
        timeUnits -= cost
    return bought_buildings, timeUnits


def buy_upgrades(bought_upgrades, upgrade_name, timeUnits, bought_buildings, price_reduction):
    print("")
    print("bought upgrades: ", bought_upgrades)
    print("bought buildings: ", bought_buildings)
    print("upgrade name: ", upgrade_name)
    upgrade = next((u for u in UPGRADES if u["name"] == upgrade_name), None)
    build_amount = next(
        (
            b["amount"]
            for b in bought_buildings["long_list"]
            if b["name"] == upgrade["building_name"]
        ),
        0,
    )
    print("upgrade: ", upgrade)
    print("build name: ", next(b for b in bought_buildings["long_list"] if b["name"] == upgrade["building_name"]))
    print("build amount: ", build_amount)
    if upgrade is None:
        return bought_upgrades, timeUnits, bought_buildings

    max_bought_level = next(
        (
            u["level"]
            for u in bought_upgrades["long_list"]
            if u["name"] == upgrade["name"]
        ),
        0,
    )
    print("max bought level: ", max_bought_level)
    if max_bought_level == len(treshold):
        return bought_upgrades, timeUnits, bought_buildings
    
    xth_build_price = next((b["cost"](treshold[max_bought_level]) for b in buildings if b["name"] == upgrade["building_name"]), 0)

    cost= xth_build_price*3*price_reduction

    print(timeUnits >= cost)
    
    # print(build_amount >= treshold[max_bought_level])
    if max_bought_level == len(treshold):
        return bought_upgrades, timeUnits, bought_buildings
    if timeUnits >= cost and build_amount >= treshold[max_bought_level]:
        build = next(
            (b for b in buildings if b["name"] == upgrade["building_name"]), None
        )
        print("build: ", build)

        if build is None:
            return bought_upgrades, timeUnits, bought_buildings

        for b in bought_buildings["long_list"]:
            if b["name"] == build["name"]:
                b["upgrade_boost"] *= upgrade["effect_value"]

        if not upgrade_name in bought_upgrades["short_list"]:
        
            bought_upgrades["short_list"].append(upgrade_name)
            bought_upgrades["long_list"].append(
                {"name": upgrade_name, "level": max_bought_level + 1}
            )
        else:
            for u in bought_upgrades["long_list"]:
                if u["name"] == upgrade_name:
                    u["level"] += 1
        timeUnits -= cost

    print("bought upgrades: ", bought_upgrades)
    print("bought buildings: ", bought_buildings)
    return bought_upgrades, timeUnits, bought_buildings


def can_buy_upgrade(bought_upgrades, upgrade_name, timeUnits, bought_buildings):
    upgrade = next((u for u in UPGRADES if u["name"] == upgrade_name), None)
    if upgrade is None:
        return False
    
    build_amount = next((b["amount"] for b in bought_buildings["long_list"] if b["name"] == upgrade["building_name"]), 0)
    max_bought_level = next((u["level"] for u in bought_upgrades["long_list"] if u["name"] == upgrade["name"]), 0)
    
    if max_bought_level == len(treshold):
        return True
    
    xth_build_price = next((b["cost"](treshold[max_bought_level]) for b in buildings if b["name"] == upgrade["building_name"]), 0)
    return timeUnits >= xth_build_price*3 and build_amount >= treshold[max_bought_level]


def show_message(msg):
    ctypes.windll.user32.MessageBoxW(0, msg, "Debug Message", 1)

def unlock_timeline(era, timeline, timeUnits):
    if era == 1:
        cost = TIMELINE_UPGRADE_PRICE
        if not timeUnits >= cost:
            return timeline, timeUnits
        return era+1, timeline+1, timeUnits - cost

def buy_timeline(timeline, timeUnits):
    cost = TIMELINE_UPGRADE["cost"](timeline)
    if not timeUnits >= cost or timeline >= 2500:
        return timeline, timeUnits
    return timeline + 1, timeUnits - cost

    
def can_buy_timeline(timeline, timeUnits, era):
    if era == 1:
        return timeUnits >= TIMELINE_UPGRADE_PRICE
    return timeline >= 2500 or timeUnits >= TIMELINE_UPGRADE["cost"](timeline)

def buy_human_skill(human_skills: dict, timeUnits: float, skill_name: str):
    print(human_skills)
    print(timeUnits)
    print(skill_name)
    if not skill_name in list(human_skills.keys()) and human_skills[skill_name] >= 100:
        return human_skills, timeUnits
    
    cost = 200 * (2**human_skills[skill_name])
    print(cost)
    if not timeUnits >= cost:
        return human_skills, timeUnits
    
    human_skills[skill_name] +=1
    print(human_skills)
    print(timeUnits-cost)
    print(" ")
    return human_skills, timeUnits-cost
    
