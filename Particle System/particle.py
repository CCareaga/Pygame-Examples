import pygame 
import math
import random

class ParticleManager():
    def __init__(self):
        """Class for updating and drawing each particle spawner, 
        then removing them once they are finished"""
        self.spawners = []

    def new(self, pos, size=5, density=4, color=[(255,255,255)], speed=6, shape='circle'):
        """Create new particle spawner"""
        new = ParticleSpawner(self, pos, size, density, color, speed, shape)
        self.spawners.append(new)

    def update(self, screen):
        """updates, draws and removes each spawner"""
        for spawner in self.spawners:
            if spawner.current > spawner.s_duration:
                self.spawners.remove(spawner)
            
            spawner.update()
            spawner.draw(screen)

class ParticleSpawner():
    def __init__(self, spawner, pos, size, density, color, speed, shape):
        """Class for actually creating each individual, 
        particle and controlling theyre attributes"""

        self.spawner = spawner
        self.pos = pos
        self.shape = shape
        self.size = size
        self.density = density
        self.speed = speed
        self.s_duration = self.size*7
        self.p_duration = self.s_duration/(self.speed + (self.size/10))
        self.color = self.generateColors(color)

        self.current = 0

        self.particles = []

        for d in xrange(self.density*5):
            self.particles.append(self.createParticle())

    def getVector(self):
        """Method to find the vector in which the particle will travel"""
        speed = random.randrange(-self.speed*10, self.speed*10)/10
        
        distance = [random.randrange(-40,40)/10.0, random.randrange(-40,40)/10.0]

        try:
            norm = math.sqrt(distance[0] ** 2.0 + distance[1] ** 2.0)
            direction = [distance[0] / norm, distance[1] / norm]
            vector = [direction[0] * speed, direction[1] * speed]
        except ZeroDivisionError:
            vector = [self.speed]*2

        return vector

    def generateColors(self, color):
        """creates the lighter and darker versions of the given color"""
        c2 = []
        c1 = [abs(i-30)for i in color]

        for i in color:
            if i < 225:
                c2.append(i+30)
            else:
                c2 = color
                break

        return [c1, c2, color]

    def createParticle(self):
        """Creates eaach particle (list of attributes)"""
        #particle list item: [rect, birthtime, vector, size]
        rect = pygame.Rect((self.pos), ([self.size]*2))
        particle = [rect, 0, self.getVector(), self.size]
        return particle
        
    def update(self):
        """Updates each one accoriding to its vector and removes particles that are dead"""
        self.current += 1
        if self.current < self.density:
            for d in xrange(self.density*5):
                self.particles.append(self.createParticle())

        for particle in self.particles:
            particle[1] += 1

            if particle[1] > self.p_duration:
                self.particles.remove(particle)
            
            if particle[1] > self.p_duration/3:
                particle[3] -= 1
            
            particle[0].x += particle[2][0]
            particle[0].y += particle[2][1]
            
            if particle[3] > 1:
                particle[0].size = [particle[3]]*2

    def draw(self, screen):
        """Draws each particle (can be circles or rects)"""
        for particle in self.particles:

            color = random.choice(self.color)

            if self.shape == 'rect':
                pygame.draw.rect(screen, color, particle[0])
            else:
                pygame.draw.circle(screen, color, particle[0].topleft, particle[0].width)
