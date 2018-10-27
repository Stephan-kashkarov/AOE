from flask import Flask, Response, request
from flask_socketio import send, emit
import json

# parts of this code where found 
# on stackoverflow:
# "https://stackoverflow.com/questions/40460846/using-flask-inside-class


class EndpointAction(object):

	def __init__(self, action):
		self.action = action
		self.response = Response(status=200, headers={})

	def __call__(self, *args):
		self.action()
		return self.response

class Server(object):
	def __init__(self, _map):
		#server stuff
		self.name = "Game Server"
		self.app = Flask(self.name)
		
		#Game stuff
		self.map = _map
		self.units = {
			'keys': [0, 1, 2, 3],
			0: {
				'alive': False,
				'units': ()
			},
			1: {
				'alive': False,
				'units': ()
			},
			2: {
				'alive': False,
				'units': ()
			},
			3: {
				'alive': False,
				'units': ()
			}
		}
		self.events = []
		self.key = 'Dev-key'
		
		# Endpoints
		self.add_endpoint(
			endpoint='/test',
			endpoint_name='test',
			handler=self.test
		)
		self.add_endpoint(
			endpoint='/map/get',
			endpoint_name='getMap',
			handler=self.getMap
		)
		self.add_endpoint(
			endpoint='/map/set',
			endpoint_name='setMap',
			handler=self.setMap,
			_methods=['POST']
		)
		self.add_endpoint(
			endpoint='/units/set',
			endpoint_name='setUnits',
			handler=self.setUnits,
			_methods=['POST']
		)
		self.add_endpoint(
			endpoint='/units/get',
			endpoint_name='getUnits',
			handler=self.getUnits
		)
		self.add_endpoint(
			endpoint='/units/add',
			endpoint_name='addUnits',
			handler=self.addUnits,
			_methods=['POST']
		)
		self.add_endpoint(
			endpoint='/events/get',
			endpoint_name='getEvents',
			handler=self.getEvents
		)
		self.add_endpoint(
			endpoint='/events/add',
			endpoint_name='addEvents',
			handler=self.addEvents,
			_methods=['POST']
		)

	# Game Routes

	# set routes
	def setMap(self):
		data = json.loads(request.json)
		print("Json Recieved: {}".format(data))
		if data['key'] == self.key:
			self.map = data['map']
			return True
		return False


	def addUnits(self):
		data = json.loads(request.json)
		print("Json Recieved: {}".format(data))
		if data['key'] == self.key:
			for i in range(0, 3):
				self.units[i]['units'] += data['units'][i]
			return True
		return False

	def setUnits(self):
		data = json.loads(request.json)
		print("Json Recieved: {}".format(data))
		if data['key'] == self.key:
			for i in range(0, 3):
				self.units = data['units']
			return True
		return False

	def addEvents(self):
		data = json.loads(request.json)
		print("Json Recieved: {}".format(data))
		if data['key'] == self.key:
			self.events += data['events']
			return True
		return False

	# get routes
	def getMap(self):
		return json.dumps(self.map)

	def getUnits(self):
		return json.dumps(self.units)

	def getEvents(self):
		return json.dumps(self.events)


	# Misc routes
	def run(self):
		self.app.run()

	def test(self):
		if request:
			print(dir(request))
		return "Hell0!"

	def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None, _methods=None):
		self.app.add_url_rule(endpoint, endpoint_name, EndpointAction(handler), methods=_methods)



# Testing 
if __name__ == '__main__':
	s = Server(None)
	s.run()
