# WeatherStation
Cyberphysical Systems Project

Client Program
Install the Adafruit libaries and the  python SocketIO client v0.5.6 on Pi.

"pip install -U socketIO-client==0.5.6"
Adafruit bmp install

https://github.com/adafruit/Adafruit_Python_BMP

Adafruit dht install
https://github.com/adafruit/Adafruit_Python_DHT

Server
Using apache, index.html replaces their standard index.html and add /static/ to the same folder. 


Server Program
Run on the server, will need to install gevent/socketIO server (look up to see if server is included in gevent)

"pip install gevent-socketio"

Might use redis for database- if so then install redis.
