import requests
import pygame as pg
import app.menu.textAssets as textAssets
import app.game.client.clientMenu as menu

# tileset https://opengameart.org/content/tiny-16-basic

class PlayerClient(object):
	def __init__(self, serverIP, screen, game, settings):
		self.game = game
		self.settings = settings
		self.screen = screen
		self.serverIP = 'http://' + serverIP
		self.map = [[]]
		self.units = {}
		self.screen.fill((0,0,0))
		self.screenWidth = self.screen.get_rect().width
		self.screenHeight = self.screen.get_rect().height
		self.tilesize = 16
		self.camera = (0,0)
		self.grass = [
			pg.image.load("../assets/imgs/Terrain/grass/basictiles-65.png").convert(),
			pg.image.load("../assets/imgs/Terrain/grass/basictiles-2.png").convert(),
			pg.image.load("../assets/imgs/Terrain/grass/basictiles-1.png").convert()
		]
		self.trees = [
			pg.image.load("../assets/imgs/Terrain/trees/basictiles-5.png").convert(),
			pg.image.load("../assets/imgs/Terrain/trees/basictiles-10.png").convert()
		]
		self.resources = [
			pg.image.load("../assets/imgs/Terrain/resources/basictiles-6.png").convert(),
			pg.image.load("../assets/imgs/Terrain/resources/basictiles-63.png").convert()
		]

	def updateState(self):
		# Gets map
		self.map = requests.get(self.serverIP + '/map/get')
		# Gets Units
		self.units = requests.get(self.serverIP+ '/units/get')
		if self.units == 'gameover':
			return False

	def drawMap(self):
		screenY = 0
		screenX = 0
		for y in range(self.camera[1], self.camera + self.screenHeight/self.tilesize):
			for x in range(self.camera[0], self.camera + self.screenWidth/self.tilesize):
				tile = self.map[y][x]
				if tile == 0:
					pg.display.blit(self.grass[2], (screenX, screenY))
				elif tile == 1:
					pg.display.blit(self.water, (screenX, screenY))
				elif tile == 2:
					pg.display.blit(self.grass[0], (screenX, screenY))
					pg.display.blit(self.trees[1], (screenX, screenY))
				elif tile == 3:
					pg.display.blit(self.grass[0], (screenX, screenY))
					pg.display.blit(self.resources[0], (screenX, screenY))
				elif tile == 4:
					pg.display.blit(self.grass[0], (screenX, screenY))
					pg.display.blit(self.resources[1], (screenX, screenY))
				else:
					pg.display.blit(self.grass[1], (screenX, screenY))
				screenX += self.tilesize
			screenY += self.tilesize

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
		menu = textAssets.Button(self.game, "Menu", x=75, y=25)
		menu.hover()
		menu.draw()
		if menu.clicked():
			# menu.pauseMenu()
			return False
	
	def getCommands(self):
		settings = self.settings['controls']
		for event in pg.event.get():
			if event.type == pg.QUIT:
				return [False, 'quit']
			if event.type == pg.KEYDOWN:
				if event.key == settings['up']:
					if self.camera
					self.camera[0] += 1
		return [True]

	def run(self):
		game = [True]
		while game[0]:
			self.updateState()
			self.drawMap()
			if self.drawUnits() == False:
				break
			if self.drawGUI() == False:
				break
			pg.display.flip()
			game = self.getCommands()
			if len(game) > 1:
				return game[1]
