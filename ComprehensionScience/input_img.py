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

# Microservice communication pipe: 
import zmq 

# Error messages
error_message3 = 'Sorry, it seems there was an issue. Please come back later.'

def input_img():
    """This page extracts text from an image"""
    # Communicate with microservice
    context = zmq.Context() 

    #  Connect socket to server
    print("Connecting to OCR server…")
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:4444")

    # Send image file to server
    PATH_TO_IMG = r'../OCR_micros/sample_images/'

    st.title("IMG 📸")
    st.write("Save yourself some time. Extract or summarize text directly from an image.")

    with st.form("myformsumIMG"):

        # Argument variables for st.file_uploader
        label = "Choose an image file with clear text present."
        img_types = 'png', 'jpg', 'jpeg'
        help = "Jpg, jpeg and png files are supported. Gif, webm, and video files are not supported."

        # Streamlit image uploader
        image_file = st.file_uploader(label, type=img_types, accept_multiple_files=False, key="IMG", help=help, on_change=None, label_visibility="visible")
        f3, f4, f5, f10 = st.columns([1, 1, 5, 1]) 
        with f3:
            extract = st.form_submit_button(label="Extract")
        
    if extract:
        try:
            st.write("Extracting text...")
            path_in = image_file.name
            full_path = PATH_TO_IMG + path_in
            socket.send_string(full_path)
            # Get the reply
            message = socket.recv()
            message = clean_text(message)

            st.code(f"{message}", language=None)
                
            # Present image
            image = st.image(image_file, caption=None, width=None, use_column_width='auto', clamp=False, channels="RGB", output_format="auto")

        except:
            st.error(error_message3, icon="🚨")