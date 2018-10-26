import pprint
import random

def generateMap(biome, size):
	canvus = []
	for i in range(size):
		canvus.append([])
		for j in range(size):
			canvus[i].append(0)

	# defines map types
	if biome == "forrest":
		trees = (40*size/100)
		water = (30*size/100)
		resorces = (20*size/100)
	elif biome == "desert":
		trees = (20*size/100)
		water = 0
		resorces = (50*size/100)

	# makes water
	x = random.randint(0, size)
	y = random.randint(0, size)
	xChange = 0
	yChange = 0
	while water:
		if y < len(canvus) and x < len(canvus[j]):
			canvus[y][x] = 1
		water -= 1
		while xChange == 0 and yChange == 0:
			xChange = random.randint(-1, 1)
			yChange = random.randint(-1, 1)
		x += xChange
		y += yChange
		xChange = 0
		yChange = 0

	print("New lake!")
	printSegment(x, y, 10, canvus)

	# makes trees
	forrests = (20*trees/100)
	x = random.randint(0, size)
	y = random.randint(0, size)
	xChange = 0
	yChange = 0
	randTrees = random.randint(0, size/2)
	while forrests:
		for i in range(100+randTrees):
			if y < len(canvus) and x < len(canvus[j]):
				canvus[y][x] = 2
			while xChange == 0 and yChange == 0:
				xChange = random.randint(-1, 1)
				yChange = random.randint(-1, 1)
			x += xChange
			y += yChange
			xChange = 0
			yChange = 0
		print("New Forrest!")
		print(x,y)
		printSegment(x, y, 20, canvus)
		x = random.randint(0, size)
		y = random.randint(0, size)
		forrests -= 1
	print(trees)
	while trees:
		x = random.randint(0, len(canvus[0]))
		y = random.randint(0, len(canvus))
		if y < len(canvus) and x < len(canvus[j]):
			canvus[y][x] = 2
		trees -= 1
	return canvus

def findPoint(location):
	pass

def choosePoint(point, player, map):
	pass

def printSegment(x, y, size, canvus):
	for i in range(x-size, x+size):
		for j in range(y-size, y + size):
			if j < len(canvus) and i < len(canvus[j]):
				print(canvus[j][i], end="")
			else:
				print('x', end="")
		print()

if __name__ == '__main__':
	map = generateMap("forrest", 2000)
	# pprint.pprint(map)
