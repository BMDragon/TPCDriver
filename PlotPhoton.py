# Created by Brandon Weiss on 7/8/2022
import numpy as np
import matplotlib.pyplot as plt

photons = np.array([x+1 for x in range(100000)])     # Which photons to draw paths for
folder = './DriverData'     # Directory where files are saved
tpcWidth = 0.3     # Width of the TPC
tpcHeight = 0.3     # Height of the TPC

# Color specifications #
stopColor = 'r'
signalColor = '#00CD00'
scatterColor = '#DD9900'
absorbColor = '#000000'
diffuseReColor = '#888888'
specularReColor = '#00BEEF'

record = np.load(folder + '/records.npy', allow_pickle=True).item()
signal = np.load(folder + '/signals.npy', allow_pickle=True).item()

for i in range(len(photons)):
    # Initialize values
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
    while n <= maxN and photons[i] in record['step'+str(n)]['status']['photon'][0]:
        # Get photon index
        dex = record['step'+str(n)]['status']['photon'][0].toarray().index(photons[i])

        # Add position of point
        xPos = np.append(xPos, record['step'+str(n)]['s']['r'][0][dex])
        yPos = np.append(yPos, record['step'+str(n)]['s']['r'][1][dex])
        zPos = np.append(zPos, record['step'+str(n)]['s']['r'][2][dex])

        # Check waveshifting
        if not shifted and record['step'+str(n)]['status']['shifted'][0][dex]:
            shiftDex = n-1
            shifted = True

        # Check if Rayleigh scattered
        if record['step'+str(n)]['status']['scatter'][0][dex]:
            scatter = np.append(scatter, n-1)

        # Check if absorbed back into material
        if record['step'+str(n)]['status']['absorb'][0][dex]:
            absorb = np.append(absorb, n-1)
        
        # Boolean if diffuse reflected
        diffused = record['step'+str(n)]['status']['diffusereflect'][0][dex] or shiftDex == n-1

        # Boolean if stopped
        stopped = record['step'+str(n)]['status']['stopped'][0][dex]

        # Check if diffuse reflected
        if diffused and not stopped:
            diffuse = np.append(diffuse, n-1)
        
        # Check if specularly reflected
        if record['step'+str(n)]['status']['specularreflect'][0][dex] and not diffused:
            spec = np.append(spec, n-1)
        
        n += 1

    if not shifted:
        shiftDex = len(xPos)

    # Make plot
    plt.figure(i)
    ax = plt.axes(projection='3d')

    # Unshifted lines
    ax.plot(xPos[0:shiftDex+1], yPos[0:shiftDex+1], zPos[0:shiftDex+1], marker='.', ls='-',
            color='m', markerfacecolor=stopColor, markeredgecolor='r')
    
    # Shifted lines
    ax.plot(xPos[shiftDex:], yPos[shiftDex:], zPos[shiftDex:], marker='.', ls='-',
            color='b', markerfacecolor=stopColor, markeredgewidth=0.0)

    # Check if signal registered and color in accordingly
    if photons[i] in signal['photon'][0].toarray():
        ax.plot(xPos[-1], yPos[-1], zPos[-1], marker='.', color=signalColor)

    # Color in scattering points
    for sc in scatter:
        sc = round(sc)
        ax.plot(xPos[sc], yPos[sc], zPos[sc], marker='.', color=scatterColor)

    # Color in absorption into medium points
    for ab in absorb:
        ab = round(ab)
        ax.plot(xPos[ab], yPos[ab], zPos[ab], marker='.', color=absorbColor)

    # Color in diffuse reflection points
    for df in diffuse:
        df = round(df)
        ax.plot(xPos[df], yPos[df], zPos[df], marker='.', color=diffuseReColor)
    
    # Color in specular reflection points
    for sp in spec:
        sp = round(sp)
        ax.plot(xPos[sp], yPos[sp], zPos[sp], marker='.', color=specularReColor)

    # Plot settings
    ax.set_title('photon number ' + str(photons[i]))
    ax.set_xlim(-1*tpcWidth/2, tpcWidth/2)
    ax.set_ylim(-1*tpcWidth/2, tpcWidth/2)
    ax.set_zlim(0, tpcHeight)
    ax.set_xlabel('X')

    # Add point labels
    for j in range(len(xPos)):
        ax.text(xPos[j], yPos[j], zPos[j], str(j))
    
    plt.show()