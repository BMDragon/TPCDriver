import numpy as np

record = np.load('./Data/records.npy', allow_pickle='TRUE').item()

for key in record['step3']['status']:
    print(key, record['step3']['status'][key][0][0])