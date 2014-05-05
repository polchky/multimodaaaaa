from kinect import Kinect
import cv2

k = Kinect()

cv2.namedWindow("Raw")
cv2.namedWindow("Thresh")
cv2.namedWindow("Masked")
cv2.namedWindow("Mask")
cv2.namedWindow("Delta")

cv2.createTrackbar("tmin", "Thresh", k.tmin, 255, lambda: None)
cv2.createTrackbar("tmax", "Thresh", k.tmax, 255, lambda: None)

print("Kinect test")
print("C: Calibrate mask")
print("O: Set origin")

while 1:
    k.tmin = cv2.getTrackbarPos("tmin", "Thresh")
    k.tmax = cv2.getTrackbarPos("tmax", "Thresh")

    k.update()

    cv2.imshow("Raw", k.raw)
    cv2.imshow("Thresh", k.thresh)
    cv2.imshow("Masked", k.masked)
    cv2.imshow("Mask", k.mask)

    delta = k.masked
    cv2.circle(delta, k.origin, 8, 127, -1)
    cv2.circle(delta, k.origin, 6, 0, -1)
    cv2.circle(delta, k.centroid, 6, 200, -1)
    cv2.line(delta, k.origin, k.centroid, 255, 1)

    cv2.imshow("Delta", delta)

    key = cv2.waitKey(10)
    if key == 27:
        break
    elif key == ord('c'):
        k.calibrate_mask()
    elif key == ord('o'):
        k.set_origin()
