# HGCTPGValidation
Tool for running automatically the HGCAL TPG validation

## General presentation
This is a Python package, CMSSW independent, used to
* Run the HGCAL TPG validation for two different CMSSW releases or the same release but different parameters (the validation code is in the package Validation/HGCalValidation),
* Compare the histograms produced during the validation process, create a corresponding *.gif file 
* Create web page presenting all the results
* A specific code (Jenkinsfile and some scripts) have been added to run Jenkins continuous integration

The package is organized in several directories:
* `hgctpgvalidation`: contain the main routines for creating CMSSW working directory for each release as well as the default parameters values, python programs for display step
* `config`: user_parameters.py allows users to customise the HGCAL TPG simulation  
* `data`: the histograms to be compared are listed in HGCALTriggerPrimitivesHistos.txt file
* `scripts`: 

  ** validation validation_tpg.py is the main program for the automatic HGCAL TPG, the displayHistos.sh is the bash script running the compare/display part of the validation, 
  
  ** installCMSSW.sh and produceData.sh are the main scripts used in the Jenkins pipeline
  
  ** extractReleaseName.sh, getScramArch.sh and writeToFile.py are used to get 1) the release name from the target branch name, 2) to get scram arch for this release, and 3) to write the information to be displayed on the web page. 


## Installation
First clone the package:
```bash
git clone https://github.com/PFCal-dev/HGCTPGValidation HGCTPGValidation
```
## Customise your parameters file
It is currently possible to choose the following parameters:
* `releaseRefName: the reference CMSSW release version you would like to compare to, CMSSW_X1_Y1_Z1_preW1`
* `releaseTestName: the new CMSSW release to validate, CMSSW_X2_Y2_Z2_preW2` 
* `workingRefDir: free name, for example CMSSW_X1_Y1_Z1_preW1_HGCalTPGValidation_ref`
* `workingTestDir: free name, for example CMSSW_X2_Y2_Z2_preW2_HGCalTPGValidation_test`
* `remoteRefBranchName: branch name of your reference code`
* `remoteTestBranchName: branch name of your new code to validate`
* `localRefBranchName: local branch name of your reference code`
* `localTestBranchName: local branch name of your new code to validate`
* `remoteRef: remote of your reference code`
* `remoteTest: remote of your new code to validate`
* `numberOfEvents: number of events to be used for the simulation, default number is set to 50`
* `conditions`
* `beamspot`
* `geometryRef`
* `geometryTest`
* `eraRefName`
* `eraTestName`
* `procModifiers`
* `inputRefFileName`
* `inputTestFileName`
* `customiseRefFile: this parameter allows you to customise the HGCAL TPG simulation`
* `customiseTestFile: this parameter allows you to customise the HGCAL TPG simulation`
* `dropedBranches`
* `webDirPath: this is the name of the directory containing all the results from the validation, gif files as well as index2.html page`

Please, pay attention, the parameter "step" should not be changed!
* `step = 'USER:Validation/HGCalValidation/hgcalRunEmulatorValidationTPG_cff.hgcalTPGRunEmulatorValidation'`

## How to run the HGCAl TPG validation
Install the environment

Edit the file HGCTPGValidation/env_install.sh and select the working envirenment (CERN, LLR, sl6 or sl7) in order
to get the python3 version.

```bash
cd HGCTPGValidation
```
Select the environment in env_install.sh (at CERN or at LLR)
If working at LLR, before starting, please check the python2 and python3 available versions on polui and put the right versions in env_install.sh and HGCTPGValidation/scripts/displayHistos.sh

For sl6 check:
```bash
module use /opt/exp_soft/vo.llr.in2p3.fr/modulefiles
module avail
```

For sl7 please check:
```bash
module use /opt/exp_soft/vo.llr.in2p3.fr/modulefiles_el7/
module avail
```
```bash
source env_install.sh
```

Create a test validation directory at the same level as HGCTPGValidation package, from this new directory run the validation code
```bash
mkdir my_test_directory
cd my_test_directory
python ../HGCTPGValidation/scripts/validation_tpg.py --cfg HGCTPGValidation.config.user_parameters_cfg.py 
```
All the results of the validation will be saved in the my_test_directory
* `two CMSSW working directories`
* `directory containing all necessery for displaying the results: *.gif files, index2.html page`
* `log file`
