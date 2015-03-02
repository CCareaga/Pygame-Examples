import pygame
from pygame.locals import *
import sys


class Label():
    '''Basic label class'''
    def __init__(self, frame, text, **kwargs):

        self.frame = frame
        self.text = text

        self.process_kwargs(kwargs)

        self.frame.widgets.append(self)

    def process_kwargs(self, kwargs):
        defaults = { "font" : pygame.font.SysFont("Calibri", 17),
                    "color" : pygame.Color("white"),
                    "position" : (0, 0)
                    }

        for kwarg in kwargs:
            if kwarg in defaults:
                defaults[kwarg] = kwargs[kwarg]
            else:
                raise KeyError("InputBox accepts no keyword {}.".format(kwarg))
        self.__dict__.update(defaults)

    def check_events(self, event):
        pass

    def update(self):
        self.image = self.font.render(self.text, True, self.color)
        self.rect = self.image.get_rect(topleft=self.position)

    def draw(self, surface):
        surface.blit(self.image, (self.rect))