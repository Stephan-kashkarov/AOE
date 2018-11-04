import requests
import pygame as pg
from app.menu import textAssets

class PlayerClient(object):
	def __init__(self, serverIP, screen):
		self.screen = screen
		self.serverIP = 'http://' + serverIP
		self.map = [[]]
		self.units = {}
		self.screen.fill((0,0,0))
		self.screenWidth = self.screen.get_rect().width
		self.screenHeight = self.screen.get_rect().height

	def updateState(self):
		# Gets map
		self.map = requests.get(self.serverIP + '/map/get')
		# Gets Units
		self.units = requests.get(self.serverIP+ '/units/get')
		if self.units == 'gameover':
			return False

	def drawMap(self):
		pass

	def drawUnits(self):
		pass

	def drawGUI(self):
		pg.draw.rect(
			self.screen,
			(150, 150, 150),
			pg.Rect(
				0,
				3*self.screenHeight/4,
				self.screenWidth,
				self.screenHeight
			)
		)
		pg.draw.rect(
			self.screen,
			(150, 150, 150),
			pg.Rect(
				0,
				0,
				self.screenWidth,
				self.screenHeight/20
			)
		)
	
	def getCommands(self):
		for event in pg.event.get():
			if event.type == pg.QUIT:
				return [False, 'quit']
		return [True]

	def run(self):
		game = [True]
		while game[0]:
			self.updateState()
			self.drawGUI()
			self.drawMap()
			if self.drawUnits() == False:
				break
			pg.display.flip()
			game = self.getCommands()
			if len(game) > 1:
				return game[1]
