import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import time

fig = plt.figure()
ax1 = plt.subplot(1,1,1)
ax2 = ax1.twinx()
ax2.get_shared_y_axes().join(ax1,ax2)

fig2=plt.figure()
ax3=plt.subplot(1,1,1)


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

def difgraph(i):
    global q
    q+=1
    dif=0
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
        
        print(yar3)
        print(xar2)
        q=0
    ax3.clear()
    ax3.plot(xar2,yar3,"b-")
        


def appendgraph(i):
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
    ax1.clear()
    ax2.clear()
    ax1.plot(xar,yar1,"b-")
    ax2.plot(xar,yar2,"r-")
    ax2.spines["left"].set_visible(False)
    ax1.spines["bottom"].set_visible(False)
    ax1.tick_params(axis='both', direction='out')
    ax1.get_xaxis().tick_bottom()   # remove unneeded ticks 
    ax1.get_yaxis().tick_left()
    ax1.set_autoscaley_on(False)
    plt.ylim((0,20))
    if len(xar)<20:
        plt.xlim((0,20))
    else:
        plt.xlim((min(xar),max(xar)))
    #print(xar)
    #print(yar)


ani = animation.FuncAnimation(fig, appendgraph, interval=900)
ani2 = animation.FuncAnimation(fig2, difgraph, interval=900)

plt.show()



#hohohoho
