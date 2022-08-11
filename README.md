# TPCDriver
Python driver code for MATLAB TPC simulations

#### By Brandon Weiss

## Setup

First, be sure to have numpy installed. Next, install the MATLAB to python API.

**Installing the API**

Before you install, verify your Python and MATLAB configurations.
- Check that your system has a supported version of Python and MATLAB R2014b or later.
- To check that Python is installed on your system, run ```python``` at the operating system prompt.
- Add the folder that contains the Python interpreter to your path, if it is not already there. (if using MATLAB cmd prompt)
- Find the path to the MATLAB folder. Start MATLAB and type ```matlabroot``` in the command window. Copy the path returned by ```matlabroot```. It will need to be pasted when prompted with ```matlabroot``` below.

To install the engine API, choose one of the following. You must call this python install command in the specified folder.

At a Windows operating system prompt (you will need administrator privileges to execute these commands) —

``` cd "matlabroot\extern\engines\python"```

``` python setup.py install```
    
At a macOS or Linux operating system prompt (you will need administrator privileges to execute these commands) —

``` cd "matlabroot/extern/engines/python"```

``` python setup.py install```
    
At the MATLAB command prompt —

``` cd (fullfile(matlabroot,'extern','engines','python'))```

``` system('python setup.py install')```

Information regarding more details of the MATLAB to python API can be found [here](https://www.mathworks.com/help/matlab/matlab-engine-for-python.html?s_tid=CRUX_topnav).

**Get MATLAB Code**

In order to get the correct version (i.e. compatible) version of Tom Schutt's MATLAB code, please fork and clone the repository [here](https://github.com/BMDragon/LeRubik). It is a private repository, so please email either Brandon Weiss (bmweiss10@gmail.com) or Gianluca Petrillo (petrillo@slac.stanford.edu) to get access.

**Important:** Once you fork and clone this repository, make sure to change the file location on line 6 of ConfigFiles/Driver.py. The new file location should be a path to where the MATLAB code from the previous paragraph is saved. (If you want to use `../`, it seems that the location should be relative to TPCDriver, not ConfigFiles)

## Usage

#### 1. Running simulations
1. ConfigFiles/NewConfig.py\
&ndash; This is a generative script that produces a new configuration file for simulations.\
&ndash; Input: Name of the new configuration file (change on line 3, variable ```filename```).\
&ndash; Output: A blank template configuration file located inside the ConfigFiles folder.\
&ndash; Once a new configuration file is generated, the user must go in and set all the values for the variables in order to use the file correctly.

2. Configuration Files\
&ndash; Within the generated configuration file there should be comments explaining what each variable corresponds to and their "physical meaning." All units should be in mks (standard SI).\
&ndash; If saving files, make sure that a directory is created with a name that accurately reflects what you are simulating. Change the folder name on line 5 to the same name as the desired directory.\
&ndash; There is more information about allowable values in the [Configuration File details](https://github.com/BMDragon/TPCDriver#configuration-file-details) section below.\
&ndash; The last line of the configuration file should be a call to the Driver.\
&ndash; Output files will be saved to the specified directory. The saved files may include stats, signals, and/or a full record, the details of which can be found in the [Output files](https://github.com/BMDragon/TPCDriver#output-files) section.

3. Driver\
&ndash; A generalized python file which holds a function to be called by the configuration files.\
&ndash; Again, the file location on line 6 called `dataPath` should be changed to where the MATLAB code is saved.\
&ndash; The function `Drive` first unpacks configuration values while asserting that all properties used are defined in the configuration file. It then drives the MATLAB simulation as described in the [Driver details](https://github.com/BMDragon/TPCDriver#driver-details) section.\
&ndash; This file should not be run by itself.

#### 2. TimePlotter

This script will create a histogram plot of the number of photons that generated a signal at a silicon photomultiplier (SiPM) at a given time. ![ Example histogram of the time plots.](./readme_images/time.png "Example histogram of the time plots")

Input: Line 5 (variable ```folder```) is a path to the directory where the data is located. Line 6 (variable ```numBins```) is the number of bins to have in the histogram plot. Line 7 (variable ```pltLimit```) is the max time in seconds to be plotted in the histogram. Also in line 27 (```hist, bins, patches = ax.hist(histArray, bins=numBins, color=('blue', 'red'), stacked=True)```), be sure to change the ```color``` keyword argument to have the same number of elements (specified colors) as the number of tracks in the dataset.

Output: A histogram plot of the time of signal observation by the SiPMs. The y-axis is a logarithmic scale of photon counts. The x-axis is time in nanoseconds. The script will also print into the terminal four numbers: first, the number of photons observed by the SiPMs (and thus considered for the histogram); second, the number of photons that get displayed by the histogram; third, the number of photons omitted (by the plot limit on the time axis); and last, the total number of photons that were simulated in this dataset.

#### 3. PlotPhoton

This script will create a visualization for the path that any given photon takes through the TPC. ![ Example of a photon path that shows a shift at the cathode, specular reflection at a wall, and then absorption into a wall.](./readme_images/path.png "Example photon path")

Input: Line 5 (variable ```photons```) is a numpy array of the photons whose path the user wants to visualize, indexed from 1 (there is no photon 0). Line 6 (variable ```folder```) is a path to the directory where the data is located. Line 7 (variable ```tpcWidth```) is the length of one side of the square base of the TPC; this should be equal to the width value used when generating the dataset. Line 8 (variable ```tpcHeight```) is the "height" of the TPC along the z-axis; this should be equal to the height value used when generating the dataset. 

Output: A 3-dimensional plot tracing the paths of photons, one at a time. The starting point (instance of scintillation) is labeled as point 0. Unshifted UV light is traced with a magenta line while shifted visible light is traced with a blue line. Diffuse reflection is marked by a gray dot while specular reflection is marked by a cyan dot. Rayleigh scattering is marked by an orange dot. Absorption back into the medium is marked by a black dot. Absoption into a surface is marked by a red dot, except for when the photon is absorbed into a SiPM *and* registers a signal, then it is marked by a green dot. These colors are customizable in lines 10-15.

#### 4. FindInfo

This is an information dumper to assist with debugging and/or understanding occurances. As such, it can be easily overhauled and modified to serve the needs of the user. For accurate results, be sure to follow the structure of the [output files](https://github.com/BMDragon/TPCDriver#output-files).

Example 1: ```photon``` and ```step``` are specified by the user, let these equal 2 and 1, respectively. The code will print into the terminal the status of photon 2 at simulation step 1.

```
dex = record['step'+str(step+1)]['status']['photon'][0].toarray().index(photon)
for key in record['step'+str(step+1)]['status']:
    print(key, record['step'+str(step+1)]['status'][key][0][dex])
```

Example 2: This will scan through all photons in step 2 and print out those that had stopped at the top of the detector in this step.

```
for ii in range(len(record['step2']['status']['stopped'][0])):
    if record['step2']['status']['stopped'][0][ii] and \
       record['step2']['status']['detectortop'][0][ii]:
        print(record['step2']['status']['photon'][0][ii])
```

## Configuration File details

#### 1. New Configuration File Generator

```filename``` should be a String that follows normal file-naming conventions. It is the name of the new config script.

If a new control feature is desired in future TPC simulations, add the control variable into the template at the desired line *and* in the dictionary and it will appear when new files are generated from this script.

#### 2. Input values

All these values get packaged into a python dictionary before calling the driver.

```saveFolder``` is the name of the folder where the data files should be saved. The directory should be manually made by the user beforehand.

```saveOptions``` is an integer in [0, 3]. 0: do not save anything. 1: save only record. 2: save record and signals. 3: save record, signals, and stats.

```height``` is a float > 0. This is the distance in meters from the cathode to the anode.

```width``` is a float > 0. This is the width of the TPC in meters. For a box, this is the legth of one side of the square base.

```wallShiftEfficiency``` is a float in [0.0, 1.0]. This is the rate of waveshifting at the walls.

```sipmShiftEfficiency``` is a float in [0.0, 1.0]. This is the rate of waveshifting at the SiPMs.

```anodeShiftEfficiency``` is a float in [0.0, 1.0]. This is the rate of waveshifting at the anode.

```detectorType``` is a String specifying the general shape of the TPC. Can have values of 'box', 'polygonal', 'cylinder', or 'cone'. However, only 'box' is compatible with the current code. Default ```'box'```.

```numSides``` is an integer >= 3. If detectorType is 'polygonal', then this determines how many wall faces the TPC will have (else it does not matter). Default ```4```.

```layerName``` is a String that will give an appropriate name to this layer. This is a legacy from Tom Shutt's MATLAB code. Default ```'cell'```.

```isLayerCone``` is a boolean. This states whether or not the layer has a conical shape. Also a legacy from Tom Schutt's MATLAB code. Default ```False```.

```medium``` is a String specifying the medium used within the TPC. Can be either 'Ar' for argon or 'Xe' for xenon. Default ```'Ar'```.

```mediumState``` is a String specyfying the state of matter of the medium within the TPC. Can be either 'liquid' or 'gas'. Default ```'liquid'```.

```temperature``` is a float > 0. This is the temperature in Kelvin of the medium inside the TPC. Default ```87.0```.

```layerWall``` is a String specifying the material of the walls. The available options are described in the [default materials](https://github.com/BMDragon/TPCDriver#4-default-materials) section below.

```wallShiftType``` is an integer in [1, 2]. 1: uniform efficiency. 2: linear z-graded efficiency. Default ```1```.

```scatterLengthUV``` is a float > 0. This is the scattering length in meters of the medium with respect to the unshifted light (UV for LAr). To set to infinity, make sure to ```import math``` at the top and set this value to ```math.inf```.

```scatterLengthShift``` is a float > 0. This is the scattering length in meters of the medium with respect to the shifted light (visible for LAr). To set to infinity, make sure to ```import math``` at the top and set this value to ```math.inf```.

```absoptionLengthUV``` is a float > 0. This is the absoption length in meters of the medium with respect to the unshifted light (UV for LAr). To set to infinity, make sure to ```import math``` at the top and set this value to ```math.inf```.

```absorptionLengthShift```  is a float > 0. This is the absoption length in meters of the medium with respect to the shifted light (visible for LAr). To set to infinity, make sure to ```import math``` at the top and set this value to ```math.inf```.

```sipmArrangement``` is a String specifying the way to organize the SiPMs. Right now, the only possible configuration is a simple square: ```'simplesquare'```.

```sipmQeUV``` is a float in [0.0, 1.0]. This is the quantum efficiency of the SiPMs with respect to the unshifted light (UV in LAr).

```sipmQeVis``` is a float in [0.0, 1.0]. This is the quantum efficiency of the SiPMs with respect to the shifted light (visible in LAr).

```sipmSize``` is a float >= 0. This is the length in meters of one side of a square SiPM. Be sure that sipmSize + sipmGapSize > 0.

```sipmGapSize``` is a float >= 0. This is the distance in meters in between adjacent sides of neighboring SiPMs. i.e. sipmSize + sipmGapSize = the center-to-center distance of neighboring SiPMs. Be sure that sipmSize + sipmGapSize > 0.

```sipmMaterial``` is a String specifying the material of the SiPMs. The available options are described in the [default materials](https://github.com/BMDragon/TPCDriver#4-default-materials) section below, although it is highly suggested to use silicon ```'si'```.

```gapMaterial``` is a String specifying the material of the gaps in the cathode. The available options are described in the [default materials](https://github.com/BMDragon/TPCDriver#4-default-materials) section below.

```anodeType``` is a String specifying the type of surface of the anode. Can be 'plate' or 'chargepcb'. Default ```'plate'```.

```anodeMaterial``` is a String specifying the material of the anode. The available options are described in the [default materials](https://github.com/BMDragon/TPCDriver#4-default-materials) section below.

```tracks``` is a dictionary of a String key and a list of tuplets value. The key should be a String which will end up being the name of the track. The value should be a list of two tuplets: the first being a tuplet of 4 floats representing the starting position (x1, y1, z1, t), the second being a tuplet of 3 floats representing the end position (x2, y2, z2). End time is calculated from particle speed in the Driver. Be sure that x1, x2, y1, y2 in [-width/2, width/2]; z1, z2 in [0, height]; and t >= 0.

Example tracks declaration:

```
tracks = {'track0' : [(-0.1, 0.15, 0.23, 0.), (-0.1, -0.13, 0.3)],
          'track1' : [(0.1, -0.15, 0.1, 5e-7), (0.1, 0.15, 0.05)]}
```

```angleMode``` is a String specifying whether the photons generated have a set starting angle or have a random starting angle. Can have values of either 'random' or 'controlled'.

```theta``` is a float in [0.0, &pi;]. This is the angle from the z-axis.

```phi``` is a float in [0.0, 2&pi;]. This is the angle from the x-axis.

```numPhotonsScale``` is a float > 0. This scales the number of photons generated per m of track. i.e. &gamma;/m = 4,400,000 * numPhotonsScale.

#### 3. Overwriting properties

```overwrite``` is a boolean. This states whether or not to override the default material properties as described in the [default materials](https://github.com/BMDragon/TPCDriver#4-default-materials) section below.

```overwriteProperties``` is a dictionary of dictionaries of dictionaries. This can be seen as ```{key0 : {key1 : {key2 : value}}}``` where: 
- key0 is a String specifying the material whose properties are being overwritten, 
- key1 is a String specifying which property to overwrite, 
- key2 is an integer either 0 or 1 indicating whether it affects unshifted or shifted light, respectively, and 
- value is a float in [0.0, 1.0] which is the new value. 

This has only been adapted for reflectivity and diffuse reflection fraction. Any other modifications to material properties should have a different control variable available in the configuration files. Also, be sure not to repeat keys as that may affect which properties get stored in the dictionary (follow the format shown in the example below).

Example: overwrite where the reflectivity of vikuiti is set to 0.0 for the shifted light but remains default for unshifted, the reflectivity of silicon is set to 0.3 for both the unshifted and shifted light, the reflectivity of black is set to 0.2 for the unshifted light and 0.3 for the shifted light, and the diffuse reflection fraction of black is set to 0.0 for the unshifted light and 0.3 for the shifted light.

```
overwriteProperties = {
    'vikuitilar' : {'reflectivity' : {1 : 0.0}},
    'si' : {'reflectivity' : {0 : 0.3, 1 : 0.3}},
    'black' : {'reflectivity' : {0 : 0.2, 1 : 0.3},
               'diffusefraction' : {0 : 0.0, 1 : 0.3}}
}
```

#### 4. Default Materials

This is a list of all the default materials that can be used as well as their properties. Some of these values may be guesses and/or inaccurate. If a change to these values is desired, they can be modified in LightGuide/CoreRoutines/Definitions/DefaultMaterials.m, and then please change the values in this table accordingly.

| Material | Name | Reflectivity | Diffuse fraction |
| :--- | - | :---: | :---: |
| | | UV &emsp; visible | UV &emsp; visible |
| | | | |
| ? | ptfegas | 0.65 &emsp; 0.65 | 1.0 &emsp;  1.0 |
| ? | ptfeliquid | 0.98 &emsp; 0.99 | 1.0 &emsp; 1.0 |
| ? | spectralon | 0.73 &emsp; 0.985 | 1.0 &emsp; 1.0 |
| Vikuiti | vikuitilar | 0.0 &emsp; 0.98 | 0.0 &emsp; 0.0 |
| ? | cirlex | 0.0 &emsp; 0.0 | 0.7 &emsp; 0.7 |
| Silver | ag | 0.2 &emsp; 0.7 | 0.5 &emsp; 0.5 |
| Aluminum | al | 0.5 &emsp; 0.95 | 0.8 &emsp; 0.8 |
| ? | alflash | 0.88 &emsp; 0.95 | 0.0 &emsp; 0.0 |
| ? | almgf2 | 0.88 &emsp; 0.95 | 0.0 &emsp; 0.0 |
| ? | becu | 0.1 &emsp; 0.7 | 0.3 &emsp; 0.3 |
| Gold | au | 0.85 &emsp; 0.4 | 0.3 &emsp; 0.3 |
| ? | ss | 0.1 &emsp; 0.7 | 0.3 &emsp; 0.3 |
| ? | ssbody | 0.1 &emsp; 0.7 | 0.1 &emsp; 0.1 |
| ? | sswireliquid | 0.1 &emsp; 0.7 | 0.3 &emsp; 0.3 |
| ? | sswiregas | 0.1 &emsp; 0.7 | 0.3 &emsp; 0.3 |
| ? | csi | 0.88 &emsp; 0.9 | 0.5 &emsp; 0.5 |
| Silicon | si | 0.2 &emsp; 0.0 | 0.0 &emsp; 0.0 |
| ? | agbare | 0.5 &emsp; 0.8 | 0.1 &emsp; 0.1 |
| Black | black | 0.0 &emsp; 0.0 | 0.0 &emsp; 0.0 |
| PMT window | pmtwindow | 0.0 &emsp; 0.0 | 0.0 &emsp; 0.0 |
| Nothing | nada | 0.0 &emsp; 0.0 | 0.0 &emsp; 0.0 |

## Driver details

#### 1. Unpacking and repackaging values

Reminder that line six (variable ```dataPath```) should be set to the MATLAB code path.

When unpacking the values from the configuration file, this script first checks if the field is in the config dictionary. Otherwise, it will throw an AssertionError with the message "Please make sure config has the field [fieldname]".

#### 2. MATLAB handling

The variable ```eng``` is the MATLAB engine started by a call to the API.

#### 3. Overwriting material properties

The nested for loops in the ```detector['materials']``` section are designed to be able to overwrite the reflectivity or diffusefraction properties of materials. If a change in the implementation and/or generalization is desired, this would be the place to do so.

#### 4. Calls to MATLAB preprocessing

The Driver makes calls to several MATLAB scripts in order to complete the simulation setup: DefaultMaterials.m, DefineSiPMPlane2.m, and ConstructDetector.m.

#### 5. Determining photon distribution

The code first determines the rate at which to generate photons based on the ```numPhotonsScale``` variable. Assuming that it equals 1, the standard photon generation assumes a minimum ionizing particle (MIP), and so assumes that 20,000 photons are generated per MeV of energy loss and that the particle loses 2.2 MeV per centimeter. Therefore, the code assumes 4,400,000 photons are produced per meter. Based on this number and the track length, the code generates photons for each track.

#### 6. Determining photon starting positions

Before determining the photon starting positions, the code asserts that the track is contained within the TPC (including borders). Then for each track, it evely distributes the allocated photons along the track through the following formula where $d$ is the index of a photon within its track: $$r_{x, y, z} = d\frac{End_{x,y,z}-Start_{x,y,z}}{\textrm{\# of photons for this track}} + Start_{x, y, z}$$

#### 7. Running Simulation in MATLAB

The script calls InitializePhotons.m and then PhotonFollower.m to run the simulation. This returns ```stats```, ```signal```, and ```fullRecord``` which are descibed below in [output files](https://github.com/BMDragon/TPCDriver#output-files).

#### 8. Time delays

First, the code defines several constants (assumptions):
- ```alpha```: a float in [0.0, 1.0]. It is the rate at which photons take the scintillation path with a short &tau;. This is currently set to a value of ```0.3```. 
- ```shortTau```: a float > 0. This is the &tau; in seconds for the short time scintillation path, currently set to a value of ```6e-9``` = 6 ns.
- ```longTau```: a float > 0. This is the &tau; in seconds for the long time scintillation path, currently set to a value of ```1.6e-6``` = 1.6 &mu;s.
- ```randSeed```: an integer that sets the seed value for the random number generator.

For each photon, the code will add two different time delays: particle travel time and time of scintillation. The code assumes that the ionizing particle travels near the speed of light (at c - 1 = 299,792,457 m/s). Thus, it calculates particle travel time delay with the following formula where $d$ is the index of a photon within its track: $$t_{\textrm{travel}} = d\frac{\textrm{TrackLength}/(c-1) - t_{\textrm{TrackStart}}}{\textrm{\# of photons for this track}} + t_{\textrm{TrackStart}}$$.

## Output files

#### 1. Stats



#### 2. Signals



#### 3. Records



## Limitations and assumptions

Assumes minimum ionizing particle (MIP), and so has a fixed photons per meter in the Driver.

Assumes particle travels at near speed of light (c - 1 = 299,792,457 m/s).

Assumes &tau; for both scintillation paths (6 ns and 1.6 &mu;s).

Since the code is very memory intensive, realistic simulations with a large number of photons may not compile properly as they would exceed the API's available memory usage.

Gaps in the SiPM array do not have waveshifting capabilities.

No pixel structure on the anode (only single material).

Default material properties not completely accurate, many reflectivity and diffuse fraction values are marked as "complete guess" in the MATLAB code.
