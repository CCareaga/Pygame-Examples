import pygame
import pygame._view
from pygame.locals import *
import sys
import random

from player import Player
from block import Block
from maploader import MapLoader
from camera import Layer

pygame.init()

class Game():
    def __init__(self):
        #window setup
        pygame.display.set_caption('Platformer')

        # initiate the clock and screen
        self.clock = pygame.time.Clock()
        self.last_tick = pygame.time.get_ticks()
        self.screen_res = [750, 500]

        self.font = pygame.font.SysFont("Impact", 55)
        self.screen = pygame.display.set_mode(self.screen_res, pygame.HWSURFACE, 32)

        self.entities = pygame.sprite.Group()
        self.solids = pygame.sprite.Group()
        self.maploader = MapLoader(self)
        self.maploader.load(1)
        self.player = self.maploader.player
        self.camera = self.maploader.camera

        self.createLayers()
        
        self.entities.add(self.solids)
        self.entities.add(self.player)

        self.clock.tick(60)
        while 1:
            self.Loop()
            
    def Loop(self):
        # main game loop
        self.eventLoop()
        
        self.Tick()
        self.Draw()
        pygame.display.update()

    def createLayers(self):
        self.layer1 = pygame.image.load('bg1.png').convert_alpha()
        self.layer2 = pygame.image.load('bg2.png').convert_alpha()
        self.l_rect1 = self.layer1.get_rect()
        self.l_rect2 = self.layer2.get_rect()

        self.back = Layer('back', self.l_rect1)
        self.front = Layer('front', self.l_rect2)

        self.camera.add_layers([self.front, self.back])

    def eventLoop(self):
        # the main event loop, detects keypresses
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    self.running = True
                if event.key == K_SPACE:
                    self.player.jump()

    def Tick(self):
        # updates to player location and animation frame
        self.ttime = self.clock.tick()
        self.mpos = pygame.mouse.get_pos()
        self.keys_pressed = pygame.key.get_pressed()

    def Draw(self):
        self.screen.fill((150,150,150))

        self.screen.blit(self.layer1, self.camera.apply_layer(self.back))
        self.screen.blit(self.layer2, self.camera.apply_layer(self.front))

        self.player.update(self.ttime / 1000.)
        self.camera.update(self.player)
        
        for e in self.entities:
            self.screen.blit(e.image, self.camera.apply(e))


Game()
