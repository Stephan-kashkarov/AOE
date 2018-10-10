from flask import Flask, Response
import threading


# Found on stackoverflow "https://stackoverflow.com/questions/40460846/using-flask-inside-class
class EndpointAction(object):

    def __init__(self, action):
        self.action = action
        self.response = Response(status=200, headers={})

    def __call__(self, *args):
        self.action()
        return self.response

class Server(object):
    def __init__(self, match):
        self.name = "Game Server"
        self.game = match
        self.gameThread = threading.Thread(name="gameThread", target=self.game.run())
        self.orderStack = []
        self.app = Flask(self.name)
        self.add_endpoint(endpoint='/mapGrid', endpoint_name='mapGrid', handler=self.returnMap)
        self.add_endpoint(endpoint='/addOrder', endpoint_name='addOrder', handler=self.addOrder)
        self.add_endpoint(endpoint='/startGame', endpoint_name='startGame', handler=self.run)

    def returnMap(self):
        pass
    
    def addOrder(self):
        pass

    def run(self):
        self.gameThread.run()
        self.app.run()

    # Found on stackoverflow "https://stackoverflow.com/questions/40460846/using-flask-inside-class"
    def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None):
        self.app.add_url_rule(endpoint, endpoint_name, EndpointAction(handler))