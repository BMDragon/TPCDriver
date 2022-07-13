# Created by Brandon Weiss on 7/13/2022
import numpy as np
import matlab.engine as gin


## File paths ##
dataPath = '../LeRubik/'     # Path location to where you have the matlab code saved
savePath = './ContPhotonData/'     # Path to where to save data
saveData = 3     # 0 - do not save anything, 1 - save stats, 
                 # 2 - save stats and signals, 3 - save stats, signals, and record

## Define chamber parameters ##
height = 0.05     # Distance in m from cathode to anode
width = 0.05     # Width of the TPC in m
wallShiftEfficiency = 0.8     # Rate of waveshifting at wall
sipmShiftEfficiency = 0.9     # Rate of waveshifting at SiPM
plateShiftEfficiency = 0.3     # Rate of waveshifting at plate

import Detectors.LArTPCBox as geo     # import geometry file as geo

## Define materials ##
temperature = 87.     # Temperature of medium
medium = 'Ar'     # Liquid inside the TPC

## Sampling stats ##
numPhotons = 100000     # Number of photons to simulate
angleMode = 'controlled'     # Mode of specifying initial angle
theta = 0.     # Initial photon theta
phi = .1     # Initial photon phi
x = (0., 0.5*height, 0.)     # Cylindrical coordinates of sampling point (r, z, phi)

## Overwriting material properties ##
overwrite = False     # False for default properties, True to change anything
owProperties = {
    'si' : {'reflectivity' : 0.01},
    'vikuitilar' : {'reflectivity' : 0.99}
}

# DO NOT MAKE CHANGES BELOW #
################################################################

eng = gin.start_matlab()
eng.clear(nargout=0)
eng.addpath(eng.genpath(dataPath))

detector = {}; sampling = {}; materials = {}; parameters = {}; pos = {}

parameters['height'] = height
parameters['width'] = width
parameters['wallshiftefficiency'] = wallShiftEfficiency
parameters['sipmshiftefficiency'] = sipmShiftEfficiency
parameters['plateshiftefficiency'] = plateShiftEfficiency
eng.workspace['parameters'] = parameters

materials['temperature'] = temperature
materials['fluid'] = medium

detector['materials'] = eng.DefaultMaterials(materials)
if overwrite:
    for key, value in owProperties.items():
        for k2, v2 in value.items():
            dex = round(detector['materials']['surfaces']['indices'][key])-1
            detector['materials']['surfaces'][k2][1][dex] = v2

detector['geometry'] = geo.design(parameters, eng)
detector = eng.ConstructDetector(detector)
eng.workspace['detector'] = detector

sampling['points'] = {'numphotons' : numPhotons}
sampling['angle'] = {'mode' : angleMode}
sampling['angle']['theta'] = theta
sampling['angle']['phi'] = phi

pos['r'] = x[0]
pos['z'] = x[1]
pos['omega'] = x[2]

s = eng.InitializePhotons(pos, sampling['angle'], numPhotons, detector)

stats, signal, fullRecord = eng.PhotonFollower(s, detector, 1, nargout=3)

# Function for saving the data files
def saveFiles(case=0):
    if case > 0:
        np.save(savePath + 'stats', stats)
    if case > 1:
        np.save(savePath + 'signals', signal)
    if case > 2:
        np.save(savePath + 'records', fullRecord)

saveFiles(saveData)

eng.quit()