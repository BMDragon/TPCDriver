# Created by Brandon Weiss on 7/11/2022

type = 'box'
# numSides = 4
layerName = 'cell'
isLayerCone = False
layerMedium = 'liquid'
layerWall = 'vikuitilar'
wallShiftType = 1     # 1 = uniform efficiency, 2 = linear z-graded efficiency

sipmArrangement = 'simplesquare'
anodeType = 'plate'
anodeMaterial = 'black'

def LArTPCBox(parameters, eng):
    geometry = {}; sipmplane = {}

    geometry['type'] = type
    geometry['layername'] = [layerName]
    geometry['cone'] = isLayerCone
    geometry['medium'] = [layerMedium]
    geometry['dx'] = parameters['width']
    geometry['dy'] = parameters['width']
    geometry['dz'] = parameters['height']
    geometry['wall'] = [layerWall]
    geometry['shift'] = {'wall' : {'type' : wallShiftType}}
    geometry['shift']['wall']['efficiency'] = parameters['wallshiftefficiency']

    sipmplane['name'] = sipmArrangement
    sipmplane['width'] = parameters['width']
    geometry['readout'] = {'bottom' : eng.DefineSiPMPlane(sipmplane)}
    geometry['shift']['readout'] = {'bottom' : {'array' : 
                                   {'efficiency' : parameters['sipmshiftefficiency']}}}
    
    geometry['readout']['top'] = {'type' : anodeType}
    geometry['readout']['top']['surface'] = {'plate' : anodeMaterial}
    geometry['shift']['readout']['top'] = {'plate' : 
                                          {'efficiency' : parameters['plateshiftefficiency']}}
    
    return geometry