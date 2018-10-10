def drawTextCentered(text, surface, x, y):
	rect = text.surface.get_rect()
	rect.center = (x, y)
	surface.blit(text.surface, rect)