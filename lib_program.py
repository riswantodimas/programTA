import httplib2
import json
import sys
import logging
import socket
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
from PyQt4.uic import loadUiType 
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
    
Ui_MainWindow, QMainWindow = loadUiType('window.ui')

class Main(QMainWindow, Ui_MainWindow):
    def __init__(self, ):
        super(Main, self).__init__()
        self.setupUi(self)
        self.fig_dict = {}
        self.node_comboBox.currentIndexChanged['QString'].connect(self.updatelistport)

        #Getting IP Address
        self.ipAddress=[(s.connect(('8.8.8.8', 80)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]
        if self.ipAddress[:3]=='167':
            self.ipAddress='localhost'

        #Initialization
        self.baseUrl = 'http://'+self.ipAddress+':8181/restconf/operational/'


        self.h = httplib2.Http(".cache")
        
        
        
        self.h.add_credentials('admin', 'admin')
        self.topo={}
        self.j=0

    def get_data(self,detUrl):
        url = self.baseUrl + detUrl
        logging.debug('url %s', url)
        resp, content = self.h.request(url, "GET")
        data = json.loads(content.decode())
        return data

    #Getting Topology Data
    def get_topo(self):
        topo_content = self.get_data('/network-topology:network-topology/')  
        
        self.topo={}
        if 'node' in (topo_content['network-topology']['topology'])[0]:
            node_list=(topo_content['network-topology']['topology'])[0]['node']
        else:
            node_list={}
            
        for node in node_list:
            list_tp=[]        
            for tp in node['termination-point']:
                list_tp.append(tp['tp-id'])
            self.topo[node['node-id']]=list_tp
        
    def addlistnode(self):
        listnode=[]
        for x in self.topo:
            listnode.append(x)
        
        listsort=[(int(node.strip("openflow:")), node) for node in listnode]
        listsort.sort()
        listnode=[node for (key,node) in listsort]
        
        listnode.append(listnode[len(listnode)-1])
        for i in range(len(listnode)-1,0,-1):
            listnode.insert(i,listnode.pop(i-1))
        listnode[0]="..."
        
        for y in listnode:            
            self.node_comboBox.addItem(y)
    
    def updatelistport(self,port):
        self.port_comboBox.clear()
        if port!="...": 
            listport=self.topo[port]
            for port in listport:
                if port.replace(port[:11],"",1)=="LOCAL":
                    local=port
            listport.remove(local)
            
            listsort=[(int(port.replace(port[:11],"",1)),port) for port in listport]
            listsort.sort()
            listport=[port for (key,port) in listsort]
            listport.append(local)
            
            i=0
            listport.append(listport[len(listport)-1])
            for i in range(len(listport)-1,0,-1):
                listport.insert(i,listport.pop(i-1))
            listport[0]="..."
            
            for x in listport:
                self.port_comboBox.addItem(x)
    
    #Getting first Traffic Data
    def get_traffic(self,node, port):
        traffic={}
        trafficUrl='opendaylight-inventory:nodes/node/'+node+'/node-connector/'+port
        traffic_content=self.get_data(trafficUrl)
        traffic['transmit']=traffic_content['node-connector'][0]['opendaylight-port-statistics:flow-capable-node-connector-statistics']['bytes']['transmitted']
        traffic['receive']=traffic_content['node-connector'][0]['opendaylight-port-statistics:flow-capable-node-connector-statistics']['bytes']['received']
        return traffic
    
    def addgraph(self):
        fig = plt.figure()
        ax_transmit = fig.add_subplot(2,1,1)
        ax_receive = ax_transmit.twinx()
        ax_receive.get_shared_y_axes().join(ax_transmit,ax_receive)
        
        ax_diftrans = fig.add_subplot(2,1,2)
        ax_difrec = ax_diftrans.twinx()
        ax_receive.get_shared_y_axes().join(ax_diftrans,ax_difrec)
        
        self.canvas = FigureCanvas(fig)
        self.tot_vl.addWidget(self.canvas)        
        
        x_time  = []
        x_diftime=[]
        y_transmit = []
        y_receive = []
        y_diftrans=[]
        y_difrec=[]
        time_init=time.time()
                
        self.j=0
        
        
        def appendgraph(i):
            self.j=self.j+1
            dif=0
            if len(x_time)>=20:
                for i in range(0,19):
                    y_transmit.insert(i,y_transmit.pop(i+1))
                    y_receive.insert(i,y_receive.pop(i+1))
                    x_time.insert(i,x_time.pop(i+1))
                y_transmit[19]=self.get_traffic("openflow:1","openflow:1:1")['transmit']
                y_receive[19]=self.get_traffic("openflow:1","openflow:1:1")['receive']
                x_time[19]=time.time()-time_init
                
            else:
                
                y_transmit.append(self.get_traffic("openflow:1","openflow:1:1")['transmit'])
                y_receive.append(self.get_traffic("openflow:1","openflow:1:1")['receive'])
                x_time.append(time.time()-time_init)
                
            if self.j==10:
                if len(y_transmit)<20:
                    y_diftrans.append(y_transmit[9]-y_transmit[0])
                    y_difrec.append(y_receive[9]-y_receive[0])
                    x_diftime.append(x_time[9])
                else:
                    if len(x_diftime)>=10:
                        for i in range(0,9):
                            y_diftrans.insert(i,y_diftrans.pop(i+1))
                            y_difrec.insert(i,y_difrec.pop(i+1))
                            x_diftime.insert(i,x_diftime.pop(i+1))
                        y_diftrans[9]=y_transmit[19]-y_transmit[10]
                        y_difrec[9]=y_receive[19]-y_receive[10]
                        x_diftime[9]=x_time[19]
                    else:
                        y_diftrans.append(y_transmit[19]-y_transmit[10])
                        y_difrec.append(y_receive[19]-y_receive[10])
                        x_diftime.append(x_time[19])
               
                self.j=0
                
            ax_transmit.clear()
            ax_receive.clear()
            ax_diftrans.clear()
            ax_difrec.clear()
            
            ax_transmit.plot(x_time,y_transmit,"r-")
            ax_receive.plot(x_time,y_receive,"b-")
            ax_diftrans.plot(x_diftime,y_diftrans,"r-")
            ax_difrec.plot(x_diftime,y_difrec,"b-")
            
            if len(x_time)<20:
                ax_transmit.set_xlim([0,20])
            else:
                ax_transmit.set_xlim([min(x_time),1.1*max(x_time)-0.1*min(x_time)])
                ax_diftrans.set_xlim([min(x_diftime),1.1*max(x_diftime)-0.1*min(x_diftime)])
                dif_scale=max(max(y_diftrans),max(y_difrec))-min(min(y_diftrans),min(y_difrec))
                ax_diftrans.set_ylim(min(min(y_diftrans),min(y_difrec))-0.1*dif_scale,max(max(y_diftrans),max(y_difrec))+0.1*dif_scale)
            diff=max(max(y_transmit),max(y_receive))-min(min(y_transmit),min(y_receive))   
            ax_transmit.set_ylim(min(min(y_transmit),min(y_receive))-0.1*diff,max(max(y_transmit),max(y_receive))+0.1*diff)
         
        ani = animation.FuncAnimation(fig, appendgraph, interval=900)
       
    
if __name__ == '__main__':
    import sys
    from PyQt4 import QtGui
    import numpy as np
 
    
    app = QtGui.QApplication(sys.argv)
    main = Main()
    main.get_topo()
    main.addgraph()
    #main.addfig('Figure 1', fig1)
    main.addlistnode()
    #main.addtext(main.readlist())
    main.show()
     
    sys.exit(app.exec_())



