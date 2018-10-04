import pygame as pg
import random
import time
import functions as func
import settings

class ClientGame(object):
	def __init__(self, settings):
		self.screenWidth = settings['width']
		self.screenHeight = settings['height']
		self.fps = settings['fps']
		self.controls = settings['controls']
		pg.init()
		pg.mixer.init()
		pg.font.init()
		self.screen = pg.display.set_mode((self.screenWidth, self.screenHeight))
		self.screen.fill((255,255,255))
		pg.display.set_caption("AOE Clone")
		self.clock = pg.time.Clock()
		self.run()


	def menu(self):
		single = func.Button(self, "Singleplayer", x='center', y=(self.screenHeight/2), borderColour=(191, 164, 9))
		multi = func.Button(self, "Multiplayer", x='center', y=(self.screenHeight/2 + 75), borderColour=(191, 164, 9))
		settings = func.Button(self, "Settings", x='center', y=(self.screenHeight/2 + 150), borderColour=(191, 164, 9))
		_quit = func.Button(self, "Quit", x='center', y=(self.screenHeight/2 + 225), borderColour=(191, 164, 9))

		buttons = pg.sprite.Group(single, multi, settings, _quit)
		run = self.menuLoop(buttons)
		return buttons.sprites().index(run)


	def menuLoop(self, buttons):
		while True:
			for event in pg.event.get():
				if event.type == pg.QUIT:
					self._quit()
			for button in buttons.sprites():
				button.hover()
				if button.clicked():
					return button
				button.draw()
			pg.display.update()
			self.clock.tick(30)

	def run(self):
		while True:
			state = self.menu()
			print(state)
			if state == 0:
				self.singleplayer()
			elif state == 1:
				self.multiplayer()
			elif state == 2: # This is a really bad idea lol dont open settings too many times
				self.settings()
			else:
				self._quit()
				break # untouched code but oh well


	def singleplayer(self):
		pass


	def multiplayer(self):
		pass


	def settings(self):
		pass


	def _quit(self):
		pg.quit()
		quit()

if __name__ == '__main__':
	ClientGame(settings.settings)