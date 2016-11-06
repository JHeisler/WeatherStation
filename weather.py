#import libraries
import sys
import Adafruit_DHT #DHT22 library
import Adafruit_BMP.BMP085 as BMP085 #BMP180/085
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
	humidity, temp = Adafruit_DHT.read_retry(sensorDHT,pin)
	values[0] = '{0:0.1f}'.format(humidity) #send humidty from dht
	values[1] = '{0:0.2f}'.format(sensorBMP.read_temperature()) #bmp temp
	values[2] = '{0:0.2f}'.format(sensorBMP.read_pressure())
	values[3] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	
	#serialize data to send
	data = json.dumps(values)
	s.emit('data',data)
	print "sent: " + data

s.shutdown(0)
s.close
