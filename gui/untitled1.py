# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 15:11:18 2015

@author: riswantodimas
"""

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
        self.mplcomboBox.currentIndexChanged['QString'].connect(self.updatelistport)
        self.mplcomboBox2.currentIndexChanged['QString'].connect(self.addtext)
        
        
    def addfig(self, name, fig):
        self.fig_dict[name] = fig
        self.mplfigs.addItem(name)
        
    def addtext(self, Qstring):
        #teks=Qstring.text()
        self.mplfigs.addItem(Qstring)
        
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
            self.mplcomboBox.addItem(y)
            
    def updatelistport(self,port):
        self.mplcomboBox2.clear()
        if port!="...": 
            for x in topo[port]:
                self.mplcomboBox2.addItem(x)
        
    def readlist(self):
        return str(self.mplcomboBox.currentText())
        
    def addmpl(self, fig):
        self.canvas = FigureCanvas(fig)
        self.mplvl.addWidget(self.canvas)
        self.canvas.draw()
 
if __name__ == '__main__':
    import sys
    from PyQt4 import QtGui
    import numpy as np
 
    fig1 = Figure()
    ax1f1 = fig1.add_subplot(111)
    ax1f1.plot(np.random.rand(5))
    
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
    main.addmpl(fig1)
    main.addfig('Figure 1', fig1)
    main.addlistnode()
    #main.addtext(main.readlist())
    main.show()
     
    sys.exit(app.exec_())