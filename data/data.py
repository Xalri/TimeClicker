import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
# Basics
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
# Colorful
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
PURPLE = (255, 0, 255)
# Special
ORANGE = (255, 127, 0)
MAGENTA = (255, 0, 255)
PINK = (255, 192, 203)
BROWN = (138,97,53)
DARK_BROWN = (54, 38, 20)
GREY = (100, 100, 100)
TURQUOISE = (64, 224, 208)
SILVER = (192, 192, 192)
GOLD = (218, 165, 32)
# Custom
LIGHT_GREY = (90, 97, 107)
DARK_GREY = (53, 53, 53)
LIGHT_DARK = (28, 28, 28)
YELLOW_GREEN = (223, 241, 103)
RED_OCHRE = (240, 74, 56)
DARK_ORANGE = (168,54,9)
MUSTARD = (198,170,9)
LIGHT_GREEN = (10,150,10)
CABLE_BLUE = (0, 109, 214)
CLOCK_GREEN = (59, 210, 0)
LIGHT_CYAN = (96, 196, 171)


UNITS = [
    "k",
    "M",
    "B",
    "T",
    "Qa",
    "Qi",
    "Sx",
    "Sp",
    "Oc",
    "No",
    "Dc",
    "Ud",
    "Dd",
    "Td",
    "Qd",
    "Qn",
    "Sxd",
    "Spd",
    "Ocd",
    "Nod",
    "Vg",
    "Uv",
    "Dv",
    "Tv",
    "Qav",
    "Qiv",
    "Sxv",
    "Spv",
    "Ocv",
    "Nov",
    "Tg",
    "Utg",
    "Dtg",
    "Ttg",
    "Qatg",
    "Qitg",
    "Sxtg",
    "Sptg",
    "Octg",
    "Notg",
    "Qag",
    "Uqag",
    "Dqag",
    "Tqag",
    "Qaqag",
    "Qiqag",
    "Sxqag",
    "Spqag",
    "Ocqag",
    "Noqag",
    "Qig",
    "Uqig",
    "Dqig",
    "Tqig",
    "Qaqig",
    "Qiqig",
    "Sxqig",
    "Spqig",
    "Ocqig",
    "Noqig",
    "Sxg",
    "Usxg",
    "Dsxg",
    "Tsxg",
    "Qasxg",
    "Qisxg",
    "Sxsxg",
    "Spsxg",
    "Ocsxg",
    "Nosxg",
    "Spg",
    "Uspg",
    "Dspg",
    "Tspg",
    "Qaspg",
    "Qispg",
    "Sxspg",
    "Spspg",
    "Ocspg",
    "Nospg",
    "Ocg",
    "Uocg",
    "Docg",
    "Tocg",
    "Qaocg",
    "Qiocg",
    "Sxocg",
    "Spocg",
    "Ococg",
    "Noocg",
    "Nog",
    "Unog",
    "Dnog",
    "Tnog",
    "Qanog",
    "Qinog",
    "Sxnog",
    "Spnog",
    "Ocnog",
    "Nonog",
]