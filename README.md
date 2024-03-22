# HGCTPGValidation
This is a tool for running automatically the validation of the HGCAL TPG code.

The code is organized in a CMSSW independent package, used to
* Run Jenkins continuous integration for HGCal TPG validation. Two different jobs allow us 
    * to validate the HGCAL trigger primitives code in the package L1Trigger/L1THGCal of the  CMSSW framework (https://github.com/hgc-tpg/cmssw/).
    * to validate the validation code itself https://github.com/hgc-tpg/HGCTPGValidation.
* Run standalone validation

The package is organized in several directories:
* hgctpgvalidation: contain python programs for display step
* config: YAML configuration files allows users to customise the HGCAL TPG simulation
* data: the histograms to be compared are listed in HGCALTriggerPrimitivesHistos.txt file
* scripts: this directory contains all the necessary scripts for installing CMSSW environment, producing data, generating and displaying the histograms. There are some additional helper script allowing to extract the release name the SCRAM_ARCH. 

More detailed information can be found at the wiki pages:
https://github.com/hgc-tpg/HGCTPGValidation/wiki

