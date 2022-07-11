# Created by Brandon Weiss on 7/11/2022

filename = 'LArTPCCell'

file = open('./Detectors/' + filename + '.py', 'w')
file.write('''\
# Created by script on [INSERT CREATION DATE HERE]

type =      # from type list
# numSides = 
layerName =      # Name of layer
isLayerCone =      # True or False
layerMedium =      # liquid or gas
layerWall =      # Material of the walls
wallShiftType =      # 1 = uniform efficiency, 2 = linear z-graded efficiency

sipmArrangement =      # from sipm geometries list
anodeType =      # from anode type list
anodeMaterial =      # Material of the anode

def design(parameters, eng):
    geometry = {}; sipmplane = {}

    geometry['type'] = type
    # geometry['numpanels'] = numSides
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
''')

print('done?')