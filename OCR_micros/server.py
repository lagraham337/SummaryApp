"""
OCR microsservice server for Comprehenson Science Project
Binds REP socket to tcp://*:4444
Expects image file from client
Replies with extracted text from image

Code copied from ZMQ
Date: 10/25/2022
Title: "Get Started"
Source URL: https://zeromq.org/get-started/?language=python&library=pyzmq#
"""

import zmq
from ocr import orc

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:4444")

print("Server is running!")

while True:
    #  Wait for next request from client
    message = socket.recv()
    print(f"Received request: {message}")

    #  Do some 'work'
    response = orc(message)

    #  Send reply back to client
    socket.send_string(response)
    