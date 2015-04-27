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

#Getting Data
h = httplib2.Http(".cache")
h.add_credentials('admin', 'admin')
url = baseUrl + '/network-topology:network-topology/'
logging.debug('url %s', url)
resp, content = h.request(url, "GET")
topo_content = json.loads(content.decode())

#Parsing Data
topo=[]
if 'node' in (topo_content['network-topology']['topology'])[0]:
    node_list=(topo_content['network-topology']['topology'])[0]['node']
else:
    node_list={}
    
for node in node_list:
    node_info={}
    node_info[node['node-id']]=[]
    for tp in node['termination-point']:
        node_info[node['node-id']].append(tp['tp-id'])
    topo.append(node_info)
        
print(topo)