import pygame
from pygame.locals import *
import sys
import random


pygame.init()

from frame import Frame
from button import Button
from textbox import TextBox
from label import Label

class GUI(Frame):
    def __init__(self, screen, game):
        ''' An example class to show how to creat custom GUI frames'''
        Frame.__init__(self, screen, (330, 110), (10, 10))

        self.game = game

        self.b1 = Button(self, "Toggle Constant", self.command)
        self.b2 = Button(self, "Toggle Random", self.command2, position=(5,40))
        self.b3 = Button(self, "Toggle Shape", self.command3, position=(5, 75))

        self.c_Label = Label(self, "False", position=(135, 10))
        self.r_Label = Label(self, "True", position=(135, 45))
        self.s_Label = Label(self, "Random", position=(135, 80))

        self.l1 = Label(self, "Size", position=(235, 10))
        self.tb1 = TextBox(self, (295, 10))

        self.l2 = Label(self, "Density", position=(235, 45))
        self.tb2 = TextBox(self, (295, 45))

        self.l3 = Label(self, "Speed", position=(235, 80))
        self.tb3 = TextBox(self, (295, 80))
        
        self.textboxes = {'size' : self.tb1,
                        'density' : self.tb2,
                        'speed' : self.tb3}
        self.current = 'circle'

    def command(self):
        if self.game.constant:
            self.game.constant = False
        else:
            self.game.constant = True
        self.c_Label.text = str(self.game.constant)

    def command2(self):
        if self.game.random:
            self.s_Label.text = 'Circle'
            self.game.random = False
        else:
            self.s_Label.text = 'Random'
            self.game.random = True

        self.r_Label.text = str(self.game.random)

    def command3(self):
        if not self.game.random:
            if self.game.attrs['shape'] == 'circle':
                self.s_Label.text = 'Rect'
            else:
                self.s_Label.text = 'Circle'

