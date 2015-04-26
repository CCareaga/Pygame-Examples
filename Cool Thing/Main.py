import pygame

from pygame.locals import *
import sys
import random, math
import time

pygame.init()

class Game():
    def __init__(self):
        pygame.display.set_caption('Cool Shit!')

        self.clock = pygame.time.Clock()
        self.last_tick = pygame.time.get_ticks()
        self.screen_res = [640, 480]

        self.circles = []

        self.screen = pygame.display.set_mode(self.screen_res, pygame.HWSURFACE, 32)

        self.createCircles()
        time.sleep(6)
     
        while 1:
            self.Loop()

    def Loop(self):
        self.eventLoop()
        
        self.Tick()
        self.Draw()
        pygame.display.update()

    def createCircles(self):
        #circle item format: [pos, vector]
        for i in xrange(100):
            pos = [320, 240]
            vector = self.getVector()
            self.circles.append([pos, vector])

    def getDistance(self, pos1, pos2):
        return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

    def getVector(self):
        speed = 5
        
        distance = [random.randrange(-40,40)/10.0, random.randrange(-40,40)/10.0]

        try:
            norm = math.sqrt(distance[0] ** 2.0 + distance[1] ** 2.0)
            direction = [distance[0] / norm, distance[1] / norm]
            vector = [direction[0] * speed, direction[1] * speed]
        except ZeroDivisionError:
            vector = [self.speed]*2

        return vector

    def eventLoop(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == pygame[K_ESCAPE]:
                    pygame.quit()
                    sys.exit()

    def Tick(self):
        self.ttime = self.clock.tick(60)

    def Draw(self):
        self.screen.fill(0)

        for circle in self.circles:
            #circle[0] = [int(circle[0][0]), int(circle[0][1])]

            #pygame.draw.circle(self.screen, [255]*3, circle[0], 0)
            circle[0][0] += circle[1][0]
            circle[0][1] += circle[1][1]
            
            if circle[0][0] > 640 or circle[0][0] < 0:
                circle[1][0] *= -1

            elif circle[0][1] > 480 or circle[0][1] < 0:
                circle[1][1] *= -1

            for c in self.circles:
                if self.getDistance(circle[0], c[0]) < 225:
                    pygame.draw.line(self.screen, [0, 255, 0], circle[0], c[0])
                if self.getDistance(circle[0], c[0]) < 200:
                    pygame.draw.line(self.screen, [0, 0, 255], circle[0], c[0])
                if self.getDistance(circle[0], c[0]) < 175:
                    pygame.draw.line(self.screen, [255, 0, 0], circle[0], c[0])
                #if self.getDistance(circle[0], c[0]) < 150:
                    #pygame.draw.line(self.screen, [0, 255, 255], circle[0], c[0])
                #if self.getDistance(circle[0], c[0]) < 125:
                    #pygame.draw.line(self.screen, [255, 255, 0], circle[0], c[0])
                #if self.getDistance(circle[0], c[0]) < 100:
                    #pygame.draw.line(self.screen, [255, 0, 255], circle[0], c[0])
Game()
