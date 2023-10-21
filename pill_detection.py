import cv2
import cvzone
import numpy as np

# Create a VideoCapture object for the default camera (0) or specify your camera index
camera_index = 1  # Change this to your camera index if needed

def empty(a):
    pass

cv2.namedWindow("Settings")
cv2.resizeWindow("Settings", 640, 240)
cv2.createTrackbar("Threshold1", "Settings", 255, 255, empty)
cv2.createTrackbar("Threshold2", "Settings", 120, 255, empty)

def preProcessing(img):
    imgPre = cv2.GaussianBlur(img, (5, 5), 3)
    thresh1 = cv2.getTrackbarPos("Threshold1", "Settings")
    thresh2 = cv2.getTrackbarPos("Threshold2", "Settings")
    imgPre = cv2.Canny(imgPre, thresh1, thresh2)
    kernel = np.ones((2, 2), np.uint8)
    imgPre = cv2.dilate(imgPre, kernel, iterations=1)
    imgPre = cv2.morphologyEx(imgPre, cv2.MORPH_CLOSE, kernel)
    return imgPre

# Create a VideoCapture object with the desired camera index
cap = cv2.VideoCapture(camera_index)

# Check if the camera is opened successfully
if not cap.isOpened():
    print("Error: Unable to open the camera.")
    exit()

totalTablets = 0

while True:
    success, img = cap.read()

    if not success:
        print("Error: Failed to capture a frame.")
        break

    imgPre = preProcessing(img)
    imgContours, conFound = cvzone.findContours(img, imgPre, minArea=20)
    totalTablets = 0

    if conFound:
        for count, contour in enumerate(conFound):
            peri = cv2.arcLength(contour['cnt'], True)
            approx = cv2.approxPolyDP(contour['cnt'], 0.02 * peri, True)

            if len(approx) > 5:
                area = contour['area']

                if 4400 < area < 5500:
                    totalTablets += 1

                x, y, w, h = contour['bbox']
                imgCrop = img[y:y + h, x:x + w]
                cv2.imshow(str(count), imgCrop)

    print(totalTablets)
    imgStacked = cvzone.stackImages([img, imgPre, imgContours], 2, 1)
    cvzone.putTextRect(imgStacked, f'Tablets: {totalTablets}', (50, 50))

    cv2.imshow("Image", imgStacked)

    # Press 'q' to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
