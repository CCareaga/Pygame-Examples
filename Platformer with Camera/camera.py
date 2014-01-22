import pygame
from pygame.locals import *

class Layer(object):
    #Class to store the name and the rect of each layer
    def __init__(self, name, rect):
        self.name = name
        self.rect = rect

class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = pygame.Rect(0, 0, width, height)
        self.layers = []

    def apply(self, target):
        return target.rect.move(self.state.topleft)
    
    def add_layers(self, layers):
        #adds layer(s)
        for layer in layers:
            self.layers.append(layer.name)

    def apply_layer(self, target):
        #applies camera offset, the gets index of layer in the list then mves the higher index slower
        index = self.layers.index(target.name)+1
        return target.rect.move(self.state.topleft[0]/(index*2),self.state.topleft[1]/(index*2))
    
    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)
 
