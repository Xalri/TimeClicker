from pprint import pprint
import time
import pygame
import sys
import os
from base64 import b64decode, b64encode
from data.buildings import buildings
from datetime import datetime
from config import TIMELINE_UPGRADE_PRICE
from data.upgrade import TIMELINE_UPGRADE, UPGRADES, treshold
import data.upgrade as upgrade
from data.data import UNITS
import ctypes
import threading


def adapt_size_height(size, height, debug=False):
    """
    Adapt the size based on the height.

    :param int size: The original size.
    :param int height: The height to adapt to.
    :param bool debug: Whether to print debug information.
    :return int: The adapted size.
    """
    if debug:
        print(int(round((size / 1080 * height))))
    return int(round(size / 1080 * height))


def adapt_size_width(size, width, debug=False):
    """
    Adapt the size based on the width.

    :param int size: The original size.
    :param int width: The width to adapt to.
    :param bool debug: Whether to print debug information.
    :return int: The adapted size.
    """
    if debug:
        print("Size: " + str(size))
        print("Size type: " + str(type(size)))
    return int(round(float(size) / 1920 * width))


def load_image(path, width, height, scale=1, debug=False):
    """
    Load and scale an image.

    :param str path: The path to the image.
    :param int width: The width to scale to.
    :param int height: The height to scale to.
    :param float scale: The scaling factor.
    :param bool debug: Whether to print debug information.
    :return pygame.Surface: The loaded and scaled image.
    """
    image: pygame.surface = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(
        image,
        (
            adapt_size_width(image.get_width(), width, debug) * scale,
            adapt_size_height(image.get_height(), height) * scale,
        ),
    )


def resource_path(relative_path):
    """
    Get the absolute path to the resource, works for dev and for PyInstaller.

    :param str relative_path: The relative path to the resource.
    :return str: The absolute path to the resource.
    """
    if getattr(sys, "frozen", False):
        base_path = sys._MEIPASS  # Temporary folder for PyInstaller
    else:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path).replace("\\", "/")


def get_timeline_font(size, height):
    """
    Get the font for the timeline.

    :param int size: The font size.
    :param int height: The height to adapt to.
    :return pygame.font.Font: The timeline font.
    """
    return pygame.font.Font(
        resource_path("src") + "/fonts/LetterGothicStd-Bold.ttf",
        int(adapt_size_height(size, height)),
    )


def get_number_font(size, height):
    """
    Get the font for numbers.

    :param int size: The font size.
    :param int height: The height to adapt to.
    :return pygame.font.Font: The number font.
    """
    return pygame.font.Font(
        resource_path("src") + "/fonts/LetterGothicStd-Bold.ttf",
        int(adapt_size_height(size, height)),
    )


def get_text_font(size, height):
    """
    Get the font for text.

    :param int size: The font size.
    :param int height: The height to adapt to.
    :return pygame.font.Font: The text font.
    """
    return pygame.font.Font(
        resource_path("src") + "/fonts/FranklinGothicHeavyRegular.ttf",
        int(adapt_size_height(size, height)),
    )

def get_clock_font(size, height):
    """
    Get the font for the clock.

    :param int size: The font size.
    :param int height: The height to adapt to.
    :return pygame.font.Font: The clock font.
    """
    return pygame.font.Font(
        resource_path("src") + "/fonts/DS-DIGIB.TTF",
        int(adapt_size_height(size, height)),
    )

def get_data(appdata_path):
    """
    Get the game data from the storage.

    :param str appdata_path: The path to the app data.
    :return tuple: The game data.
    """
    if not os.path.exists(os.path.join(appdata_path, "data")):
        save_data(appdata_path)

    print("path is: " + str(os.path.join(appdata_path, "data")))
    with open(os.path.join(appdata_path, "data"), "r") as f:
        data = f.read()
        print(data)
        data = data[::-1]
        data = data + "=="
        data = b64decode(data.encode()).decode()
        data = data.split("\n")
        # print(data)
        if data == [""]:
            save_data(appdata_path)
            return get_data(appdata_path)
        
        # Set default values
        default_values = {
            "timeUnits": 0.0,
            "tps": 0.0,
            "timeline": -1,
            "clicker_amount": 1,
            "buildings": {"short_list": [], "long_list": []},
            "temp": "",
            "upgrades": {"short_list": [], "long_list": []},
            "human_skills": {"agility": 0, "intelligence": 0, "strength": 0},
            "last_saved": datetime.now().strftime(" %Y-%m-%d %H:%M:%S"),
            "prestige": 0
        }

        # Assign values or default if missing
        timeUnits = float(data[0]) if len(data) > 0 else default_values["timeUnits"]
        tps = float(data[1]) if len(data) > 1 else default_values["tps"]
        timeline = int(float(data[2])) if len(data) > 2 else default_values["timeline"]
        clicker_amount = int(float(data[3])) if len(data) > 3 else default_values["clicker_amount"]
        buildings = eval(data[4]) if len(data) > 4 else default_values["buildings"]
        temp = data[5] if len(data) > 5 else default_values["temp"]
        upgrades = eval(data[6]) if len(data) > 6 else default_values["upgrades"]
        human_skills = eval(data[7]) if len(data) > 7 else default_values["human_skills"]
        last_saved = data[8] if len(data) > 8 else default_values["last_saved"]
        prestige = data[9] if len(data) > 9 else default_values["prestige"]

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
            prestige
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
    prestige=0,
    last_saved_time="None"
):
    """
    Save the game data to the storage.

    :param str appdata_path: The path to the app data.
    :param float timeUnits: The time units.
    :param float tps: The time units per second.
    :param int timeline: The timeline.
    :param int clicker_amount: The clicker amount.
    :param dict buildings: The buildings data.
    :param float max_timeUnits: The maximum time units.
    :param dict bought_upgrades: The bought upgrades data.
    :param dict human_skills: The human skills data.
    :param str last_saved_time: The last saved time.
    """
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
    print(f"Prestige: {prestige}")


    with open(os.path.join(appdata_path, "data"), "w") as f:
        data = f"{timeUnits}\n{tps}\n{timeline}\n{clicker_amount}\n{buildings}\n{max_timeUnits}\n{bought_upgrades}\n{human_skills}\n{last_saved_time}\n{prestige}"
        data = b64encode(data.encode())
        print("Encoded data: " + str(data))
        data = data.decode().replace("=", "").replace("=", "")
        data = data[::-1]
        f.write(data)


def crop_value(value: float):
    """
    Crop the value to an integer or a rounded float.

    :param float value: The value to crop.
    :return int|float: The cropped value.
    """
    if value == 0.0:
        return 0
    if value >= 10:
        return round(value)
    return round(value, 1)


def format_timeUnits(timeUnits: float, n=0):
    """
    Format the time units.

    :param float timeUnits: The time units to format.
    :param int n: The number of spaces to pad.
    :return str: The formatted time units.
    """
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
    """
    Format the time without conversion.

    :param int value: The value to format.
    :param int n: The number of spaces to pad.
    :return str: The formatted time.
    """
    return "".join([" " for _ in range(n + 2 - len(str(value)))]) + str(value)


def can_buy_buildings(bought_buildings, building_name, amount, timeUnits, reduction=1):
    """
    Check if the player can buy buildings.

    :param dict bought_buildings: The bought buildings data.
    :param str building_name: The name of the building.
    :param int amount: The amount to buy.
    :param float timeUnits: The time units available.
    :param float reduction: The price reduction factor.
    :return bool: True if the player can buy the buildings, False otherwise.
    """
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
    cost = sum(building["cost"](current_amount + i) for i in range(amount))*reduction

    return timeUnits >= cost


def buy_buildings(bought_buildings, building_name, amount, timeUnits, price_reduction):
    """
    Buy buildings.

    :param dict bought_buildings: The bought buildings data.
    :param str building_name: The name of the building.
    :param int amount: The amount to buy.
    :param float timeUnits: The time units available.
    :param float price_reduction: The price reduction factor.
    :return tuple: The updated bought buildings data and the remaining time units.
    """
    print(building_name)
    building = next((b for b in buildings if b["name"] == building_name), None)
    print(building)
    assert building is not None, f"Building {building_name} not found"
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
    """
    Buy upgrades.

    :param dict bought_upgrades: The bought upgrades data.
    :param str upgrade_name: The name of the upgrade.
    :param float timeUnits: The time units available.
    :param dict bought_buildings: The bought buildings data.
    :param float price_reduction: The price reduction factor.
    :return tuple: The updated bought upgrades data, remaining time units, and bought buildings data.
    """
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
    assert upgrade is not None, f"Upgrade {upgrade_name} not found"
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


def can_buy_upgrade(bought_upgrades, upgrade_name, timeUnits, bought_buildings, reduction=1):
    """
    Check if the player can buy an upgrade.

    :param dict bought_upgrades: The bought upgrades data.
    :param str upgrade_name: The name of the upgrade.
    :param float timeUnits: The time units available.
    :param dict bought_buildings: The bought buildings data.
    :param float reduction: The price reduction factor.
    :return bool: True if the player can buy the upgrade, False otherwise.
    """
    upgrade = next((u for u in UPGRADES if u["name"] == upgrade_name), None)
    if upgrade is None:
        return False
    
    build_amount = next((b["amount"] for b in bought_buildings["long_list"] if b["name"] == upgrade["building_name"]), 0)
    max_bought_level = next((u["level"] for u in bought_upgrades["long_list"] if u["name"] == upgrade["name"]), 0)
    
    if max_bought_level == len(treshold):
        return True
    
    xth_build_price = next((b["cost"](treshold[max_bought_level]) for b in buildings if b["name"] == upgrade["building_name"]), 0)*reduction
    return timeUnits >= xth_build_price*3 and build_amount >= treshold[max_bought_level]


def show_message(msg):
    """
    Show a message box.

    :param str msg: The message to display.
    """
    ctypes.windll.user32.MessageBoxW(0, msg, "Debug Message", 1)

def unlock_timeline(era, timeline, timeUnits):
    """
    Unlock the timeline.

    :param int era: The current era.
    :param int timeline: The current timeline.
    :param float timeUnits: The time units available.
    :return tuple: The updated era, timeline, and remaining time units.
    """
    assert TIMELINE_UPGRADE_PRICE is not None and isinstance(TIMELINE_UPGRADE_PRICE, int), "TIMELINE_UPGRADE_PRICE must be an integer"
    if era == 1:
        cost = TIMELINE_UPGRADE_PRICE
        if not timeUnits >= cost:
            return timeline, timeUnits
        return era+1, timeline+1, timeUnits - cost

def buy_timeline(timeline, timeUnits):
    """
    Buy a timeline.

    :param int timeline: The current timeline.
    :param float timeUnits: The time units available.
    :return tuple: The updated timeline and remaining time units.
    """
    cost = TIMELINE_UPGRADE["cost"](timeline)
    if not timeUnits >= cost or timeline >= 2500:
        return timeline, timeUnits
    return timeline + 1, timeUnits - cost

    
def can_buy_timeline(timeline, timeUnits, era):
    """
    Check if the player can buy a timeline.

    :param int timeline: The current timeline.
    :param float timeUnits: The time units available.
    :param int era: The current era.
    :return bool: True if the player can buy the timeline, False otherwise.
    """
    if era == 1:
        return timeUnits >= TIMELINE_UPGRADE_PRICE
    return timeline >= 2500 or timeUnits >= TIMELINE_UPGRADE["cost"](timeline)

def buy_human_skill(human_skills: dict, timeUnits: float, skill_name: str):
    """
    Buy a human skill.

    :param dict human_skills: The human skills data.
    :param float timeUnits: The time units available.
    :param str skill_name: The name of the skill to buy.
    :return tuple: The updated human skills data and remaining time units.
    """
    print(human_skills)
    print(timeUnits)
    print(skill_name)
    assert skill_name in list(human_skills.keys()), "skill_name must be a key in human_skills"
    if not skill_name in list(human_skills.keys()) and human_skills[skill_name] >= 100:
        return human_skills, timeUnits
    
    cost = 200 * (2**human_skills[skill_name])
    print(cost)
    if not timeUnits >= cost:
        return human_skills, timeUnits
    if human_skills[skill_name] >= 100:
        return human_skills, timeUnits
    human_skills[skill_name] +=1
    print(human_skills)
    print(timeUnits-cost)
    print(" ")
    return human_skills, timeUnits-cost
    
def can_buy_human_skill(human_skills: dict, timeUnits: float, skill_name: str):
    """
    Check if the player can buy a human skill.

    :param dict human_skills: The human skills data.
    :param float timeUnits: The time units available.
    :param str skill_name: The name of the skill to buy.
    :return bool: True if the player can buy the skill, False otherwise.
    """
    if not skill_name in list(human_skills.keys()) and human_skills[skill_name] >= 100:
        return human_skills, timeUnits
    
    cost = 200 * (2**human_skills[skill_name])
    print(cost)
    return timeUnits >= cost and human_skills[skill_name] < 100

def get_dependencies_folder():
    """
    Get the dependencies folder.

    :return str: The path to the dependencies folder.
    """
    if getattr(sys, 'frozen', False):
        exe_folder = os.path.dirname(sys.executable)
    else:
        exe_folder = os.path.dirname(os.path.realpath(__file__))

    appdata_folder = os.path.join(os.getenv('LOCALAPPDATA'), 'TimeClicker', 'dependencies')
    
    if os.path.exists(appdata_folder):
        print(f"Found dependencies in AppData at: {appdata_folder}")
        return appdata_folder
    else:
        print("Dependencies not found in AppData.")
        return None

def load_dependency(dependency_folder):
    """
    Load a dependency from the specified folder.

    :param str dependency_folder: The path to the dependency folder.
    """
    dependency_file = os.path.join(dependency_folder, 'your_dependency.dll')
    
    if os.path.exists(dependency_file):
        print(f"Found dependency: {dependency_file}")
        ctypes.CDLL(dependency_file)
    else:
        print(f"Dependency not found: {dependency_file}")

