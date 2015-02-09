import pygame

from pygame.locals import *
import sys
import random
import numpy

from pathfind import *

from grid import Grid


pygame.init()

class Game():
    def __init__(self):
        #window setup
        pygame.display.set_caption('A* Visual')

        # initiate the clock and screen
        self.clock = pygame.time.Clock()
        self.last_tick = pygame.time.get_ticks()
        self.screen_res = [750, 495]

        self.font = pygame.font.SysFont("Calibri", 16)

        self.screen = pygame.display.set_mode(self.screen_res, pygame.HWSURFACE, 32)
        self.pathing = False
        self.pathing_type = '*'
        self.show_checked = False

        self.grid = Grid(self)
  
        while 1:
            self.Loop()
          
    def Run(self):
        self.pathing = True
        self.grid.clearPath()

        node_array = self.Convert()

        path, check = astar(node_array, (0,0), (29, 49), self.pathing_type)

        
        for pos in check:
            self.grid.nodes[pos[0]][pos[1]].checked = True

        if path != False:
            for pos in path:
                self.grid.nodes[pos[0]][pos[1]].in_path = True
        else:
            pass
        
        print len(path)
        self.pathing = False 

    def Clear(self):
        self.grid = Grid(self)

    def Convert(self):
        array = [[self.grid.nodes[col][row].solid for row in xrange(self.grid.length)] for col in xrange(self.grid.width)]
        nodes = numpy.array(array)
        return nodes

    def blitInfo(self):
        text = self.font.render("Press Enter to find path, press Space to clear board", 1, (255,255,255))
        text2 = self.font.render("Press c to toggle checked nodes, and 1 and 2 to switch pathing types", 1, (255,255,255))

        check = self.font.render("Checked nodes: " + str(self.show_checked), 1, (255,255,255))
        ptype = self.font.render("Pathing type: " + self.pathing_type, 1, (255,255,255))

        self.screen.blit(text, (5, 5))
        self.screen.blit(text2, (5, 25))

        self.screen.blit(check, (500, 5))
        self.screen.blit(ptype, (500, 25))

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
                    self.Run()
                if event.key == K_SPACE:
                    self.Clear()
                if event.key == K_1:
                    self.pathing_type = '+'
                if event.key == K_2:
                    self.pathing_type = '*'
                if event.key == K_c:
                    print self.show_checked
                    if self.show_checked:
                        self.show_checked = False
                    else:
                        self.show_checked = True

    def Tick(self):
        # updates to player location and animation frame
        self.ttime = self.clock.tick()
        self.mpos = pygame.mouse.get_pos()

    def Draw(self):
        self.screen.fill(0)
        self.grid.update()
        self.blitInfo()

Game()