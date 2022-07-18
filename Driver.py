# Created by Brandon Weiss on 7/7/2022
import numpy as np
import matlab.engine as gin
import matlab as lab


## File paths ##
dataPath = '../LeRubik/'     # Path location to where you have the matlab code saved
savePath = './DriverData/'     # Path to where to save data
saveData = 3     # 0 - do not save anything, 1 - save stats, 
                 # 2 - save stats and signals, 3 - save stats, signals, and record

## Define chamber parameters ##
height = 0.05     # Distance in m from cathode to anode
width = 0.05     # Width of the TPC in m
wallShiftEfficiency = 0.5     # Rate of waveshifting at wall
sipmShiftEfficiency = 0.9     # Rate of waveshifting at SiPM
plateShiftEfficiency = 0.     # Rate of waveshifting at plate

import Detectors.LArTPCBox as geo     # import geometry file as geo

## Define materials ##
temperature = 87.     # Temperature of medium
medium = 'Ar'     # Liquid inside the TPC

## Sampling stats ##
numPhotons = 100000     # Total number of photons to simulate
tracks = {'track0' : [(0., 0., 0.01), (0., 0., 0.0499)],     # Start and end points for tracks in the TPC in (x, y, z)
          'track1' : [(0.01, -0.02, 0.02), (0.01, 0.025, 0.03)]}
angleMode = 'random'     # Mode of specifying initial angle

## Overwriting material properties ##
overwrite = False     # False for default properties, True to change anything
owProperties = {
    'si' : {'reflectivity' : 0.01},
    'vikuitilar' : {'reflectivity' : 0.99}
}

# DO NOT MAKE CHANGES BELOW #
################################################################

# Start matlab engine and add path
eng = gin.start_matlab()
eng.clear(nargout=0)
eng.addpath(eng.genpath(dataPath))

# Define dictionaries needed to pass into matlab
detector = {}; sampling = {}; materials = {}; parameters = {}; pos = {}

# Set detector parameters
parameters['height'] = height
parameters['width'] = width
parameters['wallshiftefficiency'] = wallShiftEfficiency
parameters['sipmshiftefficiency'] = sipmShiftEfficiency
parameters['plateshiftefficiency'] = plateShiftEfficiency
eng.workspace['parameters'] = parameters

materials['temperature'] = temperature
materials['fluid'] = medium

# Get material properties and overwrite if necessary
detector['materials'] = eng.DefaultMaterials(materials)
if overwrite:
    for key, value in owProperties.items():
        for k2, v2 in value.items():
            dex = round(detector['materials']['surfaces']['indices'][key])-1
            detector['materials']['surfaces'][k2][1][dex] = v2

# Define the shape of the detector and which materials were used
detector['geometry'] = geo.design(parameters, eng)
detector = eng.ConstructDetector(detector)
eng.workspace['detector'] = detector

# Initial photon angle controls
sampling['points'] = {'numphotons' : numPhotons}
sampling['angle'] = {'mode' : angleMode}

# Define the starting positions for each photon
photonsPerTrack = round(numPhotons/len(tracks))
assert photonsPerTrack*len(tracks) == numPhotons, \
    "Please make sure the number of photons is evenly divisible by the number of tracks, Thank you"
r = ([0]*numPhotons, [0]*numPhotons, [0]*numPhotons)
for trDex, trKey in enumerate(tracks):
    xStart = tracks[trKey][0][0]
    xEnd = tracks[trKey][1][0]
    yStart = tracks[trKey][0][1]
    yEnd = tracks[trKey][1][1]
    zStart = tracks[trKey][0][2]
    zEnd = tracks[trKey][1][2]
    r[0][trDex*photonsPerTrack:(trDex+1)*photonsPerTrack] = \
        [xx*(xEnd-xStart)/photonsPerTrack+xStart for xx in range(photonsPerTrack)]
    r[1][trDex*photonsPerTrack:(trDex+1)*photonsPerTrack] = \
        [yy*(yEnd-yStart)/photonsPerTrack+yStart for yy in range(photonsPerTrack)]
    r[2][trDex*photonsPerTrack:(trDex+1)*photonsPerTrack] = \
        [zz*(zEnd-zStart)/photonsPerTrack+zStart for zz in range(photonsPerTrack)]

pos['x'] = lab.double(r[0])
pos['y'] = lab.double(r[1])
pos['z'] = lab.double(r[2])

# Initialize and run the simulations
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

# Close the matlab engine
eng.quit()