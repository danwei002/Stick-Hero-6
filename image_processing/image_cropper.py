import numpy


class ImageCropper:
    def __init__(self, image, **options):
        self.image = image
        self.pixels = numpy.array(image)
        self.height = self.pixels.shape[0]
        self.width = self.pixels.shape[1]

        self.options = {
            'threshold': 40,  # Changed this to 40 from 30, 30 was a bit of a tight tolerance for some images
            'vertical_margin': 69,
        }
        self.options.update(**options)

    def _in_threshold(self, rgb):
        threshold = self.options['threshold']
        return rgb[0] < threshold and rgb[1] < threshold and rgb[2] < threshold

    def _find_vertical_edge(self, initial_row=0, initial_col=0):
        for col in range(initial_col, self.width):
            rgb = self.pixels[initial_row, col]
            if self._in_threshold(rgb):
                return col

        return -1

    def _find_horizontal_edge(self, initial_row=None, initial_col=0):
        if initial_row is None:
            initial_row = int(self.height / 5) * 4  # set initial row to 80% height of image (to avoid the floor colour)

        for row in range(initial_row, 0, -1):
            rgb = self.pixels[row, initial_col]
            if self._in_threshold(rgb):
                return row

        """
        Original Image Cropping code is here (it loops down from the top row)
        
        for row in range(initial_row, self.height):
            rgb = self.pixels[row, initial_col]
            if self._in_threshold(rgb):
                return row
        """

        return -1

    def crop(self):
        left_edge = self._find_vertical_edge()
        right_edge = self._find_vertical_edge(initial_col=left_edge + self.options['vertical_margin'])

        bottom_edge = self._find_horizontal_edge(initial_col=(left_edge + right_edge) // 2)

        image = self.image
        if left_edge != -1 and right_edge != -1:
            crop_tuple = (left_edge + self.options['vertical_margin'] // 2, 0, right_edge, bottom_edge)
            image = self.image.crop(crop_tuple)

        return image
