"""
Test code for microservice server
Connect REQ socket to tcp://localhost:6000
Sends image file to OCR server
Expects extracted text back

Code copied from ZMQ
Date: 10/25/2022
Title: "Get Started"
Source URL: https://zeromq.org/get-started/?language=python&library=pyzmq#
"""

import zmq

context = zmq.Context()

#  Connect socket to server
print("Connecting to OCR server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:4444")

# Send image file to server
PATH_TO_IMG = '../OCR_micros/sample_images/sampletext2.png'
socket.send_string(PATH_TO_IMG)

#  Get the reply
message = socket.recv()
print(f"Received reply {message}")
