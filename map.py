import pygame as pg

class Button(pg.sprite.Sprite):
	def __init__(self, game, name, x=0, y=0, borderColour=(0,0,0), size=(150, 50)):
		self.game = game
		self.name = name
		self.x = self.calc(0, x)
		self.y = self.calc(1, y)
		self.borderColour = borderColour
		self.size = size
		self.hovered = False
		self.draw()
		super().__init__()

	def calc(self, axis, originalVal):
		if originalVal == 'center':
			editVal = self.game.screenHeight if axis else self.game.screenWidth
		
		newVal = (editVal/2) + (originalVal/2)
		return newVal

	def draw(self):
		pass

	def hover(self):
		hovered = True
		pass

	def clicked(self):
		print(self.name)
		pass