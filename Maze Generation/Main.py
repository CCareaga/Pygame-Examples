
import pygame
from pygame.locals import *
import random

pygame.init()

class Node(pygame.sprite.Sprite):
    def __init__ (self, game, pos, num, color):
        pygame.sprite.Sprite.__init__(self)

        self.game = game
        self.game.node_sprites.add(self)
        self.game.node_list.append(self)

        self.pos = pos
        self.num = num
        self.color = color

        self.knocked = 0

        self.image = pygame.Surface([10, 10])
        self.image.fill(0)
        self.rect = self.image.get_rect(topleft=self.pos)

        self.point_list = {'north' : [self.rect.topleft, self.rect.topright],#N
                           'east' : [self.rect.topright, self.rect.bottomright],#E
                           'south' : [self.rect.bottomright, self.rect.bottomleft],#S
                           'west' : [self.rect.bottomleft, self.rect.topleft]}#W

        self.neighbors = {}
        self.walls = {'north' : False,
                      'east' : False,
                      'south' : False,
                      'west' : False}

    def getNeighbors(self):
        n_list = [('north', -60), ('south', 60), ('west', -1), ('east', 1)]
        neighbors = {}
        for n in n_list:
            index = self.num + n[1]
            if 2400 > index >= 0:
                cur_n = self.game.node_list[n[1] + self.num]
                if self.rect.x == 0 and n[0] == 'west' or self.rect.x == 590 and n[0] == 'east':
                    #Had to hadrcode come messiness to make sure neighbors were made properly 
                    pass
                else:
                    neighbors[n[0]] = cur_n
                    self.walls[n[0]] = True

        return neighbors

    def knockWalls(self, node, dire):
        if dire == 'north':
            self.walls['north'] = False
            node.walls['south'] = False
            del self.point_list['north']
            del node.point_list['south']

        if dire == 'south':
            self.walls['south'] = False
            node.walls['north'] = False
            del self.point_list['south']
            del node.point_list['north']

        if dire == 'west':
            self.walls['west'] = False
            node.walls['east'] = False
            del self.point_list['west']
            del node.point_list['east']

        if dire == 'east':
            self.walls['east'] = False
            node.walls['west'] = False
            del self.point_list['east']
            del node.point_list['west']

    def checkWall(self, dire):
        if self.walls[dire]:
            return True
        else:
            return False

    def update(self):
        for points in self.point_list.values():
            pygame.draw.line(self.game.screen, self.color, points[0], points[1], 1)

class Maze():
    def __init__(self):
        pygame.display.set_caption('Maze Generation')

        self.clock = pygame.time.Clock()

        self.screen_res = [601, 431]
        self.screen = pygame.display.set_mode(self.screen_res, pygame.HWSURFACE, 32)

        self.node_sprites = pygame.sprite.Group()
        self.node_list = []

        self.directions = "Press space to generate maze, press space again to generate new maze!"
        self.font = pygame.font.SysFont("Calibri", 16)

        self.renderText()
        self.createGrid()

        while 1:
            self.Loop()

    def Loop(self):
        self.eventLoop()
        self.Tick()
        self.Draw()
        pygame.display.update()

    def reset(self):
        self.node_list = []
        self.node_sprites.empty()

        self.createGrid()
        self.createMaze()

    def renderText(self):
        self.d_text = self.font.render(self.directions, 1, (255, 255, 255))
        self.t_size = self.font.size(self.directions)

    def createGrid(self):
        col = 30
        row = 0
        num = 0

        color  = [random.choice(xrange(255)), random.choice(xrange(255)), random.choice(xrange(255))]

        for y in xrange(40):
            for x in xrange(60):
                Node(self, [row, col], num, color)
                row += 10
                num += 1
            row = 0
            col += 10

        for node in self.node_list:
            node.neighbors = node.getNeighbors()

    def createMaze(self):   
        '''horribly ugly Depth First Search, but it works!'''
        checked = []
        total = len(self.node_list)

        current = self.node_list[0]
        visited = 1

        for i in xrange(4000):
            current.checked = True
            try:
                neighbors = []
                for key, value in current.neighbors.iteritems():
                    if current.checkWall(key) and value not in checked and value.knocked < 1:
                        neighbors.append([key, value]) 

                if neighbors:
                    cur_n = random.choice(neighbors)
                    current.knockWalls(cur_n[1], cur_n[0])
                    current.knocked += 1
                    cur_n[1].knocked += 1
                    checked.append(current)
                    current = cur_n[1]

                else:

                    back = checked.pop(-1)
                    if back.knocked < 2:
                        current = back
                    else:
                        current = checked.pop(-2)

            except:
                for node in self.node_list:
                    if node.knocked == 0:
                        try:
                            ran = random.choice(node.neighbors.keys())
                            neib = node.neighbors[ran]
                            node.knockWalls(neib, ran)
                        except:
                            continue
                break   


    def eventLoop(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()


    def Tick(self):
        self.keys_pressed = pygame.key.get_pressed()
        if self.keys_pressed[pygame.K_SPACE]:
            self.reset()

    def Draw(self):
        self.screen.fill(0)

        self.screen.blit(self.d_text, (300 - self.t_size[0]/2, 8))

        self.node_sprites.draw(self.screen)
        self.node_sprites.update()

Maze()

