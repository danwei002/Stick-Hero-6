from operator import itemgetter

from PIL import Image

import numpy


class EvanImageProcessor:
    def __init__(self, image, **options):
        self.options = {
            'jump_threshold': 80,
            'segment_size': 3,
            'height_resize_factor': 3,
            'width_resize_factor': 3,
        }
        self.options.update(**options)

        self.image = self._preprocess(image)
        self.pixels = numpy.asarray(self.image)

    def _preprocess(self, image):
        return (
            image
            .convert('L')
            .resize(
                (
                    image.width // self.options['width_resize_factor'],
                    image.height // self.options['height_resize_factor'],
                ),
                Image.ANTIALIAS,
            )
        )

    def _calc_jump(self, before, after):
        return abs(int(before) - int(after))

    def _find_height_bound(self):
        w = self.image.width
        h = self.image.height

        bounds = [0] * w
        prefix_average = [0] * h
        suffix_average = [0] * h

        for j in range(w):
            cur_sum = 0
            for i in range(h):
                cur_sum += self.pixels[i][j]
                prefix_average[i] = cur_sum // (i + 1)
            cur_sum = 0
            for i in range(h - 1, -1, -1):
                cur_sum += self.pixels[i][j]
                suffix_average[i] = cur_sum / (h - i)

            largest_jump, largest_jump_index = 0, 0
            for i in range(1, h):
                jump = self._calc_jump(prefix_average[i - 1], suffix_average[i])
                if jump > largest_jump:
                    largest_jump = jump
                    largest_jump_index = i

            bounds[j] = largest_jump_index if largest_jump > self.options['jump_threshold'] else 0

        bounds = list(filter(lambda x: x, bounds))
        assert bounds

        return sum(bounds) // len(bounds) + h // 20

    def _find_width_bound(self, height_bound):
        SEGMENT_SZ = self.options['segment_size']

        w = self.image.width
        h = self.image.height

        bounds = [0] * h

        average_colour = min(sum(self.pixels[height_bound - h // 10]) // w + 30, 255)

        for i in range(height_bound, h):
            largest_jumps = []
            pixels = list(self.pixels[i])
            pixels += [average_colour] * SEGMENT_SZ
            for j in range(SEGMENT_SZ, len(pixels) - SEGMENT_SZ, SEGMENT_SZ):
                prev_average = sum(pixels[j - SEGMENT_SZ:j]) / SEGMENT_SZ
                next_average = sum(pixels[j:j + SEGMENT_SZ]) / SEGMENT_SZ
                largest_jumps.append((self._calc_jump(prev_average, next_average), j))
            largest_jumps.sort(reverse=True)
            # We only care about the largest 3 jumps.
            largest_jumps = list(map(itemgetter(1), largest_jumps[:3]))
            largest_jumps.sort()

            bounds[i] = largest_jumps

        bounds = bounds[height_bound:]
        width_bound = [0] * 3

        for i in range(3):
            cur_bound = sorted(map(itemgetter(i), bounds))
            ll = len(cur_bound)
            width_bound[i] = sum(cur_bound[ll // 2 - SEGMENT_SZ:ll // 2 + SEGMENT_SZ]) // (2 * SEGMENT_SZ)

        return width_bound

    def find_platform_distance(self):
        height_bound = self._find_height_bound()
        width_bounds = self._find_width_bound(height_bound)

        height_bound *= self.options['height_resize_factor']
        width_bounds = list(map(self.options['width_resize_factor'].__mul__, width_bounds))

        # TODO
        return height_bound, width_bounds
