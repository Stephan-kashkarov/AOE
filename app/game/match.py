import pygame as pg
import requests
from app.game import maps
from app.game.assets import starts

class options(object):
	def __init__(self, serverIP, mapType, mapSize, clients, key):
		self.serverIP = serverIP
		self.mapType = mapType
		self.mapSize = mapSize
		self.key = key

class Match(object):
	def __init__(self, options):
		self.serverIP = options.serverIP
		self.map = maps.generateMap(options.mapType, options.mapSize)
		self.units = {}
		for i in range(3):
			self.units[id] = starts.default
			maps.createSpawns(i)
		self.orders = ()
		self.key = options.key

	def getOrders(self):
		self.orders += (requests.get(self.serverIP + "/getOrders") - self.orders)

	def executeOrders(self):
		for order in self.orders:
			run = self.orders.pop(order)
			run.excecute()
			if not run.complete:
				self.orders.insert(0, run)

	def renderMap(self):
		map = self.map
		return map

	def sendMap(self):
		response = requests.post(self.serverIP + "/map/set", json={'key': self.key, 'map': self.map})
		print("Broadcast status", response.status_code, response.reason)

	def run(self):
		self.getOrders()
		self.executeOrders()
		self.map = self.renderMap()
		self.sendMap()