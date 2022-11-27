import streamlit as st
from streamlit_option_menu import option_menu # nav
from PIL import Image
import cv2
import pandas as pd
import io
import os
import numpy as np
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
import pytesseract 
import zmq

from htbuilder import HtmlElement, div, ul, li, br, hr, a, p, img, styles, classes, fonts
from htbuilder.units import percent, px
from htbuilder.funcs import rgba, rgb



#import nltk
#nltk.download("punkt") # may need this if encounter an error

# sumy summary package 
# source: https://blog.jcharistech.com/2019/01/05/how-to-summarize-text-or-document-with-sumy/
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

#sumy summary function which includes tokenizer
def sumy_summarizer(docx):
    parser = PlaintextParser.from_string(docx,Tokenizer('English'))
    lex_summarizer = LexRankSummarizer()
    summary = lex_summarizer(parser.document, 3)
    summary_list = [str(sentence) for sentence in summary]
    result = ''.join(summary_list)
    return result

#remove unwanted characters from text
def clean_text(text):
    return str(text, 'utf-8')

# Web scrapping packages
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from urllib.request import FancyURLopener
from random import choice

# get text from raw URL. WORKS INCONSISTENTLY. SOME WEBSITES DENY PERMISSION*********
@st.cache
# source https://matix.io/extract-text-from-webpage-using-beautifulsoup-and-python/
def get_text(raw_url):
    """Get text from raw URL"""
    page = urlopen(raw_url)
    soup = BeautifulSoup(page, features="lxml")
    fetched_text = ''.join(map(lambda p:p.text,soup.find_all('p')))
    return fetched_text


def main():
    """Text Summarization and Extraction"""

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
            st.write("""
        The purpose of this app is for users to paste text, a URL, or upload an image file and receive a text summary, text preview, or text extraction. It is being developed using Streamlit and a number of Python libraries including Pytesseract and NLTK.

It is currently in Beta stage of development.""") 
        with st.expander("Tutorial"):
            st.write("""To test out the features, it is recommended to do the following:
            1. visit the following page:

https://www.ibm.com/cloud/learn/natural-language-processing 

2a. From this website, copy a portion of the text, 2b. click Input Text in the navigation bar, 2c. and paste it into the text box. 2d. Click Summarize to generate a summary.

3a. Next, copy the URL from IBM's webpage, 3b. click Input URL in the navigation bar, 3c. and paste it into the URL box. 3d. Click Preview to see some of the contents of the webpage, or click Summarize to summarize the entire article.

Note: The Clear button can be used to clear the text or input areas.
    """)

    def clear_form():   # clearing text https://discuss.streamlit.io/t/clear-the-text-in-text-input/2225/10 
        st.session_state["Enter Text Here:"] = ""
        st.session_state["Enter Text Here: "] = ""
        st.session_state["Enter URL"] = ""
        st.session_state["Choose an image file"] = ""
    
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
                summary_result = sumy_summarizer(raw_text)  # using sumy
                st.write(summary_result)
            except:
                st.write("Sorry, these seems to have been an issue. Please come back later.")

        if clear:
            st.write('Text was cleared.')


    if selected == 'Input URL':
        # WORKS INCONSISTENTLY. SOME WEBSITES DENY PERMISSION*********
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
                raw_text = get_text(raw_url)
                len_of_full_text = len(raw_text)
                len_of_short_text = round(len_of_full_text/text_length)
                st.write(raw_text[:len_of_short_text])
            except:
                st.write("Sorry, this website has not approved the program to retrieve data.")

        if summarize:
            try:
                st.info('Summarizing...')
                raw_text = get_text(raw_url)
                summaryURL_result = sumy_summarizer(raw_text)  # using sumy
                st.write(summaryURL_result)
                
            except:
                st.write("Sorry, this website has not approved the program to retrieve data.")

        if clear:
            st.write('Text was cleared.')

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
            image_file = st.file_uploader("Choose an image file with clear text present.", type=['png', 'jpg', 'jpeg'], accept_multiple_files=False, key="IMG", help="Jpg, jpeg and png files are supported. Gif, webm, and video files are not supported.", on_change=None, label_visibility="visible")
            f3, f4, f5, f10 = st.columns([1, 1, 5, 1]) 
            with f3:
                extract = st.form_submit_button(label="Extract")
            with f4:
                summarize = st.form_submit_button(label="Summarize")
        if extract:
            try:
                st.write("Extracting text...")
                path_in = image_file.name
                full_path = PATH_TO_IMG + path_in
                socket.send_string(full_path)
                        #  Get the reply
                message = socket.recv()
                message = clean_text(message)
                st.write(f"{message}")
                image = st.image(image_file, caption=None, width=None, use_column_width='auto', clamp=False, channels="RGB", output_format="auto")

            except:
                st.write("There was an error.")
        elif summarize:
            try:       
                st.write("Summarizing...")     
                path_in = image_file.name
                full_path = PATH_TO_IMG + path_in
                socket.send_string(full_path)
                        #  Get the reply
                message = socket.recv()
                summary_result = sumy_summarizer(message)  # using sumy
                st.write(summary_result)
                st.image(image_file, caption=None, width=None, use_column_width='auto', clamp=False, channels="RGB", output_format="auto")
                
            except:
                st.write("There was an error.")
        
    if selected == "Input from Camera":
        st.title("Camera 📸")
        st.write("Take a picture! It'll last longer.")
        img_file_buffer = st.camera_input("Text will be extracted and displayed. If no text is generated, try a clearer picture.")

        if img_file_buffer is not None:
            try:
                st.write("Extracting...") 
        # To read image file buffer as a PIL Image:
                img = Image.open(img_file_buffer)
        # To convert PIL Image to numpy array:
                img_array = np.array(img)
                img = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)
        # Get string using pytesseract
                text = pytesseract.image_to_string(img)
                if text == '':
                    st.write("Try taking a clearer picture.")
                else:
                    st.write(f"{text}")
            except:
                st.write("There was an error. Try taking a clearer picture.")




def image(src_as_string, **style):
    return img(src=src_as_string, style=styles(**style))

def link(link, text, **style):
    return a(_href=link, _target="_blank", style=styles(**style))(text)

def layout(*args):

    style = """
    <style>
      # MainMenu {visibility: hidden;}
      footer {visibility: hidden;}
    </style>
    """

    style_div = styles(
        left=0,
        bottom=0,
        margin=px(0, 0, 0, 0),
        width=percent(100),
        text_align="center",
        height="60px",
        opacity=0.6
    )

    style_hr = styles(
    )

    body = p()
    foot = div(style=style_div)(hr(style=style_hr), body)

    st.markdown(style, unsafe_allow_html=True)

    for arg in args:
        if isinstance(arg, str):
            body(arg)
        elif isinstance(arg, HtmlElement):
            body(arg)

    st.markdown(str(foot), unsafe_allow_html=True)

def footer():
    myargs = [
        "<b>Made with</b>: Python 3.10 ",
        link("https://www.python.org/", image('https://i.imgur.com/ml09ccU.png',
        	width=px(18), height=px(18), margin= "0em")),
        ", Streamlit ",
        link("https://streamlit.io/", image('https://aws1.discourse-cdn.com/business7/uploads/streamlit/original/2X/f/f0d0d26db1f2d99da8472951c60e5a1b782eb6fe.png',
        	width=px(24), height=px(25), margin= "0em")),    
        # link("https://github.com/lagraham337", "Lauren Graham"),
        "by",
        link("https://github.com/lagraham337/SummaryApp", image('https://img.icons8.com/plasticine/344/github.png', width=px(24), height=px(25), margin= "0em")),
        "Lauren Graham",
        #br(),
    ]
    layout(*myargs)


if __name__ == '__main__':
    main()

if __name__ == "__main__":
    footer()
