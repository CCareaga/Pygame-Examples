import pygame
from pygame.locals import *
import sys


class Button():
    '''Button class with multiple kwargs, pretty straight forward'''
    def __init__(self, frame, text, command, **kwargs):

        self.frame = frame
        self.text = text
        self.command = command
        self.clicked = False

        self.process_kwargs(kwargs)

        self.image = pygame.Surface(self.size)
        self.rect = self.image.get_rect(topleft=self.position)
        self.frame_rect = self.frame.off(self.rect.copy())

        self.image.fill(self.color)
        self.image.unlock()
        
        self.create_text()
        self.frame.widgets.append(self)

    def process_kwargs(self, kwargs):
        defaults = { "font" : pygame.font.SysFont('Calibri',16),
                    "color" : pygame.Color("black"),
                    "highlighted" : (25, 25, 25),
                    "hover_color" : pygame.Color("black"),
                    "font_color" : pygame.Color("white"),
                    "position" : (5, 5),
                    "size" : (120, 25)
                    }

        for kwarg in kwargs:
            if kwarg in defaults:
                defaults[kwarg] = kwargs[kwarg]
            else:
                raise KeyError("InputBox accepts no keyword {}.".format(kwarg))
        self.__dict__.update(defaults)

    def create_text(self):
        self.text = self.font.render(self.text, True, self.font_color)
        text_pos = [self.size[0]/2, self.size[1]/2]
        self.text_rect = self.text.get_rect(center=text_pos)

    def check_events(self, event):
        self.check_click(event)

    def check_hover(self):
        if self.frame_rect.collidepoint(pygame.mouse.get_pos()) and not self.clicked:
            return True

    def check_click(self, event):
        '''pass events from frame to check for click'''
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.on_click(event)

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.on_release(event)

    def on_click(self, event):
        if self.frame_rect.collidepoint(event.pos):
            self.clicked = True
            self.command()
        else:
            self.clicked = False

    def on_release(self, event):
        self.clicked = False


    def update(self):
        self.frame_rect = self.frame.off(self.rect.copy())
        self.image.fill(self.color)

        if self.clicked:
            self.image.fill(self.highlighted)

        if self.check_hover():
            self.image.fill(self.hover_color)

        self.image.blit(self.text, (self.text_rect))

    def draw(self, surface):
        surface.blit(self.image, (self.rect))
        pygame.draw.rect(surface, (255, 255, 255), self.rect, 2)