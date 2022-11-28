# Streamlit packages:
import streamlit as st
from streamlit_option_menu import option_menu # nav
from app import *

# Data manipulation packages and files:
import pandas as pd
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
from data_methods import *

# Sumy summary package:
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

# Web scrapping packages:
import requests

# Error messages
error_message1 = 'It seems there was an issue. Please come back later.'

def input_text():
    """input text page"""
    
    def clear_text_form(): 
        """Clears forms by changing the session state. Session_state is a feature of Streamlit."""  
        st.session_state["Enter Text Here:"] = ""

    st.title("Tl;dr? 📚")
    st.write("That's okay. Paste that verbose, windy, logorheic, circumocutory piece of text below.")

    with st.form("myformsumtext"):
        raw_text = st.text_area("Enter Text Here:", key="Enter Text Here:", placeholder = "Type here 👈")
        f3, f4, f5, f10 = st.columns([1, 1, 5, 1]) # columns for purpose of aligning buttons
        with f3:
            summarize = st.form_submit_button(label="Summarize")
        with f10:
            clear = st.form_submit_button(label="Clear", on_click=clear_text_form)

    if summarize:
        try:
            st.info('Summarizing...')
            summary_result = str(sumy_summarizer(raw_text))  # using Sumy function to yield summary
            st.write(summary_result)
            with st.expander("Easy-copy version"):
                st.code(summary_result, language=None)
        except:
            st.error(error_message1, icon="🚨")

    elif clear:
        st.write('Text was cleared.')