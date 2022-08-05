import numpy as np

folder = './Reflect0Data'     # Directory where files are saved
photon = 2     # Photon whose information is desired
step = 1     # Event number of the photon

record = np.load(folder + '/records.npy', allow_pickle='TRUE').item()

dex = record['step'+str(step+1)]['status']['photon'][0].toarray().index(photon)
for key in record['step'+str(step+1)]['status']:
    print(key, record['step'+str(step+1)]['status'][key][0][dex])