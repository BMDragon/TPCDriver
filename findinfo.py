import numpy as np

record = np.load('./Data/records.npy', allow_pickle='TRUE').item()

step = 6
photon = 6

dex = record['step'+str(step)]['status']['photon'][0].toarray().index(photon)
for key in record['step'+str(step)]['status']:
    print(key, record['step'+str(step)]['status'][key][0][dex])