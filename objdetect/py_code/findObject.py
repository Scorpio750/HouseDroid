import cv2 # computer vision
import sys # allow us to get the arguments
import math
import numpy as np

def main():
  # open an image
  name = sys.argv[1]
  old_image = cv2.imread(name)
  image = old_image.copy()

  # mask the image for the object
  target = [29, 228, 200]
  tolerance = 80
  print "dimensions: rows={0} cols={1}".format(len(image), len(image[0]))
  for y in range(len(image)):
    for x in range(len(image[0])):
      pixel = image[y][x]

      def magnitude(v):
        squared = map(lambda s: s ** 2, v)
        return math.sqrt(sum(squared))

      def within(color1, color2):
        difference = [color1[0] - color2[0],
                      color1[1] - color2[1],
                      color1[2] - color2[2]]
        return magnitude(difference) < tolerance

      if not within(pixel, target):
        image[y][x] = [255, 255, 255]

  # locate the center of the ball
  height = len(image)
  width = len(image[0])
  # create a histogram (x axis)
  histogram_x = range(0, width)
  histogram_x = map(lambda s: 0, histogram_x)
  # create histximage
  histximage = image.copy()
  for y in range(height):
    for x in range(width):
      pixel = image[y][x]
      red   = pixel[2] == 255
      green = pixel[1] == 255
      blue  = pixel[0] == 255
      if not blue or not green or not red:
        histogram_x[x] += 1
      histximage[y][x][0] = 255
      histximage[y][x][1] = 255
      histximage[y][x][2] = 255
  for x in range(width):
    for y in range(histogram_x[x]):
      histximage[height - y - 1][x][1] = 0
      histximage[height - y - 1][x][2] = 0

  # create a histogram (y axis)
  histogram_y = range(0, height)
  histogram_y = map(lambda s: 0, histogram_y)
  # create histyimage
  histyimage = image.copy()
  for x in range(width):
    for y in range(height):
      pixel = image[y][x]
      red   = pixel[2] == 255
      green = pixel[1] == 255
      blue  = pixel[0] == 255
      if not blue or not green or not red:
        histogram_y[y] += 1
      histyimage[y][x][0] = 255
      histyimage[y][x][1] = 255
      histyimage[y][x][2] = 255
  for y in range(height):
    for x in range(histogram_y[y]):
      histyimage[y][x][0] = 0
      histyimage[y][x][1] = 0

  # try to determine the center of the object
  # by finding the midpoint
  left = 0
  right = len(histogram_x)
  top = 0
  bottom = len(histogram_y)
  while histogram_x[left] < 3:
    left += 1
  while histogram_x[right - 1] < 3:
    right -= 1
  while histogram_y[top] < 3:
    top += 1
  while histogram_y[bottom - 1] < 3:
    bottom -= 1

  midpoint = [(left + right) / 2, (top + bottom) / 2]
  print "Midpoint: " + str(midpoint)

  new_image = []
  for y in range(top, bottom):
    new_image.append(image[y][left:right])
  new_image = np.array(new_image)

  # open a window, display it
  cv2.namedWindow("picture", cv2.WINDOW_AUTOSIZE)
  cv2.imshow("picture", old_image)
  cv2.namedWindow("histx", cv2.WINDOW_AUTOSIZE)
  cv2.imshow("histx", histximage)
  cv2.namedWindow("histy", cv2.WINDOW_AUTOSIZE)
  cv2.imshow("histy", histyimage)
  cv2.namedWindow("new picture", cv2.WINDOW_AUTOSIZE)
  cv2.imshow("new picture", new_image)
  cv2.waitKey(0)
  cv2.destroyAllWindows()

main()
