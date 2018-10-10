import pygame as pg
import app.game.maps as maps

class Match(object):
    def __init__(self, players, map, difficulty):
        self.players = players
        self.map = maps.generateMap(map, difficulty)
        self.actions[]
        for player in self.players:
            start = maps.findPoint(1 if player.team else 0)
            maps.startPoint(start, player, map)

    def run(self, orderStack):
        while True:
            for team in self.players:
                team.sprites.update()
            self.flattenMap()

    def flattenMap(self):
        pass
