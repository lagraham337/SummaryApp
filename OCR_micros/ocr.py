"""
Code for OCR Microservice.

Code adapted from Python-Bloggers
Date: 10/25/2022
Title: Extract Text from Image using Python
Source URL: https://python-bloggers.com/2022/05/extract-text-from-image-using-python/
"""

from PIL import Image
from pytesseract import pytesseract

def orc(received):
    """
    describe function
    """
    # Define path to tessaract.exe
    # Need to change path to tesseract location on local machine
    path_to_tess = r'/usr/local/bin/tesseract'

    # Point tessaract_cmd to tessaract.exe
    pytesseract.tesseract_cmd = path_to_tess

    # Open image with PIL
    img = Image.open(received)

    # Extract text from image
    text = pytesseract.image_to_string(img)
    return text
