import pygame
from pygame._sdl2 import Window
from data import *

#comentaire
screen = pygame.display.set_mode((720, 480), pygame.RESIZABLE)

Window.from_display_module().maximize()

pygame.display.set_caption('Time Clicker')

screen.fill(BACKGROUND_COLOR)

pygame.display.flip()

running = True

while running:
    
    for event in pygame.event.get():
    
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False