import streamlit as st
import pandas as pd
import numpy as np

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

# user agents so websites don't think we're a bot when we use their URLs
#user_agents = [
#    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
#    'Opera/9.25 (Windows NT 5.1; U; en)',
#    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
#    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
#    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
#    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9'
#]

#class MyOpener(FancyURLopener, object):
##    version = choice(user_agents)

#myopener = MyOpener()
#myopener.retrieve('http://www.useragent.org/', 'useragent.html')

# get text from raw URL 
@st.cache
#https://matix.io/extract-text-from-webpage-using-beautifulsoup-and-python/
def get_text(raw_url):
    page = urlopen(raw_url)
    soup = BeautifulSoup(page, features="lxml")
    fetched_text = ''.join(map(lambda p:p.text,soup.find_all('p')))
    return fetched_text

def main():
    """Summary and entity checker"""

    st.title("Comprehension Science")

    activities = ["Input Text", "Input URL", "NER Checker"]
    choice = st.sidebar.selectbox("Select Activity", activities)


    def clear_form():   # clearing text https://discuss.streamlit.io/t/clear-the-text-in-text-input/2225/10 
        st.session_state["Enter Text Here:"] = ""
        st.session_state["Enter Text Here: "] = ""
        st.session_state["Enter URL"] = ""
    
    if choice == 'Input Text':

        st.subheader("Tl;dr")

        with st.form("myformsumtext"):
            raw_text = st.text_area("Enter Text Here:", key="Enter Text Here:", placeholder = "Type Here")
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

    if choice == 'NER Checker':
        st.subheader("Entity Recognition with Spacy")

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


    if choice == 'Input URL':
        st.subheader("Summarize text, preview text, or both! All you need is a URL.")
        #st.caption("You can also choose to extract text")
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
                #st.write(raw_text)
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




        #raw_url = st.text_input("Enter URL", placeholder = "Paste a valid URL here")
        #if st.button("Extract"):
        #    if raw_url != "Type here":
        #        result = get_text(raw_url)
        #        len_of_full_text = len(result)
        #        st.write(result)
        #    else:
        #        st.write("Please paste only URLs")

if __name__ == '__main__':
    main()