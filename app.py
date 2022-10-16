import streamlit as st
import pandas as pd
import numpy as np
import pyautogui

import nltk
nltk.download("punkt")

# NLP


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

# Web scrapping packages
def main():
    """Summary and entity checker"""

    st.title("Comprehension Science")

    activities = ["Summarize", "NER Checker", "NER for URL"]
    choice = st.sidebar.selectbox("Select Activity", activities)


    def clear_form():   # clearing text https://discuss.streamlit.io/t/clear-the-text-in-text-input/2225/10 
        st.session_state["Enter Text Here:"] = ""
    
    if choice == 'Summarize':

        st.subheader("Tl;dr")


        with st.form("myform"):
            raw_text = st.text_area("Enter Text Here:", key="Enter Text Here:", placeholder = "Type Here")
            f3, f4, f5, f6, f7, f8 = st.columns([1, 1, 1, 1, 1, 1]) # columns for purpose of aligning buttons
            with f3:
                summarize = st.form_submit_button(label="Summarize")
            with f4:
                clear = st.form_submit_button(label="Clear", on_click=clear_form)

        if summarize:
            st.info('Summarizing...')
            summary_result = sumy_summarizer(raw_text)  # using sumy
            st.write(summary_result)

        if clear:
            st.write('Text was cleared')



if __name__ == '__main__':
    main()