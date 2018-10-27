import json
import requests

import pygame as pg

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
		self.units = self.getUnits()
		for id in self.units["keys"]:
			self.units[id] = starts.default
		maps.createSpawns(self.units)
		self.sendUnits()
		self.sendMap()
		self.events = ()
		self.key = options.key


	# Unit Processing
	def getUnits(self):
		return requests.get(self.serverIP + '/units/get')

	def sendUnits(self):
		requests.post(
			self.serverIP + '/units/set',
			json=json.dumps({
				'key':self.key,
				'units': self.units
			})
		)

	# Map Processing
	def sendMap(self):
		requests.post(self.serverIP + "/map/set",
		json=json.dumps({
			'key':self.key,
			'map': self.map
		}))

	# Event processing
	def getEvents(self):
		self.events += (requests.get(self.serverIP + '/events/get') - self.events)

	def executeEvents(self):
		events = []
		for event in [x for x in self.events[::-1]]:
			event = self.events.pop(event)
			event.step()
			if not event.complete:
				events.append(event)
		self.events = events

	def run(self):
		while True:
			self.sendUnits()
			self.getEvents()
			if self.executeEvents() == False:
				break
