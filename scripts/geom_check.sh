#!/bin/bash
# Usage: ./HGCTPGValidation/scripts/geom_check.sh ${TEST_RELEASE} ${LABEL_TEST}

echo '===> Geometry checking.'

# Check if there are 2 arguments supplied to the script
if (( $# != 2 ))
then
  echo "Usage: ./HGCTPGValidation/scripts/geom_check.sh TEST_RELEASE LABEL_TEST"
  exit 1
fi

TEST_RELEASE=$1
LABEL_TEST=$2

cd test_dir/${TEST_RELEASE}_HGCalTPGValidation_${LABEL_TEST}/src
source /cvmfs/cms.cern.ch/cmsset_default.sh; 
eval `scramv1 runtime -sh`;
cmsRun L1Trigger/L1THGCal/test/testHGCalL1TGeometryV16_cfg.py
if [ -f test_dir/${TEST_RELEASE}_HGCalTPGValidation_${LABEL_TEST}/src/test_triggergeom.root ]; 
then
    echo "The ROOT file test_triggergeom.root was created successfully."
else
    echo "The ROOT file was not created."
    exit 1;
fi
echo '    '
