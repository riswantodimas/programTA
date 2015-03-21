import httplib2
import json
import sys
import logging
import socket

#Getting IP Address
ipAddress=[(s.connect(('8.8.8.8', 80)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]
if ipAddress[:3]=='167':
    ipAddress='localhost'

#Initialization
baseUrl = 'http://'+ipAddress+':8181/restconf/operational/'


h = httplib2.Http(".cache")
h.add_credentials('admin', 'admin')

def get_data(detUrl):
    url = baseUrl + detUrl
    logging.debug('url %s', url)
    resp, content = h.request(url, "GET")
    data = json.loads(content.decode())
    return data

#Getting Topology Data
def get_topo():
    Nodes=[]
    topo_content = get_data('/network-topology:network-topology/')
    if 'node' in (topo_content['network-topology']['topology'])[0]:
        node_list=(topo_content['network-topology']['topology'])[0]['node']
    else:
        node_list={}

    for node in node_list:
        node_info={}
        node_info['id']=node['node-id']
        node_info['port']=[]
        for tp in node['termination-point']:
            node_info['port'].append(tp['tp-id'])
        Nodes.append(node_info)
    return Nodes

#Getting first Traffic Data
def get_traffic(node, port):
    traffic={}
    trafficUrl='opendaylight-inventory:nodes/node/'+node+'/node-connector/'+port
    traffic_content=get_data(trafficUrl)
    traffic['transmit']=traffic_content['node-connector'][0]['opendaylight-port-statistics:flow-capable-node-connector-statistics']['bytes']['transmitted']
    traffic['receive']=traffic_content['node-connector'][0]['opendaylight-port-statistics:flow-capable-node-connector-statistics']['bytes']['received']
    return traffic



