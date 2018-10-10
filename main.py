import pygame as pg
import random
import time
import functions as func
from settings import settings

class ClientGame(object):
	def __init__(self, settings):
		self.setting = settings
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
		func.drawTextCentered(title, self.screen, self.screenWidth/2, self.screenHeight/4)

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
				state = self.singleplayer()
			elif state == 1:
				state = self.multiplayer()
			elif state == 2:
				state = self.settings()
			elif state == 3:
				self._quit()
				break # untouched code but oh well just in case
			


	def singleplayer(self):
		return 0


	def multiplayer(self):
		return 0


	def settings(self):
		self.screen.fill((230,230,230))
		
		title = func.Text("Settings", fontSize=40)
		func.drawTextCentered(title, self.screen, self.screenWidth/2, self.screenHeight/16)

		''' Main Buttons '''
		controls = func.Button(self, "Controls", x=self.screenWidth/3, y=self.screenHeight/4, borderColour=(191, 164, 9))
		game = func.Button(self, "Game", x=self.screenWidth/2, y=self.screenHeight/4, borderColour=(191, 164, 9))
		system = func.Button(self, "System", x=2*self.screenWidth/3, y=self.screenHeight/4, borderColour=(191, 164, 9))
		back = func.Button(self, "Back", x="center", y=7*self.screenHeight/8, borderColour=(255, 100, 100))
		mainButtons = pg.sprite.Group(controls, game, system, back)

		''' Control Buttons '''
		directional = func.Button(self, "Directional", x=self.screenWidth/7, y=12*self.screenHeight/28, borderColour=(200,200,200), hoverColour=(230, 230, 230))
		misc = func.Button(self, "Miscellaneous", x=self.screenWidth/7, y=15*self.screenHeight/28, borderColour=(200,200,200), hoverColour=(230, 230, 230))
		controlButtons = pg.sprite.Group(directional, misc)

		''' Directional movment options generator'''
		dcontrolLables = []
		dcontrolEdits = pg.sprite.Group()
		dControlObjs = []
		i = 0
		for control in self.setting["controls"].keys():
			dcontrolLables.append(control)
			button = func.Button(self, self.setting['controls'][control], borderColour=(230,230,230))
			dcontrolEdits.add(button)
			dControlObjs.append(func.menuObject(control, button))
			i += 1

		'''Misc buttons'''
		mForward = func.Button(self, ">")
		mBack = func.Button(self, "<")
		miscButtons = pg.sprite.Group(mForward, mBack)


		pg.draw.rect(
			self.screen,
			(200, 200, 200),
			pg.Rect(
				self.screenWidth/16,
				self.screenHeight/3,
				7*self.screenWidth/8,
				12*self.screenHeight/28
			)
		)

		pg.draw.line(self.screen, (150,150,150), (self.screenWidth/4, 10*self.screenHeight/28), (self.screenWidth/4, 20*self.screenHeight/28), 3)

		state = 0
		substate = 0
		while True:
			self.screen.fill((230,230,230))
			self.drawSettings(title)
			for event in pg.event.get():
				if event.type == pg.QUIT:
					self._quit()
			for button in mainButtons.sprites():
				button.hover()
				button.draw()
				if button.clicked():
					state = mainButtons.sprites().index(button)
			if state == 0:
				for button in controlButtons.sprites():
					button.hover()
					button.draw()
					if button.clicked():
						substate = controlButtons.sprites().index(button)
				if substate == 0:
					sw = self.screenWidth
					sh = self.screenHeight
					xPos = [sw/3, sw/2, 2*sw/3, 2*sw/3 + abs(sw/2 - 2*sw/3)]
					yPos = [12*sh/28, 17*sh/28]
					i = 0
					objs = dControlObjs
					for x in xPos:
						for y in yPos:
							if i != len(objs):
								objs[i].set(x,y)
								objs[i].calc()
								objs[i].draw()
								i += 1

					if 8 < len(objs):
						if i != len(objs):
							mForward.draw()
						if i != 7:
							mBack.draw()
					for button in miscButtons.sprites():
						if button.clicked():
							print(button.name)
					for button in dcontrolEdits.sprites():
						button.draw()
						button.hover()
						if button.clicked():
							while True:
								pressed = pg.key.get_pressed()
								key = pressed.index(1) if 1 in pressed else None
								if key:
									obj = dControlObjs[dcontrolEdits.sprites().index(button)]
									key = pg.key.name(key)
									if key == "escape":
										break
									key = "pg.K_" + key.upper()
									self.setting['controls'][obj.lable.text] = key
									button.updateText(key)
									button.draw()
									break
								pg.event.pump()
				else:
					pass
			elif state == 1:
				pass # game
			elif state == 2:
				pass # system
			elif state == 3:
				return 0
			pg.display.update()

	def drawSettings(self, text):
		func.drawTextCentered(text, self.screen, self.screenWidth/2, self.screenHeight/16)
		pg.draw.rect(
			self.screen,
			(200, 200, 200),
			pg.Rect(
				self.screenWidth/16,
				self.screenHeight/3,
				7*self.screenWidth/8,
				12*self.screenHeight/28
			)
		)
		pg.draw.line(self.screen, (150,150,150), (self.screenWidth/4, 10*self.screenHeight/28), (self.screenWidth/4, 20*self.screenHeight/28), 3)

	def updateSettingsObject(self):
		self.screenWidth = self.setting['width']
		self.screenHeight = self.setting['height']
		self.fps = self.setting['fps']
		self.controls = self.setting['controls']


	def _quit(self):
		pg.quit()
		quit()

if __name__ == '__main__':
	ClientGame(settings)