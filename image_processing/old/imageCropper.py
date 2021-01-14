import numpy
from PIL import Image

def findLeftEdge(pixels, threshold):
    row = 0
    width = pixels.shape[1]

    for col in range(width):
        RGB = pixels[row, col]
        R = RGB[0]
        G = RGB[1]
        B = RGB[2]

        if R < threshold and G < threshold and B < threshold:
            return col

        col += 1

    return -1

def findRightEdge(pixels, col, threshold):
    row = 0
    width = pixels.shape[1]
    for col in range(col, width):
        RGB = pixels[row, col]
        R = RGB[0]
        G = RGB[1]
        B = RGB[2]

        if R < threshold and G < threshold and B < threshold:
            return col

        col += 1

    return -1

def findBottomEdge(pixels, col, threshold):
    height = pixels.shape[0]
    for row in range(height):
        RGB = pixels[row, col]
        R = RGB[0]
        G = RGB[1]
        B = RGB[2]

        if R < threshold and G < threshold and B < threshold:
            return row

        row += 1

    return -1
