# -*- coding: utf-8 -*-
"""
Created on Sat Dec 21 16:12:58 2019

@author: Celal
"""

#client
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 1241))

while True:
    full_msg = ''
    full_msg2 = ''
    full_msg3 =''
    while True:
        msg = s.recv(1024)
        full_msg = msg.decode("utf-8")
        print(full_msg)
        s.send(str.encode(input()))
        
        tcp_response = s.recv(1024)
        print((str(tcp_response.decode("utf-8"))))