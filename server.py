from gevent import monkey; monkey.patch_all()

from socketio import socketio_manage
from socketio.server import SocketIOServer
from socketio.namespace import BaseNamespace
from socketio.mixins import BroadcastMixin
import redis

db = redis.StrictRedis('localhost',8080,0)

class GetDataNamespace(BaseNamespace, BroadcastMixin):
    def on_data(self):
        # unsure how to request from python client
        #self.request['data']
        #get temp,humidity, pressure,timestamp
        #timer to get data every 1s
        
    def on_set(self):
        db.set("Temperature",temp)
        db.set("Humidity", hum)
        db.set("Pressure",pres)
        db.set("Time",ts)

    # test code
    # msg is a string passed, gets the fields from the db
    # page will request this
    def on_get(self, msg):
        val = db.get(msg)
        #msg will be serialized with pickle, need to change this
        
#take the data and put it in the database
class SendDataNamespace():
    
    def on_msg(self):
        self.broadcast_event(data)
        
    
        
    
def not_found(start_response):
    start_response('404 Not Found', [])
    return ['<h1>Not Found</h1>']


if __name__ == '__main__':
    print 'Listening on port 8080 and on port 843 (flash policy server)'
    SocketIOServer(('0.0.0.0', 8080), Application(),
        resource="socket.io", policy_server=True,
        policy_listener=('0.0.0.0', 843)).serve_forever()
