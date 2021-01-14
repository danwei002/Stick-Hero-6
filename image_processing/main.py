import argparse

from PIL import Image, ImageDraw

from evan_image_processor import EvanImageProcessor as ImageProcessor
from image_cropper import ImageCropper


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('image', help='Image to process')
    parser.add_argument('--save', '-s', nargs=1, help='Save processed file')
    parser.add_argument('--debug', '-d', action='store_true', default=False, help='Print debug info')

    args = parser.parse_args()

    image = Image.open(args.image)
    img = ImageCropper(image).crop()
    height_bound, width_bounds = ImageProcessor(img).find_platform_distance()

    if args.debug:
        print('Height bound:', height_bound)
        print('Width bounds:', width_bounds)

    if args.save:
        draw = ImageDraw.Draw(img)
        draw.line([width_bounds[0], height_bound, width_bounds[1], height_bound], 255, 7)
        img.save(args.save[0])

    print('Distance:', width_bounds[1] - width_bounds[0])
    print('Platform width:', width_bounds[2] - width_bounds[1])


if __name__ == '__main__':
    main()
