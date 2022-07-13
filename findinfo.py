import numpy as np

record = np.load('./ContPhotonData/records.npy', allow_pickle='TRUE').item()

step = 2
photon = 35

dex = record['step'+str(step)]['status']['photon'][0].toarray().index(photon)
for key in record['step'+str(step)]['status']:
    print(key, record['step'+str(step)]['status'][key][0][dex])