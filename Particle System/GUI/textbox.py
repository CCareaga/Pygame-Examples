import pygame
from pygame.locals import *
import sys

class TextBox():
    '''Text box class, simple right now, being worked on'''
    def __init__(self, frame, pos,  **kwargs):

        self.frame = frame
        self.keys = []
        self.text = ''

        self.pos = pos

        self.focused = False

        self.image = pygame.Surface((30, 20))
        self.outline = pygame.Surface((32, 22))
        self.outline.fill(0)
        self.rect = self.image.get_rect(topleft=self.pos)
        self.frame_rect = self.frame.off(self.rect.copy())

        self.cursor = pygame.Surface((2, 14))
        self.c_rect = self.cursor.get_rect(y=3)

        self.process_kwargs(kwargs)

        self.frame.widgets.append(self)

    def process_kwargs(self, kwargs):
        defaults = { "font" : pygame.font.SysFont('Calibri', 16),
                    "color" : pygame.Color("white"),
                    "font_color" : pygame.Color("black")
                    }

        for kwarg in kwargs:
            if kwarg in defaults:
                defaults[kwarg] = kwargs[kwarg]
            else:
                raise KeyError("InputBox accepts no keyword {}.".format(kwarg))
        self.__dict__.update(defaults)

    def check_events(self, event):
        self.get_char(event)
        self.check_click(event)

    def get_char(self, event):
        if event.type == pygame.KEYDOWN and self.focused:
            if event.key == K_BACKSPACE:
                self.keys = self.keys[:-1]
            elif event.key <= 255:
                char = chr(event.key)
                self.keys.append(char)

    def check_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.onfocus(event)

    def onfocus(self, event):
        if self.frame_rect.collidepoint(event.pos):
            self.focused = True
        else:
            self.focused = False

    def update(self):
        self.image.fill(self.color)

        self.text_surf = self.font.render(self.text, True, self.font_color)
        self.text_rect = self.image.get_rect(topleft=(2,2))

        self.test = self.text_surf.get_rect()
        self.c_rect.x = self.test.right+2

        if self.focused:
            self.text = ''.join(self.keys)
            self.image.blit(self.cursor, (self.c_rect))

        self.image.blit(self.text_surf, (self.text_rect))

    def draw(self, surface):
        surface.blit(self.outline, (self.rect.move(-1, -1)))
        surface.blit(self.image, (self.rect))