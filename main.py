from time import sleep

from camera.capture import CaptureCamera
from image_processing.evan_image_processor import EvanImageProcessor as ImageProcessor
from image_processing.image_cropper import ImageCropper
from logic.gameLogic import findTime
from motors.motor import Motor


if __name__ == "__main__":
    cam = CaptureCamera()

    counter = 0
    motor = Motor()
    while True:
        sleep(2)

        out = cam.get_pil_image()
        out.save('{}.jpg'.format(counter))

        img = ImageCropper(out).crop()
        img.save('{}-cropped.jpg'.format(counter))
        height_bound, width_bounds = ImageProcessor(img, jump_threshold=80, segment_size=2).find_platform_distance()
        distance = width_bounds[1] - width_bounds[0]

        print("--- point: {}".format(counter))
        print(distance)
        time = findTime(distance, img.width)
        print(time)

        if distance < 50:
            time += 0.03
        elif distance >= 60 and distance < 140:
            time += 0.1
        motor.press_down(time)
        counter += 1
