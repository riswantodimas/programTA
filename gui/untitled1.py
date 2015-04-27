# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 15:11:18 2015

@author: riswantodimas
"""

from PyQt4.uic import loadUiType
 
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
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
        #self.port_comboBox.currentIndexChanged['QString'].connect(self.addtext)
        
        
    """def addfig(self, fig):
        self.fig_dict[name] = fig
        self.mplfigs.addItem(name)
        
    def addtext(self, Qstring):
        #teks=Qstring.text()
        if Qstring!="...":
            self.mplfigs.addItem(Qstring)"""
        
    def addlistnode(self):
        listnode=[]
        for x in topo:
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
            listport=topo[port]
            listport.append(listport[len(listport)-1])
            for i in range(len(listport)-1,0,-1):
                listport.insert(i,listport.pop(i-1))
            listport[0]="..."
            for x in listport:
                self.port_comboBox.addItem(x)
        
    def addgraph(self):
        fig = plt.figure()
        ax1 = fig.add_subplot(2,1,1)
        ax2 = ax1.twinx()
        ax2.get_shared_y_axes().join(ax1,ax2)
        ax3 = fig.add_subplot(2,1,2)
        
        self.canvas = FigureCanvas(fig)
        self.tot_vl.addWidget(self.canvas)        
        
        xar  = []
        xar2 = []
        yar1 = []
        yar2 = []
        yar3 = []
        """"for q in range(20,0,-1):
            xar.insert(q,q)
            yar.insert(q,0)"""
        xinit=time.time()
                
        self.j=0
        
        
        def appendgraph(i):
            self.j=self.j+1
            dif=0
            if len(yar1)>=20 and len(yar2)>=20:
                for i in range(0,19):
                    yar1.insert(i,yar1.pop(i+1))
                    yar2.insert(i,yar2.pop(i+1))
                    xar.insert(i,xar.pop(i+1))
                yar1[19]=np.random.randint(20)
                yar2[19]=np.random.randint(20)
                xar[19]=time.time()-xinit
                
            else:
                
                yar1.append(np.random.randint(20))
                yar2.append(np.random.randint(20))
                xar.append(time.time()-xinit)
                
            if self.j==10:
                if len(yar1)<20:
                    for r in range(0,10):
                       dif=dif+yar1[r]
                    xar2.append(xar[9])
                else:
                    for r in range(10,20):
                       dif=dif+yar1[r]
                    xar2.append(xar[19])
                yar3.append(dif)
                self.j=0
                
            ax1.clear()
            ax2.clear()
            ax3.clear()
            
            ax1.plot(xar,yar1,"b-")
            ax2.plot(xar,yar2,"r-")
            ax3.plot(xar2,yar3,"b-")
            
            if len(xar)<20:
                ax1.set_xlim([0,20])
            else:
                ax1.set_xlim([min(xar),1.1*max(xar)-0.1*min(xar)])
            
            if len(xar2)==0:
                ax3.set_xlim([0,100])
            else:
                ax3.set_xlim([min(xar2),max(xar2)])
    

        ani = animation.FuncAnimation(fig, appendgraph, interval=900)
        #self.canvas.draw()
 
 
if __name__ == '__main__':
    import sys
    from PyQt4 import QtGui
    import numpy as np
 
    

    
    topo={'openflow:1': ['openflow:1:LOCAL', 'openflow:1:2', 
        'openflow:1:1'], 'openflow:2': ['openflow:2:1', 
        'openflow:2:3', 'openflow:2:2', 'openflow:2:LOCAL'], 
        'openflow:3': ['openflow:3:LOCAL', 'openflow:3:1', 
        'openflow:3:2', 'openflow:3:3'], 'openflow:4': ['openflow:4:1', 
        'openflow:4:2', 'openflow:4:3', 'openflow:4:LOCAL']
        ,'openflow:5': ['openflow:5:2', 'openflow:5:1', 
        'openflow:5:LOCAL', 'openflow:5:3'], 'openflow:6': 
        ['openflow:6:3', 'openflow:6:2', 'openflow:6:1', 'openflow:6:LOCAL'], 
        'openflow:7': ['openflow:7:3', 'openflow:7:2', 
        'openflow:7:LOCAL', 'openflow:7:1']}
    #topo=["openflow1","openflow2","openflow3","openflow4"]
    
    app = QtGui.QApplication(sys.argv)
    main = Main()
    main.addgraph()
    #main.addfig('Figure 1', fig1)
    main.addlistnode()
    #main.addtext(main.readlist())
    main.show()
     
    sys.exit(app.exec_())