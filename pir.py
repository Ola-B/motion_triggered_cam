import RPi.GPIO as GPIO
import time
#import datetime
from datetime import datetime
from dateutil import parser
import subprocess
import os

# https://ola-b.github.io/motion_triggered_cam/


SENSOR_PIN = 4
 
GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_PIN, GPIO.IN)

def image_sec_diff(image_list):
    """
    Calculates time difference in sec between images in list
    """
    sec_diff = []
    for d1, d2 in zip(image_list[1::],image_list[0::]):
        date_time_1 = parser.parse(d1[0:len(d1) - 4])
        date_time_2 = parser.parse(d2[0:len(d2) - 4])
        # calculate the number of seconds in between them
        sec = (date_time_2 - date_time_1).total_seconds()
        sec_diff.append(sec)
    print("Seconds between images: " + str(sec_diff))
    return sec_diff

def commit_and_push(image_list):
    """
    Check if it is time to commit
    """
    sec_diff = image_sec_diff(image_list)

    # Commit if more than 1800 sec between last images
    if int(sec_diff[0])>1800:
        rc = subprocess.call("./git_push.sh")
        print("Images comited to github")
    # also commit after a bunch of quick images in front of a long gap
    if (int(sec_diff[0])<30 and int(sec_diff[1])<30 and int(sec_diff[2])<30 and int(sec_diff[3])<30 and int(sec_diff[4])>1800):
        rc = subprocess.call("./git_push.sh")
        print("Images comited to github")
    

# ---------------------------------------------------------------- #
# 
# ---------------------------------------------------------------- #
def build_readme(image_list):
    """
    Makes a readme.md with link to images
    """
    
    static_md ="""# Motion_triggered_cam
Raspberry motion detector (PIR) triggers webcam to take photo, create html with carusell showing the last n images.

See: [https://ola-b.github.io/motion_triggered_cam/](https://ola-b.github.io/motion_triggered_cam/)\n

Or images in ./docs/images/*.jpg
"""

    # create html file...
    file_md = open("/home/pi/git/github/motion_triggered_cam/README.md", "w")
    file_md.writelines(static_md)

    for ii in range(0,len(image_list)):
#        file_md.writelines('!['+image_list[ii]+'](.docs/images/'+image_list[ii]+' "'+image_list[ii]+'")\n')
        file_md.writelines('!['+image_list[ii]+'](https://github.com/Ola-B/motion_triggered_cam/blob/main/docs/images/'+image_list[ii]+' "'+image_list[ii]+'")\n')

    # or use: ![Alt text](https://github.com/Ola-B/motion_triggered_cam/blob/main/images/img.jpg "a title")



    file_md.close()

# ---------------------------------------------------------------- #
# 
# ---------------------------------------------------------------- #
def build_html(image_list):
    """
    Makes a html page to go in the github pages a website
    """
    
    # Sorts list reverse to get last image first
    image_list.sort(reverse=True)
    
    static_html_head ="""
<!DOCTYPE html>
<html lang="en">
<head>
  <title>Bølle & Bølle</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
  <style>
  /* Make the image fully responsive */
  .carousel-inner img {
    width: 100%;
    height: 100%;
  }
  </style>
</head>
<body>\n\n"""
    static_html_end = """
</body>
</html>"""
    # create html file...
    file_html = open("/home/pi/git/github/motion_triggered_cam/docs/index.html", "w")
    file_html.writelines(static_html_head)
    
    file_html.writelines('<div id="demo" class="carousel slide" data-ride="carousel">\n')
    file_html.writelines('   <ul class="carousel-indicators">\n')
    for ii in range(0,len(image_list)):
        # print(ii, image_list[ii])
        if ii==0:
            list_str = '     <li data-target="#demo" data-slide-to="0" class="active"></li>\n'
        else:
            list_str = '     <li data-target="#demo" data-slide-to="'+str(ii)+'"></li>\n'
        file_html.writelines(list_str)
        # print(list_str)
    file_html.writelines('</ul>\n\n')
    
    
    file_html.writelines('<div class="carousel-inner">\n')

    for ii in range(0,len(image_list)):
        if ii==0:
            file_html.writelines('<div class="carousel-item active">\n')
#            file_html.writelines('<img src="images/'+image_list[ii]+'" alt="'+image_list[ii]+'" width="1100" height="500">\n')
            file_html.writelines('<img src="images/'+image_list[ii]+'" alt="'+image_list[ii]+'" width="1280" height="720">\n')
            file_html.writelines('<div class="carousel-caption">\n')
            file_html.writelines('<p>'+image_list[ii]+'</p>\n')
            file_html.writelines('</div>\n')
            file_html.writelines('</div>\n')
        else:
            file_html.writelines('<div class="carousel-item">\n')
#            file_html.writelines('<img src="images/'+image_list[ii]+'" alt="'+image_list[ii]+'" width="1100" height="500">\n')
            file_html.writelines('<img src="images/'+image_list[ii]+'" alt="'+image_list[ii]+'" width="1280" height="720">\n')
            file_html.writelines('<div class="carousel-caption">\n')
            file_html.writelines('<p>'+image_list[ii]+'</p>\n')
            file_html.writelines('</div>\n')
            file_html.writelines('</div>\n')

    
    file_html.writelines("""</div>
  <a class="carousel-control-prev" href="#demo" data-slide="prev">
    <span class="carousel-control-prev-icon"></span>
  </a>
  <a class="carousel-control-next" href="#demo" data-slide="next">
    <span class="carousel-control-next-icon"></span>
  </a>
</div>""")
    
    file_html.writelines(static_html_end)

    file_html.close()


# ---------------------------------------------------------------- #
# 
# ---------------------------------------------------------------- #
def image_files():
    """
    Check what images we got and puts in a list
    Removes (deletes) oldest image so not more than "n" images
    """
    # Puts all filenames found in directory into a list
    path = '/home/pi/git/github/motion_triggered_cam/docs/images'
    files = os.listdir(path)
    image_list = []
    for f in files:
        image_list.append(f)

    # Sorts list
    image_list.sort()
    # print("Images in directory: "+str(image_list)[1:-1])

    # If more than n images remove the first so only n in total
    n = 25
    if len(image_list)>n:
        remove_images = image_list[0:len(image_list)-n] # get first images to remove
        # print("Images to remove: ",remove_images)
        image_list = image_list[-n:]                    # get last images to store
        # print("Images to keep: ",image_list)
        for r in remove_images:
            os.remove(path+"/"+r)
            # print("Deleting file: ",path+"/"+r)

    if len(image_list)>=1:
        # Build html for github pages
        build_html(image_list)
        # Build readme to also hold the images
        build_readme(image_list)
        # Commit changes to github
        commit_and_push(image_list)

# ---------------------------------------------------------------- #
# 
# ---------------------------------------------------------------- #
def motion(SENSOR_PIN):
    """
    In case of a motion detection run webcam.sh script to take image with webcam
    """
    # Here, alternatively, an application / command etc. can be started.
    filename = str(datetime.now())+".jpg"
    print("There was a movement! New file: ",filename)
    rc = subprocess.call("./webcam.sh")
    time.sleep(2)
    image_files()
    

print("PIR setup...")
time.sleep(5)
print("Ready")

try:
    GPIO.add_event_detect(SENSOR_PIN , GPIO.RISING, callback=motion)
    while 1:
        time.sleep(20000)
except KeyboardInterrupt:
    print("Finish...")
    GPIO.cleanup()
    