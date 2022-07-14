# Created by Brandon Weiss on 7/7/2022
import numpy as np
import matplotlib.pyplot as plt

signals = np.load('./DriverData/signals.npy', allow_pickle='TRUE').item()
plt.figure(1)
plt.yscale('log')
plt.ylabel('number of photons')
plt.xlabel('time (s)')
plt.title('Time from Scintillation Event until Signal Registration')
plt.hist(signals['time'][0], 50)
plt.show()