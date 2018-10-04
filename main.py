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
		self.screen.fill((255,255,255))
		title = func.Text("Age Of Empires", fontSize=80)
		func.drawText(title, self.screen, self.screenWidth/2, self.screenHeight/4)

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
			state = False
			state = self.menu()
			if state == 0:
				self.singleplayer()
			elif state == 1:
				self.multiplayer()
			elif state == 2: # This is a really bad idea lol dont open settings too many times
				self.settings()
				print("Settings")
			else:
				self._quit()
				break # untouched code but oh well
			


	def singleplayer(self):
		pass


	def multiplayer(self):
		pass


	def settings(self):
		self.screen.fill((230,230,230))
		
		title = func.Text("Settings", fontSize=40)
		func.drawText(title, self.screen, self.screenWidth/2, self.screenHeight/16)

		controls = func.Button(self, "Controls", x=self.screenWidth/3, y=self.screenHeight/4, borderColour=(191, 164, 9))
		game = func.Button(self, "Game", x=self.screenWidth/2, y=self.screenHeight/4, borderColour=(191, 164, 9))
		system = func.Button(self, "System", x=2*self.screenWidth/3, y=self.screenHeight/4, borderColour=(191, 164, 9))
		back = func.Button(self, "Back", x="center", y=7*self.screenHeight/8, borderColour=(255, 100, 100))
		buttons = pg.sprite.Group(controls, game, back, system)

		while True:
			for event in pg.event.get():
				if event.type == pg.QUIT:
					self._quit()
			for button in buttons.sprites():
				button.hover()
				button.draw()
			if controls.clicked():
				pass
			elif game.clicked():
				pass
			elif system.clicked():
				pass
			elif back.clicked():
				time.sleep(0.5) # to ensure that quit isnt immediately clicked
				return None
			pg.display.update()

	def _quit(self):
		pg.quit()
		quit()

if __name__ == '__main__':
	ClientGame(settings.settings)