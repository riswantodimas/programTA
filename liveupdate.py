import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import time

fig = plt.figure()
ax1 = fig.add_subplot(2,1,1)
ax2 = ax1.twinx()
ax2.get_shared_y_axes().join(ax1,ax2)
ax3 = fig.add_subplot(2,1,2)


xar  = []
xar2 = []
yar1 = []
yar2 = []
yar3 = []
""""for q in range(20,0,-1):
    xar.insert(q,q)
    yar.insert(q,0)"""
xinit=time.time()
q=0


def appendgraph(i):
    global q
    q+=1
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
        
        yar1.append(np.random.ransurements since, which show that the North Magnetic Pole is moving continually northwestward. In 2001, an expedition located the pole at 81.3°N 110.8°W. In 2007, the latest survey found the pole at 83.95°N 120.72°W.[12] During the 20th century it moved 1100 km, and since 1970 its rate of motion has accelerated from 9 km/year to approximately 52 km/year (2001dint(20))
        yar2.append(np.random.randint(20))
        xar.append(time.time()-xinit)
        
    if q==10:
        if len(yar1)<20:
            for r in range(0,10):
               dif=dif+yar1[r]
            xar2.append(xar[9])
        else:
            for r in range(10,20):
               dif=dif+yar1[r]
            xar2.append(xar[19])
        yar3.append(dif)
        q=0
        
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

plt.show()



#hohohoho
