import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import time

fig = plt.figure()
ax1 = plt.subplot(1,1,1)

xar = []
yar = []
for q in range(20,0,-1):
    xar.insert(q,q)
    yar.insert(q,0)
xinit=time.time()


"""def appendgraph(i):
    yar.append(np.random.randint(20))
    xar.append(time.time()-xinit)
    ax1.clear()
    ax1.plot(xar,yar)
    ax1.set_autoscaley_on(False)
    plt.ylim((0,20))
    print(xar)
    print(yar)"""

def movegraph(i):
    for n in range(19,0,-1):
        yar.insert(n,yar.pop(n-1))
        xar.insert(n,xar.pop(n-1))
    yar[0]=np.random.randint(20)
    xar[0]=time.time()-xinit
    #xar.append(time.time()-xinit)
    ax1.clear()
    ax1.plot(xar,yar)
    ax1.set_autoscaley_on(False)
    plt.ylim((0,20))
    plt.xlim([min(xar),max(xar)])
    print(xar)

ani = animation.FuncAnimation(fig, movegraph, interval=910)

plt.show()



#hohohoho
