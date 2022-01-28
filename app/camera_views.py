from app import app

from flask import Response, render_template, make_response
from app.camera_pi import Camera, PictureCamera
import os


picture_camera = PictureCamera()
picture_camera.start()



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
    """get all files from plant folder with specific ending"""
    files = os.listdir("app/static/img/plant")#
    files_ = []
    for file in files:
        if file.lower().endswith(".jpg"):
            files_.append(file)

    return list(reversed((sorted(files_))))

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
    print(pic_names, "pic_names")
    dates = []
    for name in pic_names:
        dates.append(get_datetime_from_pic_names(name)) 
    return render_template("public/pflanzen_bilder.html", pic_names=pic_names, dates=dates)