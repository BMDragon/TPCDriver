# Created by script on 8/10/2022
import Driver

## File paths ##
saveFolder = 'PhysicsRunBase'     # Folder where to save the data
saveOptions = 3     # 0 - do not save anything, 1 - save record, 
                 # 2 - save record and signals, 3 - save record, signals, and stats

## Define chamber parameters ##
height = 0.3     # Distance in m from cathode to anode
width = 0.3     # Width of the TPC in m
wallShiftEfficiency = 0.0     # Rate of waveshifting at wall
sipmShiftEfficiency = 0.5     # Rate of waveshifting at SiPM
anodeShiftEfficiency = 0.0     # Rate of waveshifting at anode

## Define detector conditions and materials ##
detectorType = 'box'     # General shape of TPC
numSides = 4     # If type is polygonal, how many wall faces will it have (else does not matter)
layerName = 'cell'     # Name for the layer (legacy from Tom's MATLAB code)
isLayerCone = False     # Does the layer have a conical shape
medium = 'Ar'     # Liquid inside the TPC
mediumState = 'liquid'     # State of matter for this layer
temperature = 87.     # Temperature of the TPC

layerWall = 'black'     # Material used on the walls of the TPC
wallShiftType = 1     # 1 = uniform efficiency, 2 = linear z-graded efficiency

## Medium information ##
scatterLengthUV = 0.95     # Scattering length for the unshifted light (m)
scatterLengthShift = 1.0 #TODO    # Scattering length for the shifted light
absorptionLengthUV = 2.0     # Absorption length for the unshifted light
absorptionLengthShift = 2.0 #TODO     # Absorption length for the shifted light

## SiPM information ##
sipmArrangement = 'simplesquare'     # Arrangement of SiPMs to use
sipmQeUV = 0.0     # Quantum efficiency of the SiPMs for UV (unshifted) light
sipmQeVis = 0.4 #TODO    # Quantum efficiency of the SiPMs for visible (shifted) light
# Hamamatsu Vis-IR SiPM; does it include the reflective properties?
sipmSize = 3./1000     # Size of the SiPMs themselves
sipmGapSize = 0.125/1000     # Distance between SiPMs in the array
sipmMaterial = 'si'     # Material of the SiPMs
gapMaterial = 'black'     # Material of the gaps

## Anode information ##
anodeType = 'plate'     # Type of surface at the anode
anodeMaterial = 'black'     # Material of the surface at the anode

## Sampling stats ##
tracks = {     # Start and end points for tracks in the TPC in (x, y, z)
    '' : [(), ()]     # Units of meters and seconds
}
angleMode = 'random'     # Mode of specifying initial angle
theta = 0.0     # Initial photon theta
phi = 0.0     # Initial photon phi
numPhotonsScale = 1.0     # Scale the amount of photons to make computation time faster

## Overwriting material properties ##
overwrite = False     # False for default properties, True to change anything
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
