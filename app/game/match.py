import pygame as pg
import requests
from app.game import maps
from app.game.assets import starts

class Match(object):
    def __init__(self, options):
        self.serverIP = options.serverIP
        self.map = maps.generateMap(options.map, options.mapSize)
        self.clients = options.clients
        self.units = {}
        for client in self.clients:
            self.units[client.id] = starts.default(client.nation)
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
        response = requests.post(self.serverIP + "/mapUpdate", json={'key': self.key, 'map': self.map})
        print("Broadcast status", response.status_code, response.reason)

    def run(self, server):
        self.getOrders()
        self.executeOrders()
        self.map = self.renderMap()
        self.sendMap()