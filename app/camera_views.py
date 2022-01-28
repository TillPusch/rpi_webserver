from app import app

from flask import Response, render_template, make_response
from app.camera_pi import Camera
from threading import Thread
import picamera
import time
import os
import datetime

PATH_TO_PLANT = "app/static/img/plant/"
HEIGHT =320
WIDTH = 240

def take_fotos():
    camera = picamera.PiCamera()
    camera.resolution = (WIDTH, HEIGHT)
    time.sleep(2)
    while False:
        hour = int(datetime.datetime.now().strftime("%H"))
        if hour < 22 and hour > 6:
            camera.capture(PATH_TO_PLANT+ datetime.datetime.now().strftime("%Y%m%d_%H_%M_%S")+".jpg")
        time.sleep(30*60)
    camera.close()

tr1 = Thread(target=take_fotos)
tr1.start()

@app.route("/live-camera")
def live_camera():
    return render_template("public/live_camera.html")

def gen(camera):
    """Video streaming generator function."""
    yield b'--frame\r\n'
    while True:
        frame = camera.get_frame()
        yield b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n--frame\r\n'


@app.route("/video-feed")
def video_feed():
    return Response(gen(Camera()), mimetype='multipart/x-mixed-replace; boundary=frame' ) 
   
def get_pic_names():
    """get all files from plant folder"""
    files = os.listdir("app/static/img/plant")#
    #print(files)
    return files

def get_datetime_from_pic_names(filename):
    """format: YYYYMMDD_HH_MM_SS.jpg"""
    year = filename[0:4]
    month = filename[4:6]
    day = filename[6:8]
    hour = filename[9:11]
    minute = filename[12:14]
    second = filename[15:17]

    return f'{hour}:{minute}Uhr {day}.{month}.{year}'



@app.route("/pflanze")
def pflanze():
    pic_names = get_pic_names()
    dates = []
    for name in pic_names:
        dates.append(get_datetime_from_pic_names(name)) 
    return render_template("public/pflanzen_bilder.html", pic_names=pic_names, dates=dates)