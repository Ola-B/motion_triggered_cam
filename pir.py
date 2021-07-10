import RPi.GPIO as GPIO
import time
import datetime
import subprocess
import os

# https://ola-b.github.io/motion_triggered_cam/


SENSOR_PIN = 4
 
GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_PIN, GPIO.IN)

#https://github.com/Ola-B/motion_triggered_cam/blob/main/images/2021-07-10T22:26:20.jpg?raw=true

def image_files():
    path = '/home/pi/git/github/motion_triggered_cam/images'
    files = os.listdir(path)
    file_html = open("/home/pi/git/github/motion_triggered_cam/index.html", "w")
    file_html.writelines("<!DOCTYPE html>")
    file_html.writelines("<html>")
    file_html.writelines("<body>")

    for f in files:
        url = '"https://github.com/Ola-B/motion_triggered_cam/tree/main/images/'+f+'?raw=true"'
        file_html.writelines("<img src="+url+" alt='Cat'>\n")
        print(f)
    
    file_html.writelines("</body>")
    file_html.writelines("</html>")
    
    file_html.close()

def motion(SENSOR_PIN):
    # Here, alternatively, an application / command etc. can be started.
    filename = str(datetime.datetime.now())+".jpg"
    print("There was a movement! New file: ",filename)
    rc = subprocess.call("./webcam.sh")
    time.sleep(2)
    image_files()
    
    rc = subprocess.call("./git_push.sh")

print("PIR setup...")
time.sleep(5)
print("Ready")

try:
    GPIO.add_event_detect(SENSOR_PIN , GPIO.RISING, callback=motion)
    while 1:
        time.sleep(500)
except KeyboardInterrupt:
    print("Finish...")
    GPIO.cleanup()
    
    