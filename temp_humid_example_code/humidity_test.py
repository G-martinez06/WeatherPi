import RPi.GPIO as GPIO
import Adafruit_DHT
import time
 
# Adafruit_DHT.DHT22, or Adafruit_DHT.AM2302.
DHTSensor = Adafruit_DHT.DHT11
 
# The pin which is connected with the sensor will be declared here
GPIO_Pin = 23
 
while True:
    humid, temper = Adafruit_DHT.read_retry(DHTSensor, GPIO_Pin)

    if humid is not None and temper is not None:
	print("Temp={0:0.1f}C Humidity={1:0.1f}%".format(temper, humid))
    else:
	print("sensor failure")
    time.sleep(3)