import lib_program as lib
import time

allNodes = lib.get_topo()

#Getting User Input Node
i=1
print("Nodes:")
for node in allNodes:
    print("%i. %s"%(i,node['id']))
    i+=1
n=int(input("Silahkan pilih node (1-%i): "%(len(allNodes))))
print("Anda memilih node %s"%allNodes[n-1]['id'])

#Getting User Input Port
i=1
print("\nPorts:")
for port in allNodes[n-1]['port']:
    print("%i. %s"%(i,port))
    i+=1
p=int(input("Silahkan pilih port (1-%i): "%(len(allNodes[n-1]['port']))))
print("Anda memilih port %s"%allNodes[n-1]['port'][p-1])


print("\nData trafik untuk port %s pada node %s"%(allNodes[n-1]['port'][p-1],allNodes[n-1]['id']))

#Printing Data
try:
    while True:
        traffic_info=lib.get_traffic(allNodes[n-1]['id'],allNodes[n-1]['port'][p-1])
        print('Transmitted: %i bytes, Received: %i bytes'%(traffic_info['transmit'],traffic_info['receive']))
        time.sleep(2)
except KeyboardInterrupt:
    pass

