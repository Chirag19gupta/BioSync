import cv2
import numpy as np

# Function for trackbar control
def empty(a):
    pass

# Create settings window for trackbars
cv2.namedWindow("Settings")
cv2.resizeWindow("Settings", 640, 240)
cv2.createTrackbar("Threshold1", "Settings", 23, 255, empty)  # Adjusted from 255 to start
cv2.createTrackbar("Threshold2", "Settings", 20, 255, empty)  # Adjusted from 120 to start

# Image preprocessing for edge detection
def preProcessing(img):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert image to grayscale
    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)  # Add Gaussian Blur
    thresh1 = cv2.getTrackbarPos("Threshold1", "Settings")
    thresh2 = cv2.getTrackbarPos("Threshold2", "Settings")
    imgCanny = cv2.Canny(imgBlur, thresh1, thresh2)  # Canny Edge detection
    kernel = np.ones((5, 5))
    imgDil = cv2.dilate(imgCanny, kernel, iterations=2)  # Dialation
    imgThres = cv2.erode(imgDil, kernel, iterations=1)  # Erosion
    return imgThres

# Start video capture
cap = cv2.VideoCapture(1)
if not cap.isOpened():
    print("Error: Unable to open the camera.")
    exit()

while True:
    success, img = cap.read()
    if not success:
        print("Error: Failed to capture a frame.")
        break

    imgPre = preProcessing(img)
    contours, hierarchy = cv2.findContours(imgPre, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    totalTablets = 0

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if 1000 < area < 10000:  # You might need to adjust these values based on your actual tablet size
            totalTablets += 1
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            x, y, w, h = cv2.boundingRect(approx)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Draw a green rectangle around the detected object

    # Display the tablet count on the image frame
    cv2.putText(img, f'Tablets: {totalTablets}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    # Show the image
    cv2.imshow("Image", img)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Clean up
cap.release()
cv2.destroyAllWindows()
