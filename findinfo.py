import numpy as np

record = np.load('./DriverData/records.npy', allow_pickle='TRUE').item()

step = 1
photon = 1

dex = record['step'+str(step)]['status']['photon'][0].toarray().index(photon)
for key in record['step'+str(step)]['status']:
    print(key, record['step'+str(step)]['status'][key][0][dex])