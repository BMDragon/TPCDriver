# Created by Brandon Weiss on 7/26/2022

filename = 'PhysicsRun1'     # Only change this

file = open('./ConfigFiles/' + filename + '.py', 'w')
file.write('''\
# Created by script on [INSERT CREATION DATE HERE]
import Driver

## File paths ##
saveFolder =      # Folder where to save the data
saveOptions =      # 0 - do not save anything, 1 - save record, 
                 # 2 - save record and signals, 3 - save record, signals, and stats

## Define chamber parameters ##
height =      # Distance in m from cathode to anode
width =      # Width of the TPC in m
wallShiftEfficiency =      # Rate of waveshifting at wall
sipmShiftEfficiency =      # Rate of waveshifting at SiPM
anodeShiftEfficiency =      # Rate of waveshifting at anode

## Define detector conditions and materials ##
detectorType = 'box'     # General shape of TPC
numSides = 4     # If type is polygonal, how many wall faces will it have (else does not matter)
layerName = 'cell'     # Name for the layer (legacy from Tom's MATLAB code)
isLayerCone = False     # Does the layer have a conical shape
medium = 'Ar'     # Liquid inside the TPC
mediumState = 'liquid'     # State of matter for this layer
temperature = 87.     # Temperature of the TPC

layerWall =      # Material used on the walls of the TPC
wallShiftType = 1     # 1 = uniform efficiency, 2 = linear z-graded efficiency

## Medium information ##
scatterLengthUV =      # Scattering length for the unshifted light (m)
scatterLengthShift =      # Scattering length for the shifted light
absorptionLengthUV =      # Absorption length for the unshifted light
absorptionLengthShift =      # Absorption length for the shifted light

## SiPM information ##
sipmArrangement = 'simplesquare'     # Arrangement of SiPMs to use
sipmQeUV =      # Quantum efficiency of the SiPMs for UV (unshifted) light
sipmQeVis =      # Quantum efficiency of the SiPMs for visible (shifted) light
sipmSize =      # Size of the SiPMs themselves
sipmGapSize =      # Distance between SiPMs in the array
sipmMaterial =      # Material of the SiPMs
gapMaterial =      # Material of the gaps

## Anode information ##
anodeType = 'plate'     # Type of surface at the anode
anodeMaterial =      # Material of the surface at the anode

## Sampling stats ##
tracks = {     # Start and end points for tracks in the TPC in (x, y, z)
    '' : [(), ()]     # Units of meters and seconds
}
angleMode =      # Mode of specifying initial angle
theta =      # Initial photon theta
phi =      # Initial photon phi
numPhotonsScale =      # Scale the amount of photons to make computation time faster

## Overwriting material properties ##
overwrite =      # False for default properties, True to change anything
overwriteProperties = {     # See README.md for list of properties and available modifications
    
}


## Packaging the information and calling the driver ##
# To add a new parameter, just add it as a new field in the config dictionary
config = {
    'savefolder' : saveFolder,
    'saveoptions': saveOptions,

    'height' : height,
    'width' : width,
    'wallshiftefficiency' : wallShiftEfficiency,
    'sipmshiftefficiency' : sipmShiftEfficiency,
    'anodeshiftefficiency' : anodeShiftEfficiency,

    'detectortype' : detectorType,
    'numsides' : numSides,
    'layername' : layerName,
    'islayercone' : isLayerCone,
    'medium' : medium,
    'mediumstate' : mediumState,
    'temperature' : temperature,
    'layerwall' : layerWall,
    'wallshifttype' : wallShiftType,

    'scatterunshifted' : scatterLengthUV,
    'scattershifted' : scatterLengthShift,
    'absorbunshifted' : absorptionLengthUV,
    'absorbshifted' : absorptionLengthShift,

    'sipmarrangement' : sipmArrangement,
    'sipmqeuv' : sipmQeUV,
    'sipmqevis' : sipmQeVis,
    'sipmsize' : sipmSize,
    'sipmgapsize' : sipmGapSize,
    'sipmmaterial' : sipmMaterial,
    'gapmaterial' : gapMaterial,

    'anodetype' : anodeType,
    'anodematerial' : anodeMaterial,

    'tracks' : tracks,
    'anglemode' : angleMode,
    'theta' : theta,
    'phi' : phi,
    'numphotonsscale' : numPhotonsScale,

    'overwrite' : overwrite,
    'owproperties' : overwriteProperties
}

Driver.Drive(config)
''')

print('Finished making ' + filename +'.py')