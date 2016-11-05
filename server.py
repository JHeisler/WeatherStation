from gevent import monkey; monkey.patch_all()

from socketio import socketio_manage
from socketio.server import SocketIOServer
from socketio.namespace import BaseNamespace
from socketio.mixins import BroadcastMixin
#import redis maybe use another db instead
import pickle
import time
import logging

logging.basicConfig()

connected = 0
piData = []
#db = redis.StrictRedis('localhost',8080,0)
 
class StoreNamespace(BaseNamespace,BroadcastMixin):
    # Test method to print if weather.py connects
    def recv_connect(self):
        print "StoreNamespace connected"
 
    def on_data(self, msg): # self is the socket, msg is the received data
        piData = pickle.load(msg)
        # maybe try printing the msg or piData to make sure it came through ok
 
        #self is the socket you received on (From weather.py)
        self.broadcast_event('msg',piData[0]) #test
        #db.set("Temperature",piData[1])
        #db.set("Humidity", piData[0])
        #db.set("Pressure",piData[2])
        #db.set("Time",piData[3])
 
class GetNamespace(BaseNamespace,BroadcastMixin):
    def recv_connect(self):
        print "GetNamespace connected"
        connected = 1
        while(connected == 1):
            self.broadcast_event('msg2',piData[1])
            time.sleep(5)
     
    def __del__(self):
        print "socket disconnected"
        connected = 0

# You need the application class to set up the namespaces
# weather.py will connect to /Store
# html page will connect to /Get
#### Web server to direct incoming connections
class Application(object):
    def __init__(self):
        self.buffer = []
 
    def __call__(self, environ, start_response):
        path = environ['PATH_INFO'].strip('/') or 'index.html'
 
 
        if path.startswith("socket.io"):
            socketio_manage(environ, {
                '/Store': StoreNamespace,
                '/Get': GetNamespace})
        else:
            return not_found(start_response)
 
 
def not_found(start_response):
    start_response('404 Not Found', [])
    return ['<h1>Not Found</h1>']
 
 
if __name__ == '__main__':
    print 'Listening on port 8080 and on port 843 (flash policy server)'
    SocketIOServer(('0.0.0.0', 8080), Application(),
        resource="socket.io", policy_server=True,
        policy_listener=('0.0.0.0', 843)).serve_forever()
