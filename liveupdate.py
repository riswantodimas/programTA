import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import time

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
xar = []
yar = []
n=0

def animate(i):
    xar.append(i)
    yar.append(np.random.randint(20))
    ax1.clear()
    ax1.plot(xar,yar)
ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()
