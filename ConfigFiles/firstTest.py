# Created by Brandon Weiss on 7/22/2022
import Driver

## File paths ##
saveFolder = 'DriverData'     # Folder where to save the data
saveOptions = 2     # 0 - do not save anything, 1 - save record, 
                 # 2 - save record and signals, 3 - save record, signals, and stats

## Define chamber parameters ##
height = 0.3     # Distance in m from cathode to anode
width = 0.3     # Width of the TPC in m
wallShiftEfficiency = 0.5     # Rate of waveshifting at wall
sipmShiftEfficiency = 0.9     # Rate of waveshifting at SiPM
anodeShiftEfficiency = 0.9     # Rate of waveshifting at anode

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
scatterLengthUV = 0.66     # Scattering length for the unshifted light (m)
scatterLengthShift = 100     # Scattering length for the shifted light
absorptionLengthUV = 100     # Absorption length for the unshifted light
absorptionLengthShift = 1e5     # Absorption length for the shifted light

## SiPM information ##
sipmArrangement = 'simplesquare'     # Arrangement of SiPMs to use
sipmQeUV = 0.0     # Quantum efficiency of the SiPMs for UV (unshifted) light
sipmQeVis = 0.25     # Quantum efficiency of the SiPMs for visible (shifted) light
sipmSize = 4/1000     # Size of the SiPMs themselves
sipmGapSize = 1/1000     # Distance between SiPMs in the array
sipmMaterial = 'si'     # Material of the SiPMs
gapMaterial = 'black'     # Material of the gaps

## Anode information ##
anodeType = 'plate'     # Type of surface at the anode
anodeMaterial = 'black'     # Material of the surface at the anode

## Sampling stats ##
tracks = {'track0' : [(-0.1, 0.15, 0.23, 0.), (-0.1, -0.13, 0.3)],     # Start and end points for tracks in the TPC in (x, y, z)
          'track1' : [(0.1, -0.15, 0.1, 5e-7), (0.1, 0.15, 0.05)]}     # Units of meters and seconds
angleMode = 'random'     # Mode of specifying initial angle
theta = 0.1     # Initial photon theta
phi = 0.1     # Initial photon phi
numPhotonsScale = 0.1     # Scale the amount of photons to make computation time faster

## Overwriting material properties ##
overwrite = False     # False for default properties, True to change anything
overwriteProperties = {     # See README.md for list of properties and available modifications
    'si' : {'reflectivity' : {0 : 0.01}},
    'vikuitilar' : {'reflectivity' : {1 : 0.99}}
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