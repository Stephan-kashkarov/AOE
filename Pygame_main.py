"""AOE CLONE
	Written by Stephan Kashkarov 2018
	This is the main file of AOE Clone
	it contains the main menu of the game
"""
'''Imports'''
import os
import time
import random
import threading
import multiprocessing

import pygame as pg

import app.game.ai as ai
import app.game.maps as maps
import app.functions as func
import app.game.match as match
import app.game.client.clientMain as client
import app.game.server as server
from app.settings import settings
import app.menu.textAssets as textAssets


class MainMenu(object):
	"""Main Menu object.
	
	This object contains the main menu for the game
	and links together all the gameplay options and settings
	
	param settings a dictionary containing all settings
	"""
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
		"""Initializes the main menu"""
		self.screen.fill((255,255,255))
		title = textAssets.Text("Age Of Empires", fontSize=80)
		func.drawTextCentered(title, self.screen, self.screenWidth/2, self.screenHeight/4)

		single = textAssets.Button(self, "Singleplayer", x='center', y=(self.screenHeight/2), borderColour=(191, 164, 9))
		multi = textAssets.Button(self, "Multiplayer", x='center', y=(self.screenHeight/2 + 75), borderColour=(191, 164, 9))
		settings = textAssets.Button(self, "Settings", x='center', y=(self.screenHeight/2 + 150), borderColour=(191, 164, 9))
		_quit = textAssets.Button(self, "Quit", x='center', y=(self.screenHeight/2 + 225), borderColour=(191, 164, 9))

		buttons = pg.sprite.Group(single, multi, settings, _quit)
		run = self.menuLoop(buttons)
		return buttons.sprites().index(run)


	def menuLoop(self, buttons):
		"""Adds interactivity to the menu"""
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
		"""Runs the whole game by operating the menu"""
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
		self.loadingScreen("Loading...")
		# Making game objects
		options = match.options(
			'127.0.0.1:5000',
			'forrest',
			1000,
			'singleplayer'
		)
		player1 = client.PlayerClient(options.serverIP, self.screen)
		player2 = ai.Ai(options.serverIP)

		_map = maps.generateMap(options.mapType, options.mapSize)
		host = server.Server(_map, options.key)
		server_ = multiprocessing.Process(target=host.run)
		server_.start()
		# allow for the server to initializse
		time.sleep(1)
		game = match.Match(options, _map)

		# Making Threads
		gameThread = threading.Thread(target=game.run)
		aiThread = threading.Thread(target=player2.run)
		# Starting Threads
		gameThread.start()
		aiThread.start()
		# Running clientside
		state = player1.run()
		# Joining of threads
		self.loadingScreen('Game Over!')
		gameThread.join()
		aiThread.join()
		server_.terminate()
		server_.join(5)
		time.sleep(1)
		if state == 'quit':
			self._quit()
			quit()
		return 0


	def multiplayer(self):
		"""Creates a multiplayer instance of the game"""
		return 0


	def settings(self):
		"""Runs the settings for the game"""
		
		''' Title and background '''
		self.screen.fill((230,230,230))
		title = textAssets.Text("Settings", fontSize=40)
		func.drawTextCentered(title, self.screen, self.screenWidth/2, self.screenHeight/16)

		''' Main Buttons '''
		controls = textAssets.Button(self, "Controls", x=self.screenWidth/3, y=self.screenHeight/4, borderColour=(191, 164, 9))
		game = textAssets.Button(self, "Game", x=self.screenWidth/2, y=self.screenHeight/4, borderColour=(191, 164, 9))
		system = textAssets.Button(self, "System", x=2*self.screenWidth/3, y=self.screenHeight/4, borderColour=(191, 164, 9))
		back = textAssets.Button(self, "Back", x="center", y=7*self.screenHeight/8, borderColour=(255, 100, 100))
		mainButtons = pg.sprite.Group(controls, game, system, back)

		''' Control Buttons '''
		directional = textAssets.Button(self, "Directional", x=self.screenWidth/7, y=12*self.screenHeight/28, borderColour=(200,200,200), hoverColour=(230, 230, 230))
		misc = textAssets.Button(self, "Miscellaneous", x=self.screenWidth/7, y=15*self.screenHeight/28, borderColour=(200,200,200), hoverColour=(230, 230, 230))
		controlButtons = pg.sprite.Group(directional, misc)

		''' Directional movment options generator'''
		dcontrolLables = []
		dcontrolEdits = pg.sprite.Group()
		dControlObjs = []
		i = 0
		for control in self.setting["controls"].keys():
			dcontrolLables.append(control)
			button = textAssets.Button(self, pg.key.name(self.setting['controls'][control]), borderColour=(230,230,230))
			dcontrolEdits.add(button)
			dControlObjs.append(textAssets.menuObject(control, button))
			i += 1

		'''Misc buttons'''
		mForward = textAssets.Button(self, ">")
		mBack = textAssets.Button(self, "<")
		miscButtons = pg.sprite.Group(mForward, mBack)

		''' Boundry box '''
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
		''' Dividing line'''
		pg.draw.line(self.screen, (150,150,150), (self.screenWidth/4, 10*self.screenHeight/28), (self.screenWidth/4, 20*self.screenHeight/28), 3)


		''' Settings event loop '''
		state = 0
		substate = 0
		while True:
			self.screen.fill((230,230,230)) 
			self.drawSettings(title) # redraws settings
			for event in pg.event.get():
				if event.type == pg.QUIT:
					self._quit()
			for button in mainButtons.sprites(): # runs interactivity on main Buttons
				button.hover()
				button.draw()
				if button.clicked():
					state = mainButtons.sprites().index(button)
			if state == 0: # controls
				for button in controlButtons.sprites(): # runs on sub buttons
					button.hover()
					button.draw()
					if button.clicked():
						substate = controlButtons.sprites().index(button)
				if substate == 0: # directional

					'''Function shortening'''
					sw = self.screenWidth
					sh = self.screenHeight
					xPos = [sw/3, sw/2, 2*sw/3, 2*sw/3 + abs(sw/2 - 2*sw/3)]
					yPos = [12*sh/28, 17*sh/28]
					i = 0
					objs = dControlObjs

					'''Selects grid for item'''
					for x in xPos:
						for y in yPos:
							if i != len(objs):
								objs[i].set(x,y)
								objs[i].calc()
								objs[i].draw()
								i += 1

					''' Overflow check '''
					if 8 < len(objs):
						if i != len(objs):
							mForward.draw()
						if i != 7:
							mBack.draw()

					for button in miscButtons.sprites(): # Misc button interactivity
						if button.clicked():
							print(button.name)


					for button in dcontrolEdits.sprites(): # control edit buttons interactiviyt
						button.draw()
						button.hover()
						if button.clicked():
							while True:
								pressed = pg.key.get_pressed() # finds key
								key = pressed.index(1) if 1 in pressed else None # gets index w/o error if none pressed
								if key:
									obj = dControlObjs[dcontrolEdits.sprites().index(button)] # finds object index to button
									key = pg.key.name(key) # finds name to key ID

									if key == "escape": # cancles change
										break

									elif len(key) > 1: # checks for not letter keys
										key = key.upper()
										key = key.remove(" ")

									key = "pg.K_" + key # changes key string
									self.setting['controls'][obj.lable.text] = eval(key) # redefins key in settings
									button.updateText(pg.key.name(eval(key))) # updates button text
									button.draw() # redraws button
									break # exits while loop
								pg.event.pump() # updates events
				else: # Misc
					pass 
			elif state == 1:
				pass # game
			elif state == 2:
				pass # system
			elif state == 3:
				return 0
			pg.display.update()

	def drawSettings(self, text):
		'''Draws the settings again'''
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
		'''updates settings obj internally'''
		self.screenWidth = self.setting['width']
		self.screenHeight = self.setting['height']
		self.fps = self.setting['fps']
		self.controls = self.setting['controls']
	
	def loadingScreen(self, text):
		self.screen.fill((0, 0, 0))
		text = textAssets.Text(text, fontSize=50, fontColour=(255,255,255))
		func.drawTextCentered(text, self.screen, self.screenWidth/2, self.screenHeight/2)
		pg.display.update()


	def _quit(self):
		"""Safe quit function"""
		pg.quit()
		quit()

if __name__ == '__main__':
	MainMenu(settings)
