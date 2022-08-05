# Created by Brandon Weiss on 7/7/2022
import numpy as np
import matplotlib.pyplot as plt

folder = './DriverData'     # Directory where files are saved
numBins = 500     # Number of bins in the histogram
pltLimit = 3.5e-6     # Upper limit on the time for the histogram plot

signals = np.load(folder + '/signals.npy', allow_pickle='TRUE').item()
stats = np.load(folder + '/stats.npy', allow_pickle='TRUE').item()

photonDex = 0
numTracks = signals['trackorigins'][-1]
numSignals = len(signals['photon'][0])
histArray = []
for i in range(numTracks+1):
    tempArray = np.array([])
    while photonDex < numSignals and signals['trackorigins'][photonDex] == i:
        if signals['time'][0][photonDex] <= pltLimit:
            tempArray = np.append(tempArray, signals['time'][0][photonDex]*1e9)
        photonDex += 1
    histArray.append(tempArray)

plt.rcParams.update({'font.size': 8})
fig, ax = plt.subplots(dpi=200)
fig.set_size_inches(6,4.5)
hist, bins, patches = ax.hist(histArray, bins=numBins, color=('blue', 'red'), stacked=True)
ax.grid(alpha=0.7)
ax.set_axisbelow(True)
ax.set_yscale('log')
ax.set_ylabel('number of photons')
ax.set_xlabel('photon detection time (ns), binsize = ' + str(round((bins[1]-bins[0]), 5)) + ' ns')
ax.set_title('Time of photon detection by the SiPMs')
ax.legend(signals['tracknames'])

print(len(signals['photon'][0]))
print(stats['numphotons'])
plt.show()