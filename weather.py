#import libraries
import sys
import Adafruit_DHT # humidity
#BMP180/085
import Adafruit_BMP.BMP085 as BMP085
import datetime
import socket

# define sensors and pins
sensorDHT = Adafruit_DHT.AM2302
pin = 23
sensorBMP = BMP.BMP085()


s = socket.socket()
host = socket.gethostname()
port = 80

s.connect((host,port))

#s.recv(1024)

def msg():

    while 1:
        humidity = Adafruit_DHT.read_retry(sensorDHT,pin)
        hum = "{:0.1f}%".format(humidity)
        temp = "{0:0.2f} *C".format(sensorBMP.read_temperature())
        Pressure = "{0:0.2f} Pa".format(sensorBMP.read_pressure())
        ts = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        s.send(hum)
        s.send(temp)
        s.send(Pressure)
        s.send(ts)
        print "sent"


    s.shutdown(0)
    s.close
