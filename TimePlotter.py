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
numIncluded = 0
for i in range(numTracks+1):     # Organize the data into an ndarray based on tracks
    tempArray = np.array([])     # so it can be colored differently
    while photonDex < numSignals and signals['trackorigins'][photonDex] == i:
        if signals['time'][0][photonDex] <= pltLimit:
            tempArray = np.append(tempArray, signals['time'][0][photonDex]*1e9)
        photonDex += 1
    histArray.append(tempArray)
    numIncluded += len(tempArray)

# Plot settings #
plt.rcParams.update({'font.size': 8})
fig, ax = plt.subplots(dpi=200)
fig.set_size_inches(6,4.5)
hist, bins, patches = ax.hist(histArray, bins=numBins, color=('blue', 'red'), stacked=True)
ax.grid(alpha=0.7)
ax.set_axisbelow(True)
ax.set_yscale('log')
ax.set_ylabel('number of photons')
ax.set_xlabel('photon detection time (ns), bin size = ' + str(round((bins[1]-bins[0]), 5)) + ' ns')
plt.suptitle('Time of photon detection by the SiPMs')
ax.set_title('Number of displayed photons = ' + str(numIncluded), fontsize=7)
ax.legend(signals['tracknames'])

print('No. of photons that generated a signal: ' + str(len(signals['photon'][0])))
print('No. of photons included in the histogram: ' + str(numIncluded))
print('No. of photons omitted from the histogram: ' + str(len(signals['photon'][0])-numIncluded))
print('Total no. of photons that were generated: ' + str(stats['numphotons']))
plt.show()