import pygame

class Grid:
    def __init__(self, game):
        self.game = game
        self.length = self.game.screen_res[0]/15
        self.width = (self.game.screen_res[1]/15)-3

        self.nodes = [[Node(self, [row, col+3]) for row in xrange(self.length)] for col in xrange(self.width)] 

    def update(self):
        for col in self.nodes:
            for node in col:
                node.update()
                node.draw(self.game.screen)

        for i in xrange(self.length):
            pygame.draw.line(self.game.screen, [100]*3, (15*i, 45), (15*i, 495))

        for i in xrange(self.width):
            pygame.draw.line(self.game.screen, [100]*3, (0, (15*i)+45), (750, (15*i)+45))

    def clearPath(self):
        for col in self.nodes:
            for node in col:
                if node.in_path:
                    node.in_path = False
                    node.color = 0

class Node():
    def __init__(self, grid, pos):
        self.grid = grid
        self.game = self.grid.game

        self.pos = pos
        self.blit_pos = [i*15 for i in self.pos]
        self.color = [0,0,0]

        self.image = pygame.Surface((15, 15))

        self.rect = self.image.get_rect(topleft=self.blit_pos)

        self.solid = 0
        self.in_path = False
        self.checked = False

    def update(self):
        if self.checked and self.game.show_checked:
            self.color = [0, 255, 0]
        if self.checked and self.game.show_checked == False:
            self.color = [0, 0, 0]

        if self.in_path:
            self.color = [0, 0, 255]

        if self.game.pathing:
            pass

        else:
            if pygame.mouse.get_pressed()[0] and self.rect.collidepoint(self.game.mpos):
                self.solid = 1
                self.in_path = False
                self.color = [255, 0, 0]

            if pygame.mouse.get_pressed()[2] and self.rect.collidepoint(self.game.mpos):   
                self.solid = 0
                self.in_path = False
                self.color = [0, 0, 0]
                
    def draw(self, screen):
        self.image.fill(self.color)
        screen.blit(self.image, self.rect)


