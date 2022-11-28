# Lauren Graham
# CS361

# Streamlit packages:
import streamlit as st
from streamlit_option_menu import option_menu # nav

# Data manipulation packages and files:
import pandas as pd
import io
import os
import numpy as np
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
from data_methods import *
from input_text import *

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

# Error messages
error_message2 = 'Sorry, this website has not approved the program to retrieve data.'

def input_url():
    st.title("URL ⛓")
    st.write("Summarize text, preview text, or both! All you need is a URL.")

    def clear_url_form(): 
        """Clears forms by changing the session state. Session_state is a feature of Streamlit."""  
        st.session_state["Enter URL"] = ""

    with st.form("myformsumURL"):
        raw_url = st.text_input("Enter URL", key="Enter URL", placeholder = "Paste a valid URL here")
        f3, f4, f5, f10 = st.columns([1, 1, 5, 1]) # columns for purpose of aligning buttons
        with f3:
            preview = st.form_submit_button(label="Preview")
        with f4:
            summarize = st.form_submit_button(label="Summarize")
        with f10:
            clear = st.form_submit_button(label="Clear", on_click=clear_url_form)
    text_length = st.slider("Use the slider to indicate the proportional length you wish to cut from the preview. Unlike a summary, a preview will not paraphrase.", 100, 10)
        
    if preview:
        try:
            st.info("Extracting text for preview...")
            result = get_short_text_from_URL(raw_url, text_length)
            st.write(result)
            with st.expander("Easy-copy version"):
                st.code(result, language=None)
        except:
            st.error(error_message2, icon="🚨")

    if summarize:
        try:
            st.info('Summarizing...')
            raw_text = get_text(raw_url)
            summaryURL_result = sumy_summarizer(raw_text)  # using Sumy function to generate summary
            st.write(summaryURL_result)
            with st.expander("Easy-copy version"):
                st.code(summaryURL_result, language=None)
                
        except:
            st.error(error_message2, icon="🚨")

    elif clear:
        st.write('Text was cleared.')

