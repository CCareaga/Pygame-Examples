from pygame.locals import *
import pygame

from random import randint, choice

from particle import *

pygame.init()

class Example():
	def __init__(self):
		pygame.display.set_caption('Platformer')
		self.clock = pygame.time.Clock()
		self.res = [640, 480]
		self.FPS = 50
		self.screen = pygame.display.set_mode(self.res)

		self.pManager = ParticleManager()

		self.running = True

		while self.running:
			self.Loop()

	def Loop(self):
		self.clock.tick(self.FPS)
		self.eventLoop()
		self.Update()
		pygame.display.update()

	def getColor(self):
		return [randint(0, 255) for _ in xrange(3)]

	def eventLoop(self):
		for event in pygame.event.get():
			if event.type == QUIT:
				self.running = 0
				pygame.quit()
			elif event.type == MOUSEBUTTONDOWN:
				print self.getColor()
				pos = pygame.mouse.get_pos()
				shape = choice(['circle', 'rect'])
				print shape
				self.pManager.new(pos, size=randint(4,7), density=randint(4,7), color=self.getColor(), shape=shape)

	def Update(self):
		self.screen.fill(0)
		self.pManager.update(self.screen)

Example()
