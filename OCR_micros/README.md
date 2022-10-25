<h1>Using the Optical Character Recognition (OCR) Microservice</h1>

<h2>Installations</h2>
To run the ocr.py file, you will need to install:
<ul><li>Tesseract</li>
<li>pytesseract</li>
<li>pillow</li></ul>

<h3>Tesseract</h3>
Tesseract is an open source text recognition (ORC) engine commonly used to extract text from images.

To install Tesseract begin by identifying the correct <a href='https://tesseract-ocr.github.io/tessdoc/Installation.html'>installer</a> for your operating system. Below are a few common options. If you run into trouble, please reference the <a href='https://tesseract-ocr.github.io/tessdoc/Installation.html'>Tesseract documentation</a> for more information.

<h4>Windows</h4>

```
https://github.com/UB-Mannheim/tesseract/wiki
```

<h4>macOS</h4>

```
brew install tesseract
```

<h4>Ubuntu</h4>

```
sudo apt install tesseract-ocr
sudo apt install libtesseract-dev
```

<h3>pytesseract</h3>
Pytesseract is an OCR tool built specifially to work with python. It's a wrapper for the larger Tesseract project.

To install pytesseract, run the following command in your terminal.
Make sure your are in the correct directory (i.e. OCR_micros)

```
pip install pytesseract
```

<h3>pillow</h3>
Pillow is a popular python imaging library. It adds image processing capabilities to the python interpreter.

To install pillow, run the following command in your terminal.
Make sure your are in the correct directory (i.e. OCR_micros)

```
pip install pillow
```
