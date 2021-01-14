from time import sleep

from gpiozero import Servo

MIN_PULSE = 1 / 1000
MAX_PULSE = 2 / 1000
FRAME_WIDTH = 20 / 1000
PIN = "GPIO26"
DELTA = 0.11


class Motor:
    def __init__(self):
        servo = Servo(PIN, 0, MIN_PULSE, MAX_PULSE, FRAME_WIDTH, None)
        self.servo = servo
        self.servo.detach()

    def press_down(self, secs: float):
        self.servo.min()
        sleep(secs + DELTA)
        self.servo.mid()
        sleep(secs*2)
        self.servo.detach()

