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

Input: Line 5 (variable ```folder```) is the name of the folder where the data is saved. Line 6 (variable ```numBins```) is the number of bins to have in the histogram plot. Line 7 (variable ```pltLimit```) is the max time in seconds to be plotted in the histogram. Also in line 27 (```hist, bins, patches = ax.hist(histArray, bins=numBins, color=('blue', 'red'), stacked=True)```), be sure to change the ```color``` keyword argument to have the same number of elements (specified colors) as the number of tracks in the dataset.

Output: A histogram plot of the time of signal observation by the SiPMs. The y-axis is a logarithmic scale of photon counts. The x-axis is time in nanoseconds. The script will also print into the terminal four numbers: first, the number of photons observed by the SiPMs (and thus considered for the histogram); second, the number of photons that get displayed by the histogram; third, the number of photons omitted (by the plot limit on the time axis); and last, the total number of photons that were simulated in this dataset.

#### 3. PlotPhoton

This scipt will create a visualization for the path that any given photon takes through the TPC. ![ Example of a photon path that shows a shift at the cathode, specular reflection at a wall, and then absorption into a wall.](./readme_images/path.png "Example photon path")

#### 4. FindInfo


## Configuration File details

#### 1. New Configuration File Generator


#### 2. Input values


#### 3. Overwriting properties


## Driver details

#### 1. Unpacking and repackaging values


#### 2. MATLAB handling


#### 3. Overwriting material properties


#### 4. Calls to MATLAB preprocessing


#### 5. Determining photon distribution


#### 6. Determining photon starting positions


#### 7. Running Simulation in MATLAB


#### 8. Scintillation time delays


## Output files

#### 1. Stats


#### 2. Signals


#### 3. Records
