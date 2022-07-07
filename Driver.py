# Created by Brandon Weiss on 7/7/2022
import numpy as np
import matlab as lab
import matlab.engine as gin

eng = gin.start_matlab()

# Change path location to where you have the matlab code saved
eng.addpath(eng.genpath('../LeRubik/'))

# Define chamber parameters
height = 0.05
width = 0.05
wallShiftEfficiency = 0.8
sipmShiftEfficiency = 0.9
plateShiftEfficiency = 0.9
geometryFile = 'LArTPCCellDefinition'

# Define materials
temperature = 87.
medium = 'Ar'

# Sampling stats
numPhotons = 100000
angleMode = 'random'
r = 0.
z = 0.5*height
phi = 0.

# Overwriting material properties


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

pos['r'] = r
pos['z'] = z
pos['omega'] = phi

s = eng.InitializePhotons(pos, sampling['angle'], numPhotons, detector)

stats, signal = eng.PhotonFollower(s, detector, nargout=2)
print(stats)
print(signal)

eng.quit()