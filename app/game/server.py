from flask import Flask, Response, request
from flask_socketio import send, emit
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
        # self.gameThread = threading.Thread(name="gameThread", target=self.game.run())
        self.orderStack = []
        self.app = Flask(self.name)
        self.add_endpoint(endpoint='/test', endpoint_name='test', handler=self.testRoute)
        self.add_endpoint(endpoint='/mapGrid', endpoint_name='mapGrid', handler=self.returnMap)
        self.add_endpoint(endpoint='/addOrder', endpoint_name='addOrder', handler=self.addOrder, _methods=['POST'])
        self.add_endpoint(endpoint='/startGame', endpoint_name='startGame', handler=self.run)

    def returnMap(self):
        pass
    
    def addOrder(self):
        pass

    def run(self):
        # self.gameThread.run()
        self.app.run()

    def testRoute(self):
        if request:
            print(dir(request))
        return "Hell0!"

    # Found on stackoverflow "https://stackoverflow.com/questions/40460846/using-flask-inside-class"
    def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None, _methods=None):
        self.app.add_url_rule(endpoint, endpoint_name, EndpointAction(handler), methods=_methods)



# Testing 
if __name__ == '__main__':
    s = Server(None)
    s.run()