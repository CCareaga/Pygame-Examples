from pygame.locals import *
import pygame
import sys

from random import randint, choice

from particle import *

sys.path.append('GUI')

from attributesGUI import GUI

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
		self.GUI = GUI(self.screen, self)

		self.attrs = {'shape' : 'circle',
					  'size': 4,
					  'density' : 5,
					  'speed' : 6}

		self.defaults = self.attrs # save starting values

		self.random = True
		self.constant = False

		self.hide = False

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
			if not self.hide:
			    self.GUI.check_events(event)
			if event.type == QUIT:
				self.running = 0
				pygame.quit()
			elif event.type == KEYDOWN:
				if event.key == 32:
					if self.hide:
						self.hide = False
					else:
						self.hide = True
			if (event.type == MOUSEBUTTONDOWN and not self.constant) or  (event.type == MOUSEMOTION and self.constant):
				self.createParticles()

	def createParticles(self):
		pos = pygame.mouse.get_pos()
		shape = choice(['circle', 'rect'])
		if self.random:
			self.pManager.new(pos, size=randint(4,7), density=randint(4,7), color=self.getColor(), shape=shape)
		else:
			self.pManager.new(pos, size=self.attrs['size'], density=self.attrs['density'], speed=self.attrs['speed'], color=self.getColor(), shape=self.attrs['shape'])

	def updateAttributes(self):
		if not self.random:
			for key in self.attrs.keys():
				try:
					self.attrs[key] = int(self.GUI.textboxes[key].text)
				except:
					self.attrs[key] = self.defaults[key]

			self.attrs['shape'] = self.GUI.s_Label.text.lower()

	def Update(self):
		self.screen.fill(0)
		self.pManager.update(self.screen)
		if not self.hide:
		    self.GUI.update()
		    self.updateAttributes()

Example()
