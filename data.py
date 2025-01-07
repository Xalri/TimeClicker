import pygame

pygame.font.init()

TIMELINE_FONT: pygame.font = pygame.font.Font('src/fonts/LetterGothicStd-Bold.ttf', 124)
NUMBER_FONT: pygame.font = pygame.font.Font('src/fonts/LetterGothicStd-Bold.ttf', 52)
TEXT_FONT: pygame.font = pygame.font.Font('src/fonts/FranklinGothicHeavyRegular.ttf', 33)




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
BROWN = (88, 41, 0)
GRAY = (128, 128, 128)
TURQUOISE = (64, 224, 208)
SILVER = (192, 192, 192)
GOLD = (218, 165, 32)

BACKGROUND_COLOR = BROWN