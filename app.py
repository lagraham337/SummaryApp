import streamlit as st
import pandas as pd
import numpy as np

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

    if choice == 'Summarize':
        st.subheader("Tl;dr")
        raw_text = st.text_area("Enter Text Here", "Type Here")
        #summary_choice = st.selectbox("Summary Choice", ["Sumy Lex Rank 1", "Sumy Lex Rank"])
        if st.button("Summarize"):
            
            #if summary_choice == 'Sumy Lex Rank 1':
            #    summary_result = sumy_summarizer(raw_text)
            #elif summary_choice == 'Sumy Lex Rank':
            #    summary_result = sumy_summarizer(raw_text)
            summary_result = sumy_summarizer(raw_text)
            st.write(summary_result)




if __name__ == '__main__':
    main()