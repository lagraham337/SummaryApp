import streamlit as st
from PIL import Image
import io
import os
import numpy as np
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
import os
import zmq

context = zmq.Context()

#  Connect socket to server
print("Connecting to OCR server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:4444")

# Send image file to server
DEMO_IMAGE = "text1.jpg"

# Send image file to server
PATH_TO_IMG = r'../OCR_micros/sample_images/'



st.title("IMG 📸")
st.write("Save yourself some time. Extract or summarize text directly from an image.")
with st.form("myformsumIMG"):
    image_file = st.file_uploader("Choose an image file with clear text present.", type=['png', 'jpg', 'jpeg'], accept_multiple_files=False, key="IMG", help="Jpg, jpeg and png files are supported. Gif, webm, and video files are not supported.", on_change=None, label_visibility="visible")
    f3, f4, f5, f10 = st.columns([1, 1, 5, 1]) 
    with f3:
        extract = st.form_submit_button(label="Extract")
if extract:
    try:
        st.header("Extracted text")
        path_in = image_file.name
        full_path = PATH_TO_IMG + path_in
        socket.send_string(full_path)
                #  Get the reply
        message = socket.recv()
        st.write(f"{message}")
        image = st.image(image_file, caption=None, width=None, use_column_width='auto', clamp=False, channels="RGB", output_format="auto")

    except:
        st.write("There was an error.")









