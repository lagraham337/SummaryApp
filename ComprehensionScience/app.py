# Lauren Graham
# CS361

# References: 
# summarizing text https://blog.jcharistech.com/2019/01/05/how-to-summarize-text-or-document-with-sumy/
# extracting text from webpages https://matix.io/extract-text-from-webpage-using-beautifulsoup-and-python/
# clearing text in streamlit https://discuss.streamlit.io/t/clear-the-text-in-text-input/2225/10 


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

# For style.py and footer:
from htbuilder import HtmlElement, div, ul, li, br, hr, a, p, img, styles, classes, fonts
from htbuilder.units import percent, px
from htbuilder.funcs import rgba, rgb
from style import *

# Sumy summary package:
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

# Web scrapping packages:
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from urllib.request import FancyURLopener
from random import choice

def main():
    """Main function features navigation bar and all pages in the app with their functions in this order:
    Input Text, Input URL, Input IMG, Input from Camera"""

    page_title="Comprehension Science",

    with st.sidebar:
        selected = option_menu(
            menu_title = "Select Input Type",
            options = ["Input Text", "Input URL", "Input IMG", "Input from Camera"],
            icons = ["journal-text", "link-45deg", "file-image", "camera"],
            menu_icon = "door-open",
            orientation = "vertical",
            styles = {

            }
        )
        with st.expander("About"):
            st.write("""The purpose of this app is for users to paste text, a URL, or upload an image file and 
            receive a text summary, text preview, or text extraction. It is being developed using Streamlit and 
            a number of Python libraries including Pytesseract and NLTK. It is currently in Beta stage of development.""") 
        with st.expander("User Guide"):
            st.write("""To test out the features, it is recommended to do the following: 
            1. visit the following page: https://www.ibm.com/cloud/learn/natural-language-processing 
            2a. From this website, copy a portion of the text, 2b. click Input Text in the navigation bar,  
            2c. and paste it into the text box. 
            2d. Click Summarize to generate a summary.  
            3a. Next, copy the URL from IBM's webpage,  
            3b. click Input URL in the navigation bar, 
            3c. and paste it into the URL box.  
            3d. Click Preview to see some of the contents of the webpage,  
            or click Summarize to summarize the entire article.  
            Note: The Clear button can be used to clear the text or 
            input areas.""")

    def clear_form(): 
        """Clears forms by changing the session state. Session_state is a feature of Streamlit."""  
        st.session_state["Enter Text Here:"] = ""
        st.session_state["Enter Text Here: "] = ""
        st.session_state["Enter URL"] = ""
        st.session_state["Choose an image file"] = ""

    # INPUT TEXT
    if selected == 'Input Text':

        st.title("Tl;dr? 📚")
        st.write("That's okay. Paste that verbose, windy, logorheic, circumocutory piece of text below.")

        with st.form("myformsumtext"):
            raw_text = st.text_area("Enter Text Here:", key="Enter Text Here:", placeholder = "Type here 👈")
            f3, f4, f5, f10 = st.columns([1, 1, 5, 1]) # columns for purpose of aligning buttons
            with f3:
                summarize = st.form_submit_button(label="Summarize")
            with f10:
                clear = st.form_submit_button(label="Clear", on_click=clear_form)

        if summarize:
            try:
                st.info('Summarizing...')
                summary_result = str(sumy_summarizer(raw_text))  # using Sumy function to yield summary
                st.write(summary_result)
                with st.expander("Easy-copy version"):
                    st.code(summary_result, language=None)
            except:
                st.write("Sorry, these seems to have been an issue. Please come back later.")

        elif clear:
            st.write('Text was cleared.')


    # INPUT URL
    if selected == 'Input URL':
        
        st.title("URL ⛓")
        st.write("Summarize text, preview text, or both! All you need is a URL.")

        with st.form("myformsumURL"):
            raw_url = st.text_input("Enter URL", key="Enter URL", placeholder = "Paste a valid URL here")
            f3, f4, f5, f10 = st.columns([1, 1, 5, 1]) # columns for purpose of aligning buttons
            with f3:
                preview = st.form_submit_button(label="Preview")
            with f4:
                summarize = st.form_submit_button(label="Summarize")
            with f10:
                clear = st.form_submit_button(label="Clear", on_click=clear_form)
        text_length = st.slider("Use the slider to indicate the proportional length you wish to cut from the preview. Unlike a summary, a preview will not paraphrase.", 100, 10)
        
        if preview:
            try:
                st.info("Extracting text for preview...")
                result = get_short_text_from_URL(raw_url, text_length)
                st.write(result)
                with st.expander("Easy-copy version"):
                    st.code(result, language=None)
            except:
                st.write("Sorry, this website has not approved the program to retrieve data.")

        if summarize:
            try:
                st.info('Summarizing...')
                raw_text = get_text(raw_url)
                summaryURL_result = sumy_summarizer(raw_text)  # using Sumy function to generate summary
                st.write(summaryURL_result)
                with st.expander("Easy-copy version"):
                    st.code(summaryURL_result, language=None)
                
            except:
                st.write("Sorry, this website has not approved the program to retrieve data.")

        elif clear:
            st.write('Text was cleared.')

    # INPUT IMG
    if selected == 'Input IMG':

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
                st.write("There was an error.")


    # INPUT CAMERA    
    if selected == "Input from Camera":

        st.title("Camera 📸")
        st.write("Take a picture! It'll last longer.")

        # Streamlit widget for collecting the image data
        img_file_buffer = st.camera_input("Text will be extracted and displayed. If no text is generated, try a clearer picture.")

        if img_file_buffer is not None:
            try:
                st.write("Extracting...") 
                # To read image file buffer as a PIL Image:
                img = Image.open(img_file_buffer)
                text = string_from_image(img)
                if text == '':
                    st.write("Try taking a clearer picture.")
                else:
                    st.code(f"{text}", language=None)
            except:
                st.write("There was an error. Try taking a clearer picture.")


if __name__ == '__main__':
    main()

if __name__ == "__main__":
    footer()
