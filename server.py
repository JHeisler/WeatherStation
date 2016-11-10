from gevent import monkey; monkey.patch_all()
import time
from socketio import socketio_manage
from socketio.server import SocketIOServer
from socketio.namespace import BaseNamespace
from socketio.mixins import BroadcastMixin
import logging
import json
import sqlite3

# db connect and cursor
conn = sqlite3.connect('weather.db')
db = conn.cursor()

# error logger
logging.basicConfig()

connected = 0
 
# Recieves data from the websocket and stores it in the database
class StoreNamespace(BaseNamespace,BroadcastMixin):
    # Test method to print if weather.py connects
    def recv_connect(self):
        print "StoreNamespace connected"
 
    #self is the socket you received on (From weather.py), msg is recieved data
    def on_data(self, msg):
        print "received: " + msg
        global piData #serialized data to send to webpage
        piData = msg
       
        ### DB section
        global parsedData
        parsedData = json.loads(piData) #deserialize
        
        # creates a weather table if there is none
        db.execute('''CREATE TABLE if not exists weather
             (humidity, temperature, pressure, date)''')
        # set DB values
        db.execute("INSERT INTO weather VALUES(?,?,?,?)", parsedData)

# Retrieves data for the webpage, database not implemented yet
class GetNamespace(BaseNamespace,BroadcastMixin):
    def recv_connect(self):
        print "GetNamespace connected"
        connected = 1
        global piData
        while(connected==1):
            self.broadcast_event('msg2', piData)
            time.sleep(2)

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
 

if __name__ == '__main__':
    print 'Listening on port 8080 and on port 843 (flash policy server)'
    SocketIOServer(('0.0.0.0', 8080), Application(),
        resource="socket.io", policy_server=True,
        policy_listener=('0.0.0.0', 843)).serve_forever()
