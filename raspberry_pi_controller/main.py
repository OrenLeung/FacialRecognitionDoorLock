import serial
import time
import io
import picamera
import os
import requests

# Gotta change the com port when we connect the arduin to the pi
arduino = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
time.sleep(7)


def capture():
    if(os.path.exists('/home/pi/Desktop/images/guest_photo.jpg')):
        os.remove('/home/pi/Desktop/images/guest_photo.jpg')
    camera = picamera.PiCamera()
    camera.hflip = True
    camera.capture("/home/pi/Desktop/images/guest_photo.jpg")
    camera.close()


def upload():
    fileToSend = "/home/pi/Desktop/images/guest_photo.jpg"
    url = "http://104.198.69.57:8080/api/identifyguest"
    files = [('guest_photo', (fileToSend, open(
        fileToSend, 'rb'), 'application/octet'))]
    r = requests.post(url, files=files)
    result = str(r.content, "utf-8")
    return result


def lock():
    arduino.write(b'L')


def unlock():
    arduino.write(b'U')


lock()
while(True):
    # should be changed on how often we want to run the entire process.
    time.sleep(3)
    capture()
    result = upload()
    print(result)
    if(result == "true"):
        unlock()
        # Time after which the door should automatically be locked.
        time.sleep(5)
        lock()
    # break
