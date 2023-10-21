# MediMorph-DataZtroopers
This project will be useful in detecting the medicines and also it will be telling the alternatives of the medicine and their dosage and pricing and also the salts present in the medicine. 

Installation
install tkinter,csv,tate,cv2,cvzone,numpy,pytesseract,PIL,logging libraries in you system.
Usage
Here, you'll describe step by step how to use your application. Here's how you might structure it:

Step 1: Setting Up Data.py
This module will be doing the recognition of medicines using the image present in the system. Simply run the code in the pycharm and then a window will open saying to upload a image and then you can upload the image.

Step 2: Manual Entry
manualentry.py is a script by which one can get the details of a medicine, dosage, price as well as the alternative of the medicine and then also the salts of the medicine by which you can check which medicine you can take.
manualentry.py is a script in which there are preuploaded database present in csv file.
Download the csv file in you system and add the path of csv file in the code.
Run the code and a GUI will open in which you can type the medicine and get details of the medicine.


Step 3: OCR (Optical Character Recognition)
The OCR is being used to upload the prescription. Using the OCR when one can get the prescription then we can upload the medicine in manual entry code to check the dosage and some alternative medicines available for the same.

Step 4: Color Module
This color Module is used to capture the real time image color of the medicine through which we can differentiate between different medicines and get some narrowed down results to scrutinize the medicine and get some similar results.

Step 5: Running the pill detection
pill_detection.py is another which is used to get the real time image of the medicine. This code will be doing the gray scaling to get the real timme image and reading the text that might be written on the image.


bash
Copy code
# How to clone and set up your project for development
git clone https://github.com/yourusername/your-repo-name.git

License
MIT License.
