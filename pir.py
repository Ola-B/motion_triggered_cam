import RPi.GPIO as GPIO
import time
import datetime
import subprocess
 
SENSOR_PIN = 4
 
GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_PIN, GPIO.IN)


def motion(SENSOR_PIN):
    # Here, alternatively, an application / command etc. can be started.
    print("There was a movement!",str(datetime.datetime.now()))
    rc = subprocess.call("./webcam.sh")
    time.sleep(10)
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
    
    