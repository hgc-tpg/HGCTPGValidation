# HGC TPG Validation

This is a tool for running automatically the validation of the HGCAL TPG code.
The goal is to validate the Pull Requests proposing changes to be merged into hgc-tpg/cmssw. The validation performs a comparison of the objects produced by the HGCAL TPG code between the source branch and the target branch. It also checks the quality of the code.  

The code is organized in a CMSSW independent package, used to
* Run Jenkins continuous integration for HGCal TPG validation. Two different jobs allow us 
    * to validate the HGCAL trigger primitives code in the package L1Trigger/L1THGCal of the  CMSSW framework (https://github.com/hgc-tpg/cmssw/).
    * to validate the validation code itself https://github.com/hgc-tpg/HGCTPGValidation.
* Run standalone validation

The package is organized in several directories:
* hgctpgvalidation: contains python programs for display step
* config: contains a set of YAML files defining different HGCAL TPG configurations used during the validation process
* data: the histograms to be compared are listed in HGCALTriggerPrimitivesHistos.txt file
* scripts: this directory contains all the necessary scripts for installing CMSSW environment, producing data, generating and displaying the histograms. There are some additional helper script allowing to extract the release name the SCRAM_ARCH. 

More detailed information can be found at the wiki pages:
https://github.com/hgc-tpg/HGCTPGValidation/wiki

