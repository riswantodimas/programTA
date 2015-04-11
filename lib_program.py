import httplib2
import json
import sys
import logging
import socket
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

#Getting IP Address
ipAddress=[(s.connect(('8.8.8.8', 80)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]
if ipAddress[:3]=='167':
    ipAddress='localhost'

#Initialization
baseUrl = 'http://'+ipAddress+':8181/restconf/operational/'


h = httplib2.Http(".cache")
h.add_credentials('admin', 'admin')
q=0

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
    

    Nodesort=[(int(node['id'].strip(node['id'][:9])), node) for node in Nodes]
    Nodesort.sort()
    Nodes=[node for (key,node) in Nodesort]
    ##print(Nodes)
    return Nodes

#Getting first Traffic Data
def get_traffic(node, port):
    traffic={}
    trafficUrl='opendaylight-inventory:nodes/node/'+node+'/node-connector/'+port
    traffic_content=get_data(trafficUrl)
    traffic['transmit']=traffic_content['node-connector'][0]['opendaylight-port-statistics:flow-capable-node-connector-statistics']['bytes']['transmitted']
    traffic['receive']=traffic_content['node-connector'][0]['opendaylight-port-statistics:flow-capable-node-connector-statistics']['bytes']['received']
    return traffic

"""def appendgraph(i):
    yar.append(lib.get_traffic(allNodes[n-1]['id'],allNodes[n-1]['port'][p-1])['transmit'])
    xar.append(time.time()-xinit)
    ax_transmit.clear()
    ax_transmit.plot(xar,yar)
    print(yar[len(yar)-1])"""

def draw(allNodes,n,p):
    traf_fig = plt.figure(1)

    ax_transmit = plt.subplot(1,1,1)
    ax_receive = ax_transmit.twinx()
    ax_receive.get_shared_y_axes().join(ax_transmit,ax_receive)
    
    x_time = []
    y_transmit = []
    y_receive = []
    time_init=time.time()
    
    def traffic_graph(i):
        if len(x_time)>=20:
            for i in range(0,19):
                y_transmit.insert(i,y_transmit.pop(i+1))
                y_receive.insert(i,y_receive.pop(i+1))
                x_time.insert(i,x_time.pop(i+1))
            y_transmit[19]=get_traffic(allNodes[n-1]['id'],allNodes[n-1]['port'][p-1])['transmit']
            y_receive[19]=get_traffic(allNodes[n-1]['id'],allNodes[n-1]['port'][p-1])['receive']
            x_time[19]=time.time()-time_init
        else:
            y_transmit.append(get_traffic(allNodes[n-1]['id'],allNodes[n-1]['port'][p-1])['transmit'])
            y_receive.append(get_traffic(allNodes[n-1]['id'],allNodes[n-1]['port'][p-1])['receive'])
            x_time.append(time.time()-time_init)
        ax_transmit.clear()
        ax_receive.clear()
        ax_transmit.plot(x_time,y_transmit,"r-")
        ax_receive.plot(x_time,y_receive,"b-")
        if len(x_time)<20:
            plt.xlim((0,20))
        else:
            plt.xlim((min(x_time),max(x_time)))
        diff=max(max(y_transmit),max(y_receive))-min(min(y_transmit),min(y_receive))
        
        plt.ylim(min(min(y_transmit),min(y_receive))-0.1*diff,max(max(y_transmit),max(y_receive))+0.1*diff)
        #print(yar[len(yar)-1])

    ani = animation.FuncAnimation(traf_fig, traffic_graph, interval=910)

    dif_fig =plt.figure(2)
    ax_diftrans=plt.subplot(1,1,1)
    
    y_diftrans=[]
    x_diftime=[]
    
    def diftraf_graph(i):
        global q
        q+=1
        dif=0
        if q==10:
            if len(y_transmit)<20:
                for r in range (0,10):
                    dif=dif+y_transmit[r]
                x_diftime.append(x_time[9])
            else:
                for r in range(10,20):
                    dif=dif+y_transmit[r]
                x_diftime.append(x_time[19])
            print(dif)
            y_diftrans.append(dif)
            q=0
        ax_diftrans.clear()
        ax_diftrans.plot(x_diftime,y_diftrans)

    
    ani2 = animation.FuncAnimation(dif_fig, diftraf_graph, interval=910)
    plt.show()



