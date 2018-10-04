import pygame as pg
import random
import time
import functions as func
import menu

class ClientGame(object):
	def __init__(self, settings):
		self.screenWidth = settings['width']
		self.screenHeight = settings['height']
		self.fps = settings['fps']
		self.controls = settings['controls']
		pg.init()
		pg.mixer.init()
		self.screen = pg.display.set_mode((self.screenWidth, self.screenHeight))
		pg.display.set_caption("AOE Clone")
		self.clock = pg.time.Clock()
		self.run()


	def menu(self):
		single = menu.Button(self, "Singleplayer", x='center', y=(self.screenHeight/2), borderColour=(191, 164, 9))
		multi = menu.Button(self, "Multiplayer", x='center', y=(self.screenHeight/2 - 50), borderColour=(191, 164, 9))
		settings = menu.Button(self, "Settings", x='center', y=(self.screenHeight/2 - 100), borderColour=(191, 164, 9))
		_quit = menu.Button(self, "Quit", x='center', y=(self.screenHeight/2 - 150), borderColour=(191, 164, 9))

		buttons = pg.sprite.Group(single, multi, settings, _quit)
		run = self.menuLoop(buttons)
		return buttons.sprites().index(run)


	def menuLoop(self, buttons):
		while True:
			for button in buttons:
				button.hover()
				if button.clicked():
					return button
			buttons.draw()

	def run(self):
		state = self.menu()
		if state == 0:
			self.singleplayer()
		elif state == 1:
			self.multiplayer()
		elif state == 2: # This is a really bad idea lol dont open settings too many times
			self.settings()
			self.run()
		else:
			self._quit()