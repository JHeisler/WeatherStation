# WeatherStation
**Cyberphysical Systems Project**

**Client Program**

Takes data from BMP and DHT sensors, sends it to the Server program via websockets along with the date/time.


Install the Adafruit libaries and the  python SocketIO client v0.5.6 on Pi. 4.7k ohm resistor on the dht


-Install socketIO-client 0.5.6::
```pip install -U socketIO-client==0.5.6```

-Adafruit bmp install- https://github.com/adafruit/Adafruit_Python_BMP

-Adafruit dht install- https://github.com/adafruit/Adafruit_Python_DHT



**Server**

Runs the server to serve the webpage

Using apache, index.html replaces their standard index.html and add /static/ to the same folder. 

Install apache and sqlite3
```
sudo apt-get install apache2 php5 php5-mysql libapache2-mod-php5
sudo apt-get install sqlite3
```

Install gevent-SocketIO::
```
  git clone git://github.com/abourget/gevent-socketio.git
  cd gevent-socketio
  python setup.py install
```

**Server Program**

Will take data from the client's sensors and then send that data to the webpage that is served by the server.

Run on the server, will need to install gevent/socketIO server (look up to see if server is included in gevent)

-pip install gevent-socketio

-Might use redis for database- if so then install redis.

