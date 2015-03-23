import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import time

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
xar = []
yar = []
n=0
xinit=time.time()

def animate(i):
    yar.append(np.random.randint(20))
    xar.append(time.time()-xinit)
    ax1.clear()
    ax1.plot(xar,yar)
ani = animation.FuncAnimation(fig, animate, interval=910)
plt.show()
