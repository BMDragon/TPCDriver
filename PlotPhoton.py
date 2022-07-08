# Created by Brandon Weiss on 7/8/2022
import numpy as np
import matplotlib.pyplot as plt

record = np.load('./Data/records.npy', allow_pickle='TRUE').item()

photon = 69420
xPos = np.array([0])
yPos = np.array([0])
zPos = np.array([0.025])

n = 1
while photon in record['step'+str(n)]['status']['photon'][0]:
    dex = record['step'+str(n)]['status']['photon'][0].toarray().index(photon)
    xPos = np.append(xPos, record['step'+str(n)]['s']['r'][0][dex])
    yPos = np.append(yPos, record['step'+str(n)]['s']['r'][1][dex])
    zPos = np.append(zPos, record['step'+str(n)]['s']['r'][2][dex])
    n += 1

fig = plt.figure(1)
ax = plt.axes(projection='3d')
ax.plot(xPos, yPos, zPos, marker='.', ls='-', color='b', markerfacecolor='r', markeredgecolor='r')
ax.set_xlim(-0.025,0.025)
ax.set_ylim(-0.025,0.025)
ax.set_zlim(0,0.05)
ax.set_xlabel('X')
for i in range(len(xPos)):
    ax.text(xPos[i], yPos[i], zPos[i], str(i))
plt.show()