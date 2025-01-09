import pygame

def adapt_size_height(size, height):
    return size / 1080 * height
def adapt_size_width(size, width):
    return size / 1920 * width

def load_image(path, width, height):
    image: pygame.surface = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(image, (adapt_size_width(image.get_width(), width), adapt_size_height(image.get_height(), height)))


def get_timeline_font(size, height):
    return pygame.font.Font('src/fonts/LetterGothicStd-Bold.ttf', int(adapt_size_height(size, height)))
def get_number_font(size, height):
    return pygame.font.Font('src/fonts/LetterGothicStd-Bold.ttf', int(adapt_size_height(size, height)))
def  get_text_font(size, height):
    return pygame.font.Font('src/fonts/FranklinGothicHeavyRegular.ttf', int(adapt_size_height(size, height)))
