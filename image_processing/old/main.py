import numpy
from PIL import Image, ImageDraw
#import image_processing
#from image_processing import imageCropper
import imageCropper

# shape 2208, 1242, 4

def getPlatformLevel(arr):
    rows = arr.shape[0]
    rowIndex = 0

    while rowIndex < rows:
        rgbValue = arr[rowIndex, 0]
        R = rgbValue[0]
        G = rgbValue[1]
        B = rgbValue[2]

        if R < 40 and G < 40 and B < 40:
            return rowIndex

        rowIndex += 1

    return -1


def findPlatformEdge(arr, rowIndex):
    cols = arr.shape[1]
    colIndex = 0

    rgbValue = arr[rowIndex, colIndex]
    while rgbValue[0] < 40 and rgbValue[1] < 40 and rgbValue[2] < 40 and colIndex < cols:
        rgbValue = arr[rowIndex, colIndex]
        colIndex += 1

    return colIndex


def findNextPlatformDistance(arr, rowIndex, colIndex):
    cols = arr.shape[1]

    oldIndex = colIndex

    rgbValue = arr[rowIndex, colIndex]
    while rgbValue[0] > 40 and rgbValue[1] > 40 and rgbValue[2] > 40 and colIndex < cols:
        rgbValue = arr[rowIndex, colIndex]
        colIndex += 1

    return colIndex - oldIndex


def __main__():
    # This code crops the image

    im = Image.open("imgs/img8.jpg")
    arr = numpy.array(im)
    leftEdge = imageCropper.findLeftEdge(arr, 30)
    rightEdge = imageCropper.findRightEdge(arr, leftEdge + 69, 30)
    bottomEdge = imageCropper.findBottomEdge(arr, int((leftEdge + rightEdge) / 2), 30)
    print(str(leftEdge) + ", " + str(rightEdge) + ", " + str(bottomEdge))

    cropTuple = (leftEdge + 25, 0, rightEdge, bottomEdge)
    newIm = im.crop(cropTuple)

    # Get platform distances

    arr = numpy.array(newIm)

    platformLevel = getPlatformLevel(arr) + 150
    platformEdge = findPlatformEdge(arr, platformLevel)
    distance = findNextPlatformDistance(arr, platformLevel, platformEdge)

    print(distance)

#    draw = ImageDraw.Draw(newIm)
#    draw.line([platformEdge, platformLevel, platformEdge + distance, platformLevel], 255, 7)
#    newIm.show()
#    newIm.save("a.png")


if __name__ == "__main__":
    __main__()
