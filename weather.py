#import libraries
from gevent import monkey; monkey.patch_all()
import sys
import Adafruit_DHT # humidity
#BMP180/085
import Adafruit_BMP.BMP085 as BMP085
import datetime
from socketIO_client import SocketIO
import pickle
import time
import logging

logging.basicConfig()
# define sensors and pins
sensorDHT = Adafruit_DHT.DHT22
pin = 26
sensorBMP = BMP085.BMP085()

values = [0,0,0,0]

s = SocketIO('localhost/', 8080)

while 1:
    values[0] = Adafruit_DHT.read_retry(sensorDHT,pin)
    values[1] = sensorBMP.read_temperature()
    values[2] = sensorBMP.read_pressure()
    values[3] = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    print values[0]
    #serialize data to send
    data = pickle.dump(values)
    s.emit('data',data)
    print "sent"

s.shutdown(0)
s.close
