import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
import random

import nltk
#nltk.download("punkt")

# NLP
import spacy
from spacy.cli.download import download
##download(model="en_core_web_sm")
nlp = spacy.load('en_core_web_sm')
from spacy import displacy
HTML_WRAPPER = """<div style="overflow-x: auto; border: 1px solid #e6e9ef; border-radius: 0.25rem; padding: 1rem">{}</div>"""


# Summary packages
#from gensim.summarization import summarize
# source: https://blog.jcharistech.com/2019/01/05/how-to-summarize-text-or-document-with-sumy/
# sumy summary package 
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

def sumy_summarizer(docx):
    parser = PlaintextParser.from_string(docx,Tokenizer('English'))
    lex_summarizer = LexRankSummarizer()
    summary = lex_summarizer(parser.document, 3)
    summary_list = [str(sentence) for sentence in summary]
    result = ''.join(summary_list)
    return result

# NLP
@st.cache(allow_output_mutation=True)
def analyze_text(text):
    return nlp(text)

# Web scrapping packages
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from urllib.request import FancyURLopener
from random import choice

# get text from raw URL 
@st.cache
#https://matix.io/extract-text-from-webpage-using-beautifulsoup-and-python/
def get_text(raw_url):
    page = urlopen(raw_url)
    soup = BeautifulSoup(page, features="lxml")
    fetched_text = ''.join(map(lambda p:p.text,soup.find_all('p')))
    return fetched_text


# callback to update emojis in Session State
# in response to the on_click event
def random_emoji():
    st.session_state.emoji = random.choice(emojis)

# initialize emoji as a Session State variable
if "emoji" not in st.session_state:
    st.session_state.emoji = "👈"

emojis = ["📚", "📘", "📗", "📙", "📕", "📒", "📓"]


def main():
    """Summary and entity checker"""

    page_title="Comprehension Science",
    #st.title("Comprehension Science")

    #activities = ["Input Text", "Input URL", "Input IMG", "NER Checker",]
    #choice = st.sidebar.selectbox("Select Input Type", activities)

    with st.sidebar:
        selected = option_menu(
            menu_title = "Select Input Type",
            options = ["Input Text", "Input URL", "Input IMG"],
            icons = ["journal-text", "link-45deg", "file-image", "boxes"],
            menu_icon = "door-open",
            orientation = "vertical",
            styles = {

            }
        )

    def clear_form():   # clearing text https://discuss.streamlit.io/t/clear-the-text-in-text-input/2225/10 
        st.session_state["Enter Text Here:"] = ""
        st.session_state["Enter Text Here: "] = ""
        st.session_state["Enter URL"] = ""
        st.session_state["Choose an image file"] = ""
    
    if selected == 'Input Text':

        st.title("Tl;dr? 📚")
        st.write("That's okay. Paste that verbose, windy, logorheic, circumocutory piece of text below.")

        with st.form("myformsumtext"):
            raw_text = st.text_area("Enter Text Here:", key="Enter Text Here:", placeholder = "Type here " + st.session_state.emoji)
            f3, f4, f5, f6, f7, f8, f9, f10 = st.columns([1, 1, 1, 1, 1, 1, 1, 1]) # columns for purpose of aligning buttons
            with f3:
                summarize = st.form_submit_button(label="Summarize")
            with f10:
                clear = st.form_submit_button(label="Clear", on_click=clear_form)

        if summarize:
            st.info('Summarizing...')
            summary_result = sumy_summarizer(raw_text)  # using sumy
            st.write(summary_result)

        if clear:
            st.write('Text was cleared')


    if selected == 'Input URL':
        st.title("URL ⛓")
        st.write("Summarize text, preview text, or both! All you need is a URL.")
        with st.form("myformsumURL"):
            raw_url = st.text_input("Enter URL", key="Enter URL", placeholder = "Paste a valid URL here")
            f3, f4, f5, f6, f7, f8, f9, f10 = st.columns([1, 1, 1, 1, 1, 1, 1, 1]) # columns for purpose of aligning buttons
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
            st.write('Text was cleared')

    if selected == 'Input IMG':
        st.title("IMG 📸")
        st.write("Extract or summarize text from an image")
        with st.form("myformsumIMG"):
            image_file = st.file_uploader("Choose an image file", type=['png', 'jpg', 'jpeg'], accept_multiple_files=False, key="IMG", help="Jpg, jpeg and png files are supported. Gif, webm, and video files are not supported.", on_change=None, label_visibility="visible")
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
                st.image(image_file, caption=None, width=None, use_column_width='auto', clamp=False, channels="RGB", output_format="auto")
                st.write("This feature has not yet been implemented.")
            except:
                st.write("Sorry, this website has not approved the program to retrieve data.")

        if summarize:
            try:
                st.image(image_file, caption=None, width=None, use_column_width='auto', clamp=False, channels="RGB", output_format="auto")
                st.write("This feature has not yet been implemented.")
                
            except:
                st.write("Sorry, this website has not approved the program to retrieve data.")

        if clear:
            st.write('Upload was cleared')


    if selected == 'NER Checker':
        st.title("Entity Recognition with Spacy")

        with st.form("myformNER"):
            raw_text = st.text_area("Enter Text Here: ", key="Enter Text Here: ", placeholder = "Type Here")
            f3, f4, f5, f6, f7, f8 = st.columns([1, 1, 1, 1, 1, 1]) # columns for purpose of aligning buttons
            with f3:
                analyze = st.form_submit_button(label="Analyze")
            with f4:
                clear = st.form_submit_button(label="Clear ", on_click=clear_form)

        if analyze:
            st.info('Analyzing...')
            docx = analyze_text(raw_text)
            html = displacy.render(docx, style= 'ent')
            html = html.replace("\n\n", "\n")
            st.write(html, unsafe_allow_html=True)

        if clear:
            st.write('Text was cleared')

if __name__ == '__main__':
    main()