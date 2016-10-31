from gevent import monkey; monkey.patch_all()

from socketio import socketio_manage
from socketio.server import SocketIOServer
from socketio.namespace import BaseNamespace
from socketio.mixins import BroadcastMixin
#import redis maybe use another db instead
import pickle

db = redis.StrictRedis('localhost',8080,0)

class GetDataNamespace(BaseNamespace):
    def on_data(self):
        piData = pickle.load(values)
        #db.set("Temperature",piData[1])
        #db.set("Humidity", piData[0])
        #db.set("Pressure",piData[2])
        #db.set("Time",piData[3])

class SendDataNamespace(BaseNamespace, BroadcastMixin):
    
    def on_msg(self):
        self.broadcast_event(piData)

    
def not_found(start_response):
    start_response('404 Not Found', [])
    return ['<h1>Not Found</h1>']


if __name__ == '__main__':
    print 'Listening on port 8080 and on port 843 (flash policy server)'
    SocketIOServer(('0.0.0.0', 8080), Application(),
        resource="socket.io", policy_server=True,
        policy_listener=('0.0.0.0', 843)).serve_forever()
