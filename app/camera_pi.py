import io
import time
import picamera
from app.base_camera import BaseCamera
from threading import Thread
import datetime

FOTO_SEQUENCE_ACTIVE_STATUS = False
FOTO_SEQUENCE_PATH_PLANT = "app/static/img/plant/"

FOTO_SEQUENCE_WAITING_TIME = 30*60
FOTO_SEQUENCE_OFF_TIME_MIN = 22
FOTO_SEQUENCE_OFF_TIME_MAX = 6

HEIGHT =320
WIDTH = 240


class Camera(BaseCamera):
    @staticmethod
    def frames():
        with picamera.PiCamera() as camera:
            # let camera warm up
            time.sleep(2)

            stream = io.BytesIO()
            for _ in camera.capture_continuous(stream, 'jpeg',
                                                 use_video_port=True):
                # return current frame
                stream.seek(0)
                yield stream.read()

                # reset stream for next frame
                stream.seek(0)
                stream.truncate()


class PictureCamera():
    """Klasse um alle t Sekunden ein Bild zu machen und abzuspeichern, die Kamera wird automatisch im Thread betrieben.
    PROBLEM: FUnktion take_fotos kann von außen bis jetzt nicht gestoppt werden."""
    def __init__(self):
        self.thread = Thread(target=self.take_fotos)
        self.camera = picamera.PiCamera()
        self.camera.resolution = (WIDTH, HEIGHT)
        time.sleep(2)

    def take_fotos(self):
        """Takes a Foto every WAITING TIME time and stores at in an certain path"""
        while FOTO_SEQUENCE_ACTIVE_STATUS:
            hour = int(datetime.datetime.now().strftime("%H"))
            if hour < FOTO_SEQUENCE_OFF_TIME_MIN and hour > FOTO_SEQUENCE_OFF_TIME_MAX:
                self.camera.capture(FOTO_SEQUENCE_PATH_PLANT+ datetime.datetime.now().strftime("%Y%m%d_%H_%M_%S")+".jpg")

            time.sleep(FOTO_SEQUENCE_WAITING_TIME)

    def start(self):
        print("starte Thread")
        self.thread.start()

    def __del__(self):
        self.camera.close()


