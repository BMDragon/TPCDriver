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
1. ConfigFiles/NewConfig.py
-- This is a generative script that produces a new configuration file for simulations
-- Input: Name of the new configuration file (change on line 3)
-- Output: A blank template configuration file located inside the ConfigFiles folder
-- Once a new configuration file is generated, the user must go in and set all the values for the variables in order to use the file correctly
2. Configuration Files
-- 
3. Driver
-- 

#### 2. TimePlotter


#### 3. PlotPhoton


#### 4. FindInfo

## Materials and properties
