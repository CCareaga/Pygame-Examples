import pygame

from pygame.locals import *
import sys
import random

sys.path.append('src')

from player import Player
from block import Block
from maploader import MapLoader
from cam import *

pygame.init()

class Game():
    def __init__(self):

        pygame.display.set_caption('Platformer')

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


    def eventLoop(self):
        # the main event loop, detects keypresses
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    self.reset()
                    self.maploader.load(2)
                    
                if event.key == K_SPACE:
                    self.player.jump()

    def Tick(self):
        self.ttime = self.clock.tick()
        self.mpos = pygame.mouse.get_pos()
        self.keys_pressed = pygame.key.get_pressed()

    def reset(self):
        self.maploader.layers = []
        player = self.maploader.player
        self.entities.empty()
        self.solids.empty()
        self.player = player

        self.entities.add(self.player)

    def Draw(self):
        self.screen.fill((150,150,150))

        for l in self.maploader.layers[::-1]:#Update layers (have to reverse list to blit properly)
            self.screen.blit(l.image, self.camera.apply_layer(l))                

        self.player.update(self.ttime / 1000.)
        self.camera.update(self.player)
        
        for e in self.entities: #update blocks etc.
            self.screen.blit(e.image, self.camera.apply(e))


Game()
