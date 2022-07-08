# Created by Brandon Weiss on 7/8/2022
from matplotlib import projections
import numpy as np
import matplotlib.pyplot as plt

record = np.load('./Data/records.npy', allow_pickle='TRUE').item()

photon = 25
xPos = np.array([])
yPos = np.array([])
zPos = np.array([])

n = 1
while photon in record['step'+str(n)]['status']['photon'][0]:
    dex = record['step'+str(n)]['status']['photon'][0].toarray().index(photon)
    xPos = np.append(xPos, record['step'+str(n)]['s']['r'][0][dex])
    yPos = np.append(yPos, record['step'+str(n)]['s']['r'][1][dex])
    zPos = np.append(zPos, record['step'+str(n)]['s']['r'][2][dex])
    n += 1

fig = plt.figure(1)
ax = plt.axes(projection='3d')
ax.scatter3D(xPos, yPos, zPos)
for i in range(len(xPos)):
    ax.text(xPos[i], yPos[i], zPos[i], str(i+1))
plt.show()