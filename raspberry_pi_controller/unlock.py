import serial
import time
import io
import picamera
import os
import requests

arduino = serial.Serial('/dev/ttyUSB0', 9600, timeout=1) # Gotta change the com port when we connect the arduin to the pi
time.sleep(7)

def lock():
    arduino.write(b'L')

def unlock():
    arduino.write(b'U')

unlock();