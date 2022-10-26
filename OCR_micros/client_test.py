"""
Test code for microservice server
Connect REQ socket to tcp://localhost:4444
Sends image file to OCR server
Expects extracted text back

Code adapted from ZMQ
Date: 10/25/2022
Title: "Get Started"
Source URL: https://zeromq.org/get-started/?language=python&library=pyzmq#
"""

import zmq
import os

context = zmq.Context()

#  Connect socket to server
print("Connecting to OCR server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:4444")

# Send image file to server
PATH_TO_IMG = r'../OCR_micros/sample_images/'

for root, dirs, file_names in os.walk(PATH_TO_IMG):
    for file_name in file_names:
        full_path = PATH_TO_IMG + file_name
        socket.send_string(full_path)
        
        #  Get the reply
        message = socket.recv()
        print(f"Received reply {message}")
