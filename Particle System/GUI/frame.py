import pygame
from pygame.locals import *
import sys


class Frame(object):
    ''' Frame class, holds widgets and updates them also'''
    def __init__(self, screen, size, pos, **kwargs):

        self.screen = screen
        self.size = size
        self.pos = pos
        
        
        self.image = pygame.Surface(self.size)
        self.rect = self.image.get_rect(topleft=self.pos)

        self.process_kwargs(kwargs)

        self.border = pygame.Surface((self.size[0]+8, self.size[1]+8))
        self.border.fill(self.border_color)

        self.widgets = []


    def process_kwargs(self, kwargs):
        defaults = {
                    "color" : pygame.Color("black"),
                    "border_color" : pygame.Color("white")
                    }

        for kwarg in kwargs:
            if kwarg in defaults:
                defaults[kwarg] = kwargs[kwarg]
            else:
                raise KeyError("Button accepts no keyword {}.".format(kwarg))
        self.__dict__.update(defaults)

    def update(self):
        self.screen.blit(self.border, (self.rect.move(-4,-4)))
        self.screen.blit(self.image, (self.rect))
        self.image.fill(self.color)

        for w in self.widgets:
            w.update()
            w.draw(self.image)

    def off(self, rect):
        rect.x = rect.x + self.rect.x
        rect.y = rect.y + self.rect.y        
        return rect

    def check_events(self, event):
        for w in self.widgets:
            w.check_events(event)