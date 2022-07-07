# Created by Brandon Weiss on 7/7/2022
import numpy as np
import matplotlib.pyplot as plt

signals = np.load('./Data/signals.npy', allow_pickle='TRUE').item()
plt.figure(1)
plt.yscale('log')
plt.ylabel('number of photons')
plt.xlabel('time (s)')
plt.hist(signals['time'][0], 50)
plt.show()