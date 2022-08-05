# Created by Brandon Weiss on 7/8/2022
import numpy as np
import matplotlib.pyplot as plt

photons = np.array([x+1 for x in range(100000)])
folder = './DriverData'
tpcSize = 0.03

signalColor = '#00CD00'
scatterColor = '#DD9900'
absorbColor = '#000000'
diffuseReColor = '#888888'
specularReColor = '#00BEEF'

record = np.load(folder + '/records.npy', allow_pickle=True).item()
signal = np.load(folder + '/signals.npy', allow_pickle=True).item()

for i in range(len(photons)):
    xPos = np.array([])
    yPos = np.array([])
    zPos = np.array([])

    shifted = False
    scatter = np.array([])
    absorb = np.array([])
    diffuse = np.array([])
    spec = np.array([])
    maxN = len(record.keys())

    n = 1
    shiftDex = -1
    while n < maxN and photons[i] in record['step'+str(n)]['status']['photon'][0]:
        dex = record['step'+str(n)]['status']['photon'][0].toarray().index(photons[i])
        xPos = np.append(xPos, record['step'+str(n)]['s']['r'][0][dex])
        yPos = np.append(yPos, record['step'+str(n)]['s']['r'][1][dex])
        zPos = np.append(zPos, record['step'+str(n)]['s']['r'][2][dex])
        if not shifted and record['step'+str(n)]['status']['shifted'][0][dex]:
            shiftDex = n-1
            shifted = True
        if record['step'+str(n)]['status']['scatter'][0][dex]:
            scatter = np.append(scatter, n-1)
        if record['step'+str(n)]['status']['absorb'][0][dex]:
            absorb = np.append(absorb, n-1)
        diffused = record['step'+str(n)]['status']['diffusereflect'][0][dex] or shiftDex == n-1
        stopped = record['step'+str(n)]['status']['stopped'][0][dex]
        if diffused and not stopped:
            diffuse = np.append(diffuse, n-1)
        if record['step'+str(n)]['status']['specularreflect'][0][dex] and not diffused:
            spec = np.append(spec, n-1)
        n += 1
    if not shifted:
        shiftDex = len(xPos)

    plt.figure(i)
    ax = plt.axes(projection='3d')
    ax.set_title('photon number ' + str(photons[i]))

    ax.plot(xPos[0:shiftDex+1], yPos[0:shiftDex+1], zPos[0:shiftDex+1], marker='.', ls='-',
            color='m', markerfacecolor='r', markeredgecolor='r')
    ax.plot(xPos[shiftDex:], yPos[shiftDex:], zPos[shiftDex:], marker='.', ls='-',
            color='b', markerfacecolor='r', markeredgewidth=0.0)

    if photons[i] in signal['photon'][0].toarray():
        ax.plot(xPos[-1], yPos[-1], zPos[-1], marker='.', color=signalColor)
    for sc in scatter:
        sc = round(sc)
        ax.plot(xPos[sc], yPos[sc], zPos[sc], marker='.', color=scatterColor)
    for ab in absorb:
        ab = round(ab)
        ax.plot(xPos[ab], yPos[ab], zPos[ab], marker='.', color=absorbColor)
    for df in diffuse:
        df = round(df)
        ax.plot(xPos[df], yPos[df], zPos[df], marker='.', color=diffuseReColor)
    for sp in spec:
        sp = round(sp)
        ax.plot(xPos[sp], yPos[sp], zPos[sp], marker='.', color=specularReColor)

    ax.set_xlim(-1*tpcSize/2, tpcSize/2)
    ax.set_ylim(-1*tpcSize/2, tpcSize/2)
    ax.set_zlim(0, tpcSize)
    ax.set_xlabel('X')
    for j in range(len(xPos)):
        ax.text(xPos[j], yPos[j], zPos[j], str(j))
    plt.show()