#import libraries
import sys
import Adafruit_DHT
#BMP180/085
import Adafruit_BMP.BMP085 as BMP085
import datetime
import pickle
import socket

# define sensors and pins
sensorDHT = Adafruit_DHT.DHT22
pin = 26
sensorBMP = BMP085.BMP085()

values = [0,0,0,0]

port = 443
s = socket.socket()
s.connect(('localhost',port))


while 1:
    values[0] = Adafruit_DHT.read_retry(sensorDHT,pin)
    values[1] = sensorBMP.read_temperature()
    values[2] = sensorBMP.read_pressure()
    values[3] = datetime.datetime.now()
    print values[0]
    #serialize data to send
    data = pickle.dumps(values)
    s.sendall(data)
    print "sent"
s.close()
