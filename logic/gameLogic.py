
# The distance and width would be in pixels
def findTime(distance, width):
    distInWidth = distance * 1.0 / width
    time = distInWidth / 0.92
    return time
