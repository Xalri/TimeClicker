import pygame
import sys
import os
from base64 import b64decode, b64encode


def adapt_size_height(size, height, debug=False):
    if debug:
        print(int(round((size / 1080 * height))))
    return int(round(size / 1080 * height))
def adapt_size_width(size, width, debug=False):
    if debug:
        print(int(round(size / 1920 * width)))
    return int(round(size / 1920 * width))


def load_image(path, width, height):
    image: pygame.surface = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(
        image,
        (
            adapt_size_width(image.get_width(), width),
            adapt_size_height(image.get_height(), height),
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
    return pygame.font.Font(resource_path("src") + "/fonts/FranklinGothicHeavyRegular.ttf", int(adapt_size_height(size, height)))



def get_data(appdata_path):
    if not os.path.exists(os.path.join(appdata_path, 'data')):
        save_data(0, 0, 0, 1, {"short_list": [], "long_list": []}, 0)
    
    print("path is: " + str(os.path.join(appdata_path, 'data')))
    with open(os.path.join(appdata_path, 'data'), 'r') as f:
        data = f.read()
        print(data)
        data = data[::-1]
        data = data + "=="
        data = b64decode(data.encode()).decode()
        data = data.split('\n')
        print(data)
        if data == ['']:
            save_data(appdata_path, 0, 0, 0, 1, {"short_list": [], "long_list": []}, 0)
            return 0, 0, 0, 1, {"short_list": [], "long_list": []}, 0
        timeUnits = float(data[0])
        tps = float(data[1])
        timeline = float(data[2])
        clicker_amount = int(data[3])
        buildings = eval(data[4]) # {'short_list': [], 'long_list': []}
        temp = data[5]
        return timeUnits, tps, timeline, clicker_amount, buildings, temp
    
def save_data(appdata_path, timeUnits=0, tps=0, timeline=0, clicker_amount=1, buildings={"short_list": [], "long_list": []}, max_timeUnits=0):    
            
    if max_timeUnits == 0:
        max_timeUnits = timeUnits
    print("path is: " + str(os.path.join(appdata_path, 'data')))
    with open(os.path.join(appdata_path, 'data'), 'w') as f:
        data = f"{timeUnits}\n{tps}\n{timeline}\n{clicker_amount}\n{buildings}\n{max_timeUnits}"
        data = b64encode(data.encode())
        print("saving data: " + str(data))
        data = data.decode().replace("=", "").replace("=", "")
        data = data[::-1]
        f.write(data)



def crop_value(value: float):
    if value == 0.0:
        return 0
    if value >= 10:
        return int(value)
    return round(value, 3)



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
