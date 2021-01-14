from picamera import PiCamera
from PIL import Image
from io import BytesIO
from time import sleep


class CaptureCamera:
    def __init__(self):
        # ignore the errors, picamera can only be installed on a raspberry pi
        camera = PiCamera()
        self.camera = camera

    def get_pil_image(self, width: int = 1920, height: int = 1088) -> Image:
        """
        Get a height*width numpy array of whatever the camera is seeing right now
        Avoid changing the default resolution for now, the internal resizing mechanism is weird
        """
        # number of (columns, rows)
        self.camera.resolution = (width, height)
        self.camera.start_preview()
        stream = BytesIO()
        sleep(2)
        self.camera.capture(stream, format='jpeg')
        stream.seek(0)
        return Image.open(stream)
