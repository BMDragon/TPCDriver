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
height = 0.3     # Distance in m from cathode to anode
width = 0.3     # Width of the TPC in m
wallShiftEfficiency = 0.5     # Rate of waveshifting at wall
sipmShiftEfficiency = 0.9     # Rate of waveshifting at SiPM
plateShiftEfficiency = 0.     # Rate of waveshifting at plate

import Detectors.LArTPCBox as geo     # import geometry file as geo

## Define materials ##
temperature = 87.     # Temperature of medium
medium = 'Ar'     # Liquid inside the TPC

## Sampling stats ##
tracks = {'track0' : [(-0.1, 0.15, 0.23, 0.), (-0.1, -0.13, 0.3)]}#,     # Start and end points for tracks in the TPC in (x, y, z, t)
          #'track1' : [(0.1, -0.15, 0.1, 1e-9), (0.1, 0.15, 0.05)]}     # Units of meters and seconds
angleMode = 'random'     # Mode of specifying initial angle
# theta = 0.1     # Initial photon theta
# phi = 0.1     # Initial photon phi

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

# Function for finding track lengths
def trackLength(path):
    xDiff = path[1][0]-path[0][0]
    yDiff = path[1][1]-path[0][1]
    zDiff = path[1][2]-path[0][2]
    return np.sqrt(xDiff**2 + yDiff**2 + zDiff**2)

# Sum lengths to determine photon distribution
photonsPerMeV = 20000
MeVPerCM = 2.2
photonsPerMeter = photonsPerMeV * MeVPerCM * 100
particleSpeed = 299792457
photonDistro = np.array([], dtype=int)
endTimes = np.array([])
for trDex, trKey in enumerate(tracks):
    tempLength = trackLength(tracks[trKey])
    endTimes = np.append(endTimes, tempLength/particleSpeed)
    photonDistro = np.append(photonDistro, round(tempLength*photonsPerMeter))
numPhotons = round(np.sum(photonDistro))

# Define the starting positions for each photon and assert that it is valid
r = ([0]*numPhotons, [0]*numPhotons, [0]*numPhotons)
runningSum = 0
for trDex, trKey in enumerate(tracks):
    xStart = tracks[trKey][0][0]
    xEnd = tracks[trKey][1][0]
    yStart = tracks[trKey][0][1]
    yEnd = tracks[trKey][1][1]
    zStart = tracks[trKey][0][2]
    zEnd = tracks[trKey][1][2]

    xBounds = (-0.5*width <= xStart <= 0.5*width) and (-0.5*width <= xEnd <= 0.5*width)
    yBounds = (-0.5*width <= yStart <= 0.5*width) and (-0.5*width <= yEnd <= 0.5*width)
    zBounds = (0.0 <= zStart <= height) and (0.0 <= zEnd <= height)
    assert xBounds and yBounds and zBounds, \
        "Please make sure your track boundaries are contained in the TPC"

    amount = photonDistro[trDex]
    r[0][runningSum:runningSum+amount] = [xx*(xEnd-xStart)/amount+xStart for xx in range(amount)]
    r[1][runningSum:runningSum+amount] = [yy*(yEnd-yStart)/amount+yStart for yy in range(amount)]
    r[2][runningSum:runningSum+amount] = [zz*(zEnd-zStart)/amount+zStart for zz in range(amount)]
    runningSum += amount

pos['x'] = lab.double(r[0])
pos['y'] = lab.double(r[1])
pos['z'] = lab.double(r[2])

# Initial photon angle controls
sampling['points'] = {'numphotons' : numPhotons}
sampling['angle'] = {'mode' : angleMode}

# Initialize and run the simulations
s = eng.InitializePhotons(pos, sampling['angle'], numPhotons, detector)

stats, signal, fullRecord = eng.PhotonFollower(s, detector, 1, nargout=3)

# Implement scintillation time delays
alpha = 0.3
shortTau = 1e-9
longTau = 1.6e-6
randSeed = 314
rng = np.random.default_rng(randSeed)

# Keep track of photon origin in signal
signal['tracknames'] = list(tracks.keys())

# Add the time delays to the dataset
startDex = 0
trackDex = 0
runningSum2 = photonDistro[0]
trackOrigin = np.array([], dtype=int)
for gamma in range(len(signal['photon'][0])):
    gDex = signal['photon'][0][gamma]-1
    if runningSum2 < gDex:
        startDex += photonDistro[trackDex]
        trackDex += 1
        runningSum2 += photonDistro[trackDex]

    trackKey = list(tracks.keys())[trackDex]
    tStart = tracks[trackKey][0][3]
    tEnd = endTimes[trackDex]
    timeStamp = (gDex-startDex)*(tStart-tEnd)/photonDistro[trackDex] + tStart
    if rng.random() < alpha:
        timeStamp += np.random.exponential(shortTau)
    else:
        timeStamp += np.random.exponential(longTau)
    signal['time'][0][gamma] += timeStamp
    trackOrigin = np.append(trackOrigin, trackDex)
signal['trackorigins'] = trackOrigin

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