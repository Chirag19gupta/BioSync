import cv2
import numpy as np
import logging


class ColorFinder:
    def __init__(self, trackBar=False):
        self.trackBar = trackBar
        if self.trackBar:
            self.initTrackbars()

        # Define the dictionary of color ranges in HSV
        self.color_ranges = {
            'red': [{'hmin': 0, 'smin': 120, 'vmin': 70, 'hmax': 10, 'smax': 255, 'vmax': 255},
                    {'hmin': 170, 'smin': 120, 'vmin': 70, 'hmax': 180, 'smax': 255, 'vmax': 255}],
            # red has two ranges
            'orange': [{'hmin': 10, 'smin': 100, 'vmin': 20, 'hmax': 25, 'smax': 255, 'vmax': 255}],
            'yellow': [{'hmin': 25, 'smin': 100, 'vmin': 20, 'hmax': 35, 'smax': 255, 'vmax': 255}],
            'green': [{'hmin': 35, 'smin': 100, 'vmin': 20, 'hmax': 85, 'smax': 255, 'vmax': 255}],
            'blue': [{'hmin': 85, 'smin': 100, 'vmin': 20, 'hmax': 125, 'smax': 255, 'vmax': 255}],
            'indigo': [{'hmin': 125, 'smin': 100, 'vmin': 20, 'hmax': 135, 'smax': 255, 'vmax': 255}],
            'violet': [{'hmin': 135, 'smin': 100, 'vmin': 20, 'hmax': 170, 'smax': 255, 'vmax': 255}],
            'white': [{'hmin': 0, 'smin': 0, 'vmin': 200, 'hmax': 180, 'smax': 55, 'vmax': 255}]
        }

    def empty(self, a):
        pass

    def initTrackbars(self):
        pass

    # [Method to initialize trackbars, if used]

    def getTrackbarValues(self):
        pass

    # [Method to get trackbar values, if used]

    def getColorHSV(self, myColor):
        return self.color_ranges.get(myColor, None)

    def calculate_area_of_color(self, mask):
        return cv2.countNonZero(mask)

    def update(self, img, myColor=None):
        imgColor = None
        mask = None

        if self.trackBar:
            myColor = self.getTrackbarValues()

        if isinstance(myColor, str):
            myColor = self.getColorHSV(myColor)

        if myColor is not None:
            for color_range in myColor:  # updated to handle multiple ranges per color
                imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
                lower = np.array([color_range['hmin'], color_range['smin'], color_range['vmin']])
                upper = np.array([color_range['hmax'], color_range['smax'], color_range['vmax']])
                current_mask = cv2.inRange(imgHSV, lower, upper)

                if mask is None:
                    mask = current_mask
                else:
                    mask = cv2.bitwise_or(mask, current_mask)  # Combine masks if there are multiple ranges

            imgColor = cv2.bitwise_and(img, img, mask=mask)

        return imgColor, mask


def main():
    useTrackBar = False  # Change to True if you want to use trackbars
    myColorFinder = ColorFinder(useTrackBar)

    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)

    while True:
        success, img = cap.read()
        if not success:
            logging.error("Failed to read frame. Exiting...")
            break

        combined_image = np.zeros_like(img)
        color_areas = {}

        for color in myColorFinder.color_ranges.keys():  # Using the colors from the dictionary
            imgColor, mask = myColorFinder.update(img, color)
            combined_image = cv2.addWeighted(combined_image, 1, imgColor, 1, 0)

            color_area = myColorFinder.calculate_area_of_color(mask)
            color_areas[color] = color_area

        # Determine the color with the maximum area
        predominant_color = max(color_areas, key=color_areas.get)

        # Create a text to display
        text = f"Predominant color: {predominant_color}"

        # Put the text on the combined image
        cv2.putText(combined_image, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        cv2.imshow("Detected Colors", combined_image)
        cv2.imshow("Original Image", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
