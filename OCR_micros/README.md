<h1>Using the Optical Character Recognition (OCR) Microservice</h1>

<h2>Installations</h2>
To run the ocr.py file, you will need to install:
<ul><li>Tesseract</li>
<li>pytesseract</li>
<li>pillow</li></ul>

<h3>Tesseract</h3>
Tesseract is an open source text recognition (ORC) engine commonly used to extract text from images. To install Tesseract begin by identifying the correct <a href='https://tesseract-ocr.github.io/tessdoc/Installation.html'>installer</a> for your operating system. Below are a few common options. 
<br></br>
If you run into trouble, please reference the <a href='https://tesseract-ocr.github.io/tessdoc/Installation.html'>Tesseract documentation</a> for more information.

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

<hr></hr>
<h3>IMPORTANT!</h3>
Now that you've installed Tesseract, you will need to identify the installation path. 
To do so, you can type the command below into your terminal. 
<br></br>
Copy the path into the path_to_tess variable located in ocr.py
Example: path_to_tess = r'your_path'
<br></br>

```
where tesseract
```

<hr></hr>

<h3>pytesseract</h3>
Pytesseract is an OCR tool built specifially to work with python. It's a wrapper for the larger Tesseract project. To install pytesseract, run the following command in your terminal. Make sure your are in the correct directory (i.e. OCR_micros).
<br></br>

```
pip install pytesseract
```

<h3>pillow</h3>
Pillow is a popular python imaging library. It adds image processing capabilities to the python interpreter. To install pillow, run the following command in your terminal. Make sure your are in the correct directory (i.e. OCR_micros).
<br></br>

```
pip install pillow
```

<h2>Server.py</h2>
The server.py file uses ZeroMQ to build the communication pipe. ZeroMQ should not require any set up apart from library installation. 
<br></br>
However, if you run into trouble, please reference the <a href='https://zeromq.org/get-started/'>ZeroMQ documentation</a>.
<br></br>
To run server.py, copy the following command in your terminal. Make sure you are in the OCR_micros directory.

```
python3 server.py
```

<h3> How it works</h3>
Server.py creates a TCP socket bound to an IP address respresented with an astrick at port 4444.


```
socket.bind("tcp://*:4444")
```

It then waits for an incoming message. Once an incoming message is received, it makes a call to ocr.py, which does the data extraction.


```
response = orc(message)
```


It then send the "response" (i.e. the extracted text) back to the client via the socket connection at "tcp://*:4444". 


```
socket.send_string(response)
```


<b>Note:</b> the response is sent as binary. So, it may need to be decoded. Example: b'Sample Text 1\n'

<h3>Troubleshooting server.py</h3>
If server.py is running but appears not to be working, first check the <em>port number</em>.

<h2>Client_test.py</h2>
This is the client side code used to test server.py while the client-side server is being built. This file should not be used for anything other than testing the communication pipe.
<br></br>
To run client_test.py, copy the following command in your terminal. Make sure you are in the OCR_micros directory. 
<br></br>

```
python3 client_test.py
```

<h2>Contact Information</h2>
monteza@oregonstate.edu

Date: 10/25/2022