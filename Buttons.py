import pygame as pg

class Button:
    def __init__(self, rect, command):
        self.color = (255,0,0)
        self.rect = pg.Rect(rect)
        self.image = pg.Surface(self.rect.size)
        self.image.fill(self.color)
        self.command = command
    def render(self, screen):
        screen.blit(self.image, self.rect)
    def get_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(pg.mouse.get_pos()):
                self.command()