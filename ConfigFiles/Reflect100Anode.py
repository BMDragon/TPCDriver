# Created by script on 8/8/2022
import Driver
import math

## File paths ##
saveFolder = 'Reflect100AnodeData'     # Folder where to save the data
saveOptions = 3     # 0 - do not save anything, 1 - save record, 
                 # 2 - save record and signals, 3 - save record, signals, and stats

## Define chamber parameters ##
height = 0.05     # Distance in m from cathode to anode
width = 0.05     # Width of the TPC in m
wallShiftEfficiency = 0.0     # Rate of waveshifting at wall
sipmShiftEfficiency = 0.0     # Rate of waveshifting at SiPM
anodeShiftEfficiency = 0.0     # Rate of waveshifting at anode

## Define detector conditions and materials ##
detectorType = 'box'     # General shape of TPC
numSides = 4     # If type is polygonal, how many wall faces will it have (else does not matter)
layerName = 'cell'     # Name for the layer (legacy from Tom's MATLAB code)
isLayerCone = False     # Does the layer have a conical shape
medium = 'Ar'     # Liquid inside the TPC
mediumState = 'liquid'     # State of matter for this layer
temperature = 87.     # Temperature of the TPC

layerWall = 'vikuitilar'     # Material used on the walls of the TPC
wallShiftType = 1     # 1 = uniform efficiency, 2 = linear z-graded efficiency

## Medium information ##
scatterLengthUV = math.inf     # Scattering length for the unshifted light (m)
scatterLengthShift = math.inf     # Scattering length for the shifted light
absorptionLengthUV = math.inf     # Absorption length for the unshifted light
absorptionLengthShift = math.inf     # Absorption length for the shifted light

## SiPM information ##
sipmArrangement = 'simplesquare'     # Arrangement of SiPMs to use
sipmQeUV = 0.0     # Quantum efficiency of the SiPMs for UV (unshifted) light
sipmQeVis = 0.0     # Quantum efficiency of the SiPMs for visible (shifted) light
sipmSize = 5/100     # Size of the SiPMs themselves
sipmGapSize = 0.     # Distance between SiPMs in the array
sipmMaterial = 'si'     # Material of the SiPMs
gapMaterial = 'si'     # Material of the gaps

## Anode information ##
anodeType = 'plate'     # Type of surface at the anode
anodeMaterial = 'black'     # Material of the surface at the anode

## Sampling stats ##
tracks = {     # Start and end points for tracks in the TPC in (x, y, z)
    'track' : [(0., 0., 0.5*height, 0.), (0., 0., 0.5*height-0.01)]     # Units of meters and seconds
}
angleMode = 'random'     # Mode of specifying initial angle
theta = 1.0     # Initial photon theta
phi = 1.0     # Initial photon phi
numPhotonsScale = 10     # Scale the amount of photons to make computation time faster

## Overwriting material properties ##
overwrite = True     # False for default properties, True to change anything
overwriteProperties = {     # See README.md for list of properties and available modifications
    'vikuitilar' : {'reflectivity' : {0 : 1.0, 1 : 1.0},
                    'diffusefraction' : {0 : 0.95, 1 : 0.95}},
    'si' : {'reflectivity' : {0 : 0.0, 1 : 0.0},
            'diffusefraction' : {0 : 1.0, 1 : 1.0}},
    'black' : {'reflectivity' : {0 : 1.0, 1 : 1.0},
            'diffusefraction' : {0 : 0.95, 1 : 0.95}}
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
