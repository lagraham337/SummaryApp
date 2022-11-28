# Lauren Graham
# CS361

# Streamlit packages:
import streamlit as st
from streamlit_option_menu import option_menu # nav

# Data manipulation packages and files:
from PIL import Image
import cv2
import pandas as pd
import io
import os
import numpy as np
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
import pytesseract
from data_methods import *
from input_img import *

# Microservice communication pipe: 
import zmq 

# Error messages
error_message4 = 'There was an issue. Try taking a clearer picture.'

def input_camera():  
    """The user can take an image from their computer and extract text from it"""      
    st.title("Camera 📸")
    st.write("Take a picture! It'll last longer.")

    # Streamlit widget for collecting the image data
    img_file_buffer = st.camera_input("Text will be extracted and displayed.")

    if img_file_buffer is not None:
        try:
            st.write("Extracting...") 
            # To read image file buffer as a PIL Image:
            img = Image.open(img_file_buffer)
            text = string_from_image(img)
            if text == '':
                st.error(error_message4, icon = "📸")
            else:
                st.code(f"{text}", language=None)
        except:
            st.error(error_message4, icon = "📸")
