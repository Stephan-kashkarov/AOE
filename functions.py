import pygame as pg


class Button(pg.sprite.Sprite):
	def __init__(self, game, name, x=0, y=0, borderColour=(0,0,0), hoverColour=(0,0,0), size=(150, 50), image=None):
		super().__init__()
		self.game = game
		self.name = name
		self.size = size
		self.x = self.calc(0, x)
		self.y = self.calc(1, y)
		self.hovered = False
		if not image:
			self.text = Text(
				self.name,
				fontColour=(
					(255, 255, 255) if not self.hovered else (255, 100, 100)
				)
			)
		self.image = image
		self.surface = pg.Surface([size[0], size[1]])
		self.borderColour = borderColour
		self.hoverColour = hoverColour
		self.rect = self.surface.get_rect()
		self.rect.x = self.x
		self.rect.y = self.y


	def calc(self, axis, originalVal):
		if originalVal == 'center':
			originalVal = self.game.screenHeight/2 if axis else self.game.screenWidth/2
		changeVal = self.size[axis]
		return int(originalVal - (changeVal/2))


	def draw(self):
		pg.draw.rect(
				self.game.screen,
				self.borderColour,
				pg.Rect(
					self.x,
					self.y,
					self.size[0],
					self.size[1]
				),
				3
			)
		if self.image:
			self.game.screen.blit(self.image, (self.size - 3))
		else:
			pg.draw.rect(
				self.game.screen,
				self.hoverColour if not self.hovered else (100,100,100),
				pg.Rect(
					self.x + 3,
					self.y + 3,
					self.size[0] - 6,
					self.size[1] - 6
				)
			)
			rect = self.text.surface.get_rect()
			rect.center = (self.x + (self.size[0]/2), self.y + (self.size[1]/2))
			self.game.screen.blit(self.text.surface, rect)


	def hover(self):
		if self.rect.collidepoint(pg.mouse.get_pos()):
			self.hovered = True
		else:
			self.hovered = False


	def clicked(self):
		if pg.mouse.get_pressed()[0]:
			if self.rect.collidepoint(pg.mouse.get_pos()):
				return True
		return False


class Text(pg.sprite.Sprite):
	def __init__(self, text, font="Times New Roman", fontSize=20, fontColour=(0,0,0)):
		self.text = text
		self.font = font
		self.fontSize = fontSize
		self.fontColour = fontColour
		self.font = pg.font.SysFont(font, fontSize)
		self.surface = self.font.render(self.text, True, self.fontColour)
		super().__init__()



def drawTextCentered(text, surface, x, y):
	rect = text.surface.get_rect()
	rect.center = (x, y)
	surface.blit(text.surface, rect)