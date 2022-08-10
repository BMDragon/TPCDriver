# Created by Brandon Weiss on 8/8/2022
import numpy as np
import matlab as lab

testName = 'Reflect30'

record = np.load('./' + testName + 'Data/records.npy', allow_pickle='TRUE').item()

# Test if all photons stop in step 2 (first contact with a surface) #
def testReflect0():
    numStopped = sum(record['step2']['status']['stopped'][0])
    check = numStopped == len(record['step1']['status']['stopped'][0])
    if check:
        print("\033[1;32m Reflect0 passes!\033[1;0m")
    else:
        print("\033[1;31m Reflect0 doesn't pass\033[1;0m")

if testName == 'Reflect0':
    testReflect0()

# Test if 70% of the photons were absorbed in step 2 at the anode  #
# And the the other 30% absorbed in step 3 at a wall               #
def testReflect30():
    numStopTop = 0
    numStopWall = 0
    for ii in range(len(record['step2']['status']['stopped'][0])):
        if record['step2']['status']['stopped'][0][ii] and \
           record['step2']['status']['detectortop'][0][ii]:
            numStopTop += 1
    for ii in range(len(record['step3']['status']['stopped'][0])):
        if record['step3']['status']['stopped'][0][ii] and \
           record['step3']['status']['wall'][0][ii]:
            numStopWall += 1
    total = len(record['step1']['status']['photon'][0])
    percentTop = numStopTop*100/total
    percentWall = numStopWall*100/total
    check = (69.9 < percentTop < 70.1) and (29.9 < percentWall < 30.1)
    if check:
        print("\033[1;32m Reflect30 passes!\033[1;0m")
    else:
        print("\033[1;31m Reflect30 doesn't pass\033[1;0m")

if testName == 'Reflect30':
    testReflect30()

# Test if all photons die at the anode #
def testReflect100():
    runningSum = 0
    for ii in range(len(record.keys())-1):
        if type(record['step'+str(ii+2)]['status']['stopped']) is lab.logical:
            for jj in range(len(record['step'+str(ii+2)]['status']['stopped'][0])):
                if record['step'+str(ii+2)]['status']['stopped'][0][jj] and \
                   record['step'+str(ii+2)]['status']['detectortop'][0][jj]:
                    runningSum += 1
        else:
            if record['step'+str(ii+2)]['status']['stopped'] and \
               record['step'+str(ii+2)]['status']['detectortop']:
                runningSum += 1
    check = runningSum == len(record['step1']['status']['photon'][0])
    if check:
        print("\033[1;32m Reflect100 passes!\033[1;0m")
    else:
        print("\033[1;31m Reflect100 doesn't pass\033[1;0m")

if testName == 'Reflect100':
    testReflect100()

# Test if all photons die at the cathode #
def testReflect100Anode():
    runningSum = 0
    for ii in range(len(record.keys())-1):
        if type(record['step'+str(ii+2)]['status']['stopped']) is lab.logical:
            for jj in range(len(record['step'+str(ii+2)]['status']['stopped'][0])):
                if record['step'+str(ii+2)]['status']['stopped'][0][jj] and \
                   record['step'+str(ii+2)]['status']['detectorbottom'][0][jj]:
                    runningSum += 1
        else:
            if record['step'+str(ii+2)]['status']['stopped'] and \
               record['step'+str(ii+2)]['status']['detectorbottom']:
                runningSum += 1
    check = runningSum == len(record['step1']['status']['photon'][0])
    if check:
        print("\033[1;32m Reflect100Anode passes!\033[1;0m")
    else:
        print("\033[1;31m Reflect100Anode doesn't pass\033[1;0m")

if testName == 'Reflect100Anode':
    testReflect100Anode()