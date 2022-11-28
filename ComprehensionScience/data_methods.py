# Lauren Graham
# CS361

# Streamlit
import streamlit as st

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

# Data manipulation packages:
from PIL import Image
import cv2
import pandas as pd
import io
import os
import numpy as np
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
import pytesseract

def sumy_summarizer(docx):
    """Created summary of long text utilizing a tokenizer"""
    parser = PlaintextParser.from_string(docx,Tokenizer('English'))
    lex_summarizer = LexRankSummarizer()
    summary = lex_summarizer(parser.document, 3)
    summary_list = [str(sentence) for sentence in summary]
    result = ''.join(summary_list)
    return result

def clean_text(text):
    """remove unwanted characters from text"""
    return str(text, 'utf-8')

@st.cache
def get_text(raw_url):
    """Get text from raw URL"""
    page = urlopen(raw_url)
    soup = BeautifulSoup(page, features="lxml")
    fetched_text = ''.join(map(lambda p:p.text,soup.find_all('p')))
    return fetched_text

def string_from_image(img):
    """Converts image data to a string using pytesseract"""
    # To convert PIL Image to numpy array:
    img_array = np.array(img)
    img = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)
    # Get string using pytesseract
    return pytesseract.image_to_string(img)

def get_short_text_from_URL(raw_url, text_length):
    """accepts a URL and the proportional length to be removed and returns only a piece of text from the website"""
    raw_text = get_text(raw_url)
    len_of_full_text = len(raw_text)
    len_of_short_text = round(len_of_full_text/text_length)
    return raw_text[:len_of_short_text]