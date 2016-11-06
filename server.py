from gevent import monkey; monkey.patch_all()
import time
from socketio import socketio_manage
from socketio.server import SocketIOServer
from socketio.namespace import BaseNamespace
from socketio.mixins import BroadcastMixin
#import redis maybe use another db instead
import logging
import json

logging.basicConfig()

connected = 0
piData = []
#db = redis.StrictRedis('localhost',8080,0)
 
class StoreNamespace(BaseNamespace,BroadcastMixin):
    # Test method to print if weather.py connects
    def recv_connect(self):
        print "StoreNamespace connected"
 
    #self is the socket you received on (From weather.py), msg is recieved data
    def on_data(self, msg):
        print "received: " + msg
        #print msg
        global piData
        piData = msg
 
        #db.set("Temperature",piData[1])
        #db.set("Humidity", piData[0])
        #db.set("Pressure",piData[2])
        #db.set("Time",piData[3])
 
class GetNamespace(BaseNamespace,BroadcastMixin):
    def recv_connect(self):
        print "GetNamespace connected"
        connected = 1
        global piData
        while(connected==1):
            self.broadcast_event('msg2', piData)
            time.sleep(5)

    def __del__(self):
        print "socket disconnected"
        connected = 0

# Application class to set up the namespaces
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
                '': StoreNamespace,
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
