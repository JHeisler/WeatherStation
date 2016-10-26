#import libraries
import sys
import Adafruit_DHT # humidity
#BMP180/085
import Adafruit_BMP.BMP085 as BMP085
import datetime
from socketIO_client import SocketIO, BaseNamespace
import pickle

# define sensors and pins
sensorDHT = Adafruit_DHT.AM2302
pin = 23
sensorBMP = BMP.BMP085()

values = []

socketIO = SocketIO('localhost', 80, Namespace)
socketIO.wait(seconds=1)

class Namespace(BaseNamespace):
    def data():

        while 1:
            humidity = Adafruit_DHT.read_retry(sensorDHT,pin)
            values[0] = "{:0.1f}%".format(humidity)
            values[1] = "{0:0.2f} *C".format(sensorBMP.read_temperature())
            values[2] = "{0:0.2f} Pa".format(sensorBMP.read_pressure())
            values[3] = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            
            #serialize data to send
            data = pickle.dump(values)
            s.send(data)
            print "sent"


        s.shutdown(0)
        s.close
