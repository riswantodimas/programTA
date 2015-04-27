# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 17:26:14 2015

@author: riswantodimas
"""

import httplib2
import json
import sys
import logging
import socket


#Getting IP Address
s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('8.8.8.8', 80))
ipAddress=s.getsockname()[0]
if ipAddress[:3]=='167':
    ipAddress='localhost'
    
#Initialization
baseUrl = 'http://'+ipAddress+':8181/restconf/operational/'

h = httplib2.Http(".cache")
h.add_credentials('admin', 'admin')

url = baseUrl + '/network-topology:network-topology/'
logging.debug('url %s', url)
resp, content = h.request(url, "GET")
data = json.loads(content.decode())

print(data)