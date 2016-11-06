#import libraries
from gevent import monkey; monkey.patch_all()
import sys
import Adafruit_DHT
#BMP180/085
import Adafruit_BMP.BMP085 as BMP085
import datetime
from socketIO_client import SocketIO
import json
import logging

logging.basicConfig()

# define sensors and pins
sensorDHT = Adafruit_DHT.DHT22
pin = 26
sensorBMP = BMP085.BMP085()

values = [0,0,0,0]

s = SocketIO('localhost:8080')

while 1:
	dht = Adafruit_DHT.read_retry(sensorDHT,pin)
	values[0] = dht[0]
	values[1] = sensorBMP.read_temperature()
	values[2] = sensorBMP.read_pressure()
	values[3] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	#serialize data to send
	data = json.dumps(values)
	s.emit('data',data)
	print "sent: " + data

s.shutdown(0)
s.close
