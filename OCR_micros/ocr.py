"""
Code for OCR Microservice 
Code copied from https://python-bloggers.com/2022/05/extract-text-from-image-using-python/
"""

import os
from PIL import Image
from pytesseract import pytesseract

# Define path to tessaract.exe
# Need to change path on local machine
PATH_TO_TESSERACT = r'/opt/homebrew/bin/tesseract'

# Define path to image
PATH_TO_IMAGES = '../OCR_micros/sample_images/'

# Point tessaract_cmd to tessaract.exe
pytesseract.tesseract_cmd = PATH_TO_TESSERACT

# Extract text from image
for root, dirs, file_names in os.walk(PATH_TO_IMAGES):
    # Iterate over each file_name in the folder
    for file_name in file_names:
        # Open image with PIL
        img = Image.open(PATH_TO_IMAGES + file_name)
        # Extract text from image
        text = pytesseract.image_to_string(img)
        print(text)
