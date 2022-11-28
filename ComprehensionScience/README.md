# Comprehension Science SummaryApp

The purpose of this app is for users to paste text, a URL, or upload an image file and receive either a text summary or (in the case of an image file) text extraction. It is being developed using Streamlit and a number of Python libraries including NLTK. 

It is currently in Beta.
The URL page works inconsistently. I recommended trying the following URLs for fun:

[Natural Language Processing](https://www.ibm.com/cloud/learn/natural-language-processing)

[What Is Coastal Engineering](https://geo.libretexts.org/Bookshelves/Oceanography/Coastal_Dynamics_(Bosboom_and_Stive)/01%3A_Overview/1.02%3A_Coastal_dynamics_for_coastal_engineers/1.2.01%3A_What_is_coastal_engineering)

[How The Grimm Brothers Saved The Fairy Tale](https://www.neh.gov/humanities/2015/marchapril/feature/how-the-grimm-brothers-saved-the-fairy-tale)

These may also be good sources to copy text directly for trying the main page.

[<img src="https://upload.wikimedia.org/wikipedia/commons/0/09/YouTube_full-color_icon_%282017%29.svg" width="5%">](https://youtu.be/Dwzc0zhGkEA "Cognitive Style Heuristics")

## Usage

Use the package manager [pip](https://pypi.org/project/pip/) to install pipenv:

```bash
pip3 install pipenv
```

Navigate into the repo and activate the virtual environment:
```bash
pipenv shell
```

Install requirements:
```bash
pipenv install -r requirements.txt
```

Run with file name:
```bash
streamlit run app.py
```
or address from github:
```bash
streamlit run https://github.com/lagraham337/SummaryApp/blob/main/ComprehensionScience/app.py
```

If you have difficulty, you may try activating the shell and installing Streamlit in the virtual environment:
```bash
pipenv install streamlit
```

See [Streamlit Documentation](https://docs.streamlit.io/library/get-started/installation) for more information on getting started with Streamlit.

## Exit

To stop the server, press ctrl-c. Type exit to return to your normal shell.
