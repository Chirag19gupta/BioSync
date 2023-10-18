import pytesseract
from PIL import Image

# Set the path to your Tesseract executable (usually installed with Tesseract)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Function to perform OCR on an image
def perform_ocr(image_path):
    try:
        # Open the image using PIL (Python Imaging Library)
        img = Image.open(image_path)

        # Perform OCR on the image
        text = pytesseract.image_to_string(img)

        return text
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return ""

if __name__ == "__main__":
    # Replace "your_image.jpg" with the path to your image file
    input_image_path = r"C:\Users\Chirag Gupta\Downloads\AIST_RP977.jpg"

    # Perform OCR on the specified image
    recognized_text = perform_ocr(input_image_path)

    # Print the recognized text
    print("Recognized Text:")
    print(recognized_text)
