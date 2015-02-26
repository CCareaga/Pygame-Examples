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

		self.font = pygame.font.SysFont("Calibri", 16)

		self.pManager = ParticleManager()

		self.constant = False
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
			elif event.type == KEYDOWN:
				if event.key == 32:
					if self.constant:
						self.constant = False
					else:
						self.constant = True

			elif event.type == MOUSEBUTTONDOWN and not self.constant:
				pos = pygame.mouse.get_pos()
				shape = choice(['circle', 'rect'])
				self.pManager.new(pos, size=randint(4,7), density=randint(4,7), color=self.getColor(), shape=shape)

			elif event.type == MOUSEMOTION and self.constant:
				pos = pygame.mouse.get_pos()
				shape = choice(['circle', 'rect'])
				self.pManager.new(pos, size=randint(4,7), density=randint(4,7), color=self.getColor(), shape=shape)

	def blitText(self):
		text = self.font.render("Constant: " + str(self.constant), 1, (255,255,255))
		text2 = self.font.render("(Space to toggle)", 1, (255,255,255))
		textrect, text2rect = text.get_rect(), text2.get_rect()
		
		textrect.centerx = text2rect.centerx = self.res[0]/2
		text2rect.centery, textrect.centery = 38, 20

		self.screen.blit(text, textrect)
		self.screen.blit(text2, text2rect)

	def Update(self):
		self.screen.fill(0)
		self.blitText()
		self.pManager.update(self.screen)

Example()
