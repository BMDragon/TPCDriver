import numpy as np

folder = './DriverData'     # Directory where files are saved
photon = 1     # Photon whose information is desired
step = 0     # Event number of the photon

record = np.load(folder + '/records.npy', allow_pickle='TRUE').item()

dex = record['step'+str(step+1)]['status']['photon'][0].toarray().index(photon)
for key in record['step'+str(step+1)]['status']:
    print(key, record['step'+str(step+1)]['status'][key][0][dex])