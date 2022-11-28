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

# App pages and methods
from data_methods import *
from input_text import *
from input_url import *
from input_img import *
from input_camera import *

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
            st.write("""To test out some of the features, it is recommended to do the following: 
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

    # input_text.py
    if selected == 'Input Text': 
        input_text()

    # input_url.py
    if selected == 'Input URL':
        input_url()
        
    # input_img.py
    if selected == 'Input IMG':
        input_img()

    # input_camera.py
    if selected == "Input from Camera":
        input_camera()


if __name__ == '__main__':
    main()

if __name__ == "__main__":
    footer()
