# Created by Brandon Weiss on 7/7/2022
import numpy as np
import matlab.engine as gin
import matlab as lab

dataPath = '../LeRubik/'     # Path location to where you have the matlab code saved

def Drive(config):
    # Make sure config is a dictionary
    assert type(config) is dict, \
        "Invalid input, make sure the parameter for Driver.Drive() is a dictionary"

    # Function to assert that the key exists in config
    keys = config.keys()
    def checkKey(keyVal):
        assert keyVal in keys, \
            "Please make sure config has the field " + keyVal

    ## File paths ##
    checkKey('savefolder')
    savePath = './' + config['savefolder'] + '/'
    checkKey('saveoptions')
    saveData = config['saveoptions']

    ## Define chamber parameters ##
    checkKey('height')
    height = config['height']
    checkKey('width')
    width = config['width']
    checkKey('wallshiftefficiency')
    wallShiftEfficiency = config['wallshiftefficiency']
    checkKey('sipmshiftefficiency')
    sipmShiftEfficiency = config['sipmshiftefficiency']
    checkKey('anodeshiftefficiency')
    anodeShiftEfficiency = config['anodeshiftefficiency']

    ## Define detector conditions and materials ##
    checkKey('detectortype')
    detectorType = config['detectortype']
    if detectorType == 'polygonal':
        checkKey('numsides')
        numSides = config['numsides']
    checkKey('layername')
    layerName = config['layername']
    checkKey('islayercone')
    isLayerCone = config['islayercone']
    checkKey('medium')
    medium = config['medium']
    checkKey('mediumstate')
    mediumState = config['mediumstate']
    checkKey('temperature')
    temperature = config['temperature']

    checkKey('layerwall')
    layerWall = config['layerwall']
    checkKey('wallshifttype')
    wallShiftType = config['wallshifttype']

    ## Medium information ##
    checkKey('scatterunshifted')
    scatterLengthUV = config['scatterunshifted']
    checkKey('scattershifted')
    scatterLengthShift = config['scattershifted']
    checkKey('absorbunshifted')
    absorptionLengthUV = config['absorbunshifted']
    checkKey('absorbshifted')
    absorptionLengthShift = config['absorbshifted']

    ## SiPM information ##
    checkKey('sipmarrangement')
    sipmArrangement = config['sipmarrangement']
    checkKey('sipmqeuv')
    sipmQeUV = config['sipmqeuv']
    checkKey('sipmqevis')
    sipmQeVis = config['sipmqevis']
    checkKey('sipmsize')
    sipmSize = config['sipmsize']
    checkKey('sipmgapsize')
    sipmGapSize = config['sipmgapsize']
    checkKey('sipmmaterial')
    sipmMaterial = config['sipmmaterial']
    checkKey('gapmaterial')
    gapMaterial = config['gapmaterial']

    ## Anode information ##
    checkKey('anodetype')
    anodeType = config['anodetype']
    checkKey('anodematerial')
    anodeMaterial = config['anodematerial']

    ## Sampling stats ##
    checkKey('tracks')
    tracks = config['tracks']
    checkKey('anglemode')
    angleMode = config['anglemode']
    if angleMode == 'controlled':
        checkKey('theta')
        theta = config['theta']
        checkKey('phi')
        phi = config['phi']
    checkKey('numphotonsscale')
    numPhotonsScale = config['numphotonsscale']

    ## Overwriting material properties ##
    checkKey('overwrite')
    overwrite = config['overwrite']
    checkKey('owproperties')
    owProperties = config['owproperties']

    # Start Processing #
    ################################################################

    # Start matlab engine and add path
    print("Starting MATLAB engine")
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
    parameters['plateshiftefficiency'] = anodeShiftEfficiency
    eng.workspace['parameters'] = parameters

    materials['temperature'] = temperature
    materials['fluid'] = medium

    # Get material properties and overwrite if necessary
    detector['materials'] = eng.DefaultMaterials(materials)
    detector['materials']['media']['scatterlength'][0][0] = scatterLengthUV
    detector['materials']['media']['scatterlength'][0][1] = scatterLengthShift
    detector['materials']['media']['absorptionlength'][0][0] = absorptionLengthUV
    detector['materials']['media']['absorptionlength'][0][1] = absorptionLengthShift
    if overwrite:
        for key, value in owProperties.items():
            dex = round(detector['materials']['surfaces']['indices'][key])-1
            for k2, v2 in value.items():
                for row in list(v2.keys()):
                    detector['materials']['surfaces'][k2][row][dex] = v2[row]

    # Define the shape of the detector and which materials were used
    geometry = {}; sipmplane = {}

    geometry['type'] = detectorType
    # geometry['numpanels'] = numSides
    geometry['layername'] = [layerName]
    geometry['cone'] = isLayerCone
    geometry['medium'] = [mediumState]
    geometry['dx'] = parameters['width']
    geometry['dy'] = parameters['width']
    geometry['dz'] = parameters['height']
    geometry['wall'] = [layerWall]
    geometry['shift'] = {'wall' : {'type' : wallShiftType}}
    geometry['shift']['wall']['efficiency'] = parameters['wallshiftefficiency']

    # Define the SiPM and its parameters
    sipmplane['name'] = sipmArrangement
    sipmplane['width'] = parameters['width']
    sipmplane['array'] = {'qe' : lab.double([sipmQeUV, sipmQeVis])}
    sipmplane['d'] = {'array' : sipmSize}
    sipmplane['edge_gap'] = sipmGapSize
    sipmplane['surface'] = {'array' : sipmMaterial}
    sipmplane['surface']['gap'] = gapMaterial
    geometry['readout'] = {'bottom' : eng.DefineSiPMPlane2(sipmplane)}
    geometry['shift']['readout'] = {'bottom' : {'array' : 
                                   {'efficiency' : parameters['sipmshiftefficiency']}}}
    
    # Define the anode and its parameters
    geometry['readout']['top'] = {'type' : anodeType}
    geometry['readout']['top']['surface'] = {'plate' : anodeMaterial}
    geometry['shift']['readout']['top'] = {'plate' : 
                                          {'efficiency' : parameters['plateshiftefficiency']}}
    
    # Get the rest of the geometry from matlab
    detector['geometry'] = geometry
    detector = eng.ConstructDetector(detector)
    eng.workspace['detector'] = detector

    # Function for finding track lengths
    def trackLength(path):
        xDiff = path[1][0]-path[0][0]
        yDiff = path[1][1]-path[0][1]
        zDiff = path[1][2]-path[0][2]
        return np.sqrt(xDiff**2 + yDiff**2 + zDiff**2)

    # Sum lengths to determine photon distribution
    photonsPerMeV = 20000 * numPhotonsScale
    MeVPerCM = 2.2
    photonsPerMeter = photonsPerMeV * MeVPerCM * 100
    particleSpeed = 299792457
    photonDistro = np.array([], dtype=int)
    endTimes = np.array([])
    for trDex, trKey in enumerate(tracks):
        tempLength = trackLength(tracks[trKey])
        endTimes = np.append(endTimes, tempLength/particleSpeed + tracks[trKey][0][3])
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
    if angleMode == 'controlled':
        sampling['angle']['theta'] = theta
        sampling['angle']['phi'] = phi

    # Initialize and run the simulations
    s = eng.InitializePhotons(pos, sampling['angle'], numPhotons, detector)

    print('Simulating photons')
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

    print("Saving files")
    saveFiles(saveData)

    # Close the matlab engine
    print("Closing MATLAB engine")
    eng.quit()