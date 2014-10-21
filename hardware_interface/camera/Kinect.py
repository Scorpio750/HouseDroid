import numpy as np
import cv2 # computer vision
import sys

if len(sys.argv) < 2:
  print "not enough args"
  sys.exit(0)

cap = cv2.VideoCapture(int(sys.argv[1]))

if not cap.isOpened():
  print "cant open device"
  sys.exit(0)

while(True):
  try:
    print "reading frame"
    ret, frame = cap.read()
    print "Got frame"
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) == ord('q'):
      break
  except:
    print "cannot read frame"

cap.release()
cv2.destroyAllWindows()
