# Created by Brandon Weiss on 7/7/2022
import numpy as np
import matlab as lab
import matlab.engine as gin

eng = gin.start_matlab()

# Change path location to where you have the matlab code saved
eng.addpath(eng.genpath('../LeRubik/'))
savePath = './'     # Path to where to save data
saveData = 2     # 0 - do not save anything, 1 - save stats, 
                 # 2 - save stats and signals, 3 - save stats, signals, and record

## Define chamber parameters ##
height = 0.05     # Height of the TPC
width = 0.05     # Width of the TPC
wallShiftEfficiency = 0.8     # Rate of waveshifting at wall
sipmShiftEfficiency = 0.9     # Rate of waveshifting at SiPM
plateShiftEfficiency = 0.9     # Rate of waveshifting at plate
geometryFile = 'LArTPCCellDefinition'     # Matlab file where the geometry is defined

## Define materials ##
temperature = 87.     # Temperature of medium
medium = 'Ar'     # Liquid inside the TPC

## Sampling stats ##
numPhotons = 100000     # Number of photons to simulate
angleMode = 'random'     # Mode of specifying initial angle
x = (0., 0.5*height, 0.)     # Cylindrical coordinates of sampling point (r, z, phi)

## Overwriting material properties ##
overwrite = True     # False for default properties, True to change anything
owProperties = {
    'si' : {'reflectivity' : 0.1},
    'vikuitilar' : {'reflectivity' : 0.5}
}

# DO NOT MAKE CHANGES BELOW #
################################################################

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
detector['geometry'] = eng.eval(geometryFile + '(parameters)')
detector = eng.ConstructDetector(detector)

sampling['points'] = {'numphotons' : numPhotons}
sampling['angle'] = {'mode' : angleMode}

pos['r'] = x[0]
pos['z'] = x[1]
pos['omega'] = x[2]

s = eng.InitializePhotons(pos, sampling['angle'], numPhotons, detector)

stats, signal = eng.PhotonFollower(s, detector, nargout=2)
print(stats)
print(signal)

eng.quit()