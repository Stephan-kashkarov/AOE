import os
import json
import requests

import pygame as pg

from app.game import maps
from app.game.assets import starts


class options(object):
	def __init__(self, serverIP, mapType, mapSize, key):
		self.serverIP = serverIP
		self.mapType = mapType
		self.mapSize = mapSize
		self.key = key

class Match(object):
	def __init__(self, options, _map):
		self.serverIP = 'http://' + options.serverIP
		self.map = _map
		self.events = []
		self.key = options.key
		self.units = self.getUnits()
		for id in self.units['keys']:
			self.units[id] = starts.default
		maps.createSpawns(self.units)
		self.sendUnits()
		self.sendMap()


	# Unit Processing
	def getUnits(self):
		return requests.get(str(self.serverIP + '/units/get')).json()

	def sendUnits(self):
		requests.post(
			str(self.serverIP + '/units/set'),
			json=json.dumps({
				'key':self.key,
				'units': self.units
			})
		)

	# Map Processing
	def sendMap(self):
		requests.post(str(self.serverIP + '/map/set'),
		json=json.dumps({
			'key':self.key,
			'map': self.map
		}))

	# Event processing
	def getEvents(self):
		request = requests.get(str(self.serverIP + '/events/get'))
		for event in list(set(request.json()) - set(self.events)):
			self.events.append(event)

	def executeEvents(self):
		events = []
		for event in [x for x in self.events[::-1]]:
			event = self.events.pop(event)
			event.step()
			if not event.complete:
				events.append(event)
		self.events = events

	def checkWin(self):
		for i in self.units['keys']:
			if not len(self.units[i]['units']):
				return True
		return False

	def run(self):
		while True:
			print('Game: tick')
			self.sendUnits()
			self.getEvents()
			self.executeEvents()
			if self.checkWin() == True:
				break
