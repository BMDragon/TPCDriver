# Created by Brandon Weiss on 7/8/2022
import numpy as np
import matplotlib.pyplot as plt

record = np.load('./Data/records.npy', allow_pickle=True).item()
signal = np.load('./Data/signals.npy', allow_pickle=True).item()
photons = np.array([x+10 for x in range(100000)])

signalColor = '#00CD00'
scatterColor = '#DD9900'
absorbColor = '#000000'
diffuseReColor = '#888888'
specularReColor = '#00BEEF'

for i in range(len(photons)):
    xPos = np.array([0])
    yPos = np.array([0])
    zPos = np.array([0.025])

    shifted = False
    scatter = np.array([])
    absorb = np.array([])
    diffuse = np.array([])
    spec = np.array([])

    n = 1
    shiftDex = -1
    while photons[i] in record['step'+str(n)]['status']['photon'][0]:
        dex = record['step'+str(n)]['status']['photon'][0].toarray().index(photons[i])
        xPos = np.append(xPos, record['step'+str(n)]['s']['r'][0][dex])
        yPos = np.append(yPos, record['step'+str(n)]['s']['r'][1][dex])
        zPos = np.append(zPos, record['step'+str(n)]['s']['r'][2][dex])
        if not shifted and record['step'+str(n)]['status']['shifted'][0][dex]:
            shiftDex = n
            shifted = True
        if record['step'+str(n)]['status']['scatter'][0][dex]:
            scatter = np.append(scatter, n)
        if record['step'+str(n)]['status']['absorb'][0][dex]:
            absorb = np.append(absorb, n)
        diffused = record['step'+str(n)]['status']['diffusereflect'][0][dex]
        stopped = record['step'+str(n)]['status']['stopped'][0][dex]
        if diffused and not stopped:
            diffuse = np.append(diffuse, n)
        if record['step'+str(n)]['status']['specularreflect'][0][dex] and not diffused:
            spec = np.append(spec, n)
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

    ax.set_xlim(-0.025,0.025)
    ax.set_ylim(-0.025,0.025)
    ax.set_zlim(0,0.05)
    ax.set_xlabel('X')
    for j in range(len(xPos)):
        ax.text(xPos[j], yPos[j], zPos[j], str(j))
    plt.show()