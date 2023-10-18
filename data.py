import cv2
import cvzone
import numpy as np
from skimage.metrics import structural_similarity as ssim
import tkinter as tk
from tkinter import filedialog, Label, Button, Entry, Text, Scrollbar, Frame
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

from tate import tablet_images

# Initialize the main application window
root = tk.Tk()
root.geometry("1280x720")
root.title("Medicine Tablet Recognition")

# Initialize global variables
cap = cv2.VideoCapture(0)
imgCrop = None
totalTablets = 0
best_match_window_open = False  # Keep track of whether the "Best Match" window is open

# Initialize data from Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("hallowed-medley-398404-d8ecc3085063", scope)  # Replace with your JSON key file
client = gspread.authorize(creds)

# Replace with your Google Sheets document's title
spreadsheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1Gbrk5wLVODZWjmfTYl5Pee_Rr8k_2M3ipDJHRHnNgW4/edit?usp=sharing")  # Replace with your Google Sheets URL
worksheet = spreadsheet.worksheet("Untitled spreadsheet")  # Replace with your sheet name

# Function to perform preprocessing on the input image
def preProcessing(img):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
    imgCanny = cv2.Canny(imgBlur, 100, 100)
    kernel = np.ones((5, 5))
    imgDil = cv2.dilate(imgCanny, kernel, iterations=2)
    imgThre = cv2.erode(imgDil, kernel, iterations=1)
    return imgThre

# Function to detect the shape of a contour
def detect_shape(contour):
    peri = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, 0.02 * peri, True)

    if len(approx) == 3:
        return "Triangle"
    elif len(approx) == 4:
        return "Rectangle"
    elif len(approx) == 5:
        return "Pentagon"
    elif len(approx) == 6:
        return "Hexagon"
    else:
        return "Unknown"

# Function to load images from a folder
def get_tablet_images():
    tablet_images = []
    folder_path = filedialog.askdirectory()
    if folder_path:
        for filename in os.listdir(folder_path):
            if filename.endswith(".jpg") or filename.endswith(".png"):
                image_path = os.path.join(folder_path, filename)
                tablet_images.append(image_path)
    return tablet_images

# Function to update the GUI
def update_gui():
    global totalTablets, imgCrop, best_match_window_open
    success, img = cap.read()
    imgPre = preProcessing(img)
    imgContours, conFound = cvzone.findContours(img, imgPre, minArea=20)
    totalTablets = 0

    if conFound:
        for count, contour in enumerate(conFound):
            peri = cv2.arcLength(contour['cnt'], True)
            approx = cv2.approxPolyDP(contour['cnt'], 0.02 * peri, True)

            if len(approx) > 5:
                area = contour['area']

                if area < 4400:
                    totalTablets += 1
                elif 4400 < area < 5500:
                    totalTablets += 1
                else:
                    totalTablets += 0
                x, y, w, h = contour['bbox']
                imgCrop = img[y:y + h, x:x + w]

    imgStacked = cvzone.stackImages([img, imgPre, imgContours], 2, 1)
    cvzone.putTextRect(imgStacked, f'Tablets: {totalTablets}', (50, 50))
    cv2.imshow("Image", imgStacked)

    # Find the tablet image with the highest similarity
    max_similarity = 0
    best_match_image_path = None

    if imgCrop is not None:  # Check if imgCrop is defined
        for tablet_image_path in tablet_images:
            tablet_img = cv2.imread(tablet_image_path)
            if imgCrop.shape == tablet_img.shape:
                similarity = ssim(imgCrop, tablet_img, multichannel=True)
                if similarity > max_similarity:
                    max_similarity = similarity
                    best_match_image_path = tablet_image_path

    if max_similarity >= 0.2:  # If similarity is at least 20%
        best_match_image = cv2.imread(best_match_image_path)
        cv2.imshow("Best Match", best_match_image)
        shape_info = f"Shape: {detect_shape(conFound[0]['cnt'])}" if conFound else "Shape: None"
        shape_label.config(text=shape_info)
        similarity_label.config(text=f"Similarity: {max_similarity:.2f}")
        best_match_window_open = True  # The "Best Match" window is open
    else:
        if best_match_window_open:
            cv2.destroyWindow("Best Match")  # Close the "Best Match" window if open
            best_match_window_open = False  # The "Best Match" window is closed
        shape_info = f"Shape: {detect_shape(conFound[0]['cnt'])}" if conFound else "Shape: None"
        shape_label.config(text=shape_info)
        similarity_label.config(text="Similarity: N/A")

    cv2.waitKey(1)

# Function to retrieve medicine information from the spreadsheet
def get_medicine_info():
    medicine_name = medicine_name_entry.get()
    if not medicine_name:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "Please enter a medicine name.")
    else:
        try:
            cell = worksheet.find(medicine_name)
            row = cell.row
            medicine_info = worksheet.row_values(row)
            result_text.config(state=tk.NORMAL)  # Enable text widget for editing
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, f"Medicine Name: {medicine_info[0]}\n")
            result_text.insert(tk.END, f"Price: {medicine_info[1]}\n")
            result_text.insert(tk.END, f"When to Take: {medicine_info[2]}\n")
            result_text.insert(tk.END, f"Dosage: {medicine_info[3]}\n")
            result_text.insert(tk.END, f"Alternative Medicine: {medicine_info[4]}\n")
            result_text.config(state=tk.DISABLED)  # Disable text widget for display only
        except gspread.exceptions.CellNotFound:
            result_text.config(state=tk.NORMAL)  # Enable text widget for editing
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, "Medicine not found in the database.")
            result_text.config(state=tk.DISABLED)  # Disable text widget for display only

# Create labels to display shape and similarity information
shape_label = Label(root, text="Shape: None")
shape_label.pack()
similarity_label = Label(root, text="Similarity: N/A")
similarity_label.pack()

# Create a button to load tablet images
load_button = Button(root, text="Load Tablet Images", command=get_tablet_images)
load_button.pack()

# Create an entry field to manually enter medicine name
medicine_name_label = Label(root, text="Enter Medicine Name:")
medicine_name_label.pack()
medicine_name_entry = Entry(root)
medicine_name_entry.pack()

# Create a button to get medicine information
get_info_button = Button(root, text="Get Medicine Info", command=get_medicine_info)
get_info_button.pack()

# Create a text widget to display medicine information
result_text = Text(root, wrap=tk.WORD, width=50, height=10)
result_text.pack()
result_text.config(state=tk.DISABLED)  # Disable text widget for display only

# Create a button to start the tablet recognition process
start_button = Button(root, text="Start Recognition", command=update_gui)
start_button.pack()

root.mainloop()
