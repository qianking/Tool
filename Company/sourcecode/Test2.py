import imutils
from imutils import contours
from skimage import measure
import numpy as np
import cv2
image = cv2.imread(r'D:\Qian\Codeing\Tool\LED\test photo\2367258900089_LED Green Upper_20230628190646.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (11, 11), 0)
cv2.imshow('blurred',blurred)
cv2.waitKey(0)
thresh = cv2.threshold(blurred, 51, 255, cv2.THRESH_BINARY)[1]
cv2.imshow('thresh',thresh)
cv2.waitKey(0)
thresh = cv2.erode(thresh, None, iterations=2)
thresh = cv2.dilate(thresh, None, iterations=4)
labels = measure.label(thresh, background=0)
mask = np.zeros(thresh.shape, dtype="uint8")
for label in np.unique(labels):
  if label == 0:
    continue
  labelMask = np.zeros(thresh.shape, dtype="uint8")
  labelMask[labels == label] = 255
  numPixels = cv2.countNonZero(labelMask)
  if numPixels > 50:
    mask = cv2.add(mask, labelMask)
cv2.imshow('mask',mask)
cv2.waitKey(0)
cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
  cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cnts = contours.sort_contours(cnts)[0]
for (i, c) in enumerate(cnts):
  (x, y, w, h) = cv2.boundingRect(c)
  ((cX, cY), radius) = cv2.minEnclosingCircle(c)
  cv2.circle(image, (int(cX), int(cY)), int(radius),
    (0, 0, 255), 3)
  cv2.putText(image, "{}".format(i + 1), (x, y - 2),
    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
cv2.imshow("Image", image)
cv2.waitKey(0)

