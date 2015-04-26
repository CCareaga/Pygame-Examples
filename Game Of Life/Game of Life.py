import pygame

from pygame.locals import *
import sys
import random

from cell import Cell


pygame.init()

class Game():
    def __init__(self):
        pygame.display.set_caption('Game Of Life')

        self.clock = pygame.time.Clock()
        self.last_tick = pygame.time.get_ticks()
        self.screen_res = [740, 490]

        self.font = pygame.font.SysFont("Impact", 19)

        self.sprites = pygame.sprite.Group()
        self.cells = []
        self.generation = 0
        self.population = 0

        self.screen = pygame.display.set_mode(self.screen_res, pygame.HWSURFACE, 32)

        self.running = False
        self.createGrid()
     
        while 1:
            self.Loop()

    def createGrid(self):
        col = 0
        row = 50
        cell_num = 0

        for y in xrange(44):
            for x in xrange(74):
                cell_num +=1
                cell = Cell(self, [col, row], cell_num)
                if row == 50 or row  == 480 or col == 0 or col == 730:
                    cell.edge = True
                #if row == 60 or row  == 470 or col == 10 or col == 720:
                    #cell.alive = True
                self.sprites.add(cell)
                col += 10
            row += 10
            col = 0
          
    def Run(self):
        self.population = 0
        for cell in self.cells:
            if cell.alive:
                self.population += 1
                if len(cell.a_neighbors) < 2:
                    cell.die()
                elif len(cell.a_neighbors) > 3:
                    cell.die()
                elif len(cell.a_neighbors) == 2 or len(cell.a_neighbors) == 3:
                    cell.live()
            else:
                if len(cell.a_neighbors) == 3:
                    cell.live()
                    
    def blitDirections(self):
        text = self.font.render("Press Enter to begin, and Space to stop and clear board", 1, (255,255,255))
        generations = self.font.render("Generation: %s" %str(self.generation), 1, (255,255,255))
        pop = self.font.render("Pop: %s" %str(self.population), 1, (255,255,255))
        self.screen.blit(text, (10, 15))
        self.screen.blit(generations, (500, 15))
        self.screen.blit(pop, (650, 15))

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
                    self.running = True
                if event.key == K_SPACE:
                    self.running = False
                    self.sprites.empty()
                    self.cells = []
                    self.createGrid()

    def Tick(self):
        # updates to player location and animation frame
        self.ttime = self.clock.tick()
        self.mpos = pygame.mouse.get_pos()
        self.keys_pressed = pygame.key.get_pressed()
        if self.running:
            self.generation +=1
            self.Run()
        else:
            self.generation = 0
            self.population = 0

    def Draw(self):
        self.screen.fill(0)
        self.blitDirections()
        self.sprites.update()
        self.sprites.draw(self.screen)

Game()
